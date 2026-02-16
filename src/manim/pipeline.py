"""
Manim video pipeline orchestrator.
Handles the full lifecycle for each slide: generate → compile → feedback → retry.
Supports parallelization with configurable concurrency.
Supports two backends:
  - LMStudio (default): local Chat Completions API with message history
  - OpenAI Codex (--codex): OpenAI Responses API with previous_response_id chaining
"""

import asyncio
import csv
import time
from pathlib import Path
from typing import Optional, Any, Union

from src.slides.models import Slide, SlidesOutput
from src.manim.executor import ManimExecutor
from src.manim.feedback import VisualFeedback
from src.manim.tracker import ResultsTracker, AttemptRecord
from src.manim.models import ManimCode

MAX_GENERATION_ATTEMPTS = 3
MAX_COMPILE_RETRIES = 3

# Type alias: context is either a str (OpenAI response_id) or list[dict] (LMStudio messages)
GeneratorContext = Any


def _create_generator(use_codex: bool = False, vertical: bool = False):
    """Create the appropriate generator based on the backend flag."""
    if use_codex:
        from src.manim.generator import ManimGenerator
        return ManimGenerator(vertical=vertical)
    else:
        from src.manim.generator_lmstudio import ManimGeneratorLMStudio
        return ManimGeneratorLMStudio(vertical=vertical)


async def _try_compile(
    executor: ManimExecutor,
    generator,
    manim_code: ManimCode,
    context: GeneratorContext,
    slide: Slide,
    version: int,
    paper_content: str,
    log_prefix: str,
    prompt_text: str = "",
    is_fresh_context: bool = False,
    quality: str = "l",
    vertical: bool = False,
) -> tuple[bool, Optional[Path], ManimCode, GeneratorContext, int, str]:
    """
    Try to compile manim code, retrying up to MAX_COMPILE_RETRIES times.
    """
    compile_retries = 0
    current_code = manim_code
    current_context = context
    last_error = ""
    
    # Capture initial state for logging (assuming first attempt is Qwen/Base model)
    initial_code_content = current_code.code
    
    for compile_attempt in range(MAX_COMPILE_RETRIES):
        print(f"{log_prefix}   Compile attempt {compile_attempt + 1}/{MAX_COMPILE_RETRIES}...")
        # Save the code file
        code_file = executor.save_code(current_code, version=version, vertical=vertical)
        
        # Try to compile/render
        success, video_path, stderr = executor.execute(
            current_code, code_file, quality=quality, version=version, vertical=vertical
        )
        
        if success:
            print(f"{log_prefix} ✓ Compiled successfully")
            
            # Log successful outcome (CSV)
            if hasattr(generator, "log_outcome") and prompt_text:
                if compile_attempt == 0:
                    # Qwen succeeded immediately
                    generator.log_outcome(prompt_text, initial_code_content, True)
                else:
                    # Qwen failed, but subsequent fix (GPT-5) succeeded
                    generator.log_outcome(prompt_text, initial_code_content, False, current_code.code, True)
            
            return True, video_path, current_code, current_context, compile_retries, ""
        
        # Compile failed
        compile_retries += 1
        last_error = stderr
        
        if compile_attempt < MAX_COMPILE_RETRIES - 1:
            print(f"{log_prefix} ✗ Compile failed (retry {compile_retries}/{MAX_COMPILE_RETRIES})")
            print(f"{log_prefix}   Error: {stderr[:500]}")
            
            if is_fresh_context:
                current_code, current_context = await generator.fresh_retry_with_error(
                    slide, current_code.code, stderr, paper_content
                )
            else:
                current_code, current_context = await generator.retry_with_error(
                    slide.id, current_context, stderr
                )
            version += 1
        else:
            print(f"{log_prefix} ✗ Compile failed — max retries exhausted")
            print(f"{log_prefix}   Error: {stderr[:500]}")
            
            # Log failure outcome (CSV)
            if hasattr(generator, "log_outcome") and prompt_text:
                # First attempt (Qwen) failed, and last attempt (GPT-5) also failed
                generator.log_outcome(prompt_text, initial_code_content, False, current_code.code, False)
    
    return False, None, current_code, current_context, compile_retries, last_error


async def process_single_slide(
    slide: Slide,
    generator,
    executor: ManimExecutor,
    feedback_reviewer: VisualFeedback,
    tracker: ResultsTracker,
    paper_content: str = "",
    use_codex: bool = False,
    quality: str = "l",
    vertical: bool = False,
    slide_index: int = 0,
    total_slides: int = 0,
) -> Optional[Path]:
    """
    Process a single slide through the full pipeline:
    generate → compile (with retries) → feedback → retry (with feedback).
    """
    progress = f"[{slide_index}/{total_slides}]" if total_slides else ""
    prefix = f"  {progress} [{slide.id}]"
    best_video: Optional[Path] = None
    version = 1
    slide_start = time.time()
    
    for attempt in range(1, MAX_GENERATION_ATTEMPTS + 1):
        print(f"\n{prefix} === Attempt {attempt}/{MAX_GENERATION_ATTEMPTS} ===")
        
        record = AttemptRecord(slide_id=slide.id, attempt=attempt)
        
        # --- Step 1: Generate (or retry) manim code ---
        if attempt == 1:
            print(f"{prefix} Step 1/3: Generating manim code...")
            t0 = time.time()
            manim_code, context, prompt_text, instructions = await generator.generate_code(slide, paper_content)
            print(f"{prefix} Step 1/3: Code generated ({time.time() - t0:.1f}s)")
        else:
            # This path is taken when feedback said score=0
            # The retry_with_feedback was already called before the loop continued
            pass  # manim_code and context are already set from the feedback retry below
        
        record.manim_file = f"slides/{manim_code.slide_id}_v{version}.py" if version > 1 else f"slides/{manim_code.slide_id}.py"
        
        # --- Step 2: Try to compile (with retries) ---
        print(f"{prefix} Step 2/3: Compiling & rendering with Manim...")
        t0 = time.time()
        compiled, video_path, manim_code, context, compile_retries, last_error = await _try_compile(
            executor=executor,
            generator=generator,
            manim_code=manim_code,
            context=context,
            slide=slide,
            version=version,
            paper_content=paper_content,
            log_prefix=prefix,
            prompt_text=prompt_text,
            quality=quality,
            vertical=vertical,
        )
        
        compile_elapsed = time.time() - t0
        print(f"{prefix} Step 2/3: Compile {'succeeded' if compiled else 'failed'} ({compile_elapsed:.1f}s, {compile_retries} retries)")
        
        record.compiled = compiled
        record.compile_retries = compile_retries
        
        if not compiled:
            record.status = "compile_failed"
            record.manim_file = f"slides/{manim_code.slide_id}_v{version}.py" if version > 1 else f"slides/{manim_code.slide_id}.py"
            record.conversation_log = tracker.save_conversation(
                slide.id, attempt,
                _build_log_messages(instructions, prompt_text, manim_code.code, last_error)
            )
            tracker.add_record(record)
            
            # Start fresh with error context for next attempt
            if attempt < MAX_GENERATION_ATTEMPTS:
                print(f"{prefix} Starting fresh generation with error context for next attempt...")
                t0 = time.time()
                manim_code, context = await generator.fresh_retry_with_error(
                    slide, manim_code.code, last_error, paper_content
                )
                print(f"{prefix} Fresh code generated ({time.time() - t0:.1f}s)")
                # Re-build prompt/instructions for logging
                instructions, prompt_text = generator._build_prompt(slide, paper_content)
                version += 1
            continue
        
        # --- Step 3: Compiled! Run visual feedback (ONLY if --codex enabled) ---
        record.video_file = str(video_path.name) if video_path else ""
        best_video = video_path
        
        if not use_codex:
            # Skip review cycle, mark as success immediately
            record.status = "success"
            record.conversation_log = tracker.save_conversation(
                slide.id, attempt,
                _build_log_messages(instructions, prompt_text, manim_code.code)
            )
            tracker.add_record(record)
            slide_elapsed = time.time() - slide_start
            print(f"{prefix} ✓ Done! Video ready ({slide_elapsed:.1f}s total)")
            return video_path

        print(f"{prefix} Step 3/3: Running visual feedback review...")
        t0 = time.time()
        feedback_result = await feedback_reviewer.review(video_path, slide.voice)
        print(f"{prefix} Step 3/3: Feedback received ({time.time() - t0:.1f}s)")
        
        record.feedback_score = feedback_result.score
        record.feedback_text = feedback_result.feedback
        
        if feedback_result.score == 1:
            record.status = "success"
            record.conversation_log = tracker.save_conversation(
                slide.id, attempt,
                _build_log_messages(instructions, prompt_text, manim_code.code)
            )
            tracker.add_record(record)
            slide_elapsed = time.time() - slide_start
            print(f"{prefix} ✓ Visual review PASSED — done! ({slide_elapsed:.1f}s total)")
            return video_path
        
        # Feedback score = 0
        print(f"{prefix} ✗ Visual review FAILED: {feedback_result.feedback[:100]}...")
        record.status = "feedback_rejected"
        record.conversation_log = tracker.save_conversation(
            slide.id, attempt,
            _build_log_messages(instructions, prompt_text, manim_code.code)
        )
        tracker.add_record(record)
        
        # --- Step 4: Retry with feedback (if we have attempts left) ---
        if attempt < MAX_GENERATION_ATTEMPTS:
            print(f"{prefix} Retrying with feedback...")
            version += 1
            t0 = time.time()
            manim_code, context = await generator.retry_with_feedback(
                slide.id, context, feedback_result.feedback
            )
            print(f"{prefix} Feedback-improved code generated ({time.time() - t0:.1f}s)")
            
            # Try to compile the feedback-improved code
            print(f"{prefix} Compiling feedback-improved code...")
            compiled2, video_path2, manim_code, context2, cr2, err2 = await _try_compile(
                executor=executor,
                generator=generator,
                manim_code=manim_code,
                context=context,
                slide=slide,
                version=version,
                paper_content=paper_content,
                log_prefix=prefix,
                prompt_text=prompt_text,
                is_fresh_context=True,
                quality=quality,
                vertical=vertical,
            )
            
            if compiled2 and video_path2:
                context = context2
                best_video = video_path2
                
                # Record this compile result
                record2 = AttemptRecord(
                    slide_id=slide.id,
                    attempt=attempt,
                    manim_file=f"slides/{manim_code.slide_id}_v{version}.py",
                    video_file=str(video_path2.name),
                    compiled=True,
                    compile_retries=cr2,
                    status="pending_feedback",
                )
                
                # Run feedback on this version too
                print(f"{prefix} Running visual feedback on improved version...")
                feedback_result2 = await feedback_reviewer.review(video_path2, slide.voice)
                record2.feedback_score = feedback_result2.score
                record2.feedback_text = feedback_result2.feedback
                
                if feedback_result2.score == 1:
                    record2.status = "success"
                    record2.conversation_log = tracker.save_conversation(
                        slide.id, attempt,
                        _build_log_messages(instructions, prompt_text, manim_code.code),
                        suffix="feedback_retry"
                    )
                    tracker.add_record(record2)
                    slide_elapsed = time.time() - slide_start
                    print(f"{prefix} ✓ Improved version PASSED — done! ({slide_elapsed:.1f}s total)")
                    return video_path2
                else:
                    record2.status = "feedback_rejected"
                    record2.conversation_log = tracker.save_conversation(
                        slide.id, attempt,
                        _build_log_messages(instructions, prompt_text, manim_code.code),
                        suffix="feedback_retry"
                    )
                    tracker.add_record(record2)
                    print(f"{prefix} ✗ Improved version also failed review")
                    
                    # Start fresh with error context for next attempt
                    if attempt + 1 <= MAX_GENERATION_ATTEMPTS:
                        version += 1
                        manim_code, context, prompt_text, instructions = await generator.generate_code(slide, paper_content)
            else:
                # Feedback-improved code didn't compile even after retries
                record_fail = AttemptRecord(
                    slide_id=slide.id,
                    attempt=attempt,
                    manim_file=f"slides/{manim_code.slide_id}_v{version}.py",
                    compiled=False,
                    compile_retries=cr2,
                    status="compile_failed",
                    conversation_log=tracker.save_conversation(
                        slide.id, attempt,
                        _build_log_messages(instructions, prompt_text, manim_code.code, err2),
                        suffix="feedback_retry_fail"
                    ),
                )
                tracker.add_record(record_fail)
                
                # Start fresh with error context for next attempt
                if attempt + 1 <= MAX_GENERATION_ATTEMPTS:
                    version += 1
                    manim_code, context = await generator.fresh_retry_with_error(
                        slide, manim_code.code, err2, paper_content
                    )
                    instructions, prompt_text = generator._build_prompt(slide, paper_content)
    
    slide_elapsed = time.time() - slide_start
    print(f"{prefix} ✗ All attempts exhausted — using best available result ({slide_elapsed:.1f}s total)")
    return best_video


def _build_log_messages(
    instructions: str,
    prompt_text: str,
    generated_code: str,
    compile_error: str = "",
) -> list[dict[str, str]]:
    """Build a messages-style list for logging to .txt files."""
    messages = [
        {"role": "system", "content": instructions},
        {"role": "user", "content": prompt_text},
        {"role": "assistant", "content": generated_code},
    ]
    if compile_error:
        messages.append({"role": "error", "content": compile_error})
    return messages


def _get_completed_slides(output_dir: Path) -> set[str]:
    """
    Check the pipeline_results.csv for slides that already succeeded.
    Returns a set of slide IDs that have a 'success' status.
    Also verifies the video file actually exists.
    """
    csv_path = output_dir / "pipeline_results.csv"
    if not csv_path.exists():
        return set()
    
    completed = set()
    videos_dir = output_dir / "videos"
    
    try:
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get("status") == "success" and row.get("video_file"):
                    # Verify the video file still exists
                    video_path = videos_dir / row["video_file"]
                    if video_path.exists():
                        completed.add(row["slide_id"])
    except Exception:
        # If CSV is malformed, just start fresh
        return set()
    
    return completed


async def run_manim_pipeline(
    slides_output: SlidesOutput,
    output_dir: Path,
    paper_content: str = "",
    concurrency: int = 3,
    use_codex: bool = False,
    quality: str = "l",
    vertical: bool = False,
) -> ResultsTracker:
    """
    Run the full manim video pipeline for all slides.
    Resumes from previous progress — skips slides that already have successful videos.
    """
    generator = _create_generator(use_codex=use_codex, vertical=vertical)
    executor = ManimExecutor(output_dir)
    feedback_reviewer = VisualFeedback(vertical=vertical)
    tracker = ResultsTracker(output_dir)
    
    backend_name = "OpenAI Codex" if use_codex else "LMStudio (local)"
    
    # Check for previously completed slides
    completed_slides = _get_completed_slides(output_dir)
    
    # Filter out already-completed slides
    remaining_slides = [s for s in slides_output.slides if s.id not in completed_slides]
    skipped_count = len(slides_output.slides) - len(remaining_slides)
    
    semaphore = asyncio.Semaphore(concurrency)
    
    total_slide_count = len(slides_output.slides)
    
    # Build a map of slide_id → display index (1-based, across all slides)
    slide_display_index = {s.id: i + 1 for i, s in enumerate(slides_output.slides)}
    
    async def process_with_semaphore(slide: Slide):
        async with semaphore:
            return await process_single_slide(
                slide=slide,
                generator=generator,
                executor=executor,
                feedback_reviewer=feedback_reviewer,
                tracker=tracker,
                paper_content=paper_content,
                use_codex=use_codex,
                quality=quality,
                vertical=vertical,
                slide_index=slide_display_index.get(slide.id, 0),
                total_slides=total_slide_count,
            )
    
    print(f"\n{'='*60}")
    print(f"Manim Video Pipeline")
    print(f"{'='*60}")
    print(f"  Backend: {backend_name}")
    print(f"  Slides: {len(slides_output.slides)}")
    if skipped_count > 0:
        print(f"  ✓ Already completed: {skipped_count} (resuming from previous run)")
        print(f"  Remaining: {len(remaining_slides)}")
        for sid in sorted(completed_slides):
            print(f"    ✓ {sid} — already done")
    print(f"  Concurrency: {concurrency}")
    print(f"  Max attempts per slide: {MAX_GENERATION_ATTEMPTS}")
    print(f"  Max compile retries per attempt: {MAX_COMPILE_RETRIES}")
    print(f"{'='*60}\n")
    
    if not remaining_slides:
        print("  All slides already completed! Nothing to do.")
        return tracker
    
    if concurrency == 1:
        # Sequential processing (LMStudio) — one slide at a time
        results = []
        for slide in remaining_slides:
            try:
                result = await process_single_slide(
                    slide=slide,
                    generator=generator,
                    executor=executor,
                    feedback_reviewer=feedback_reviewer,
                    tracker=tracker,
                    paper_content=paper_content,
                    use_codex=use_codex,
                    quality=quality,
                    vertical=vertical,
                    slide_index=slide_display_index.get(slide.id, 0),
                    total_slides=total_slide_count,
                )
                results.append(result)
            except Exception as e:
                print(f"\n  [{slide.id}] ✗ Unexpected error: {e}")
                tracker.add_record(AttemptRecord(
                    slide_id=slide.id,
                    attempt=0,
                    status=f"error: {str(e)[:200]}",
                ))
                results.append(e)
    else:
        # Concurrent processing (Codex) — bounded by semaphore
        tasks = [process_with_semaphore(slide) for slide in remaining_slides]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Log any exceptions
        for slide, result in zip(remaining_slides, results):
            if isinstance(result, Exception):
                print(f"\n  [{slide.id}] ✗ Unexpected error: {result}")
                tracker.add_record(AttemptRecord(
                    slide_id=slide.id,
                    attempt=0,
                    status=f"error: {str(result)[:200]}",
                ))
    
    # Print summary
    summary = tracker.get_summary()
    print(f"\n{'='*60}")
    print(f"Pipeline Complete!")
    print(f"{'='*60}")
    print(f"  Total slides: {len(slides_output.slides)}")
    print(f"  Previously completed: {skipped_count}")
    print(f"  Processed this run: {len(remaining_slides)}")
    print(f"  Slides with success (this run): {summary['slides_with_success']}")
    print(f"  Total attempts (this run): {summary['total_attempts']}")
    print(f"  Successful: {summary['successful_attempts']}")
    print(f"  Compile failures: {summary['compile_failures']}")
    print(f"  Feedback rejections: {summary['feedback_rejections']}")
    print(f"  Results CSV: {summary['csv_path']}")
    print(f"{'='*60}\n")
    
    return tracker

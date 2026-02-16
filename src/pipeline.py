"""
Top-level pipeline CLI for processing papers into Manim explainer videos.

Usage:
    uv run python -m src.pipeline <folder_path> [options]

Options:
    --slides-only       Stop after generating slides.json
    --code-only         Stop after generating manim code (no rendering/feedback)
    --from-slides       Skip OCR, load existing slides.json
    --include-paper     Include full paper content in manim prompts
    --concurrency N     Max parallel slide processing (default: 3)
    --codex             Use OpenAI gpt-5.2-codex instead of local LMStudio model
    --vertical          Generate videos in vertical 9:16 portrait format
    
The folder should contain:
    - A PDF file (the paper to process)
    - A profile.txt file (optional, for personalization)

Outputs will be saved to <folder_path>/outputs/:
    - paper.md: OCR markdown result
    - slides.json: Generated slides
    - slides/*.py: Generated Manim code (versioned)
    - videos/*.mp4: Rendered videos
    - screenshots/: Feedback screenshots
    - pipeline_results.csv: Detailed results tracking
"""

import sys
import json
import asyncio
import argparse
import os
from pathlib import Path
from dotenv import load_dotenv

# Fix for "Other threads are currently calling into gRPC, skipping fork() handlers"
os.environ["GRPC_ENABLE_FORK_SUPPORT"] = "0"
os.environ["GRPC_POLL_STRATEGY"] = "poll"  # Often helps on Mac/Linux with fork issues

load_dotenv()


async def run_pipeline(
    folder_path: str,
    slides_only: bool = False,
    code_only: bool = False,
    from_slides: bool = False,
    include_paper: bool = False,
    concurrency: int = 3,
    use_codex: bool = False,
    quality: str = "l",
    vertical: bool = False,
):
    """
    Main pipeline: paper → slides → manim videos.
    
    Args:
        folder_path: Path to folder containing the PDF
        slides_only: Stop after generating slides.json
        code_only: Stop after generating manim code (no rendering/feedback)
        from_slides: Skip OCR and slide generation, load existing slides.json
        include_paper: Include full paper content in manim prompts
        concurrency: Max parallel slide processing
        use_codex: Use OpenAI Codex instead of LMStudio for code generation
        quality: Manim video quality (l=480p, m=720p, h=1080p, k=4k)
        vertical: If True, generate videos in 9:16 portrait format
    """
    from src.slides.generator import SlideGenerator
    from src.slides.models import SlidesOutput
    from src.paper.image_processor import ImageProcessor
    from src.paper.formula_processor import FormulaProcessor
    from src.manim.pipeline import run_manim_pipeline
    
    folder = Path(folder_path).resolve()
    if not folder.exists():
        raise FileNotFoundError(f"Folder not found: {folder}")
    
    output_dir = folder / "outputs"
    output_dir.mkdir(exist_ok=True)
    
    print(f"\n{'='*60}")
    print(f"PaperTok Pipeline")
    print(f"{'='*60}")
    print(f"  Folder: {folder}")
    print(f"  From slides: {from_slides}")
    print(f"  Slides only: {slides_only}")
    print(f"  Code only: {code_only}")
    print(f"  Include paper: {include_paper}")
    print(f"  Concurrency: {concurrency}")
    print(f"  Vertical (9:16): {vertical}")
    print(f"{'='*60}\n")
    
    # Auto-detect existing slides.json for resume (even without --from-slides)
    slides_file = output_dir / "slides.json"
    auto_resume = not from_slides and slides_file.exists()
    
    if from_slides or auto_resume:
        # Load existing slides
        if auto_resume:
            print("[1/4] Found existing slides.json — resuming from previous run...")
        else:
            print("[1/4] Loading existing slides from slides.json...")
        
        if not slides_file.exists():
            raise FileNotFoundError(f"slides.json not found at {slides_file}")
        
        with open(slides_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            slides_output = SlidesOutput.model_validate(data)
        print(f"  ✓ Loaded: {len(slides_output.slides)} slides")
        
        # Always load paper.md for manim context
        paper_content = ""
        paper_md = output_dir / "paper.md"
        if paper_md.exists():
            paper_content = paper_md.read_text()
            print(f"  ✓ Loaded paper.md ({len(paper_content)} chars)")
    else:
        # Step 1: OCR + Slide generation
        print("[1/4] Processing paper (OCR → Slides)...")
        slide_generator = SlideGenerator()
        
        # Process paper (OCR)
        folder_resolved = Path(folder_path).resolve()
        pdfs = list(folder_resolved.glob("*.pdf"))
        if not pdfs:
            raise FileNotFoundError(f"No PDF file found in {folder_resolved}")
        pdf_path = pdfs[0]
        
        # Load profile
        profile_path = folder_resolved / "profile.txt"
        user_profile = "A curious reader interested in this topic."
        if profile_path.exists():
            user_profile = profile_path.read_text().strip()
            print(f"  ✓ Loaded user profile ({len(user_profile)} chars)")
        
        print(f"  Running OCR on {pdf_path.name}...")
        ocr_results = slide_generator.extract_paper(pdf_path, output_dir)
        markdown = ocr_results["markdown"]
        images = ocr_results["images"]
        title = slide_generator.extract_title(markdown)
        print(f"  ✓ Paper title: {title}")
        
        # Step 2: Process images and formulas
        print(f"\n[2/4] Processing images and formulas...")
        image_processor = ImageProcessor()
        amazing_images = await image_processor.process_images(images, max_amazing=2)
        
        formula_processor = FormulaProcessor()
        important_formulas = await formula_processor.process_formulas(
            markdown, title, max_formulas=3
        )
        
        # Step 3: Generate slides
        print(f"\n[3/4] Generating slides...")
        slides_output = await slide_generator.generate_slides(
            title, markdown, images, user_profile
        )
        
        # Save slides.json
        slides_file = output_dir / "slides.json"
        with open(slides_file, "w", encoding="utf-8") as f:
            json.dump(slides_output.model_dump(), f, indent=2)
        print(f"  ✓ Saved: {slides_file}")
        
        # Always load paper content for manim prompts
        paper_content = markdown
    
    if slides_only:
        print(f"\n{'='*60}")
        print("✓ Slides generation complete (--slides-only)")
        print(f"{'='*60}\n")
        return
    
    if code_only:
        # Generate code only without the full pipeline (no feedback/retry)
        from src.manim.pipeline import _create_generator
        from src.manim.executor import ManimExecutor
        
        print(f"\n[4/4] Generating Manim code (--code-only)...")
        generator = _create_generator(use_codex=use_codex, vertical=vertical)
        executor = ManimExecutor(output_dir)
        
        for i, slide in enumerate(slides_output.slides, 1):
            print(f"  [{i}/{len(slides_output.slides)}] {slide.id}...")
            try:
                manim_code, _, _, _ = await generator.generate_code(slide, paper_content)
                code_file = executor.save_code(manim_code, vertical=vertical)
                print(f"    ✓ Code: {code_file.name}")
            except Exception as e:
                print(f"    ✗ Failed: {e}")
        
        print(f"\n{'='*60}")
        print(f"✓ Code generation complete (--code-only)")
        print(f"{'='*60}\n")
        return
    
    # Step 4: Full Manim pipeline with compile retry + feedback
    print(f"\n[4/4] Running Manim video pipeline...")
    
    # Force serial execution for local LMStudio to prevent crashes
    if not use_codex and concurrency > 1:
        print(f"  ⚠ Local LMStudio backend detected: forcing concurrency=1 to prevent system crash.")
        concurrency = 1
    
    tracker = await run_manim_pipeline(
        slides_output=slides_output,
        output_dir=output_dir,
        paper_content=paper_content,
        concurrency=concurrency,
        use_codex=use_codex,
        quality=quality,
        vertical=vertical,
    )
    
    summary = tracker.get_summary()
    print(f"\n🎬 Results CSV: {summary['csv_path']}")


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Process papers into Manim explainer videos"
    )
    parser.add_argument("folder", help="Path to folder containing the PDF")
    parser.add_argument(
        "--slides-only",
        action="store_true",
        help="Only generate slides.json, skip manim generation"
    )
    parser.add_argument(
        "--code-only",
        action="store_true",
        help="Generate slides and code, skip video rendering/feedback"
    )
    parser.add_argument(
        "--from-slides",
        action="store_true",
        help="Skip OCR and slide generation, load from outputs/slides.json"
    )
    parser.add_argument(
        "--include-paper",
        action="store_true",
        help="Include full paper content in manim code generation prompts"
    )
    parser.add_argument(
        "--concurrency",
        type=int,
        default=3,
        help="Max parallel slide processing (default: 3)"
    )
    parser.add_argument(
        "--codex",
        action="store_true",
        help="Use OpenAI gpt-5.2-codex instead of local LMStudio model"
    )

    parser.add_argument(
        "--quality",
        choices=["l", "m", "h", "k"],
        default="l",
        help="Video quality: l=480p (default), m=720p, h=1080p, k=2160p"
    )
    parser.add_argument(
        "--vertical",
        action="store_true",
        help="Generate videos in vertical 9:16 portrait format (for TikTok/Reels/Shorts)"
    )
    
    args = parser.parse_args()
    
    try:
        asyncio.run(run_pipeline(
            args.folder,
            slides_only=args.slides_only,
            code_only=args.code_only,
            from_slides=args.from_slides,
            include_paper=args.include_paper,
            concurrency=args.concurrency,
            use_codex=args.codex,
            quality=args.quality,
            vertical=args.vertical,
        ))
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

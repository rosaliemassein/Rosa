"""
Audio generation for the pipeline using kokoro-tts.

This module is preserved for future use but is NOT wired into the main pipeline.
It can be run standalone to generate audio files from a slides.json.

Usage:
    uv run python -m src.audio.generator <folder_path>
"""

import os
import sys
import json
from pathlib import Path

# kokoro-tts imports
from kokoro import KPipeline
import soundfile as sf


def load_slides_json(output_dir: Path) -> dict:
    """Load the slides.json from the outputs folder."""
    slides_path = output_dir / "slides.json"
    if not slides_path.exists():
        raise FileNotFoundError(
            f"slides.json not found at {slides_path}. "
            "Please run the pipeline first."
        )
    
    with open(slides_path, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_audio_for_slides(slides_data: dict, audio_dir: Path):
    """
    Generate audio files and word-level timestamps for each slide.
    
    Args:
        slides_data: The parsed slides.json content
        audio_dir: Directory to save audio files and timestamp JSON
    """
    import numpy as np
    
    # Initialize kokoro pipeline
    # 'a' = American English
    print("  Initializing kokoro-tts pipeline...")
    pipeline = KPipeline(lang_code='a', repo_id='hexgrad/Kokoro-82M')
    
    slides = slides_data.get("slides", [])
    total_slides = len(slides)
    
    print(f"  Processing {total_slides} slides...\n")
    
    for idx, slide in enumerate(slides, 1):
        slide_id = slide.get("id", f"slide_{idx}")
        content = slide.get("voice", "")
        
        if not content:
            print(f"  [{idx}/{total_slides}] Skipping {slide_id} (no voice content)")
            continue
        
        print(f"  [{idx}/{total_slides}] Generating audio for {slide_id}...")
        
        # Generate audio using kokoro
        # voice='af_heart' is a female American English voice
        generator = pipeline(content, voice='af_heart')
        
        # Collect all audio segments and their timestamps
        audio_segments = []
        all_words = []
        time_offset = 0.0  # Track cumulative time for multi-segment audio
        
        for result in generator:
            # Result has .audio, .tokens, .graphemes, .phonemes properties
            audio = result.audio
            if audio is None:
                continue
                
            audio_segments.append(audio)
            
            # Extract word timestamps from tokens
            if result.tokens:
                for token in result.tokens:
                    # Only include tokens with actual text (skip pure whitespace)
                    if token.text and token.text.strip():
                        word_data = {
                            "word": token.text,
                            "start": round(time_offset + getattr(token, 'start_ts', 0.0), 3),
                            "end": round(time_offset + getattr(token, 'end_ts', 0.0), 3)
                        }
                        all_words.append(word_data)
            
            # Update time offset for next segment
            segment_duration = len(audio) / 24000.0
            time_offset += segment_duration
        
        # Concatenate all segments if there are multiple
        if audio_segments:
            full_audio = np.concatenate(audio_segments)
            duration = len(full_audio) / 24000.0
            
            # Save audio file
            audio_path = audio_dir / f"{slide_id}.wav"
            sf.write(str(audio_path), full_audio, 24000)
            
            # Save timestamps JSON
            timestamps_data = {
                "slide_id": slide_id,
                "duration": round(duration, 3),
                "words": all_words
            }
            json_path = audio_dir / f"{slide_id}.json"
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(timestamps_data, f, indent=2, ensure_ascii=False)
            
            print(f"           ✓ Saved: {audio_path.name} ({duration:.1f}s, {len(all_words)} words)")
        else:
            print(f"           ⚠ No audio generated for {slide_id}")


def process_audio(folder_path: str):
    """
    Main function to generate audio for processed slides.
    
    Args:
        folder_path: Path to folder containing the outputs/slides.json
    """
    folder = Path(folder_path).resolve()
    if not folder.exists():
        raise FileNotFoundError(f"Folder not found: {folder}")
    
    output_dir = folder / "outputs"
    if not output_dir.exists():
        raise FileNotFoundError(
            f"Outputs folder not found at {output_dir}. "
            "Please run the pipeline first."
        )
    
    print(f"\n{'='*60}")
    print(f"Generating audio for: {folder}")
    print(f"{'='*60}\n")
    
    # Load slides.json
    print("[1/2] Loading slides.json...")
    slides_data = load_slides_json(output_dir)
    print(f"  ✓ Loaded: {slides_data.get('title', 'Untitled')}")
    print(f"  ✓ Found {len(slides_data.get('slides', []))} slides")
    
    # Create audio directory
    audio_dir = output_dir / "audio"
    audio_dir.mkdir(exist_ok=True)
    
    # Generate audio
    print(f"\n[2/2] Generating audio files...")
    generate_audio_for_slides(slides_data, audio_dir)
    
    # Summary
    print(f"\n{'='*60}")
    print(f"✓ Audio generation complete!")
    print(f"{'='*60}")
    print(f"  Audio files saved to: {audio_dir}")
    audio_files = list(audio_dir.glob("*.wav"))
    print(f"  Total audio files: {len(audio_files)}")
    print()


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: uv run python -m src.audio.generator <folder_path>")
        print("\nThe folder should contain:")
        print("  - outputs/slides.json (from the pipeline)")
        print("\nExample:")
        print("  uv run python -m src.audio.generator test_paper")
        sys.exit(1)
    
    folder_path = sys.argv[1]
    
    try:
        process_audio(folder_path)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

"""
Visual feedback reviewer for Manim-generated videos.
Extracts screenshots and uses GPT vision to evaluate visual quality.
"""

import os
import base64
import subprocess
from pathlib import Path
from typing import Optional
from google import genai
from google.genai import types
from PIL import Image
from dotenv import load_dotenv

from src.manim.models import FeedbackResult
from src.manim.prompts import VISUAL_FEEDBACK_SYSTEM, VISUAL_FEEDBACK_INPUT
from src.utils.gemini_schema import get_gemini_schema

load_dotenv()

MODEL = "gemini-3-flash-preview"


class VisualFeedback:
    """Extracts screenshots from videos and reviews visual quality."""
    
    def __init__(self, vertical: bool = False):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in .env")
        
        self.client = genai.Client(api_key=self.api_key)
        self.vertical = vertical
    
    def extract_frames(self, video_path: Path) -> tuple[Optional[Path], Optional[Path]]:
        """
        Extract middle frame and last frame from a video using ffmpeg.
        
        Returns:
            Tuple of (middle_frame_path, last_frame_path)
        """
        screenshots_dir = video_path.parent.parent / "screenshots"
        screenshots_dir.mkdir(exist_ok=True)
        
        stem = video_path.stem
        middle_path = screenshots_dir / f"{stem}_middle.png"
        last_path = screenshots_dir / f"{stem}_last.png"
        
        try:
            # Get video duration
            probe_cmd = [
                "ffprobe", "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                str(video_path)
            ]
            result = subprocess.run(probe_cmd, capture_output=True, text=True, timeout=10)
            duration = float(result.stdout.strip())
            
            middle_time = duration / 2.0
            last_time = max(0, duration - 0.1)  # Slightly before end
            
            # Extract middle frame
            mid_cmd = [
                "ffmpeg", "-y", "-ss", str(middle_time),
                "-i", str(video_path),
                "-frames:v", "1",
                "-q:v", "2",
                str(middle_path)
            ]
            subprocess.run(mid_cmd, capture_output=True, timeout=10)
            
            # Extract last frame
            last_cmd = [
                "ffmpeg", "-y", "-ss", str(last_time),
                "-i", str(video_path),
                "-frames:v", "1",
                "-q:v", "2",
                str(last_path)
            ]
            subprocess.run(last_cmd, capture_output=True, timeout=10)
            
            # Validate files exist and have content
            mid_ok = middle_path.exists() and middle_path.stat().st_size > 0
            last_ok = last_path.exists() and last_path.stat().st_size > 0
            
            return (
                middle_path if mid_ok else None,
                last_path if last_ok else None
            )
            
        except Exception as e:
            print(f"    ⚠ Frame extraction error: {e}")
            return None, None
    
    async def review(self, video_path: Path, voice_text: str) -> FeedbackResult:
        """
        Review a rendered video for visual quality.
        
        Args:
            video_path: Path to the rendered MP4 video
            voice_text: The narration text for context
            
        Returns:
            FeedbackResult with score (0 or 1) and feedback text
        """
        # Extract frames
        middle_frame, last_frame = self.extract_frames(video_path)
        
        if not middle_frame and not last_frame:
            return FeedbackResult(
                score=0,
                feedback="Could not extract frames from video for review."
            )
        
        # Build prompt content with images
        vertical_notes = ""
        if self.vertical:
            vertical_notes = (
                "\n\nVERTICAL REVIEW RULES (9:16 phone video):\n"
                "- Safe zone: x in [-4, 4], y in [-7, 7].\n"
                "- Text must be comfortably readable on a phone screen.\n"
                "- Flag tiny text and overly dense layouts as FAIL.\n"
                "- Prefer top-to-bottom composition over wide horizontal spreads.\n"
            )

        parts = [
            types.Part(
                text=(
                    f"{VISUAL_FEEDBACK_SYSTEM}\n\n"
                    f"{VISUAL_FEEDBACK_INPUT.format(voice=voice_text[:500])}"
                    f"{vertical_notes}"
                )
            )
        ]
        
        # Add middle frame
        if middle_frame:
            try:
                with open(middle_frame, 'rb') as f:
                    image_bytes = f.read()
                parts.append(types.Part.from_bytes(data=image_bytes, mime_type="image/png"))
            except Exception as e:
                print(f"    ⚠ Could not load middle frame: {e}")
        
        # Add last frame
        if last_frame:
            try:
                with open(last_frame, 'rb') as f:
                    image_bytes = f.read()
                parts.append(types.Part.from_bytes(data=image_bytes, mime_type="image/png"))
            except Exception as e:
                print(f"    ⚠ Could not load last frame: {e}")
        
        contents = [types.Content(role="user", parts=parts)]
        
        try:
            response = self.client.models.generate_content(
                model=MODEL,
                contents=contents,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=get_gemini_schema(FeedbackResult)
                )
            )
            
            import json
            json_output = json.loads(response.text)
            return FeedbackResult(**json_output)
            
        except Exception as e:
            print(f"    ⚠ Visual feedback error: {e}")
            return FeedbackResult(
                score=0,
                feedback=f"Error during visual review: {str(e)}"
            )

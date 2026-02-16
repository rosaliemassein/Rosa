"""
Manim executor for the pipeline.
Runs generated Manim code to produce video files.
Returns structured results including success/failure and error details.
"""

import subprocess
import sys
import shutil
import time
from pathlib import Path
from typing import Optional, Tuple

from src.manim.models import ManimCode


class ManimExecutor:
    """Executes Manim code and collects output videos."""
    
    def __init__(self, output_dir: Path):
        """
        Initialize executor with output directory.
        
        Args:
            output_dir: Directory to save generated videos
        """
        self.output_dir = Path(output_dir)
        self.slides_dir = self.output_dir / "slides"
        self.videos_dir = self.output_dir / "videos"
        
        # Create directories
        self.slides_dir.mkdir(parents=True, exist_ok=True)
        self.videos_dir.mkdir(parents=True, exist_ok=True)
    
    def _inject_vertical_config(self, code: str) -> str:
        """
        Inject portrait frame config near the top of generated code.
        Keeps generated scene code phone-native during pipeline execution.
        """
        # Avoid duplicate injection on retries/versioned writes.
        if "config.frame_height = 16.0" in code and "config.frame_width = 9.0" in code:
            return code

        vertical_header = (
            "from manim import config\n"
            "config.frame_height = 16.0\n"
            "config.frame_width = 9.0\n"
            "\n"
        )

        import_line = "from manim import *"
        if import_line in code:
            return code.replace(import_line, f"{import_line}\n{vertical_header}", 1)

        # Fallback if import line is unexpectedly missing.
        return f"{vertical_header}{code}"

    def save_code(self, manim_code: ManimCode, version: int = 1, vertical: bool = False) -> Path:
        """
        Save Manim code to a Python file with version number.
        
        Args:
            manim_code: The code to save
            version: Version number for the file (e.g., slide_1_v2.py)
            vertical: If True, inject 9:16 portrait frame config
            
        Returns:
            Path to the saved file
        """
        if version == 1:
            filename = f"{manim_code.slide_id}.py"
        else:
            filename = f"{manim_code.slide_id}_v{version}.py"
        
        code_file = self.slides_dir / filename
        code_to_write = self._inject_vertical_config(manim_code.code) if vertical else manim_code.code
        code_file.write_text(code_to_write)
        return code_file
    
    def execute(
        self, 
        manim_code: ManimCode,
        code_file: Path,
        quality: str = "l",  # l=low, m=medium, h=high, k=4k
        version: int = 1,
        vertical: bool = False,
    ) -> Tuple[bool, Optional[Path], str]:
        """
        Execute Manim code to generate video.
        
        Args:
            manim_code: The ManimCode to execute
            code_file: Path to the saved .py file
            quality: Video quality (l/m/h/k)
            version: Version number for output naming
            vertical: If True, render in 9:16 portrait format
        
        Returns:
            Tuple of (success, video_path, stderr)
            - success: True if video was generated
            - video_path: Path to the video file (or None)
            - stderr: Error output (empty string on success)
        """
        # Run manim command
        cmd = [
            "manim",
            f"-q{quality}",
            str(code_file),
            manim_code.scene_name,
            "--media_dir", str(self.output_dir / "media"),
        ]
        
        # For vertical (9:16) format, override resolution to swap width/height
        if vertical:
            vertical_resolutions = {
                "l": "480,854",
                "m": "720,1280",
                "h": "1080,1920",
                "k": "2160,3840",
            }
            res = vertical_resolutions.get(quality, "720,1280")
            cmd.extend(["-r", res])
        
        try:
            # Use Popen to stream output in real-time (shows manim progress bars)
            # No timeout — we wait for manim to finish and only fail on errors
            print(f"    🎬 Manim rendering: {manim_code.scene_name} (quality={quality})...")
            render_start = time.time()
            
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,  # Line-buffered
            )
            
            # Stream stderr (where manim prints progress bars) to console in real-time
            stderr_lines = []
            
            # Read stdout and stderr concurrently
            # Manim prints progress to stderr, so we stream that
            import threading
            import io
            
            stdout_buf = io.StringIO()
            
            def _read_stdout():
                for line in process.stdout:
                    stdout_buf.write(line)
            
            stdout_thread = threading.Thread(target=_read_stdout, daemon=True)
            stdout_thread.start()
            
            # Stream stderr to console AND capture it
            for line in process.stderr:
                stderr_lines.append(line)
                # Print manim progress (loading bars, render info) directly to console
                sys.stderr.write(line)
                sys.stderr.flush()
            
            process.wait()
            stdout_thread.join(timeout=5)
            render_elapsed = time.time() - render_start
            
            stderr_output = "".join(stderr_lines)
            
            if process.returncode != 0:
                print(f"    ✗ Manim render failed ({render_elapsed:.1f}s)")
                return False, None, stderr_output
            
            # Find the output video
            quality_dirs = {
                "l": "854p15",
                "m": "1280p30",
                "h": "1920p60",
                "k": "3840p60",
            } if vertical else {
                "l": "480p15",
                "m": "720p30",
                "h": "1080p60",
                "k": "2160p60",
            }
            video_subdir = quality_dirs.get(quality, "720p30")
            
            # Manim outputs to: media/videos/{filename_stem}/{quality}/SceneName.mp4
            expected_video = (
                self.output_dir / "media" / "videos" / 
                code_file.stem / video_subdir / 
                f"{manim_code.scene_name}.mp4"
            )
            
            # Determine output video name with version
            if version == 1:
                video_name = f"{manim_code.slide_id}.mp4"
            else:
                video_name = f"{manim_code.slide_id}_v{version}.mp4"
            
            if expected_video.exists():
                final_video = self.videos_dir / video_name
                shutil.copy2(expected_video, final_video)
                print(f"    ✓ Manim render complete ({render_elapsed:.1f}s) → {video_name}")
                return True, final_video, ""
            else:
                # Fallback 1: search this code file's render directory for any final mp4.
                # This handles cases where scene name parsing is imperfect but render succeeded.
                code_video_dir = self.output_dir / "media" / "videos" / code_file.stem
                if code_video_dir.exists():
                    for mp4 in code_video_dir.rglob("*.mp4"):
                        if "partial_movie_files" in str(mp4):
                            continue
                        final_video = self.videos_dir / video_name
                        shutil.copy2(mp4, final_video)
                        print(f"    ✓ Manim render complete ({render_elapsed:.1f}s) → {video_name}")
                        return True, final_video, ""

                # Try to find any mp4 in media folder matching the scene
                for mp4 in (self.output_dir / "media").rglob("*.mp4"):
                    if manim_code.scene_name in mp4.name:
                        final_video = self.videos_dir / video_name
                        shutil.copy2(mp4, final_video)
                        print(f"    ✓ Manim render complete ({render_elapsed:.1f}s) → {video_name}")
                        return True, final_video, ""
                
                return False, None, "Video not found after render"
                
        except Exception as e:
            return False, None, f"Execution error: {str(e)}"

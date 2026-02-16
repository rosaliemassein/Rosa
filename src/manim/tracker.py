"""
CSV results tracker for the manim video pipeline.
Records every attempt for every slide with detailed status information.
Saves full conversation logs as .txt files for preference pair training.
"""

import csv
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional, List, Dict


@dataclass
class AttemptRecord:
    """A single attempt at generating a video for a slide."""
    slide_id: str
    attempt: int
    manim_file: str = ""
    video_file: str = ""
    compiled: bool = False
    compile_retries: int = 0
    feedback_score: Optional[int] = None
    feedback_text: str = ""
    status: str = ""  # compile_failed, feedback_rejected, success
    conversation_log: str = ""  # relative path to the .txt conversation log


class ResultsTracker:
    """Tracks all pipeline results and writes them to a CSV file."""
    
    def __init__(self, output_dir: Path):
        self.output_dir = Path(output_dir)
        self.records: List[AttemptRecord] = []
        self.csv_path = self.output_dir / "pipeline_results.csv"
        self.logs_dir = self.output_dir / "conversation_logs"
        self.logs_dir.mkdir(parents=True, exist_ok=True)
    
    def save_conversation(
        self,
        slide_id: str,
        attempt: int,
        messages: List[Dict[str, str]],
        suffix: str = "",
    ) -> str:
        """
        Save the full LLM conversation to a .txt file.
        
        Args:
            slide_id: The slide ID
            attempt: Attempt number
            messages: The conversation messages list
            suffix: Optional suffix (e.g., 'feedback_retry')
            
        Returns:
            Relative path to the saved file (relative to output_dir)
        """
        parts = [slide_id, f"attempt{attempt}"]
        if suffix:
            parts.append(suffix)
        filename = "_".join(parts) + ".txt"
        filepath = self.logs_dir / filename
        
        lines = []
        for msg in messages:
            role = msg["role"].upper()
            content = msg["content"] if isinstance(msg["content"], str) else str(msg["content"])
            lines.append(f"=== {role} ===")
            lines.append(content)
            lines.append("")  # blank line separator
        
        filepath.write_text("\n".join(lines), encoding="utf-8")
        
        # Return relative path for CSV
        return f"conversation_logs/{filename}"
    
    def add_record(self, record: AttemptRecord):
        """Add an attempt record."""
        self.records.append(record)
        # Write immediately so we don't lose data on crashes
        self._write_csv()
    
    def _write_csv(self):
        """Write all records to CSV."""
        fieldnames = [
            "slide_id", "attempt", "manim_file", "video_file",
            "compiled", "compile_retries", "feedback_score",
            "feedback_text", "status", "conversation_log"
        ]
        
        with open(self.csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for record in self.records:
                writer.writerow({
                    "slide_id": record.slide_id,
                    "attempt": record.attempt,
                    "manim_file": record.manim_file,
                    "video_file": record.video_file,
                    "compiled": record.compiled,
                    "compile_retries": record.compile_retries,
                    "feedback_score": record.feedback_score if record.feedback_score is not None else "",
                    "feedback_text": record.feedback_text,
                    "status": record.status,
                    "conversation_log": record.conversation_log,
                })
    
    def get_summary(self) -> dict:
        """Get a summary of all results."""
        total = len(self.records)
        successes = sum(1 for r in self.records if r.status == "success")
        compile_fails = sum(1 for r in self.records if r.status == "compile_failed")
        feedback_rejects = sum(1 for r in self.records if r.status == "feedback_rejected")
        
        # Unique slides
        slide_ids = set(r.slide_id for r in self.records)
        slides_with_success = set(
            r.slide_id for r in self.records if r.status == "success"
        )
        
        return {
            "total_attempts": total,
            "successful_attempts": successes,
            "compile_failures": compile_fails,
            "feedback_rejections": feedback_rejects,
            "total_slides": len(slide_ids),
            "slides_with_success": len(slides_with_success),
            "csv_path": str(self.csv_path),
        }

"""
Data models for the manim video generation pipeline.
"""

from typing import Optional
from pydantic import BaseModel, ConfigDict


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ManimCode(StrictModel):
    """Generated Manim code for a single slide."""
    slide_id: str
    scene_name: str            # Class name for the Scene
    code: str                  # Full Python code


class ManimCodeOutput(StrictModel):
    """Output from the manim code generator."""
    manim_code: ManimCode


class FeedbackResult(BaseModel):
    """Result from the visual feedback reviewer."""
    score: int                 # 0 = has issues, 1 = perfect
    feedback: str              # Detailed feedback text

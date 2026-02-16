"""
Data models for the pipeline.
Includes slide models, evaluation models, and shared base classes.
"""

from typing import List, Optional
from pydantic import BaseModel, ConfigDict


# Pydantic config for strict JSON schema (required by OpenAI Responses API)
class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


# =============================================================================
# Slide Models
# =============================================================================

class Slide(StrictModel):
    """
    A slide in the explainer video.
    Each slide represents one animated segment with narration.
    """
    id: str                    # e.g., "slide_1"
    voice: str                 # Narration text to be spoken
    goal: str                  # What should be clear after this slide
    remarks: str               # Visual/animation hints for manim generator
    formula: Optional[str] = None      # LaTeX formula if relevant
    image_ref: Optional[str] = None    # Reference to an image from the paper


class SlidesGenerationResponse(StrictModel):
    """Schema for the Gemini response — only the generated slides."""
    slides: List[Slide]


class SlidesOutput(StrictModel):
    """Complete output from the slide generator (slides + known title)."""
    title: str
    slides: List[Slide]


# =============================================================================
# Image & Formula Evaluation Models (used by paper processors)
# =============================================================================

class ImageEvaluation(StrictModel):
    """Result of evaluating whether an image is 'amazing'."""
    is_amazing: bool
    reason: str  # Why it's amazing or not
    explanation: str  # What the user should learn (only relevant if amazing)


class FormulaEvaluation(StrictModel):
    """Result of evaluating whether a formula is important."""
    is_important: bool
    reason: str  # Why it's important or not
    explanation: str  # What the user should understand
    selection_rationale: str  # Why this formula matters


class FormulaFilterOutput(StrictModel):
    """Output from the formula filtering step."""
    selected_formulas: List[FormulaEvaluation]

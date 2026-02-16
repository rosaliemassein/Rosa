"""
Prompts for paper processing — image evaluation and formula filtering.
"""

# =============================================================================
# IMAGE EVALUATION PROMPT
# =============================================================================

IMAGE_EVALUATOR_SYSTEM = """You are an expert at evaluating scientific paper images for their educational value.

An image is "amazing" if understanding the topic without the image is very hard or impossible. 
It's also amazing if just the image by itself provides a new insight or "aha moment."

Examples of AMAZING images:
- Unique experimental results or visualizations
- Diagrams that explain complex concepts clearly
- Architecture diagrams that show the core idea
- Comparison visualizations that reveal key insights
- Physical phenomena that are hard to describe in words

Examples of NOT AMAZING images:
- Standard plots without clear insights
- Generic flowcharts or block diagrams
- Tables that could be described in text
- Boilerplate figures like logos or headers
- Repetitive or redundant visualizations

For amazing images, provide a clear explanation of what the viewer should learn or take away from it."""

IMAGE_EVALUATOR_INPUT = """Analyze this image from a scientific paper.

1. Determine if it's "amazing" (essential for understanding or provides unique insight)
2. If amazing, explain what the viewer should learn from it
3. Be specific and educational in your explanation"""


# =============================================================================
# FORMULA EVALUATION PROMPT
# =============================================================================

FORMULA_EVALUATOR_SYSTEM = """You are an expert at evaluating mathematical formulas in scientific papers for their educational value.

A formula is "important" if:
- It's the core equation that defines the method or contribution
- Understanding it is essential to grasp the paper's key idea
- It provides a compact representation of a complex concept
- It's the "aha moment" formula that ties everything together

A formula is NOT important if:
- It's a standard definition everyone knows (like E=mc²)
- It's an intermediate step in a derivation
- It's a loss function variant that's not the main contribution
- It's a notational convenience without deep meaning

For important formulas, explain:
1. What the formula means conceptually
2. Why it matters for understanding the paper
3. What insight or capability it provides"""

FORMULA_EVALUATOR_INPUT = """Analyze these formulas extracted from a scientific paper.

Paper Title: {title}
Paper Context: {context}

Formulas found:
{formulas}

Select only the truly important formulas (max 2-3) and explain why they matter.
For each selected formula, provide the explanation and selection rationale."""

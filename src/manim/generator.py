"""
Manim code generator using the OpenAI Responses API.
Generates Manim Python code from slide metadata using LLM.
Supports multi-turn retries via previous_response_id chaining.
"""

import os
import re
from typing import Optional, List, Dict
from openai import AsyncOpenAI
from dotenv import load_dotenv

from src.manim.models import ManimCode
from src.manim.prompts import (
    MANIM_GENERATOR_SYSTEM,
    MANIM_GENERATOR_INPUT,
    MANIM_GENERATOR_WITH_FORMULA,
    MANIM_COMPILE_ERROR_MSG,
    MANIM_FEEDBACK_MSG,
    VERTICAL_ADDENDUM,
)
from src.slides.models import Slide

load_dotenv()

MODEL = "gpt-5.2-codex"


class ManimGenerator:
    """Generates Manim code for slides using the OpenAI Responses API."""
    
    def __init__(self, vertical: bool = False):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found.")
        self.client = AsyncOpenAI(api_key=self.api_key)
        self.vertical = vertical
    
    def _build_prompt(
        self,
        slide: Slide,
        paper_content: str = ""
    ) -> tuple[str, str]:
        """
        Build system instructions and user input for a slide.
        
        Returns:
            Tuple of (instructions, input_text)
        """
        formula_section = ""
        if slide.formula:
            formula_section = MANIM_GENERATOR_WITH_FORMULA.format(formula=slide.formula)
        
        paper_context = paper_content[:10000] if paper_content else "No paper context available."
        
        input_text = MANIM_GENERATOR_INPUT.format(
            slide_id=slide.id,
            voice=slide.voice,
            goal=slide.goal,
            remarks=slide.remarks,
            formula_section=formula_section,
            paper_context=paper_context,
        )
        
        system = MANIM_GENERATOR_SYSTEM
        if self.vertical:
            system += VERTICAL_ADDENDUM
        
        return system, input_text
    
    def _parse_manim_code(self, raw_output: str, slide_id: str) -> ManimCode:
        """Parse LLM output into a ManimCode object."""
        code = self._extract_code(raw_output)
        scene_name = self._extract_scene_name(code, slide_id)
        return ManimCode(slide_id=slide_id, scene_name=scene_name, code=code)
    
    async def generate_code(
        self,
        slide: Slide,
        paper_content: str = ""
    ) -> tuple[ManimCode, str, str, str]:
        """
        Generate Manim code for a single slide (initial generation).
        
        Returns:
            Tuple of (ManimCode, response_id, prompt_text, instructions)
            - response_id: Used for chaining follow-up turns
            - prompt_text: The user input text for logging
            - instructions: The system instructions for logging
        """
        instructions, input_text = self._build_prompt(slide, paper_content)
        
        response = await self.client.responses.create(
            model=MODEL,
            instructions=instructions,
            input=input_text,
        )
        
        raw_code = response.output_text
        manim_code = self._parse_manim_code(raw_code, slide.id)
        return manim_code, response.id, input_text, instructions
    
    async def retry_with_error(
        self,
        slide_id: str,
        previous_response_id: str,
        error_msg: str
    ) -> tuple[ManimCode, str]:
        """
        Retry by chaining onto the previous response with compile error info.
        
        Returns:
            Tuple of (ManimCode, new_response_id)
        """
        error_prompt = MANIM_COMPILE_ERROR_MSG.format(error=error_msg[:2000])
        
        response = await self.client.responses.create(
            model=MODEL,
            input=error_prompt,
            previous_response_id=previous_response_id,
        )
        
        raw_code = response.output_text
        manim_code = self._parse_manim_code(raw_code, slide_id)
        return manim_code, response.id
    
    async def retry_with_feedback(
        self,
        slide_id: str,
        previous_response_id: str,
        feedback_text: str
    ) -> tuple[ManimCode, str]:
        """
        Retry by chaining onto the previous response with visual feedback.
        
        Returns:
            Tuple of (ManimCode, new_response_id)
        """
        feedback_prompt = MANIM_FEEDBACK_MSG.format(feedback=feedback_text)
        
        response = await self.client.responses.create(
            model=MODEL,
            input=feedback_prompt,
            previous_response_id=previous_response_id,
        )
        
        raw_code = response.output_text
        manim_code = self._parse_manim_code(raw_code, slide_id)
        return manim_code, response.id
    
    async def fresh_retry_with_error(
        self,
        slide: Slide,
        failed_code: str,
        error_msg: str,
        paper_content: str = ""
    ) -> tuple[ManimCode, str]:
        """
        Start a completely fresh generation (new conversation) for a compile fix.
        Used when feedback-retry code doesn't compile — avoids muddying context.
        
        Returns:
            Tuple of (ManimCode, response_id)
        """
        instructions, input_text = self._build_prompt(slide, paper_content)
        
        # Include the failed code and error in the input to give context
        combined_input = f"""{input_text}

NOTE: A previous attempt generated this code which FAILED to compile:
```python
{failed_code[:3000]}
```

Error:
```
{error_msg[:2000]}
```

Please generate a corrected version. Output ONLY the Python code."""
        
        response = await self.client.responses.create(
            model=MODEL,
            instructions=instructions,
            input=combined_input,
        )
        
        raw_code = response.output_text
        manim_code = self._parse_manim_code(raw_code, slide.id)
        return manim_code, response.id
    
    def _extract_code(self, raw_output: str) -> str:
        """Extract Python code from LLM output, removing markdown fences."""
        code = raw_output.strip()
        
        # Remove ```python or ``` wrappers
        if code.startswith("```python"):
            code = code[9:]
        elif code.startswith("```"):
            code = code[3:]
        
        if code.endswith("```"):
            code = code[:-3]
        
        return code.strip()
    
    def _extract_scene_name(self, code: str, fallback_id: str) -> str:
        """Extract the Scene class name from code."""
        match = re.search(r'class\s+(\w+)\s*\(\s*\w*Scene\w*\s*\)', code)
        if match:
            return match.group(1)
        
        # Fallback: generate from slide id
        return f"Slide{fallback_id.replace('slide_', '').replace('_', '').replace('-', '').title()}"

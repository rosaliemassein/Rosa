"""
Formula processor for extracting and filtering important math formulas.
Uses gpt-5-mini with the OpenAI beta.chat.completions.parse API for structured outputs.
"""

import os
import re
from typing import List, Dict, Any
from google import genai
from google.genai import types
from src.slides.models import FormulaEvaluation, FormulaFilterOutput
from src.paper.prompts import FORMULA_EVALUATOR_SYSTEM, FORMULA_EVALUATOR_INPUT
from src.utils.gemini_schema import get_gemini_schema
from dotenv import load_dotenv

load_dotenv()

MODEL = "gemini-3-flash-preview"


class FormulaProcessor:
    """Extracts and filters important math formulas from paper markdown."""
    
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found. Please set it in .env or environment variables.")
        
        self.client = genai.Client(api_key=self.api_key)

    def extract_formulas(self, markdown: str) -> List[Dict[str, str]]:
        """
        Extract LaTeX formulas from markdown content.
        Looks for both inline ($...$) and display ($$...$$) math.
        """
        formulas = []
        
        # Pattern for display math: $$ ... $$
        display_pattern = r'\$\$(.+?)\$\$'
        display_matches = re.findall(display_pattern, markdown, re.DOTALL)
        
        # Pattern for inline math: $ ... $ (but not $$)
        inline_pattern = r'(?<!\$)\$(?!\$)(.+?)(?<!\$)\$(?!\$)'
        inline_matches = re.findall(inline_pattern, markdown, re.DOTALL)
        
        # Get context for each formula (surrounding text)
        for match in display_matches:
            latex = match.strip()
            if len(latex) > 5:  # Filter out trivially short formulas
                # Find context: text before and after the formula
                idx = markdown.find(f"$${match}$$")
                start = max(0, idx - 200)
                end = min(len(markdown), idx + len(match) + 200)
                context = markdown[start:end].replace(f"$${match}$$", "[FORMULA]")
                
                formulas.append({
                    "latex": latex,
                    "context": context,
                    "type": "display"
                })
        
        for match in inline_matches:
            latex = match.strip()
            if len(latex) > 10:  # Inline formulas should be more substantial
                idx = markdown.find(f"${match}$")
                if idx != -1:
                    start = max(0, idx - 150)
                    end = min(len(markdown), idx + len(match) + 150)
                    context = markdown[start:end]
                    
                    formulas.append({
                        "latex": latex,
                        "context": context,
                        "type": "inline"
                    })
        
        print(f"  - Extracted {len(formulas)} candidate formulas")
        return formulas

    async def filter_formulas(
        self, 
        formulas: List[Dict[str, str]], 
        title: str,
        markdown_summary: str,
        max_formulas: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Filter formulas to find the most important ones.
        Returns a list of dicts with 'latex', 'explanation', 'selection_rationale'.
        """
        if not formulas:
            return []
        
        # Format formulas for the prompt
        formula_text = "\n\n".join([
            f"Formula {i+1}:\n```\n{f['latex']}\n```\nContext: {f['context'][:150]}..."
            for i, f in enumerate(formulas[:15])  # Limit to first 15 to avoid token limits
        ])
        
        prompt_input = FORMULA_EVALUATOR_INPUT.format(
            title=title,
            context=markdown_summary[:1000],
            formulas=formula_text
        )
        
        try:
            # Build contents with system instruction
            contents = [
                types.Content(
                    role="user",
                    parts=[types.Part(text=f"{FORMULA_EVALUATOR_SYSTEM}\n\n{prompt_input}")]
                )
            ]
            
            response = self.client.models.generate_content(
                model=MODEL,
                contents=contents,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=get_gemini_schema(FormulaFilterOutput)
                )
            )
            
            import json
            json_output = json.loads(response.text)
            output = FormulaFilterOutput(**json_output)
            
            # Convert to our output format
            selected = []
            for f in output.selected_formulas[:max_formulas]:
                if f.is_important:
                    selected.append({
                        "latex": f.explanation,  # The model includes the formula in explanation
                        "explanation": f.explanation,
                        "selection_rationale": f.selection_rationale
                    })
            
            print(f"  - Selected {len(selected)} important formulas")
            return selected
            
        except Exception as e:
            print(f"  ⚠ Error filtering formulas: {e}")
            return []

    async def process_formulas(
        self, 
        markdown: str, 
        title: str,
        max_formulas: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Main entry point: extract and filter formulas from markdown.
        """
        print("  Processing formulas...")
        
        # Extract candidate formulas
        candidates = self.extract_formulas(markdown)
        
        if not candidates:
            print("  - No formulas found in paper")
            return []
        
        # Filter to find important ones
        important = await self.filter_formulas(
            candidates, 
            title, 
            markdown[:2000],
            max_formulas
        )
        
        return important

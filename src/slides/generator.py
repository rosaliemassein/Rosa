"""
Slide generator for the pipeline.
Converts paper PDF into structured slides with voice, goal, and remarks.
Uses Mistral OCR for PDF processing and OpenAI for slide generation.
"""

import os
from pathlib import Path
from typing import List, Dict, Any
from google import genai
from google.genai import types
from dotenv import load_dotenv

from src.paper.ocr_client import MistralOCRClient
from src.slides.models import SlidesOutput, SlidesGenerationResponse, Slide
from src.slides.prompts import SLIDE_GENERATOR_SYSTEM, SLIDE_GENERATOR_INPUT
from src.utils.gemini_schema import get_gemini_schema

load_dotenv()

MODEL = "gemini-3-flash-preview"


class SlideGenerator:
    """Generates slides from a paper PDF using OCR and Google Gemini."""
    
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in .env")
        
        self.client = genai.Client(api_key=self.api_key)
        self.ocr_client = MistralOCRClient()
    
    def extract_paper(self, pdf_path: Path, output_dir: Path) -> Dict[str, Any]:
        """Run OCR on the PDF to get markdown and images."""
        return self.ocr_client.extract_from_pdf(pdf_path, output_dir)
    
    def extract_title(self, markdown: str) -> str:
        """Extract paper title from markdown."""
        lines = markdown.strip().split("\n")
        for line in lines[:20]:
            line = line.strip()
            if line.startswith("# "):
                return line[2:].strip()
            if line and not line.startswith("!") and 10 < len(line) < 200:
                return line
        return "Untitled Paper"
    
    async def generate_slides(
        self,
        title: str,
        markdown_content: str,
        images: List[Dict[str, Any]],
        user_profile: str = "A curious reader interested in understanding this paper."
    ) -> SlidesOutput:
        """Generate slides from paper content using Gemini."""
        
        # Format image descriptions
        if images:
            image_desc = "\n".join([
                f"- {img['id']}: {img.get('filename', 'image')}"
                for img in images
            ])
        else:
            image_desc = "No images extracted from this paper."
        
        # Build prompt
        user_input = SLIDE_GENERATOR_INPUT.format(
            title=title,
            user_profile=user_profile,
            markdown_content=markdown_content[:30000],  # Increased token limit for Gemini
            image_descriptions=image_desc
        )
        
        print("  Generating slides with Gemini...")
        
        # Build contents with system instruction
        contents = [
            types.Content(
                role="user",
                parts=[types.Part(text=f"{SLIDE_GENERATOR_SYSTEM}\n\n{user_input}")]
            )
        ]
        
        response = self.client.models.generate_content(
            model=MODEL,
            contents=contents,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=get_gemini_schema(SlidesGenerationResponse)
            )
        )
        
        # Parse JSON output — Gemini returns {slides: [...]}, we add the known title
        import json
        json_output = json.loads(response.text)
        gen_response = SlidesGenerationResponse(**json_output)
        output = SlidesOutput(title=title, slides=gen_response.slides)
        
        print(f"  ✓ Generated {len(output.slides)} slides")
        return output
    
    async def process_paper(
        self, 
        folder_path: Path,
        user_profile: str = None
    ) -> SlidesOutput:
        """
        Full pipeline: PDF → OCR → Slides.
        
        Args:
            folder_path: Path to folder containing the PDF
            user_profile: Optional user profile for personalization
        """
        folder = Path(folder_path).resolve()
        output_dir = folder / "outputs"
        output_dir.mkdir(exist_ok=True)
        
        # Find PDF
        pdfs = list(folder.glob("*.pdf"))
        if not pdfs:
            raise FileNotFoundError(f"No PDF file found in {folder}")
        pdf_path = pdfs[0]
        
        # Load profile if exists
        if user_profile is None:
            profile_path = folder / "profile.txt"
            if profile_path.exists():
                user_profile = profile_path.read_text().strip()
            else:
                user_profile = "A curious reader interested in this topic."
        
        print(f"\n[1/2] Running OCR on {pdf_path.name}...")
        ocr_results = self.extract_paper(pdf_path, output_dir)
        
        markdown = ocr_results["markdown"]
        images = ocr_results["images"]
        title = self.extract_title(markdown)
        
        print(f"  ✓ Paper title: {title}")
        
        print(f"\n[2/2] Generating slides...")
        slides = await self.generate_slides(title, markdown, images, user_profile)
        
        return slides

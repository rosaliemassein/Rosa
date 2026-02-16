"""
Image processor for evaluating and filtering amazing images.
Uses gpt-5-mini with the OpenAI beta.chat.completions.parse API for structured outputs.
"""

import os
import asyncio
import base64
from typing import List, Dict, Any
from google import genai
from google.genai import types
from src.slides.models import ImageEvaluation
from src.paper.prompts import IMAGE_EVALUATOR_SYSTEM, IMAGE_EVALUATOR_INPUT
from src.utils.gemini_schema import get_gemini_schema
from dotenv import load_dotenv

load_dotenv()

MODEL = "gemini-3-flash-preview"


class ImageProcessor:
    """Evaluates images to find 'amazing' ones and generates explanations."""
    
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found. Please set it in .env or environment variables.")
        
        self.client = genai.Client(api_key=self.api_key)

    async def evaluate_image(self, image_data: Dict[str, Any]) -> ImageEvaluation:
        """
        Uses Gemini for structured output.
        """
        if not image_data.get("base64"):
            return ImageEvaluation(is_amazing=False, reason="No image data", explanation="")

        try:
            # Decode base64 to bytes
            image_bytes = base64.b64decode(image_data['base64'])
            
            # Build contents with system instruction and image
            contents = [
                types.Content(
                    role="user",
                    parts=[
                        types.Part(text=f"{IMAGE_EVALUATOR_SYSTEM}\n\n{IMAGE_EVALUATOR_INPUT}"),
                        types.Part.from_bytes(data=image_bytes, mime_type="image/png")
                    ]
                )
            ]
            
            response = self.client.models.generate_content(
                model=MODEL,
                contents=contents,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=get_gemini_schema(ImageEvaluation)
                )
            )
            
            import json
            json_output = json.loads(response.text)
            return ImageEvaluation(**json_output)
            
        except Exception as e:
            print(f"Error evaluating image {image_data.get('id', 'unknown')}: {e}")
            return ImageEvaluation(is_amazing=False, reason=f"Error: {str(e)}", explanation="")

    async def process_images(self, images: List[Dict[str, Any]], max_amazing: int = 2) -> List[Dict[str, Any]]:
        """
        Evaluates a list of images and returns the top amazing ones.
        Returns a list of dicts with 'id', 'path', 'explanation'.
        """
        if not images:
            return []
            
        amazing_candidates = []
        
        print(f"  - Evaluating {len(images)} images...")
        
        # Parallel evaluation
        tasks = [self.evaluate_image(img) for img in images]
        evaluations = await asyncio.gather(*tasks)
        
        for img, eval_res in zip(images, evaluations):
            if eval_res.is_amazing:
                amazing_candidates.append({
                    "id": img["id"],
                    "path": img["path"],
                    "base64": img.get("base64"),  # Keep base64 for block generator
                    "explanation": eval_res.explanation,
                    "reason": eval_res.reason
                })
                print(f"    ✓ Image {img['id']}: AMAZING - {eval_res.explanation[:50]}...")
            else:
                print(f"    ✗ Image {img['id']}: Not essential")

        # Select top amazing images
        selected_images = amazing_candidates[:max_amazing]
        print(f"  - Selected {len(selected_images)} amazing images")
        
        return selected_images

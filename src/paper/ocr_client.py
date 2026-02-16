"""
OCR client for processing a single PDF paper using Mistral OCR.
Saves markdown and images to the specified output directory.
"""

import os
import base64
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv
from mistralai import Mistral

load_dotenv()


class MistralOCRClient:
    """
    Handles OCR extraction from PDFs using Mistral's official Python SDK.
    Extracts text and images, saving them to the specified output directory.
    """
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("MISTRAL_API_KEY")
        if not self.api_key:
            raise ValueError("MISTRAL_API_KEY not found. Please set it in .env or environment variables.")
        self.client = Mistral(api_key=self.api_key)

    def extract_from_pdf(self, pdf_path: Path, output_dir: Path) -> Dict[str, Any]:
        """
        Run Mistral OCR on a local PDF file.
        
        Args:
            pdf_path: Path to the PDF file
            output_dir: Directory where files will be saved
            
        Returns:
            Dictionary containing:
                - markdown: Full extracted text in markdown format
                - markdown_file: Path to saved markdown file
                - images: List of extracted images with metadata
                - output_dir: Directory where files are saved
        """
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF not found at: {pdf_path}")
        
        # Validate it's a PDF
        with open(pdf_path, "rb") as f:
            header = f.read(4)
            if header != b'%PDF':
                raise ValueError(f"File is not a valid PDF: {pdf_path}")
        
        print(f"Running Mistral OCR on {pdf_path.name}...")
        
        # Read and encode PDF as data URI
        with open(pdf_path, "rb") as f:
            encoded_pdf = base64.b64encode(f.read()).decode("utf-8")
        
        # Create data URI for base64 PDF
        data_uri = f"data:application/pdf;base64,{encoded_pdf}"

        # Call Mistral OCR API using official SDK
        try:
            ocr_response = self.client.ocr.process(
                model="mistral-ocr-latest",
                document={
                    "type": "document_url",
                    "document_url": data_uri
                },
                include_image_base64=True
            )
        except Exception as e:
            print(f"✗ Mistral API Error: {type(e).__name__}: {e}")
            raise
        
        # Create output directory and images subdirectory
        output_dir.mkdir(parents=True, exist_ok=True)
        images_dir = output_dir / "images"
        images_dir.mkdir(exist_ok=True)
        
        # Process results
        full_markdown = ""
        images = []
        
        # Extract markdown and images from each page
        for i, page in enumerate(ocr_response.pages):
            page_markdown = page.markdown or ""
            full_markdown += page_markdown + "\n\n"
            
            # Extract images from this page
            page_images = page.images or []
            
            for img_idx, img in enumerate(page_images):
                img_id = img.id or f"p{i}_i{img_idx}"
                img_data = img.image_base64
                
                if img_data:
                    # Mistral returns data URIs: data:image/png;base64,...
                    if "," in img_data:
                        header, base64_str = img_data.split(",", 1)
                        # Try to get extension from header like "data:image/png;base64"
                        ext = "png"  # default
                        if "image/" in header:
                            ext_part = header.split("image/", 1)[1].split(";", 1)[0]
                            if ext_part:
                                ext = ext_part
                    else:
                        base64_str = img_data
                        ext = "png"

                    # Use img_id directly as filename if it seems to have an extension
                    img_filename = img_id
                    if "." not in img_filename:
                        img_filename = f"{img_id}.{ext}"
                    
                    img_path = images_dir / img_filename
                    
                    try:
                        with open(img_path, "wb") as f:
                            f.write(base64.b64decode(base64_str))
                        
                        images.append({
                            "id": img_id,
                            "filename": img_filename,
                            "path": str(img_path),
                            "base64": base64_str  # Keep for LLM evaluation
                        })
                        
                        # Update markdown references
                        old_placeholder = f"![{img_id}]({img_id})"
                        new_placeholder = f"![{img_filename}](images/{img_filename})"
                        if old_placeholder != new_placeholder:
                            full_markdown = full_markdown.replace(old_placeholder, new_placeholder)
                    except Exception as e:
                        print(f"  ⚠ Failed to save image {img_id}: {e}")
        
        # Save markdown file
        markdown_file = output_dir / "paper.md"
        with open(markdown_file, "w", encoding="utf-8") as f:
            f.write(full_markdown)
        
        print(f"✓ Extracted {len(ocr_response.pages)} pages, {len(images)} images")
        print(f"  Saved to: {output_dir}")
        
        return {
            "markdown": full_markdown,
            "markdown_file": str(markdown_file),
            "images": images,
            "output_dir": str(output_dir)
        }

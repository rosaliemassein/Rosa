"""
Manim code generator using LMStudio's local Chat Completions API.
Generates Manim Python code from slide metadata using a local LLM.
Uses fresh conversations for retries with avoidance notes (no message history chaining).
Optimized for small context windows.
"""

import csv
import re
import json
import asyncio
import time
from typing import Optional, List, Dict, Any
import os
from openai import AsyncOpenAI
from google import genai
from google.genai import types

from src.manim.models import ManimCode
from src.manim.prompts_lmstudio import (
    LMSTUDIO_SYSTEM,
    LMSTUDIO_INPUT,
    LMSTUDIO_WITH_FORMULA,
    LMSTUDIO_RETRY_AVOIDANCE,
    LMSTUDIO_COMPILE_ERROR,
    LMSTUDIO_FEEDBACK,
    MANIM_TUTOR_SYSTEM,
    MANIM_TUTOR_FIRST_FIX,
    MANIM_TUTOR_SUBSEQUENT_FIX,
    LMSTUDIO_TIER_A_ADDENDUM,
    LMSTUDIO_TIER_B_ADDENDUM,
    LMSTUDIO_TIER_BPLUS_ADDENDUM,
    LMSTUDIO_TIER_C_ADDENDUM,
    LMSTUDIO_TIER_3DLITE_ADDENDUM,
    VERTICAL_ADDENDUM_LMSTUDIO,
    VERTICAL_ADDENDUM_TUTOR,
)
from src.slides.models import Slide


BASE_URL = "http://localhost:1234/v1"
MODEL = os.getenv("LMSTUDIO_MODEL", "qwen2.5-coder-3b-instruct-mlx")
GEMINI_MODEL = "gemini-3-flash-preview"


def _extract_avoidance_notes(error_msg: str) -> str:
    """
    Convert a raw compilation error into concise avoidance notes
    for the next fresh attempt.
    """
    notes = []

    err_lower = error_msg.lower()

    if "mathtex" in err_lower or "latex" in err_lower or "tex" in err_lower:
        notes.append("- Do NOT use invalid LaTeX. Use raw strings: MathTex(r\"\\\\frac{a}{b}\").")
    if "animate" in err_lower:
        notes.append("- Do NOT use .animate inside Transform(). Use Transform(a, b) with raw Mobjects.")
    if "has no attribute" in err_lower or "attributeerror" in err_lower:
        notes.append("- Check Manim API method names. Some methods may not exist. Verify before using.")
    if "typeerror" in err_lower or "argument" in err_lower:
        notes.append("- self.play() takes Animation objects (Write, FadeIn, Create, Transform), NOT raw Mobjects.")
    if "nameerror" in err_lower or "not defined" in err_lower:
        notes.append("- Make sure all variables are defined before use. Use `from manim import *`.")
    if "syntaxerror" in err_lower or "syntax" in err_lower:
        notes.append("- Fix Python syntax: check parentheses, colons, indentation.")
    if "indentation" in err_lower:
        notes.append("- Fix indentation: all code inside construct() must be indented consistently.")

    # Always include the raw error (truncated) as a catch-all
    truncated_err = error_msg.strip()[:400]
    notes.append(f"- Previous error was: {truncated_err}")

    return "\n".join(notes)


class ManimGeneratorLMStudio:
    """Generates Manim code for slides using LMStudio's local Chat Completions API."""
    
    
    def __init__(self, vertical: bool = False):
        # LMStudio local client
        self.client = AsyncOpenAI(base_url=BASE_URL, api_key="lm-studio")
        self.vertical = vertical
        self.gate_tier = os.getenv("MANIM_GATE_TIER", "A").strip().upper()
        self.disable_gemini_fallback = os.getenv("LMSTUDIO_DISABLE_GEMINI_FALLBACK", "0").strip() == "1"
        
        # Google Gemini setup for fallback/tutor
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        if self.gemini_api_key:
            self.gemini_client = genai.Client(api_key=self.gemini_api_key)
        else:
            self.gemini_client = None

    def _tier_addendum(self) -> str:
        if self.gate_tier in {"3DLITE", "3D-LITE"}:
            return LMSTUDIO_TIER_3DLITE_ADDENDUM
        if self.gate_tier in {"B+", "BPLUS"}:
            return LMSTUDIO_TIER_BPLUS_ADDENDUM
        if self.gate_tier == "C":
            return LMSTUDIO_TIER_C_ADDENDUM
        if self.gate_tier == "B":
            return LMSTUDIO_TIER_B_ADDENDUM
        return LMSTUDIO_TIER_A_ADDENDUM
        
    def log_outcome(
        self,
        original_prompt: str,
        qwen_response: str,
        qwen_compiled: bool,
        gpt5mini_response: Optional[str] = None,
        gpt5mini_compiled: Optional[bool] = None
    ):
        """Append outcome to a CSV file."""
        file_path = "manim_generation_log.csv"
        file_exists = os.path.exists(file_path)
        
        with open(file_path, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["original_prompt", "qwen_response", "qwen_compiled", "gpt5mini_response", "gpt5mini_compiled"])
            
            writer.writerow([
                original_prompt,
                qwen_response,
                qwen_compiled,
                gpt5mini_response if gpt5mini_response is not None else "",
                gpt5mini_compiled if gpt5mini_compiled is not None else ""
            ])

    
    def _build_prompt(
        self,
        slide: Slide,
        paper_content: str = ""
    ) -> tuple[str, str]:
        """
        Build system instructions and user input for a slide.
        Now passes the FULL slide JSON object to the LLM.
        
        Returns:
            Tuple of (instructions, input_text)
        """
        formula_section = ""
        if slide.formula:
            formula_section = LMSTUDIO_WITH_FORMULA.format(formula=slide.formula[:500])
        
        # Serialize slide to JSON
        slide_json = json.dumps(slide.model_dump(), indent=2)

        input_text = LMSTUDIO_INPUT.format(
            slide_json=slide_json,
            formula_section=formula_section,
        )
        
        system = LMSTUDIO_SYSTEM
        system += self._tier_addendum()
        if self.vertical:
            system += VERTICAL_ADDENDUM_LMSTUDIO
        
        return system, input_text
    
    def _build_retry_prompt(
        self,
        slide: Slide,
        avoidance_notes: str,
        paper_content: str = ""
    ) -> tuple[str, str]:
        """
        Build system instructions and user input for a retry with avoidance notes.
        Starts a completely fresh conversation — no history from prior attempts.
        
        Returns:
            Tuple of (instructions, input_text)
        """
        formula_section = ""
        if slide.formula:
            formula_section = LMSTUDIO_WITH_FORMULA.format(formula=slide.formula[:500])
        
        # Serialize slide to JSON
        slide_json = json.dumps(slide.model_dump(), indent=2)

        input_text = LMSTUDIO_RETRY_AVOIDANCE.format(
            slide_json=slide_json,
            formula_section=formula_section,
            avoidance_notes=avoidance_notes,
        )
        
        system = LMSTUDIO_SYSTEM
        system += self._tier_addendum()
        if self.vertical:
            system += VERTICAL_ADDENDUM_LMSTUDIO
        
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
    ) -> tuple[ManimCode, list[dict], str, str]:
        """
        Generate Manim code for a single slide (initial generation).
        
        Returns:
            Tuple of (ManimCode, messages, prompt_text, instructions)
            - messages: Full conversation history for logging
            - prompt_text: The user input text for logging
            - instructions: The system instructions for logging
        """
        instructions, input_text = self._build_prompt(slide, paper_content)
        
        messages = [
            {"role": "system", "content": instructions},
            {"role": "user", "content": input_text},
        ]
        
        print(f"    ⏳ Calling LMStudio ({MODEL})...")
        t0 = time.time()
        response = await self.client.chat.completions.create(
            model=MODEL,
            messages=messages,
        )
        elapsed = time.time() - t0
        print(f"    ✓ LMStudio responded ({elapsed:.1f}s)")
        
        raw_code = response.choices[0].message.content
        manim_code = self._parse_manim_code(raw_code, slide.id)
        
        # Append assistant response to history for logging
        messages.append({"role": "assistant", "content": raw_code})
        
        return manim_code, messages, input_text, instructions
    
    async def retry_with_error(
        self,
        slide_id: str,
        messages: list[dict],
        error_msg: str
    ) -> tuple[ManimCode, list[dict]]:
        """
        Retry logic with fallback to Gemini 3 Flash "Tutor" if not already using it.
        
        Logic:
        1. If current messages use Qwen (LMSTUDIO_SYSTEM), SWITCH to Gemini (Tutor).
           - Construct new "Tutor" conversation: System + (Prompt + BadCode + Error).
        2. If current messages use Tutor (MANIM_TUTOR_SYSTEM), APPEND error to history.
           - Continue conversation: + (NewError).
        """
        
        # Check if we are already in "Tutor Mode"
        # Use startswith() because the system content may include VERTICAL_ADDENDUM_TUTOR
        is_tutor_mode = False
        if messages and messages[0].get("content", "").startswith(MANIM_TUTOR_SYSTEM):
            is_tutor_mode = True
            
        if not is_tutor_mode:
            # Qwen-only mode: retry using LMStudio directly, no Gemini fallback.
            if self.disable_gemini_fallback or not self.gemini_client:
                retry_prompt = LMSTUDIO_COMPILE_ERROR.format(error=error_msg[:2000])
                fresh_messages = [
                    messages[0],  # Keep the tier-aware system prompt
                    {"role": "user", "content": retry_prompt},
                ]
                print(f"    ⏳ Retrying with LMStudio only (Gemini fallback disabled)...")
                t0 = time.time()
                response = await self.client.chat.completions.create(
                    model=MODEL,
                    messages=fresh_messages,
                )
                elapsed = time.time() - t0
                print(f"    ✓ LMStudio responded ({elapsed:.1f}s)")
                raw_code = response.choices[0].message.content
                manim_code = self._parse_manim_code(raw_code, slide_id)
                fresh_messages.append({"role": "assistant", "content": raw_code})
                return manim_code, fresh_messages

            # --- FALLBACK START: Switch to Gemini Tutor ---
            # We need the original prompt (idea) and the failed code.
            
            original_prompt = messages[1]["content"] if len(messages) > 1 else "Unknown Prompt"
            failed_code = messages[-1]["content"] if len(messages) > 0 else ""
            
            # Construct the "Tutor" Prompt
            vertical_section = ""
            if self.vertical:
                vertical_section = "\nIMPORTANT: This video uses VERTICAL FORMAT (9:16 portrait). Keep all elements within x ∈ [-3.5, 3.5], y ∈ [-6.5, 6.5]. Use .scale() aggressively, stack vertically with .arrange(DOWN), and do NOT use wide horizontal layouts.\n"
            
            tutor_input = MANIM_TUTOR_FIRST_FIX.format(
                original_prompt=original_prompt,
                failed_code=failed_code,
                error_log=error_msg[:2000],
                vertical_section=vertical_section,
            )
            
            # Build tutor system prompt (with vertical addendum if needed)
            tutor_system = MANIM_TUTOR_SYSTEM
            if self.vertical:
                tutor_system += VERTICAL_ADDENDUM_TUTOR
            
            # Start fresh conversation in OpenAI format for consistency
            fresh_messages = [
                {"role": "system", "content": tutor_system},
                {"role": "user", "content": tutor_input}
            ]
            
            print(f"    ⏳ Switching to {GEMINI_MODEL} (Tutor Mode) for correction...")
            
            # Helper to generate with Gemini
            t0 = time.time()
            raw_code = await self._generate_with_gemini(fresh_messages)
            elapsed = time.time() - t0
            print(f"    ✓ Gemini responded ({elapsed:.1f}s)")
            manim_code = self._parse_manim_code(raw_code, slide_id)
            
            fresh_messages.append({"role": "assistant", "content": raw_code})
            
            return manim_code, fresh_messages

        else:
            # --- CONTINUE TUTOR MODE: Append new error ---
            print(f"    ⏳ {GEMINI_MODEL} (Tutor Mode) retrying with new error...")
            
            retry_input = MANIM_TUTOR_SUBSEQUENT_FIX.format(
                error_log=error_msg[:2000]
            )
            
            messages.append({"role": "user", "content": retry_input})
            
            t0 = time.time()
            raw_code = await self._generate_with_gemini(messages)
            elapsed = time.time() - t0
            print(f"    ✓ Gemini responded ({elapsed:.1f}s)")
            manim_code = self._parse_manim_code(raw_code, slide_id)
            messages.append({"role": "assistant", "content": raw_code})
            
            return manim_code, messages

    async def _generate_with_gemini(self, messages: list[dict], max_retries: int = 3) -> str:
        """Helper to call Gemini API with OpenAI-style messages.
        
        Retries up to max_retries times on 503/UNAVAILABLE errors with exponential backoff.
        """
        if not self.gemini_client:
            raise ValueError("Gemini client not initialized. Please set GEMINI_API_KEY in .env")
        
        # separate system prompt
        system_instruction = None
        contents = []
        
        for msg in messages:
            role = msg["role"]
            content = msg["content"]
            
            if role == "system":
                system_instruction = content
            elif role == "user":
                contents.append(types.Content(role="user", parts=[types.Part(text=content)]))
            elif role == "assistant":
                contents.append(types.Content(role="model", parts=[types.Part(text=content)]))
        
        # Prepend system instruction to first user message if present
        if system_instruction and contents:
            for i, content in enumerate(contents):
                if content.role == "user":
                    contents[i] = types.Content(
                        role="user",
                        parts=[types.Part(text=f"{system_instruction}\n\n{contents[i].parts[0].text}")]
                    )
                    break
        
        last_error = None
        for attempt in range(1, max_retries + 1):
            try:
                response = self.gemini_client.models.generate_content(
                    model=GEMINI_MODEL,
                    contents=contents
                )
                return response.text
            except Exception as e:
                error_str = str(e)
                last_error = e
                # Check for 503 UNAVAILABLE or rate limit errors
                if "503" in error_str or "UNAVAILABLE" in error_str or "overloaded" in error_str.lower() or "high demand" in error_str.lower() or "429" in error_str:
                    wait_time = 30 * attempt  # 30s, 60s, 90s
                    print(f"    ⚠ Gemini API unavailable (attempt {attempt}/{max_retries}). Waiting {wait_time}s before retry...")
                    await asyncio.sleep(wait_time)
                else:
                    # Non-retryable error, raise immediately
                    raise
        
        # All retries exhausted
        raise last_error
    
    async def retry_with_feedback(
        self,
        slide_id: str,
        messages: list[dict],
        feedback_text: str
    ) -> tuple[ManimCode, list[dict]]:
        """
        Retry by starting a fresh conversation with feedback notes.
        
        Returns:
            Tuple of (ManimCode, updated_messages)
        """
        feedback_prompt = LMSTUDIO_FEEDBACK.format(feedback=feedback_text[:500])
        
        # Fresh conversation: system + feedback prompt only
        fresh_messages = [
            messages[0],  # system prompt
            {"role": "user", "content": feedback_prompt},
        ]
        
        print(f"    ⏳ Calling LMStudio ({MODEL}) with feedback...")
        t0 = time.time()
        response = await self.client.chat.completions.create(
            model=MODEL,
            messages=fresh_messages,
        )
        elapsed = time.time() - t0
        print(f"    ✓ LMStudio responded ({elapsed:.1f}s)")
        
        raw_code = response.choices[0].message.content
        manim_code = self._parse_manim_code(raw_code, slide_id)
        
        fresh_messages.append({"role": "assistant", "content": raw_code})
        
        return manim_code, fresh_messages
    
    async def fresh_retry_with_error(
        self,
        slide: Slide,
        failed_code: str,
        error_msg: str,
        paper_content: str = ""
    ) -> tuple[ManimCode, list[dict]]:
        """
        Start a fresh retry sequence with a completely new generation.
        
        Pipeline calls this when 'is_fresh_context' is True (after feedback failure or max retries exhausted loops).
        Usually implies a full reset.
        
        Returns only (ManimCode, messages) — discarding prompt_text and instructions
        since callers re-build those separately.
        """
        print(f"    ⏳ Starting fresh code generation (full reset)...")
        manim_code, messages, _, _ = await self.generate_code(slide, paper_content)
        return manim_code, messages

    
    def _extract_code(self, raw_output: str) -> str:
        """Extract Python code from LLM output, removing markdown fences."""
        code = raw_output.strip()

        # Remove any markdown fence lines globally (not only outer wrappers).
        cleaned_lines = []
        for line in code.splitlines():
            if line.strip().startswith("```"):
                continue
            cleaned_lines.append(line)
        code = "\n".join(cleaned_lines).strip()

        # Handle common accidental leading language marker.
        if code.lower().startswith("python\n"):
            code = code[len("python\n") :]

        return code.strip()
    
    def _extract_scene_name(self, code: str, fallback_id: str) -> str:
        """Extract the Scene class name from code."""
        match = re.search(r'class\s+(\w+)\s*\(\s*\w*Scene\w*\s*\)', code)
        if match:
            return match.group(1)
        
        # Fallback: generate from slide id
        return f"Slide{fallback_id.replace('slide_', '').replace('_', '').replace('-', '').title()}"

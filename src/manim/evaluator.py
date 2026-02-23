"""
Code evaluation utilities for compile-first stabilization.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

from src.manim.gate import GateConfig, strip_markdown_fences, validate_manim_code
from src.manim.models import ManimCode


ERROR_BUCKETS = {"gate_fail", "syntax", "undefined_name", "manim_error", "timeout"}


@dataclass
class EvaluationResult:
    reward: int
    error_bucket: str
    gate_pass: bool
    gate_errors: list[str]
    gate_reason_tags: list[str]
    detected_features: list[str]
    undefined_names: list[str]
    compiled: bool
    video_path: Optional[Path]
    stderr: str
    sanitized_code: str


def _classify_render_error(stderr: str) -> str:
    err = (stderr or "").lower()
    if "syntaxerror" in err:
        return "syntax"
    if "nameerror" in err or "not defined" in err:
        return "undefined_name"
    if "timed out" in err or "timeout" in err:
        return "timeout"
    return "manim_error"


def evaluate_code(
    *,
    manim_code: ManimCode,
    executor: Any,
    version: int = 1,
    quality: str = "l",
    vertical: bool = False,
    gate_config: GateConfig | None = None,
    timeout_seconds: int | None = 90,
) -> EvaluationResult:
    """
    Evaluate generated Manim code with strict gate-first policy.

    1) Gate validation
    2) If gate passes, render test with Manim
    """
    sanitized = strip_markdown_fences(manim_code.code)
    gate = validate_manim_code(sanitized, config=gate_config)

    if not gate["gate_pass"]:
        return EvaluationResult(
            reward=-1,
            error_bucket="gate_fail",
            gate_pass=False,
            gate_errors=gate["gate_errors"],
            gate_reason_tags=gate.get("gate_reason_tags", []),
            detected_features=gate["detected_features"],
            undefined_names=gate["undefined_names"],
            compiled=False,
            video_path=None,
            stderr="; ".join(gate["gate_errors"]),
            sanitized_code=sanitized,
        )

    code_to_eval = ManimCode(
        slide_id=manim_code.slide_id,
        scene_name=manim_code.scene_name,
        code=sanitized,
    )
    code_file = executor.save_code(code_to_eval, version=version, vertical=vertical)
    success, video_path, stderr = executor.execute(
        code_to_eval,
        code_file,
        quality=quality,
        version=version,
        vertical=vertical,
        timeout_seconds=timeout_seconds,
    )
    bucket = "manim_error" if not success else ""
    if not success:
        bucket = _classify_render_error(stderr)
    return EvaluationResult(
        reward=1 if success else -1,
        error_bucket=bucket,
        gate_pass=True,
        gate_errors=[],
        gate_reason_tags=gate.get("gate_reason_tags", []),
        detected_features=gate["detected_features"],
        undefined_names=gate["undefined_names"],
        compiled=success,
        video_path=video_path,
        stderr=stderr,
        sanitized_code=sanitized,
    )

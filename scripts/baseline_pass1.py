#!/usr/bin/env python3
"""
Phase 1 baseline pass@1 runner with error bucket breakdown.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.manim.evaluator import evaluate_code
from src.manim.executor import ManimExecutor
from src.manim.models import ManimCode


def infer_scene_name(code: str, default: str = "GeneratedScene") -> str:
    match = re.search(r"class\s+(\w+)\s*\(\s*(?:Scene|ThreeDScene)\s*\)\s*:", code)
    if match:
        return match.group(1)
    return default


def base_slide_id(path: Path) -> str:
    return re.sub(r"_v\d+$", "", path.stem)


def choose_pass1_candidates(slides_dir: Path) -> list[Path]:
    groups: dict[str, list[Path]] = {}
    for file in slides_dir.glob("*.py"):
        groups.setdefault(base_slide_id(file), []).append(file)

    selected: list[Path] = []
    for sid, files in groups.items():
        preferred = slides_dir / f"{sid}.py"
        if preferred in files:
            selected.append(preferred)
        else:
            selected.append(sorted(files, key=lambda p: p.name)[0])
    return sorted(selected, key=lambda p: p.name)


def main() -> None:
    parser = argparse.ArgumentParser(description="Compute pass@1 and error breakdown.")
    parser.add_argument("output_dir", help="Path to outputs directory (contains slides/ and videos/)")
    args = parser.parse_args()

    output_dir = Path(args.output_dir).resolve()
    slides_dir = output_dir / "slides"
    if not slides_dir.exists():
        raise FileNotFoundError(f"Slides directory not found: {slides_dir}")

    executor = ManimExecutor(output_dir)
    candidates = choose_pass1_candidates(slides_dir)

    rewards: list[int] = []
    buckets = Counter()

    for code_path in candidates:
        code = code_path.read_text(encoding="utf-8")
        sid = base_slide_id(code_path)
        scene_name = infer_scene_name(code, default=f"Scene_{sid}")
        result = evaluate_code(
            manim_code=ManimCode(slide_id=sid, scene_name=scene_name, code=code),
            executor=executor,
            version=1,
            quality="l",
            vertical=False,
            timeout_seconds=90,
        )
        rewards.append(result.reward)
        bucket = result.error_bucket if result.error_bucket else "success"
        buckets[bucket] += 1

    total = len(rewards)
    passed = sum(1 for r in rewards if r == 1)
    pass_at_1 = (passed / total) if total else 0.0
    reward_mean = (sum(rewards) / total) if total else 0.0

    print("=== Phase 1 Baseline ===")
    print(f"total_evaluated: {total}")
    print(f"pass@1: {pass_at_1:.3f}")
    print(f"reward_mean: {reward_mean:.3f}")
    print("error_breakdown:")
    for key in ["gate_fail", "syntax", "undefined_name", "manim_error", "timeout", "success"]:
        print(f"  {key}: {buckets.get(key, 0)}")


if __name__ == "__main__":
    main()

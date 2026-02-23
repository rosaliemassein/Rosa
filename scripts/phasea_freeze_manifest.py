#!/usr/bin/env python3
"""
Create a reproducible run manifest for Phase A benchmark experiments.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path


def git_commit(root: Path) -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()
    except Exception:
        return "unknown"


def main() -> None:
    parser = argparse.ArgumentParser(description="Freeze Phase A benchmark manifest.")
    parser.add_argument(
        "--benchmark-config",
        default="config/phasea_benchmark.json",
        help="Path to benchmark config JSON.",
    )
    parser.add_argument("--run-id", default=None, help="Optional run identifier.")
    parser.add_argument("--model-id", default="qwen2.5-coder-3b-instruct-mlx")
    parser.add_argument("--prompt-version", default="phasea_tiera_v1")
    parser.add_argument("--gate-tier", default=None, help="Override gate tier (A/B/C).")
    parser.add_argument("--notes", default="")
    parser.add_argument(
        "--out-json",
        default="reports/phasea_run_manifest.json",
        help="Output manifest JSON path.",
    )
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parents[1]
    config_path = (project_root / args.benchmark_config).resolve()
    cfg = json.loads(config_path.read_text(encoding="utf-8"))

    run_id = args.run_id or datetime.now(timezone.utc).strftime("phasea_%Y%m%dT%H%M%SZ")
    gate_tier = args.gate_tier or os.environ.get("MANIM_GATE_TIER") or cfg.get("settings", {}).get("tier", "A")
    manifest = {
        "run_id": run_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "benchmark_name": cfg.get("name", "phasea_compile_reliability"),
        "benchmark_config": str(config_path),
        "model_id": args.model_id,
        "prompt_version": args.prompt_version,
        "gate_tier": str(gate_tier).upper(),
        "quality": cfg.get("settings", {}).get("quality", "l"),
        "timeout_seconds": cfg.get("settings", {}).get("timeout_seconds", 90),
        "papers_count": len(cfg.get("papers", [])),
        "papers": cfg.get("papers", []),
        "git_commit": git_commit(project_root),
        "notes": args.notes,
    }

    out_path = (project_root / args.out_json).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"saved_manifest: {out_path}")


if __name__ == "__main__":
    main()

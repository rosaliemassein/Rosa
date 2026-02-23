#!/usr/bin/env python3
"""
Export structured compile-focused dataset from tracker CSV + conversation logs.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


def parse_conversation_log(path: Path) -> dict[str, str]:
    if not path.exists():
        return {"system": "", "user": "", "assistant": "", "error": ""}

    sections: dict[str, str] = {"SYSTEM": "", "USER": "", "ASSISTANT": "", "ERROR": ""}
    current: str | None = None
    buffer: list[str] = []

    for raw_line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw_line.rstrip("\n")
        if line.startswith("=== ") and line.endswith(" ==="):
            if current is not None:
                sections[current] = "\n".join(buffer).strip()
            current = line.replace("=== ", "").replace(" ===", "")
            buffer = []
        else:
            buffer.append(line)

    if current is not None:
        sections[current] = "\n".join(buffer).strip()

    return {
        "system": sections.get("SYSTEM", ""),
        "user": sections.get("USER", ""),
        "assistant": sections.get("ASSISTANT", ""),
        "error": sections.get("ERROR", ""),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Export Phase A dataset as JSONL.")
    parser.add_argument(
        "--results-root",
        default="paper",
        help="Root directory to scan for outputs/pipeline_results.csv",
    )
    parser.add_argument(
        "--out-jsonl",
        default="reports/phasea_dataset.jsonl",
        help="Output JSONL path",
    )
    args = parser.parse_args()

    root = Path(args.results_root).resolve()
    csv_paths = sorted(root.glob("**/outputs/pipeline_results.csv"))
    if (root / "outputs" / "pipeline_results.csv").exists():
        p = root / "outputs" / "pipeline_results.csv"
        if p not in csv_paths:
            csv_paths.append(p)

    out_path = Path(args.out_jsonl).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    count = 0
    source_counts = Counter()
    bucket_counts = Counter()
    with out_path.open("w", encoding="utf-8") as out:
        for csv_path in csv_paths:
            output_dir = csv_path.parent
            with csv_path.open("r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    convo_rel = row.get("conversation_log", "")
                    convo_path = output_dir / convo_rel if convo_rel else Path("")
                    convo = parse_conversation_log(convo_path) if convo_rel else {
                        "system": "",
                        "user": "",
                        "assistant": "",
                        "error": "",
                    }

                    compiled = str(row.get("compiled", "")).lower() == "true"
                    retries = int(row.get("compile_retries", "0") or 0)
                    if not compiled:
                        success_source = "none"
                    elif retries == 0:
                        success_source = "qwen_only"
                    else:
                        # In current retry flow, compile retries imply correction loop engagement.
                        success_source = "assisted_or_retry"

                    bucket = row.get("error_bucket", "") or "success"
                    item = {
                        "slide_id": row.get("slide_id", ""),
                        "attempt": row.get("attempt", ""),
                        "status": row.get("status", ""),
                        "compiled": row.get("compiled", ""),
                        "reward": row.get("reward", ""),
                        "error_bucket": row.get("error_bucket", ""),
                        "gate_errors": row.get("gate_errors", ""),
                        "gate_reason_tags": row.get("gate_reason_tags", ""),
                        "detected_features": row.get("detected_features", ""),
                        "undefined_names": row.get("undefined_names", ""),
                        "manim_file": row.get("manim_file", ""),
                        "video_file": row.get("video_file", ""),
                        "compile_retries": row.get("compile_retries", ""),
                        "prompt_system": convo["system"],
                        "prompt_user": convo["user"],
                        "generated_code": convo["assistant"],
                        "stderr_or_error": convo["error"],
                        "source_csv": str(csv_path),
                        "success_source": success_source,
                    }
                    out.write(json.dumps(item, ensure_ascii=False) + "\n")
                    count += 1
                    source_counts[success_source] += 1
                    bucket_counts[bucket] += 1

    print(f"exported_records: {count}")
    print(f"success_source_counts: {dict(source_counts)}")
    print(f"bucket_counts: {dict(bucket_counts)}")
    print(f"saved_jsonl: {out_path}")


if __name__ == "__main__":
    main()

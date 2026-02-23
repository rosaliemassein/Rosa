#!/usr/bin/env python3
"""
Check Phase A go/no-go criteria from a sequence of metrics JSON files.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


LOW_LEVEL_BUCKETS = ["syntax", "undefined_name", "gate_fail"]


def load_metrics(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate Phase A go/no-go criteria.")
    parser.add_argument(
        "metrics_files",
        nargs="+",
        help="Ordered metrics JSON files (oldest -> newest).",
    )
    args = parser.parse_args()

    metrics = [load_metrics(Path(p).resolve()) for p in args.metrics_files]
    if len(metrics) < 2:
        raise ValueError("Provide at least baseline and one follow-up metrics file.")

    baseline = metrics[0]
    latest = metrics[-1]
    recent = metrics[-3:] if len(metrics) >= 3 else metrics

    pass_improved = latest.get("pass_at_1", 0.0) > baseline.get("pass_at_1", 0.0)

    sustained_bucket_reduction = True
    for bucket in LOW_LEVEL_BUCKETS:
        values = [m.get("bucket_counts", {}).get(bucket, 0) for m in recent]
        if any(values[i] > values[i - 1] for i in range(1, len(values))):
            sustained_bucket_reduction = False
            break

    reproducible = all(m.get("csv_files") for m in recent)

    go = pass_improved and sustained_bucket_reduction and reproducible

    print("=== Phase A Go/No-Go ===")
    print(f"baseline_pass@1: {baseline.get('pass_at_1', 0.0)}")
    print(f"latest_pass@1: {latest.get('pass_at_1', 0.0)}")
    print(f"pass_improved: {pass_improved}")
    print(f"sustained_low_level_bucket_reduction: {sustained_bucket_reduction}")
    print(f"reproducible_inputs_detected: {reproducible}")
    print(f"decision: {'GO' if go else 'NO_GO'}")


if __name__ == "__main__":
    main()

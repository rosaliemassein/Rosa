#!/usr/bin/env python3
"""
Aggregate Phase A compile metrics from pipeline_results.csv files.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path


BUCKET_KEYS = ["gate_fail", "syntax", "undefined_name", "manim_error", "timeout"]


def detect_bucket(row: dict[str, str]) -> str:
    bucket = (row.get("error_bucket") or "").strip()
    if bucket:
        return bucket

    status = (row.get("status") or "").lower()
    if "timeout" in status:
        return "timeout"
    if "syntax" in status:
        return "syntax"
    if "undefined" in status or "nameerror" in status:
        return "undefined_name"
    if "compile_failed" in status:
        return "manim_error"
    return ""


def parse_results(csv_path: Path) -> list[dict[str, str]]:
    with csv_path.open("r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def summarize(csv_paths: list[Path]) -> dict:
    total_attempts = 0
    total_compiled = 0
    bucket_counts = Counter()
    feature_counts = Counter()
    reason_tag_counts = Counter()
    pass1_total = 0
    pass1_success = 0
    top_errors = Counter()
    by_slide_first_attempt: dict[str, dict[str, str]] = {}

    for csv_path in csv_paths:
        rows = parse_results(csv_path)
        for row in rows:
            total_attempts += 1
            compiled = str(row.get("compiled", "")).lower() == "true"
            if compiled:
                total_compiled += 1

            bucket = detect_bucket(row)
            if bucket:
                bucket_counts[bucket] += 1

            features = (row.get("detected_features") or "").strip()
            if features:
                for feat in features.split("|"):
                    if feat:
                        feature_counts[feat] += 1

            tags = (row.get("gate_reason_tags") or "").strip()
            if tags:
                for tag in tags.split("|"):
                    if tag:
                        reason_tag_counts[tag] += 1

            gate_err = (row.get("gate_errors") or "").strip()
            if gate_err:
                top_errors[gate_err] += 1
            elif not compiled and row.get("status"):
                top_errors[row["status"]] += 1

            slide_id = row.get("slide_id", "")
            if slide_id:
                prev = by_slide_first_attempt.get(slide_id)
                attempt_raw = row.get("attempt") or ""
                try:
                    attempt = int(attempt_raw)
                except Exception:
                    attempt = 999999
                if prev is None:
                    by_slide_first_attempt[slide_id] = {"attempt": str(attempt), "compiled": str(compiled)}
                else:
                    prev_attempt = int(prev["attempt"])
                    if attempt < prev_attempt:
                        by_slide_first_attempt[slide_id] = {"attempt": str(attempt), "compiled": str(compiled)}

    pass1_total = len(by_slide_first_attempt)
    for item in by_slide_first_attempt.values():
        if item["attempt"] == "1" and item["compiled"].lower() == "true":
            pass1_success += 1

    pass_at_1 = (pass1_success / pass1_total) if pass1_total else 0.0
    compile_rate = (total_compiled / total_attempts) if total_attempts else 0.0

    return {
        "csv_files": [str(p) for p in csv_paths],
        "total_attempts": total_attempts,
        "compiled_attempts": total_compiled,
        "compile_rate": round(compile_rate, 4),
        "slides_evaluated_for_pass1": pass1_total,
        "pass_at_1": round(pass_at_1, 4),
        "bucket_counts": {k: bucket_counts.get(k, 0) for k in BUCKET_KEYS},
        "feature_counts": dict(feature_counts),
        "gate_reason_tag_counts": dict(reason_tag_counts),
        "top_error_signatures": top_errors.most_common(10),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Collect Phase A compile metrics.")
    parser.add_argument(
        "--results-root",
        default="paper",
        help="Root directory to scan for outputs/pipeline_results.csv",
    )
    parser.add_argument(
        "--out-json",
        default="reports/phasea_metrics_latest.json",
        help="Where to write JSON summary.",
    )
    args = parser.parse_args()

    root = Path(args.results_root).resolve()
    csv_paths = sorted(root.glob("**/outputs/pipeline_results.csv"))
    # Also include direct outputs path at root (legacy single-run layout).
    if (root / "outputs" / "pipeline_results.csv").exists():
        p = root / "outputs" / "pipeline_results.csv"
        if p not in csv_paths:
            csv_paths.append(p)

    summary = summarize(csv_paths)

    out_path = Path(args.out_json).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print("=== Phase A Metrics ===")
    print(f"csv_files: {len(summary['csv_files'])}")
    print(f"total_attempts: {summary['total_attempts']}")
    print(f"compile_rate: {summary['compile_rate']}")
    print(f"pass@1: {summary['pass_at_1']}")
    print("bucket_counts:")
    for key in BUCKET_KEYS:
        print(f"  {key}: {summary['bucket_counts'].get(key, 0)}")
    print(f"saved_json: {out_path}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Compare two Phase A metrics snapshots and report net-positive status.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


LOW_LEVEL_BUCKETS = ["gate_fail", "syntax", "undefined_name"]


def load(path: str) -> dict:
    return json.loads(Path(path).resolve().read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare Phase A metric snapshots.")
    parser.add_argument("before", help="Path to earlier metrics JSON.")
    parser.add_argument("after", help="Path to later metrics JSON.")
    args = parser.parse_args()

    before = load(args.before)
    after = load(args.after)

    pass_before = before.get("pass_at_1", 0.0)
    pass_after = after.get("pass_at_1", 0.0)
    compile_before = before.get("compile_rate", 0.0)
    compile_after = after.get("compile_rate", 0.0)

    low_before = sum(before.get("bucket_counts", {}).get(k, 0) for k in LOW_LEVEL_BUCKETS)
    low_after = sum(after.get("bucket_counts", {}).get(k, 0) for k in LOW_LEVEL_BUCKETS)

    net_positive = (pass_after >= pass_before) and (compile_after >= compile_before) and (low_after <= low_before)

    print("=== Phase A Metrics Comparison ===")
    print(f"pass@1: {pass_before} -> {pass_after}")
    print(f"compile_rate: {compile_before} -> {compile_after}")
    print(f"low_level_bucket_total: {low_before} -> {low_after}")
    print(f"net_positive: {net_positive}")


if __name__ == "__main__":
    main()

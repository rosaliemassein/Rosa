#!/usr/bin/env python3
"""
Prepare a local SFT/LoRA dataset from compile-focused JSONL exports.

Outputs:
  - sft_all.jsonl
  - sft_train.jsonl
  - sft_val.jsonl
  - split_manifest.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def _stable_bucket(key: str, val_ratio: float) -> str:
    digest = hashlib.sha256(key.encode("utf-8")).hexdigest()
    frac = int(digest[:8], 16) / 0xFFFFFFFF
    return "val" if frac < val_ratio else "train"


def _paper_id(source_csv: str) -> str:
    parts = Path(source_csv).parts
    if "paper" in parts:
        i = parts.index("paper")
        if i + 2 < len(parts):
            return parts[i + 2]
    # Fallback: last folder before outputs/
    try:
        p = Path(source_csv)
        if "outputs" in p.parts:
            oi = p.parts.index("outputs")
            if oi >= 1:
                return p.parts[oi - 1]
    except Exception:
        pass
    return "unknown_paper"


def _quality_bucket(success_source: str, compile_retries: int) -> str:
    if success_source == "qwen_only":
        return "high"
    if success_source == "assisted_or_retry" and compile_retries <= 1:
        return "high"
    if success_source == "assisted_or_retry":
        return "medium"
    return "low"


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare local 7B LoRA SFT dataset.")
    parser.add_argument(
        "--input-jsonl",
        nargs="+",
        required=True,
        help="One or more phasea_dataset*.jsonl files.",
    )
    parser.add_argument(
        "--out-dir",
        default="reports/lora_7b_prep",
        help="Output directory for split artifacts.",
    )
    parser.add_argument(
        "--val-ratio",
        type=float,
        default=0.2,
        help="Validation split ratio by paper id.",
    )
    parser.add_argument(
        "--min-quality",
        choices=["high", "medium", "low"],
        default="medium",
        help="Minimum quality bucket to include.",
    )
    args = parser.parse_args()

    quality_rank = {"low": 0, "medium": 1, "high": 2}
    min_rank = quality_rank[args.min_quality]

    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    all_items: list[dict] = []
    dropped = {"not_compiled": 0, "missing_fields": 0, "low_quality": 0}
    source_counts: dict[str, int] = {}
    paper_counts: dict[str, int] = {}
    quality_counts = {"high": 0, "medium": 0, "low": 0}

    for in_path_raw in args.input_jsonl:
        in_path = Path(in_path_raw).resolve()
        if not in_path.exists():
            continue
        for raw in in_path.read_text(encoding="utf-8", errors="ignore").splitlines():
            if not raw.strip():
                continue
            row = json.loads(raw)

            compiled = str(row.get("compiled", "")).lower() == "true"
            if not compiled:
                dropped["not_compiled"] += 1
                continue

            prompt_system = (row.get("prompt_system") or "").strip()
            prompt_user = (row.get("prompt_user") or "").strip()
            completion = (row.get("generated_code") or "").strip()
            if not prompt_system or not prompt_user or not completion:
                dropped["missing_fields"] += 1
                continue

            success_source = row.get("success_source", "")
            retries = int(row.get("compile_retries") or 0)
            quality = _quality_bucket(success_source, retries)
            quality_counts[quality] += 1
            if quality_rank[quality] < min_rank:
                dropped["low_quality"] += 1
                continue

            paper = _paper_id(row.get("source_csv", ""))
            prompt = f"{prompt_system}\n\n{prompt_user}"
            item = {
                "prompt": prompt,
                "completion": completion,
                "paper_id": paper,
                "slide_id": row.get("slide_id", ""),
                "success_source": success_source,
                "compile_retries": retries,
                "quality_bucket": quality,
                "source_csv": row.get("source_csv", ""),
            }
            all_items.append(item)
            source_counts[success_source] = source_counts.get(success_source, 0) + 1
            paper_counts[paper] = paper_counts.get(paper, 0) + 1

    train_items: list[dict] = []
    val_items: list[dict] = []
    for item in all_items:
        bucket = _stable_bucket(item["paper_id"], args.val_ratio)
        if bucket == "val":
            val_items.append(item)
        else:
            train_items.append(item)

    all_path = out_dir / "sft_all.jsonl"
    train_path = out_dir / "sft_train.jsonl"
    val_path = out_dir / "sft_val.jsonl"

    with all_path.open("w", encoding="utf-8") as f:
        for item in all_items:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
    with train_path.open("w", encoding="utf-8") as f:
        for item in train_items:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
    with val_path.open("w", encoding="utf-8") as f:
        for item in val_items:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    manifest = {
        "input_files": [str(Path(p).resolve()) for p in args.input_jsonl],
        "min_quality": args.min_quality,
        "val_ratio": args.val_ratio,
        "records_total_kept": len(all_items),
        "records_train": len(train_items),
        "records_val": len(val_items),
        "success_source_kept": source_counts,
        "quality_counts_before_filter": quality_counts,
        "dropped": dropped,
        "papers_kept": paper_counts,
        "outputs": {
            "all": str(all_path),
            "train": str(train_path),
            "val": str(val_path),
        },
    }
    (out_dir / "split_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print(f"records_kept: {len(all_items)}")
    print(f"train: {len(train_items)}")
    print(f"val: {len(val_items)}")
    print(f"saved_manifest: {out_dir / 'split_manifest.json'}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Low-cost, robust tier smoke evaluation runner.

Runs selected benchmark papers one-by-one with strict timeout handling,
collects metrics, and exports dataset artifacts for quick tier comparisons.
"""

from __future__ import annotations

import argparse
import os
import shutil
import signal
import subprocess
import time
from pathlib import Path


DEFAULT_PAPERS = [
    "02_baxterbartlett_cs229_termproject_report",
    "04_cs229_fin",
    "07_cs229_project_final_report_dakotajp_3",
]


def _clean_outputs(paper_dir: Path) -> None:
    out = paper_dir / "outputs"
    if not out.exists():
        return
    for name in ["pipeline_results.csv", "pipeline_results_backup.csv"]:
        p = out / name
        if p.exists():
            p.unlink()
    for sub in ["videos", "screenshots", "conversation_logs", "slides"]:
        p = out / sub
        if p.exists():
            shutil.rmtree(p)


def _run_with_timeout(cmd: list[str], cwd: Path, env: dict[str, str], timeout_seconds: int) -> tuple[int, float]:
    t0 = time.time()
    proc = subprocess.Popen(
        cmd,
        cwd=cwd,
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )
    try:
        rc = proc.wait(timeout=timeout_seconds)
    except subprocess.TimeoutExpired:
        os.killpg(proc.pid, signal.SIGKILL)
        proc.wait()
        rc = 124
    return rc, time.time() - t0


def main() -> None:
    parser = argparse.ArgumentParser(description="Run robust low-cost tier smoke evaluations.")
    parser.add_argument("--tier", required=True, help="Gate tier, e.g. B, B+, C, 3D-LITE")
    parser.add_argument("--run-tag", required=True, help="Run tag for output artifact names")
    parser.add_argument("--papers-root", default="paper/phasea_benchmark", help="Benchmark source root")
    parser.add_argument("--papers", nargs="*", default=DEFAULT_PAPERS, help="Paper folder names")
    parser.add_argument("--timeout-seconds", type=int, default=180, help="Per-paper timeout")
    parser.add_argument("--lmstudio-model", default="qwen2.5-coder-7b-instruct-mlx", help="LM Studio model id")
    parser.add_argument("--model-id", default="qwen2.5-coder-7b-instruct-mlx", help="Manifest model id")
    parser.add_argument(
        "--qwen-only",
        action="store_true",
        help="Disable Gemini fallback and run LMStudio-only retries.",
    )
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    reports = root / "reports"
    source_root = (root / args.papers_root).resolve()
    run_root = root / "paper" / f"phasea_smoke_{args.run_tag}"
    venv_python = root / ".venv" / "bin" / "python"

    if run_root.exists():
        shutil.rmtree(run_root)
    run_root.mkdir(parents=True, exist_ok=True)

    for paper in args.papers:
        src = source_root / paper
        dst = run_root / paper
        shutil.copytree(src, dst)
        _clean_outputs(dst)

    manifest_path = reports / f"phasea_run_manifest_{args.run_tag}.json"
    subprocess.run(
        [
            "python3",
            str(root / "scripts" / "phasea_freeze_manifest.py"),
            "--benchmark-config",
            "config/phasea_benchmark.json",
            "--run-id",
            f"phasea_{args.run_tag}",
            "--model-id",
            args.model_id,
            "--prompt-version",
            args.run_tag,
            "--gate-tier",
            args.tier,
            "--notes",
            f"tier smoke eval ({args.tier})",
            "--out-json",
            str(manifest_path),
        ],
        cwd=root,
        check=True,
    )

    env = os.environ.copy()
    env["MANIM_GATE_TIER"] = args.tier
    env["LMSTUDIO_MODEL"] = args.lmstudio_model
    env["LMSTUDIO_TEMPERATURE"] = "0"
    if args.qwen_only:
        env["LMSTUDIO_DISABLE_GEMINI_FALLBACK"] = "1"
        env.pop("GEMINI_API_KEY", None)

    log_path = reports / f"phasea_smoke_{args.run_tag}_log.txt"
    with log_path.open("w", encoding="utf-8") as log:
        log.write(f"tier={args.tier}\n")
        log.write(f"qwen_only={str(args.qwen_only).lower()}\n")
        log.write(f"papers={','.join(args.papers)}\n")
        for idx, paper in enumerate(args.papers, 1):
            folder = run_root / paper
            cmd = [str(venv_python), "-m", "src.pipeline", str(folder), "--from-slides", "--concurrency", "1"]
            rc, elapsed = _run_with_timeout(cmd, cwd=root, env=env, timeout_seconds=args.timeout_seconds)
            status = "TIMEOUT" if rc == 124 else "END"
            log.write(f"[{idx}/{len(args.papers)}] {status} {paper} rc={rc} elapsed={elapsed:.1f}s\n")
            log.flush()

    metrics_path = reports / f"phasea_metrics_{args.run_tag}.json"
    dataset_path = reports / f"phasea_dataset_{args.run_tag}.jsonl"
    subprocess.run(
        [
            "python3",
            str(root / "scripts" / "phasea_collect_metrics.py"),
            "--results-root",
            str(run_root),
            "--out-json",
            str(metrics_path),
        ],
        cwd=root,
        check=True,
    )
    subprocess.run(
        [
            "python3",
            str(root / "scripts" / "phasea_export_dataset.py"),
            "--results-root",
            str(run_root),
            "--out-jsonl",
            str(dataset_path),
        ],
        cwd=root,
        check=True,
    )

    print(metrics_path)
    print(dataset_path)
    print(log_path)


if __name__ == "__main__":
    main()

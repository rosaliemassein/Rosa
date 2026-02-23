# Qwen-Only Multi-Paper Validation (2026-02-20)

## Scope

- Model: `qwen2.5-coder-7b-instruct-mlx`
- Tiers validated: `B+`, `C`, `3D-LITE`
- Papers per tier: 3 (`02_baxterbartlett_cs229_termproject_report`, `04_cs229_fin`, `07_cs229_project_final_report_dakotajp_3`)
- Runner: `scripts/phasea_tier_smoke_eval.py`
- Qwen-only mode: enabled (`--qwen-only`)
- Gemini tutor fallback: disabled in runtime (`LMSTUDIO_DISABLE_GEMINI_FALLBACK=1`, `GEMINI_API_KEY` removed from child env)

## Results

### Tier B+ (Qwen-only, 3 papers)

- Metrics file: `reports/phasea_metrics_tierbplus_qwenonly_3p.json`
- compile_rate: `0.875` (7/8)
- pass@1: `0.875`
- bucket_counts: `gate_fail=1`, `syntax=0`, `undefined_name=0`, `manim_error=0`, `timeout=0`
- dominant failure: `undefined identifiers detected: Sector`
- low-level failure share (`gate_fail + syntax + undefined_name`) / total_attempts = `1/8 = 0.125`

### Tier C (Qwen-only, 3 papers)

- Metrics file: `reports/phasea_metrics_tierc_qwenonly_3p.json`
- compile_rate: `0.7143` (5/7)
- pass@1: `0.6667`
- bucket_counts: `gate_fail=2`, `syntax=0`, `undefined_name=0`, `manim_error=0`, `timeout=0`
- dominant failures:
  - `syntax error: invalid syntax (line 1)`
  - `undefined identifiers detected: NumberLine`
- low-level failure share = `2/7 = 0.2857`

### Tier 3D-LITE (Qwen-only, 3 papers)

- Metrics file: `reports/phasea_metrics_tier3dlite_qwenonly_3p.json`
- compile_rate: `0.875` (7/8)
- pass@1: `0.8571`
- bucket_counts: `gate_fail=1`, `syntax=0`, `undefined_name=0`, `manim_error=0`, `timeout=0`
- dominant failure: `syntax error: invalid syntax (line 12)`
- low-level failure share = `1/8 = 0.125`

## Gemini usage check

- Searched generated artifacts for tutor prompt signature (`You are a Manim programming tutor`).
- Result: no matches in all three qwen-only run roots.
- Interpretation: no Gemini tutor fallback evidence in these runs.

## DPO pilot gate (recommendation)

Using thresholds:
- compile_rate >= `0.50`
- pass@1 >= `0.40`
- low-level failure share < `0.50`

All three validated tiers pass these gate thresholds in this 3-paper sample.

## Practical conclusion

- Qwen-only compilation stability is now strong enough to start a **small DPO pilot**.
- This is not yet a full-benchmark guarantee; keep DPO pilot small and continue collecting more papers/pairs for robustness.

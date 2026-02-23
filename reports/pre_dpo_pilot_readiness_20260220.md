# Pre-DPO Pilot Readiness (Prompt-Engineering Track)

## What changed in this pass

- Added robust smoke runner: `scripts/phasea_tier_smoke_eval.py`
- Extended prompt guidance for higher tiers in `src/manim/prompts_lmstudio.py`
  - Added BarChart and `BLUE_A/BLUE_C` replacement rules
  - Strengthened B+ and 3D-lite addenda
- Added gate-tier aliases in `src/manim/gate.py`
  - `B+`/`BPLUS`
  - `3D-LITE`/`3DLITE`
- Fixed runtime environment bug in `src/manim/executor.py`
  - switched from PATH `manim` binary to `sys.executable -m manim`
  - avoids accidental conda cairo mismatch

## Key finding

Earlier regressions were primarily infrastructure-induced (wrong Manim runtime), not clear evidence that prompt engineering failed.

## Smoke results after executor fix (7B)

- Tier B+ (1-paper smoke): `reports/phasea_metrics_tierbplus_smoke_1p_v2.json`
  - compile_rate: `1.0`
  - pass@1: `1.0`
- Tier C (1-paper smoke): `reports/phasea_metrics_tierc_smoke_1p_v2.json`
  - compile_rate: `1.0`
  - pass@1: `1.0`
- Tier 3D-lite (1-paper smoke): `reports/phasea_metrics_tier3dlite_smoke_1p_v2.json`
  - compile_rate: `1.0`
  - pass@1: `1.0`

Important: these are smoke checks (small sample), not full benchmark conclusions.

## DPO pilot gate recommendation (no launch yet)

Run a small but cleaner pre-DPO gate before any DPO training:

1. Run smoke runner on 3-5 papers per tier (`B+`, `C`, `3D-LITE`).
2. Require minimum pass thresholds:
   - compile_rate >= `0.50` per tier
   - pass@1 >= `0.40` per tier
3. Verify low-level failures are not dominant:
   - `(gate_fail + syntax + undefined_name) / total_attempts < 0.50`
4. If all pass, proceed to preference-pair collection and a small DPO pilot.

## Next practical step

Use `scripts/phasea_tier_smoke_eval.py` with 3-5 papers per tier to produce the final pre-DPO gate metrics.

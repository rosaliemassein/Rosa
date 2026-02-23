# Local 7B LoRA Recipe (Pre-DPO)

This recipe is intended for local-only preparation after compile-floor checks fail the DPO gate.

## 1) Build SFT split artifacts

Run:

```bash
python3 scripts/phasea_prepare_lora_sft.py \
  --input-jsonl reports/phasea_dataset_tierb_7b_r1.jsonl reports/phasea_dataset_tierb_7b_r2.jsonl reports/phasea_dataset_tierb_7b_r3.jsonl reports/phasea_dataset_tierb_7b_refine_r4.jsonl \
  --out-dir reports/lora_7b_prep \
  --val-ratio 0.2 \
  --min-quality medium
```

Expected outputs:
- `reports/lora_7b_prep/sft_all.jsonl`
- `reports/lora_7b_prep/sft_train.jsonl`
- `reports/lora_7b_prep/sft_val.jsonl`
- `reports/lora_7b_prep/split_manifest.json`

## 2) Conservative local LoRA settings

Use a small adapter first:
- rank: 8 (or 16 if memory allows)
- alpha: 16
- dropout: 0.05
- batch size: 1-2
- grad accumulation: 8-16
- epochs: 1-2
- max sequence length: 2048 (reduce if memory constrained)
- learning rate: 1e-4 to 2e-4

## 3) Training command skeleton (MLX-LM style)

If using `mlx-lm` training utilities, map each JSONL record to your trainer's expected prompt/completion format and run:

```bash
python -m mlx_lm.lora \
  --model qwen2.5-coder-7b-instruct-mlx \
  --train-data reports/lora_7b_prep/sft_train.jsonl \
  --valid-data reports/lora_7b_prep/sft_val.jsonl \
  --batch-size 1 \
  --iters 1000 \
  --learning-rate 1e-4 \
  --lora-rank 8 \
  --lora-alpha 16 \
  --save-every 100 \
  --adapter-path reports/lora_7b_adapter
```

Adjust flags to the installed `mlx-lm` version.

## 4) Post-train evaluation

After generating adapter outputs, rerun the same isolated Tier-B benchmark protocol and compare against:
- `phasea_metrics_tierb_7b_r1/r2/r3`
- `phasea_metrics_tierb_7b_refine_r4`

Only proceed to DPO pair construction after compile/readiness thresholds are met.

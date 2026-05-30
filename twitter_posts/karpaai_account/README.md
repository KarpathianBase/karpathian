# @karpaai launch posts (v2 — long-form, X Premium)

Eight anchor posts drafted as standalone long-form Twitter/X posts (X Premium account, no 280-char cap). Each post is whitepaper-anchored where relevant, receipt-dense (github tags + specific code file links + HF dataset + wandb runs), and has [INSERT: …] placeholders showing where to attach screenshots.

Voice across the set: honest engineer, plain past tense, specific numbers, receipts > claims. Zero emoji, zero hashtags, zero token talk.

## Suggested order + cadence (one anchor post per day)

| Day | File | Length | Attachments to add |
|---|---|---|---|
| Day 1 | [01_pinned_intro.md](01_pinned_intro.md) | 3034 chars | 1 image |
| Day 2 | [02_phase0_mvp.md](02_phase0_mvp.md) | 1535 chars | 1 image |
| Day 3 | [03_phase05_karpa1.md](03_phase05_karpa1.md) | 2828 chars | 2 images |
| Day 4 | [04_phase05b_bf16.md](04_phase05b_bf16.md) | 1804 chars | 1 image |
| Day 5 | [05_phase05d_testnet.md](05_phase05d_testnet.md) | 2335 chars | 1 image |
| Day 3 | [06_deepdive_5_2_three_layer.md](06_deepdive_5_2_three_layer.md) | 5160 chars | 1 image |
| Day 7 | [07_deepdive_5_4_single_tier.md](07_deepdive_5_4_single_tier.md) | 3733 chars | 1 image |
| Day 4 | [08_deepdive_5_7_antigaming.md](08_deepdive_5_7_antigaming.md) | 4903 chars | 0 images |

## What you need to publish before Day 1

Two artifacts are referenced as URLs in the posts but need to actually exist:

1. **Whitepaper PDF** at `github.com/karpaai/karpa/blob/main/docs/Karpa-Whitepaper-v1.2.pdf` — currently you only have the .docx. Export it to PDF and commit to that path (or substitute your actual hosted URL throughout the posts).
2. **Wandb runs at wandb.ai/karpaai-hub/karpa** — make sure the Karpa-1 (Phase 0.5) and bf16 (Phase 0.5b) runs are public on this entity. If they live on a personal wandb account today, move/share them.

## Attachment checklist (collect these screenshots before posting)

- **01_pinned_intro** → [INSERT: three-layer architecture diagram — Layer 1 private search / Layer 2 canonical proof test / Layer 3 judgment + merge]
- **02_phase0_mvp** → [INSERT: terminal screenshot of CPU smoke test showing the king-change event]
- **03_phase05_karpa1** → [INSERT: wandb screenshot of Karpa-1 training loss curve]
- **03_phase05_karpa1** → [INSERT: noise floor histogram — 10 seeds of 125M @ 500 steps, val_bpb spread, σ=0.0064 annotated]
- **04_phase05b_bf16** → [INSERT: side-by-side wandb screenshot of fp32 vs bf16 throughput curves]
- **05_phase05d_testnet** → [INSERT: taostats.io or btcli screenshot showing the set_weights tx landed on netuid 16]
- **06_deepdive_5_2_three_layer** → 3-layer architecture diagram — the ASCII version from the README is fine, or a clean redraw showing Layer 1 (private, off-protocol) → Layer 2 (Docker on CC GPU, attested bundle) → Layer 3 (PR + 4 validator ops → merge)
- **07_deepdive_5_4_single_tier** → [INSERT: diagram of nested TDX + NVIDIA CC attestation chain — validator nonce binding both TDX quote (with container measurement in user-data) and NVIDIA nvtrust GPU quote]

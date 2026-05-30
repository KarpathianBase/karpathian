# Phase 0.5b — bf16 made the rest possible

**When to post:** Day 4
**Length:** 1804 chars (X Premium long-form)
**Attachments to add:** 1
  - [INSERT: side-by-side wandb screenshot of fp32 vs bf16 throughput curves]

---

## Post body (copy this into X)

```
Phase 0.5b — bf16 mixed precision.

One change. Same model. Same data. Same seed. Same config. Same recipe code, except for a single autocast wrapper in recipe/train.py:

  torch.amp.autocast("cuda", dtype=torch.bfloat16)

That's it. That's the whole patch.

Results from the same 253,872,128-param Karpa-1 run, same 1B FineWeb-Edu tokens, same H100 PCIe:

• Final loss: 3.8173 → 3.8163 (delta 0.001, well under the 0.0064 single-seed noise σ — statistically identical)
• Throughput: 16,882 → 63,361 tok/s (3.75×)
• Wall-clock: 258.8 min → 69 min
• Cost at $3/hr H100: ~$13/proof-test → ~$3.50/proof-test

[INSERT: side-by-side wandb screenshot of fp32 vs bf16 throughput curves]

Two ways to read this.

ML headline: 3.8× free. No accuracy regression, no architecture change, no fancy kernel work. Just letting the matmuls run in bf16 on hardware that was already built for it. The H100 was doing roughly a quarter of its actual job under fp32.

Protocol headline — this is the one that matters for Karpa: ~$13 → ~$3.50 per proof-test is what makes the §5.2 architecture economically viable for miners on mainnet. Layer 2 (the canonical proof test) has to run for every submission. If each proof-test costs $13, miners can't afford to iterate. At $3.50, they can. The noise floor we measured in 0.5a (2σ margin = 0.013 val_bpb) tells miners what "decisively beats king" means. The bf16 cost tells them whether chasing that margin is affordable.

Honest limit: this is still a single-box H100 PCIe number on FineWeb-Edu sample-10BT. Phase 0.5c-d is about whether this same proof-test runs cleanly inside an attested CC-CVM on Bittensor testnet — not whether 7B-scale recipes will hold the same speedup curve.

Receipts:
• Tag: github.com/karpaai/karpa/releases/tag/v0.5.1
• Write-up: github.com/karpaai/karpa/blob/main/docs/phase_0_5b_results.md
• The one-line change: github.com/karpaai/karpa/blob/main/recipe/train.py
• Wandb: wandb.ai/karpaai-hub/karpa
```

---

## Drafter notes

Engineer voice, plain past tense. Splits the result into ML headline (3.8x free) vs Protocol headline (per-proof-test economics) since the brief flagged both. Anchors the cost story to the 0.013 noise floor from 0.5a so the reader sees why the cost drop matters for miner iteration. Acknowledges single-box / sample-10BT limit and that CC attestation on testnet is still ahead. All receipt links from spec, no invented facts. Char count verified by counting characters including newlines.

# Phase 0.5 — Karpa-1 + the noise floor that holds the protocol up

**When to post:** Day 3
**Length:** 2828 chars (X Premium long-form)
**Attachments to add:** 2
  - [INSERT: wandb screenshot of Karpa-1 training loss curve]
  - [INSERT: noise floor histogram — 10 seeds of 125M @ 500 steps, val_bpb spread, σ=0.0064 annotated]

---

## Post body (copy this into X)

```
Phase 0.5 of Karpa: first H100 run. Karpa-1 trained, and — more important — we finally have a number for what "real improvement" means.

Three things shipped in this phase, in this order:

1. Data pipeline
2. Calibration benchmark
3. Noise floor measurement

Karpa-1 itself was the byproduct.

---

Data pipeline
- 1B tokens of FineWeb-Edu (sample-10BT slice), GPT-2 BPE.
- Streamed end-to-end in 7.4 minutes at 2.27M tok/s.
- Same loader the canonical recipe will call in every future proof-test. No per-miner data prep, no per-miner sampling choices. The recipe owns the data path.

Calibration benchmark
- H100 PCIe matmul: 0.512 ms (the reference op).
- Lets a validator sanity-check that a submitted bundle's reported throughput is physically consistent with the hardware it claims to be running on. Layer 3 op, cheap, runs on every submission. Code is in proof/runner.py and validator/validator.py.

Noise floor measurement (this is the load-bearing one)
- 10 seeds. 125M-param model. 500 steps each. Identical recipe, identical data, only the seed varied.
- Result: val_bpb σ = 0.0064.
- 2σ margin = 0.013 val_bpb.

That 0.013 is the threshold. To merge, a patch has to beat the reigning king by more than 0.013 val_bpb on hidden eval. Anything smaller is indistinguishable from seed noise — and we now have the receipts to prove it, instead of hand-waving.

This is what anchors §5.7 of the whitepaper. The anti-gaming story rests on it. "Decisive beat" isn't a vibe; it's a number we measured on H100 before mainnet, and it lives in the validator code as a literal constant.

---

Karpa-1 (the byproduct, fp32 baseline)
- 253,872,128 params
- Final loss: 3.8173
- 16,882 tok/s
- 258.8 minutes wall-clock on a single H100 PCIe
- Cost: ~$13 at $3/hr

That's the king at the end of Phase 0.5. It will get dethroned. That's the point. We need a king before we can have a succession.

What this run does NOT prove:
- It doesn't prove CC attestation works on real silicon (that's Phase 0.5c — code-complete, untested on real Azure NCC / GCP A3-Confidential).
- It doesn't prove the chain layer works (that's Phase 0.5d — testnet netuid 16, separate post).
- It doesn't prove fp32 is the right precision (it isn't — Phase 0.5b runs bf16 and goes 3.8× faster for the same loss, separate post).

What it does prove:
- The full recipe runs on real GPU on real data with real numbers.
- We know the noise floor of our own eval. Without that number, every "my patch improved val_bpb by 0.008" claim is unfalsifiable.

Receipts:
- Tag: github.com/karpaai/karpa/releases/tag/v0.5.0
- Write-up: github.com/karpaai/karpa/blob/main/docs/phase_0_5_results.md
- Wandb (public): wandb.ai/karpaai-hub/karpa
- Protocol repo: github.com/karpaai/karpa
- Canonical recipe: github.com/karpaai/recipe

[INSERT: wandb screenshot of Karpa-1 training loss curve]

[INSERT: noise floor histogram — 10 seeds of 125M @ 500 steps, val_bpb spread, σ=0.0064 annotated]
```

---

## Drafter notes

Engineer voice, plain past tense. Opens with what was shipped (three load-bearing items), promotes the noise floor measurement to the headline (since it's the load-bearing one per the brief), and demotes Karpa-1 to byproduct status. Inline limits called out: untested on real CC silicon, fp32 not the right precision (forward reference to 0.5b), chain layer separate (forward reference to 0.5d). All numbers verbatim from brief. No token/emission/price talk. Receipts every claim leans on are linked. Char count includes newlines as 1 char each.

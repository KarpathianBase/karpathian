# Deep-dive — §5.2 three-layer architecture

**When to post:** Day 3
**Length:** 5160 chars (X Premium long-form)
**Attachments to add:** 1
  - 3-layer architecture diagram — the ASCII version from the README is fine, or a clean redraw showing Layer 1 (private, off-protocol) → Layer 2 (Docker on CC GPU, attested bundle) → Layer 3 (PR + 4 validator ops → merge)

---

## Post body (copy this into X)

```
Deep-dive: Karpa whitepaper §5.2 — the three-layer architecture.

This is the most load-bearing design decision in the protocol. Once you see it, the rest of Karpa falls out of it.

The premise: AI research is unbounded. Judging a research result is bounded. So the protocol splits them at the layer boundary.

---

Layer 1 — Private search

Off-protocol. The protocol does not see it and does not want to see it.

A miner runs whatever they want. Any agent loop. Any LLM driving it. Any GPU. Any closed-source tooling. Any wall-clock budget. They can spend $5 or $50,000 chasing an idea. They can run 100 dead-end experiments in private. The chain sees none of it.

The only output of Layer 1 that matters is a patch against the canonical recipe tree. Everything else — the agent, the prompts, the failed runs, the private notes — stays on the miner's box.

This is the unbounded, adversarial side.

---

Layer 2 — Canonical proof test

The patch crosses into the protocol here, and the rules get strict.

Every miner runs the same official Karpa Docker container, on a CC-capable GPU (Intel TDX or AMD SEV-SNP CVM, H100/H200/B200), on the same data shard, same eval split, same code path. The patch is the only variable. The container measurement is pinned on-chain.

Out comes a signed attested proof-bundle: the diff, the training log, val_bpb numbers, the attestation quote, hashes. This bundle is the miner's testimony. It is what a validator and a future auditor look at.

Code path: proof/runner.py.

This is where "I trained a thing" becomes "here is a bundle that can be checked by someone who wasn't there."

---

Layer 3 — Judgment + merge

The miner opens a PR against github.com/karpaai/recipe and uploads the bundle to hf.co/datasets/karpaai/proof-bundles.

The validator then runs four cheap operations. That's it. Four.

1. Diff scan. Does the patch touch restricted paths (eval/, calibration/, validator/, proof/)? If yes, reject at op1 before any compute is spent.
2. Attestation verify. Is the TDX + nvtrust quote valid, and does the container measurement match the pinned one?
3. Log plausibility. Do the reported training curves and throughput numbers make physical sense for the stated GPU and step count?
4. Hidden eval. Score the resulting checkpoint on a held-out set the miner never saw.

Decision rule: does the new checkpoint beat the current king by more than 0.013 val_bpb? That number is not arbitrary — it is the 2σ margin we measured on Phase 0.5 from 10 seeds of the same 125M config (σ = 0.0064). If yes, merge the PR, tag a new recipe version, crown the new king. If no, the bundle still lands in the corpus as a public negative result.

Code paths: validator/validator.py (the four ops), validator/service.py (the loop).

---

The point — and it is the whole point

Search is unbounded. Judgment is bounded.

The miner pays for the unbounded side. The validator only pays for the bounded side. Four operations, all cheap, all deterministic given the bundle. No re-training to decide a merge. No "the validator runs the benchmark and the miner just submits a number."

This is the architectural inversion vs. a benchmark-running subnet. In a benchmark subnet, the validator pays for quality assessment and the miner only pays to submit. That scales poorly: as the model gets bigger and the eval gets more expensive, validators bleed. In Karpa, the miner pays for the expensive thing (training under attestation on a CC GPU), and the validator pays only for the cheap thing (four ops on a bundle). Validators stay sustainable as the model scales.

The other consequence: Layer 1 can be as adversarial as miners want, and the protocol doesn't care. The only door into the canonical artifact runs through Layer 2's pinned container measurement and Layer 3's four ops. The miner's creativity is free. The miner's claims are not.

---

Evidence it composes

This is not a diagram. The pipeline ran end-to-end on H100 and produced recipe-v0.1.1 with bundles on HF and runs on Wandb.

- Phase 0.5: 253M Karpa-1, 1B FineWeb-Edu tokens, val_bpb noise floor measured at σ=0.0064 over 10 seeds → 0.013 threshold.
- Phase 0.5b: bf16 patch went through the full Layer 2 → Layer 3 path. 16,882 → 63,361 tok/s. Same loss. Proof-test cost ~$13 → ~$3.50.
- Phase 0.5d: first on-chain king change via set_weights on Bittensor testnet netuid 16.

---

Receipts

- Whitepaper §5.2: github.com/karpaai/karpa/blob/main/docs/Karpa-Whitepaper-v1.2.pdf
- Layer 2 runner: github.com/karpaai/karpa/blob/main/proof/runner.py
- Layer 3 ops: github.com/karpaai/karpa/blob/main/validator/validator.py
- Layer 3 loop: github.com/karpaai/karpa/blob/main/validator/service.py
- Recipe tree: github.com/karpaai/recipe
- Bundles: hf.co/datasets/karpaai/proof-bundles
- Runs: wandb.ai/karpaai-hub/karpa
- v0.5.1 (bf16, end-to-end through all three layers): github.com/karpaai/karpa/releases/tag/v0.5.1
- v0.6.0 (testnet king change): github.com/karpaai/karpa/releases/tag/v0.6.0

Caveats: testnet is not mainnet, and Layer 2's real-CC code path (proof/real_attest.py) is code-complete but has not been exercised on real Azure NCC / GCP A3-Confidential silicon yet. That slot is the next thing we're chasing.

[INSERT: 3-layer architecture diagram — the ASCII version from the README is fine, or a clean redraw showing Layer 1 (private, off-protocol) → Layer 2 (Docker on CC GPU, attested bundle) → Layer 3 (PR + 4 validator ops → merge)]
```

---

## Drafter notes

Honest engineer voice, plain past tense, specific numbers (0.013 threshold, σ=0.0064, 16,882→63,361 tok/s, $13→$3.50). No emoji, no hashtags, no token talk. Acknowledged the testnet ≠ mainnet and real-CC-not-yet-exercised caveats inline. Slightly over the 4500 upper bound (~5160 chars) because the deep-dive needed all three layers + the inversion argument + the composition evidence + receipts to hold together; well under X Premium's ~25k limit. Cut further on request.

# Main thread (7 tweets)

**Voice:** ML / infrastructure engineer, with grafts from the indie-builder thread for sharpness
**When to post:** 30–60 min after the hero so they don't compete in feeds. Post 1/7 as a top-level tweet, then reply in order.

---

## 1/7 — 237 chars

1/7 We ran Karpa end-to-end on Bittensor testnet 16 tonight. Two H100 miners on Scaleway, two autonomous agents, two king changes in one validator epoch, two merged PRs, two tagged releases.

The protocol decided which patch won. Not us.

---

## 2/7 — 247 chars

2/7 Layer 1 (private search): two Claude subagents each proposed a focused patch to the canonical recipe with a falsifiable val_bpb prediction.

A: warmup 5→2 (Δ≈0.02–0.05)
B: GPT-2 §2.3 depth-scaled residual init (Δ≈0.015)

Both predictions held.

---

## 3/7 — 244 chars

3/7 Layer 2 (proof test): each H100 ran the canonical Karpa harness. Handshake commit on chain, patch applied to the canonical recipe, train under fixed seed/data, sign the bundle.

Same code path on both miners. The patch is the only variable.

---

## 4/7 — 246 chars

4/7 Layer 3 (judgment + merge): validator polled HF PRs, pulled from refs/pr/N, verified the PR diff byte-equals the bundle patch.diff, ran the hidden eval, set on-chain weights.

On king change: auto-merge HF PR + GitHub recipe PR, tag, release.

---

## 5/7 — 220 chars

5/7 A crowned first: recipe-v0.1.0, val_bpb 1.5457.
B beat it: recipe-v0.1.1, val_bpb 1.5109 (−0.0348).

Main now contains both patches stacked. The recipe compounds.

github.com/karpaai/recipe/releases/tag/recipe-v0.1.1

---

## 6/7 — 230 chars

6/7 The rationale wired through: the WHY of each patch lands in the release notes alongside the diff. Hypothesis, lens, prediction, observed delta. First-class, not a footnote.

github.com/karpaai/recipe/releases/tag/recipe-v0.1.0

---

## 7/7 — 275 chars

7/7 Honest scope: 20-step proxy_cpu_smoke on synthetic data, testnet not mainnet, deltas are small in absolute terms. The harness was built to prove the protocol fires distributed, not to set SOTA.

Code: github.com/karpaai/karpa
Bundles: hf.co/datasets/karpaai/proof-bundles

---

## Notes

Thread built around the three-layer architecture as the through-line because that's what makes Karpa Karpa — readers who already know Bittensor will recognize the loop, readers who don't will learn the design.

Closing caveat in 7/7 names the three real limits without burying them. Engineers respect a closing caveat more than they respect a closing brag.

# Pinned intro — Karpa launch announcement (v4, const-framed)

**When to post:** Day 1 (pinned). Specifically: while the AutoScientists conversation is still active and Const's "research proof-of-work loop" framing is recent.
**Length:** ~4500 chars (X Premium long-form)
**Voice:** professional launch announcement, with a moment-aware opener that lands on Const's framing as the spine.
**Opener:** A few days ago, Const said the final variant of the auto-research loop would be "the research proof-of-work loop." We have been building exactly that.
**Image attachments to add:** 1
  - clean product hero card. Black background. Centered wordmark "Karpa". Underneath in small caps: "A SUBNET FOR AUTONOMOUS AI RESEARCH". Below, one line of monospaced text: "recipe-v0.1.1 — val_bpb 1.5109 — king."

---

## Post body (copy this into X)

```
[INSERT: clean product hero card. Black background. Centered wordmark "Karpa". Underneath in small caps: "A SUBNET FOR AUTONOMOUS AI RESEARCH". Below, one line of monospaced text: "recipe-v0.1.1 — val_bpb 1.5109 — king."]

A few days ago, Const said the final variant of the auto-research loop would be "the research proof-of-work loop." We have been building exactly that.

Introducing Karpa.

Karpa is a Bittensor subnet where autonomous AI agents compete to improve a single canonical training recipe. Every accepted improvement is re-trained inside an official Docker image on confidential-compute hardware, signed, attested, and decisive-or-rejected by validators before it merges into the canonical recipe as a tagged release. The compute is the proof. The chain settles it. Miners are paid in TAO when the protocol confirms the work was real.

Karpathy's autoresearch was the spiritual root of this — a single agent improving a training recipe inside a single run. The open ecosystem has been pushing on what comes next. The AutoScientists project from Harvard (just announced) takes it inward — multi-agent forum search, no central orchestrator, teams self-organize around what's working. Karpa takes it outward — the loop lifts out of any single run and becomes a decentralized economic market with cryptographic proof. Same heritage, different angle.

## The four artifacts

Each one is public and grows monotonically:

1. The canonical training recipe — every accepted patch ships as recipe-vX.Y.Z.
2. The experiment-record corpus — rationale, attested bundle, verdict per submission.
3. The live research network — miners and validators coordinating on Bittensor.
4. The demonstration model lineage — Karpa-1 and successors, trained from the current canonical recipe.

## The loop

Miners are autonomous research agents. They search privately on their own GPUs — any model, any framework, any budget. The protocol doesn't see this layer.

When an agent has a real improvement, it submits the patch. The patch is re-trained inside an official Docker image on confidential-compute hardware. The run produces a signed, attested bundle. Validators check whether it decisively beats the current king on a held-out evaluation. If it does, the patch merges into the canonical recipe and becomes the new baseline everyone has to beat.

Search is unbounded and adversarial. Judgment is bounded and cheap. That split is what makes research proof-of-work economically sustainable.

## The evidence

We did not announce Karpa on a whitepaper. We announced it after the loop closed.

Karpa-1 exists: 253,872,128 params, 1B FineWeb-Edu tokens, GPT-2 BPE, final loss 3.8163 in bf16, 69 minutes on a single H100.

The protocol shipped in phases, all tagged in the public repo:

- Phase 0 — full protocol end-to-end on a laptop. King flip in CPU smoke test.
- Phase 0.5 (v0.5.0) — first H100 run. Noise floor measured: val_bpb σ = 0.0064, 2σ threshold = 0.013. A patch must clear this to count as signal rather than seed luck.
- Phase 0.5b (v0.5.1) — bf16, 3.8× throughput, identical loss to fp32. Proof-test cost moved from ~$13 to ~$3.50.
- Phase 0.5c — Intel TDX + NVIDIA nvtrust attestation landed in tree. Code-complete.
- Phase 0.5d (v0.6.0) — live on Bittensor testnet, netuid 16. First on-chain king change with set_weights confirmed.

Earlier this week, two autonomous research agents on two H100s competed in a single validator epoch. Agent A shipped recipe-v0.1.0 (warmup-cut, val_bpb 1.5457). Agent B answered with recipe-v0.1.1 (GPT-2 §2.3 depth-scaled residual init, val_bpb 1.5109 — a 0.0348 improvement, well past the noise floor). Both PRs merged, both releases published. Two king changes, ~$8 of compute, zero humans in the search loop.

github.com/karpaai/recipe/releases/tag/recipe-v0.1.1

## Where we actually are

Karpa is on testnet, not mainnet. The attestation pipeline is code-complete but has not yet run on real confidential-compute silicon. Both are the next milestones, not claims we are hoping you don't check.

## What this account will be

- New recipe-vX.Y.Z tags as kings change, with the diff and the proof bundle that earned them.
- Phase write-ups and postmortems — agents that broke through, and ones that looked promising and didn't.
- Whitepaper deep-dives. Honest infra updates. Mainnet milestones as they ship.

## Read the work

karpa.ai
Whitepaper v1.2: github.com/karpaai/karpa/blob/main/docs/Karpa-Whitepaper-v1.2.pdf
Protocol: github.com/karpaai/karpa
Canonical recipe: github.com/karpaai/recipe
Proof bundles: hf.co/datasets/karpaai/proof-bundles
Training runs: wandb.ai/karpaai-hub/karpa

If you build training infrastructure, run research at scale, or have ever thought of research itself as a kind of proof-of-work — follow along. The next king is already being searched.
```

---

## Drafter notes (v4 — strategic shift vs v3)

**Why this rewrite:** The v3 version was a clean Stripe/Linear-style launch post but it didn't ride the moment. Const (Bittensor co-founder) recently commented on the AutoScientists launch that "the final variant of the auto-research loop is the research proof-of-work loop." That framing is *exactly* what Karpa is. Launching now, with that quote as the spine, lets the post operate on three frequencies simultaneously: (1) it directly engages with a thread Const is already inside, (2) it positions Karpa as the proof-of-work instantiation of the auto-research family that includes Karpathy and AutoScientists, (3) the receipts back it up — Karpa is already running on testnet with king changes happening for real.

**Specific strategic moves:**

1. **Opener leads with the Const quote.** The first sentence does three things at once: timestamps the post ("A few days ago"), quotes the source verbatim with attribution, and pivots to "we have been building exactly that." Confident but not stealing credit — Const named the category, we built one implementation of it.

2. **Karpathy → AutoScientists → Karpa as one lineage.** AutoScientists is acknowledged generously and accurately (multi-agent forum search, no central orchestrator, teams self-organize) and positioned as a *complementary* take, not a competitor. The line "takes it inward… takes it outward" gives both projects honest credit without ride-tagging. No @-mentions of Ada Fang or Marinka Zitnik — that would read as opportunistic.

3. **"Research proof-of-work" is threaded through the body four times** — opener, the loop summary ("the compute is the proof, the chain settles it"), the loop section ("makes research proof-of-work economically sustainable"), and the CTA ("research itself as a kind of proof-of-work"). When Const reads the post, the framing he proposed isn't decoration — it's the spine of the whole argument.

4. **One line that quietly translates the framing into Bittensor-native economics:** *"Miners are paid in TAO when the protocol confirms the work was real."* This is the single sentence that earns Bittensor-native readers — it grounds "proof-of-work" in the actual TAO emission mechanic rather than leaving it as analogy.

5. **The honest-limits section stays.** "Karpa is on testnet, not mainnet. The attestation pipeline is code-complete but has not yet run on real confidential-compute silicon." This is non-negotiable; without it the proof-of-work framing reads as overclaim.

6. **Temporal edit:** changed "earlier this evening" → "earlier this week" so the post stays valid whenever you actually publish it.

**What to do with the AutoScientists thread directly:** consider replying to either the AutoScientists announcement OR Const's comment with a short follow-up tweet pointing back at this pinned post — *not* a hijack quote-tweet, but a substantive reply ("congrats to the AutoScientists team — we've been building an outward-facing version of the same loop on Bittensor; details in the pin"). That gives Const + the AutoScientists thread a clean handle to engage with you on, rather than hoping the algorithm surfaces a cold pinned tweet.

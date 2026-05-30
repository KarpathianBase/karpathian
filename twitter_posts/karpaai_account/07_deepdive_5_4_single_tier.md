# Deep-dive — §5.4 single attested-execution tier (v1.2 pivot)

**When to post:** Day 7
**Length:** 3733 chars (X Premium long-form)
**Attachments to add:** 1
  - [INSERT: diagram of nested TDX + NVIDIA CC attestation chain — validator nonce binding both TDX quote (with container measurement in user-data) and NVIDIA nvtrust GPU quote]

---

## Post body (copy this into X)

```
Deep-dive: §5.4 — the single attested-execution tier. Why v1.2 collapsed v0.9's two tiers into one.

Background: v0.9.

v0.9 ran a two-tier emission model. A submission attested by Intel TDX + NVIDIA nvtrust got α=1.0. A submission without a valid attestation chain got α=0.5. The economic logic: if you lie about your hardware, your emission is halved, so over enough rounds honest hardware dominates.

That math works. But it's a statistical fence, not a wall. A determined miner with a public checkpoint and a fast non-CC box could still occasionally win at α=0.5 — especially in low-competition rounds. The protocol would discount the lie, not foreclose it.

The v1.2 pivot.

v1.2 deletes the unverified tier. There is one tier. Every miner runs the official Karpa Docker image, inside a Confidential VM (Intel TDX or AMD SEV-SNP), on a CC-capable NVIDIA GPU (H100 / H200 / B200). The Docker image measurement is pinned on-chain.

No valid attestation off the official image. No emission off a valid attestation. The "borrow a public checkpoint and ship it" attack is foreclosed architecturally, not priced out probabilistically.

How the mechanism actually works.

This is the part skeptics care about, so here it is end-to-end:

1. The validator issues a fresh nonce for the submission window.
2. The miner boots the official Karpa Docker image inside a TDX (or SEV-SNP) CVM on an H100/H200/B200.
3. The container runtime computes the image measurement and writes it into the TDX quote's user-data field, alongside the validator nonce.
4. nvtrust produces an NVIDIA GPU attestation quote, also bound to the same validator nonce.
5. The submission bundle ships both quotes plus the training log and the patch.
6. The validator verifies: TDX quote signature chain valid, GPU quote signature chain valid, both bound to the issued nonce, and the container measurement in the TDX user-data matches the on-chain pinned measurement.

Any link broken → the bundle fails op2 (attestation verify) before any expensive check runs. There is no path to a valid bundle that runs unofficial code, or runs the official code on a non-CC GPU, or replays an old attestation. The chain is nested and nonce-bound.

That is what "deterministic foreclosure" means in practice. Not "the expected value of cheating is negative." More like "the cryptographic chain doesn't exist."

Honest trade-offs.

This is not free. Two things to name out loud:

- Consumer-GPU exclusion at launch. A 4090 cannot produce a valid bundle. CC-capable silicon (H100 / H200 / B200) is the floor. Lowering that floor is tracked as Phase 4 work — once Hopper-class confidential compute is broadly available on consumer SKUs, the tier can widen without weakening the chain.

- Not yet validated on real CC silicon. The attestation code path is implemented end-to-end and auto-detects CC, falling back to a mock path for local development. But the production path needs an Azure NCC or GCP A3-Confidential slot to run against real Intel TDX + real nvtrust. That's the next external dependency. Code-complete is not the same as shipped on real CC, and I'm not going to pretend otherwise.

Why I think the trade is right.

Statistical discounts are fine when the worst-case cheat costs the protocol a little reputation. They are not fine when the worst-case cheat is "the canonical training recipe absorbed a patch produced by a model the protocol cannot verify." The recipe compounds. A bad patch landed once is in the lineage forever. Foreclosing the attack architecturally is the only honest answer for an artifact whose whole value is that every accepted patch was actually produced by the work it claims to represent.

Receipts:
- Whitepaper §5.4: github.com/karpaai/karpa/blob/main/docs/Karpa-Whitepaper-v1.2.pdf
- v1.2 update notes: github.com/karpaai/karpa/blob/main/docs/whitepaper_v1.2_updates.md
- Attestation code: github.com/karpaai/karpa/blob/main/proof/real_attest.py

[INSERT: diagram of nested TDX + NVIDIA CC attestation chain — validator nonce binding both TDX quote (with container measurement in user-data) and NVIDIA nvtrust GPU quote]
```

---

## Drafter notes

Honest engineer voice, plain past tense for what shipped, present tense for mechanism. Walks the attestation chain step-by-step so a skeptical reader can see why "deterministic foreclosure" isn't hand-wave. Names both trade-offs (consumer-GPU exclusion, untested on real silicon) inline. No token / emission / price language. Three receipts: whitepaper PDF section, v1.2 update notes, real_attest.py.

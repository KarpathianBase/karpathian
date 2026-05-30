# Deep-dive — §5.7 anti-gaming

**When to post:** Day 4
**Length:** 4903 chars (X Premium long-form)

---

## Post body (copy this into X)

```
Deep-dive: §5.7 — anti-gaming.

The section reply guys will probe hardest. Any single mechanism here is gameable. The combination is what makes Karpa's score actually mean something.

— Hidden eval set —

The score deciding king isn't val_bpb on the miner's training data. It's a held-out pool: ~3M tokens off-network plus a benchmark mix.

• Rotates per round under commit-reveal, seeded by an on-chain randomness beacon. Slice for round N is committed before the round opens, revealed after submissions close.
• Monthly pool refresh. Tokens turn over, so "memorize the eval" has a shelf life of weeks.
• Never published, never streamed to miners. Lives on validator hardware.

— Eval data NEVER enters the miner's submission path —

This is what makes the hidden set more than a hidden test set.

A miner trains on whatever they want and optimises val_bpb on their own holdout. They submit a patch + bundle. They never see the eval pool, never get per-sample scores, never get logits back. One scalar verdict: did you beat king by >0.013 val_bpb on the hidden slice, yes or no.

You cannot gradient-descent against a number you don't observe.

— Restricted-file scanner (op1, before any compute) —

Validators run 4 cheap ops per submission. Op1 is a diff scan against restricted_files.yaml. Any patch touching:

• eval/
• calibration/
• validator/
• proof/
• restricted_files.yaml itself

is rejected at op1. No proof-test, no compute spent. Miner pays for their own Layer-1 search; if they wasted it patching the judge, that's on them.

Receipt: restricted_files.yaml, validator/validator.py.

— Probabilistic audit —

Validators re-run training on a sample of accepted patches.

• 10% baseline random — every accepted patch has a 10% chance regardless of suspicion.
• 100% on triggers: king-margin submissions (the ones that flip king), miners on probation, community-flagged patches.

Audits don't check hash equality of weights — GPU training isn't bit-reproducible (non-deterministic kernels, atomic adds, scheduler ordering). We check score-and-trajectory equivalence: does the re-run reproduce the loss curve within the noise floor and land on a final eval inside the same band.

Receipt: validator/audit.py.

— Consequences (real Bittensor weights) —

A miner caught — failed audit, restricted-file bypass, attestation mismatch — gets:

• Forfeit of the round emission.
• Zeroed validator weights.
• Blacklist propagated by coldkey, so a fresh hotkey doesn't help.
• Permanent entry in the public experiment-record corpus. Every verdict, including the bad ones, is kept.

— Noise floor (0.013) ensures real, not lucky —

Phase 0.5 measured the seed-to-seed noise floor: 125M model, 10 seeds, 500 steps, val_bpb σ = 0.0064. "Decisively beat king" = 2σ = 0.013 val_bpb.

Empirical, not made up. In docs/phase_0_5_results.md with the seeds.

A patch with a lucky seed cannot flip king. The improvement has to survive noise. There is no winning by a hair. You either reproduce a 0.013+ delta on re-run or you don't.

— "Isn't this just a hidden test set with extra steps?" —

Direct answer: no, and the difference is why this works.

A static private benchmark is a hidden test set. Hold it long enough, leak it, infer it from the score signal — and it dies. That hill is a graveyard.

What's different:

1. Eval rotates per round on a beacon. Today's slice isn't last week's. Can't memorize a moving target.
2. Monthly pool refresh. Even if you inferred the current pool, your inference rots.
3. No per-sample feedback. One scalar per submission. Signal-to-noise on "infer the eval from scores" is brutal.
4. Restricted-file scanner forecloses the obvious attacks (patch the eval loader, patch scoring) at op1.
5. 10% random audit + 100% on king-margin: flip king with a fluke or cheat, you defend it on re-run.
6. Noise floor means flukes can't flip king in the first place.
7. Bittensor weight consequences make the downside real. A static benchmark gets you off a leaderboard. This gets you blacklisted by coldkey and immortalised in the corpus.

None alone is novel. The combination changes the equilibrium.

— Honest limits —

Restricted-file scanner implemented. Op1-op4 implemented. Audit logic implemented. Commit-reveal beacon specced in §5.7; on-chain integration is Phase 1 — testnet (v0.6.0) uses a deterministic per-round seed.

The v1.2 attestation tier (TDX + nvtrust on CC silicon) is what makes "lie about hardware" non-viable, untested on real CC GPUs — no Azure NCC slot yet.

Everything specced is in §5.7. Everything coded is in the repo.

Receipts:
• Whitepaper §5.7: github.com/karpaai/karpa/blob/main/docs/Karpa-Whitepaper-v1.2.pdf
• restricted_files.yaml: github.com/karpaai/karpa
• validator/validator.py (op1 + decisive-beat threshold)
• validator/audit.py (re-train + trajectory equivalence)
• Noise floor: github.com/karpaai/karpa/blob/main/docs/phase_0_5_results.md
```

---

## Drafter notes

Within 3000-5000 char target (4903). Honest-engineer voice maintained: each subsection states a mechanism, names the receipt file or measurement, and the "extra steps" objection gets a direct numbered rebuttal. Honest limits section calls out (1) on-chain beacon integration as Phase 1, not yet wired into testnet v0.6.0 which uses deterministic per-round seed, and (2) v1.2 attestation tier untested on real CC silicon. No emoji, no hashtags, no token/price talk. All seven required items covered (hidden eval, eval-data-isolated path, restricted-file scanner, probabilistic audit, consequences, noise floor, and the objection rebuttal).

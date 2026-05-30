# Phase 0 — the CPU MVP

**When to post:** Day 2
**Length:** 1535 chars (X Premium long-form)
**Attachments to add:** 1
  - [INSERT: terminal screenshot of CPU smoke test showing the king-change event]

---

## Post body (copy this into X)

```
Phase 0 of Karpa was the MVP. The whole point was to prove the design worked before I rented a single GPU.

~3000 lines of code. Full protocol. Running on a laptop CPU.

End-to-end means end-to-end:
- model init
- training step
- eval
- proof-test harness
- validator ops
- scoring
- king change

The smoke test wired all of it together. A challenger model trained on CPU, the validator ran its four ops, the score beat the sitting king, and the king flipped on-chain (well, on-mock-chain). That king-change event was the whole reason to build Phase 0.

[INSERT: terminal screenshot of CPU smoke test showing the king-change event]

Receipts:
- github.com/karpaai/karpa
- scripts/smoke_test.py
- tests/test_model.py

Phase 0 is not impressive on its own. 125M params on CPU is a toy. The point wasn't sophistication. The point was discipline: if the protocol can't survive a laptop run, it definitely can't survive an H100 bill. Every assumption in the whitepaper — the three-layer split, the scoring, the king state machine, the rejection paths — got exercised cheap before anything got exercised expensive.

It also caught real bugs. Validator ops fired in the wrong order. Score comparison off by a sign. Edge cases in the king state machine when two challengers landed in the same epoch. All cheaper to fix on a CPU than at $3/hr on H100.

The discipline lesson I'd give anyone building a subnet: write the protocol top-to-bottom in cheap mode first. Make the king flip on a laptop. Then go rent the GPU.

Phase 0.5 (real H100, real data, real noise floor) is the next post.
```

---

## Drafter notes

Honest engineer voice, plain past tense. Leads with the discipline framing (prove on laptop before paying GPU bill) rather than overselling the code. Lists what end-to-end actually meant, names the bugs the smoke test caught (concrete, not hand-wavy). Receipts inline as bare URLs. One image placeholder for the king-change terminal screenshot. Closes with a forward hook to Phase 0.5. No tokens, no emoji, no hashtags. Within 800-1800 range at 1535 chars.

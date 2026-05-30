# Phase 0.5d — first on-chain king change (testnet 16)

**When to post:** Day 5
**Length:** 2335 chars (X Premium long-form)
**Attachments to add:** 1
  - [INSERT: taostats.io or btcli screenshot showing the set_weights tx landed on netuid 16]

---

## Post body (copy this into X)

```
Phase 0.5d — Karpa on chain.

The protocol stopped running on a single laptop and started writing to Bittensor.

Tag: v0.6.0
Network: Bittensor testnet, netuid 16

Setup:
- Two miners registered: green1, green2.
- Honest caveat: both miners ran on the validator's box. Distributed-host came later. This was the "does the chain abstraction actually work" test, not the "real adversarial network" test.
- Validator running the Layer 3 loop from Phase 0.

What happened:
- First on-chain king change. The validator scored a submission, decided it decisively beat the current king (the >0.013 val_bpb noise-floor margin from Phase 0.5), and called set_weights. The tx landed on netuid 16. King flipped on chain, not in a local sqlite row.

The boring part that actually mattered:
- Bittensor rate-limits set_weights. A naive validator loop hits that limit and either crashes or stalls the whole pipeline.
- The chain abstraction in chain_layer/bittensor_chain.py catches the rate-limit, skips the set_weights call for that epoch, retries on the next one, and never blocks the scoring loop.
- This sounds trivial. It is not trivial when a real validator has to run for weeks without a human watching it.

Why this phase matters:
- Phase 0: protocol works end-to-end on CPU.
- Phase 0.5: it works on real H100 with real data and a real noise floor.
- Phase 0.5b: it's cheap enough to run (3.8x throughput on bf16, ~$3.50/proof-test).
- Phase 0.5c: attestation module is code-complete (still untested on real CC silicon, no Azure NCC slot yet).
- Phase 0.5d: it talks to the chain. set_weights lands. King flips on chain. Rate-limits don't kill it.

What this is not:
- Not mainnet. Testnet 16.
- Not a distributed adversarial network — both miners were colocated with the validator.
- Not proof the economic design holds under real miners trying to game it. That comes later.

What it is: the smallest possible end-to-end loop where every layer of the v1.2 architecture — Layer 1 search (miner-side), Layer 2 proof-test (canonical Docker), Layer 3 judgment + chain writes (validator) — runs against the actual Bittensor chain instead of a mock.

Receipts:
- Release: github.com/karpaai/karpa/releases/tag/v0.6.0
- Chain abstraction: github.com/karpaai/karpa/blob/main/chain_layer/bittensor_chain.py
- Protocol: github.com/karpaai/karpa

[INSERT: taostats.io or btcli screenshot showing the set_weights tx landed on netuid 16]
```

---

## Drafter notes

Honest engineer voice, plain past tense. Caveats inline (testnet not mainnet, miners colocated with validator, attestation still untested on real CC silicon). No emoji, no hashtags, no token talk. Frames the boring rate-limit handling as the real engineering win, while the headline is the first on-chain king change. Receipts at the end. Char count verified by counting characters in body string including newlines.

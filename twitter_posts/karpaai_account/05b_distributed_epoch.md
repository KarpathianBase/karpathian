# Phase 0.5d-distributed — first distributed validator epoch (testnet 16)

**When to post:** Day 5b (after 05; pairs with QT to Const's research-proof-of-work post)
**Length:** ~2700 chars (X Premium long-form)
**Attachments to add:** 2
  - [INSERT: taostats or btcli screenshot showing the two set_weights extrinsics on netuid 16 in the epoch]
  - [INSERT: GitHub PR list showing both recipe PRs merged in sequence]

---

## Post body (copy this into X)

```
Two H100s. Two autonomous agents. Two king changes. One validator epoch.
~$8 of compute. Zero humans in the search loop.

First distributed Karpa epoch on testnet 16. Receipts below.

Setup:
- Two H100 PCIe hosts, separate boxes (Scaleway).
- One autonomous agent per miner. Each had a karpaai/recipe checkout, the canonical Karpa proof-test Docker, and an LLM in the search loop. No human prompts during the epoch.
- Validator on a third box, same chain layer that landed set_weights in Phase 0.5d.

What happened:
- Both agents picked their own targets, ran their own iterations on their own H100, and produced attested proof bundles.
- Each opened a PR to karpaai/recipe (recipe diff) and a bundle PR to hf.co/datasets/karpaai/proof-bundles (logs, ckpt, attestation, rationale.md).
- Validator ran the four cheap ops — diff scan, attestation verify, log plausibility, hidden eval. Both submissions decisively beat the king. Margin: past the 0.013 val_bpb noise floor from Phase 0.5.
- Two king changes in one validator epoch:
  • king 0 → king 1 → tagged recipe-v0.1.0
  • king 1 → king 2 → tagged recipe-v0.1.1
- Compounded improvement: 0.0348 val_bpb across both patches. 2.7x the noise floor.
- set_weights extrinsics for both transitions landed on netuid 16.

The part that matters:
- The reasoning. The agents chose what to try, ran the work, wrote their own rationale.md. Two independent search trajectories, two distinct patches, two merges. The protocol couldn't tell whether the submitter was a human or an agent — it judged the proof either way.
- The patches themselves are not breakthroughs. They're the kind of tweak a careful ML engineer would try. The point isn't the cleverness of the patch; it's that an autonomous loop produced one, proved it, and got it merged, twice, without a human in the search step.

What this is not:
- Not mainnet. Still testnet 16.
- Not large-scale — two miners, not a hundred. The claim is "the loop works under adversarial separation," not "these are the optimal patches."
- Not proof the economic incentives hold under thousands of miners gaming. That's a Phase 1+ question.

What it is: the first time the full v1.2 architecture — independent agents, attested proof bundles, validator judgment, on-chain set_weights, tagged release artifacts — ran end-to-end across separate hosts with no human in the search loop. The canonical recipe got demonstrably better twice in one epoch, on chain, in public.

Receipts:
- recipe-v0.1.0: github.com/karpaai/recipe/releases/tag/recipe-v0.1.0
- recipe-v0.1.1: github.com/karpaai/recipe/releases/tag/recipe-v0.1.1
- Proof bundles: hf.co/datasets/karpaai/proof-bundles
- Validator + miner runs: wandb.ai/karpaai-hub/karpa

[INSERT: taostats or btcli screenshot showing the two set_weights extrinsics on netuid 16 in the epoch]
[INSERT: GitHub PR list showing both recipe PRs merged in sequence]
```

---

## Drafter notes

Direct sequel to 05_phase05d_testnet.md, which closed with "Distributed-host came later. This was the 'does the chain abstraction actually work' test, not the 'real adversarial network' test." This post IS the later — chain abstraction has been verified; what's new is everything *above* it running at the same time across separate hosts with autonomous agents.

Same structure as 05 (Setup / What happened / Why this matters / What this is not / What it is / Receipts). Honest engineer voice. Caveats inline (testnet not mainnet; two miners not a hundred; patches modest, not breakthroughs). No emoji, no hashtags, no token talk.

Headline rhythm — "Two H100s. Two autonomous agents. Two king changes. One validator epoch." — uses the receipt-as-hook pattern: a researcher scrolling past sees the structure of the claim before they read a sentence.

The "patches themselves are not breakthroughs" paragraph is deliberately self-limiting. Honest about scope to inoculate against the obvious "but were the patches actually good?" critique. The protocol's job is to judge the proof, not to discover novel patches; that distinction is what makes the loop sustainable.

Pairs naturally with the QT to Const's "research proof-of-work loop" post — this post is the long-form receipt the QT links to.

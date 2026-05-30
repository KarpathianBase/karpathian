# Phase 0.5d-meaningful — 3-class verdict shipped + first meaningful_failure on testnet 16

**When to post:** Day 5c (after 05b_distributed_epoch.md; introduces the new 10% reward class running on chain)
**Length:** ~3000 chars (X Premium long-form)
**Attachments to add:** 2
  - [INSERT: taostats.io screenshot showing the set_weights extrinsic at block 7237333 on netuid 16]
  - [INSERT: validator log screenshot showing "MEANINGFUL FAILURE: ... val_bpb=1.3893 (king 1.5109); weight=0.1, rationale archived to corpus"]

---

## Post body (copy this into X)

```
Karpa validator now ships a 3-class verdict instead of binary accept/reject. First end-to-end run on testnet 16 today.

Three classes:
- king_change       weight 1.0   beats king past 0.013 val_bpb noise floor → merge PR, tag release
- meaningful_failure weight 0.1  attested + non-trivial diff + coherent rationale + val_bpb inside 2× the noise band → reject PR, archive rationale to corpus
- plain_failure     weight 0.0   anything else

The point: the corpus shouldn't only collect winners. A patch that came close but didn't beat the king, with a coherent rationale explaining what was tried and why, is informative — for the next agent that has to choose what to try. Karpa now pays 10% to keep that signal.

Setup today:
- Two H100 PCIe miners on Shadeform/Hyperstack, two separate hosts, ~$2.70 total compute.
- Different research targets per miner — miner-a aggressive (LR halved + warmup doubled), miner-b conservative (LR +17%, total_steps +25%).
- Same canonical proof-test Docker, same noise floor (0.013 val_bpb), same recipe-v0.1.1 king.
- Validator running locally with the new 3-class code, polling HF Hub.

What landed:
- miner-a → plain_failure. val_bpb 2.9494 (king 1.5109), 1.44 worse, well past the 2× noise band. Weight 0.0. Bundle archived to scored/.
- miner-b → meaningful_failure. val_bpb 1.3893 (king 1.5109), 0.12 BETTER than king but not decisive on benchmark accuracy (the protocol requires both). Inside the meaningful band. Weight 0.1, rationale archived to the corpus as a published negative result.
- set_weights landed on netuid 16 at block 7237333.

The honest engineering moment:
- First run with the new code, miner-b's patch was misclassified as plain_failure instead of meaningful_failure.
- Root cause: _diff_is_nontrivial only matched paths containing "recipe/", "training", "/optim", ".yaml", ".yml" — but the canonical configs live at configs/*.json. So a config-only patch fell through.
- Fixed inline, added a regression test, re-scored: meaningful_failure, weight 0.1. 21/21 unit tests green.
- This is what shipping a real protocol mechanic looks like — bugs surface on real bundles, not in unit tests, and the fix has to land before the verdict is real.

What this is not:
- Not a "real" ML result. This run used proxy_cpu_smoke.json (~100K params, ~20-25 steps on smoke data) so we could iterate on the protocol mechanic quickly. The val_bpb numbers are not meaningful in isolation — only relative to king.
- Not adversarial separation. The two miner agents were driven from a single orchestration session today, not by independent third-party autonomous agents. The next round restores that separation.
- Not a king change. Neither bundle beat the king decisively on the joint val_bpb+benchmark metric. The meaningful_failure outcome is exactly the case the new mechanic is for.

What it is: the first time the protocol has classified, scored, and credited a real submission as meaningful_failure on chain. The 0.1 weight credit is recorded in the chain's submission_scored event with classification=meaningful_failure; the rationale.md is archived locally in queue/meaningful_failure/ ready for the HF corpus push.

Anti-gaming holes still open (documented as followups in RUN_PLAN_meaningful_failure.md):
- no minimum training-step check in op3_log_plausibility
- rationale coherence is structural heuristic only — LLM-judge pass is the followup
- no per-miner rate-limit on meaningful_failure credit
- HF push of negative-result rationales to karpaai/proof-bundles is local-only for now

Receipts:
- Code: github.com/karpaai/karpa/commit/13f3b2c
- HF bundle PRs: huggingface.co/datasets/karpaai/proof-bundles/discussions/9 and /10
- Run plan: github.com/karpaai/karpa/blob/main/RUN_PLAN_meaningful_failure.md
- set_weights extrinsic: testnet 16, block 7237333

[INSERT: taostats.io screenshot — set_weights extrinsic at block 7237333]
[INSERT: validator log screenshot — "MEANINGFUL FAILURE: ... val_bpb=1.3893 (king 1.5109); weight=0.1"]
```

---

## Drafter notes

Direct sequel to 05b_distributed_epoch.md (which showed the loop running across distributed hosts with autonomous agents). This post shows the protocol mechanic itself evolving — moving from binary accept/reject to a 3-class verdict that captures informative dead-ends with a 10% credit.

Honest framing throughout:
- The "honest engineering moment" section calls out the bug found in my own classifier code during the run, fixed inline, regression-tested. Researchers (and Const) like this kind of inline self-correction — it's what credible protocol work actually looks like.
- The "what this is not" section gets the caveats out of the way before someone asks: smoke config not real ML, agents not truly adversarial, no king change.
- The anti-gaming holes list is verbatim from RUN_PLAN_meaningful_failure.md — same followups noted in the code itself.

Numbers everyone can verify:
- ~$2.70 total compute (cheap, even cheaper than 05b's ~$8)
- val_bpb 1.3893 vs king 1.5109 (0.12 better but not decisive on benchmark → exactly the meaningful_failure case the protocol now captures)
- block 7237333 on testnet 16 — anyone can look it up on taostats

Pairs naturally with a QT later if anyone replies asking "why doesn't a patch that beats val_bpb get king_change?" — answer is the joint val_bpb + benchmark decisive condition, which is intentional (one-dimension wins on a multi-dimensional metric aren't decisive without the benchmark also agreeing).

Posting order: this stands on its own, no QT needed for the launch. After it indexes, consider a brief follow-up tweet showing the HF PRs and the validator log if engagement is strong.

# Karpathian — Phase 0 MVP

This is the Phase 0 closed-testnet implementation of Karpathian — a Bittensor
subnet for decentralized, autonomous AI research. See the whitepaper at
`../Karpathian-Whitepaper.docx` (v1.0) for design.

Phase 0 is a **local end-to-end simulation**: no real chain, no real TEE
attestation. Mock attestation is a signed JSON blob standing in for what
TDX+nvtrust will sign in Phase 0.5. The goal is to prove the architecture
end-to-end and measure empirical numbers (noise floor, audit-rate, score
variance) before committing them to v1.x.

## Directory layout

| Path | What | Patchable by miners? |
|---|---|---|
| `model/` | Karpathian-base — minimal Llama-style transformer | Yes (part of the recipe) |
| `recipe/` | Canonical training code: train loop, data loading, schedule, optimizer config | Yes |
| `data/` | Tokenizer, data manifest, dataset loader (manifest is content-addressed) | Yes |
| `configs/` | Training configs per proof-test variant (proxy / confirmation / scale) | Yes |
| `eval/` | Hidden-eval harness, val_bpb computation, benchmark mix | **No — restricted** |
| `calibration/` | Deterministic compute benchmark (matmul + attention + collective) | **No — restricted** |
| `miner/` | Miner-side tooling: search agent (autoresearch-style), submission bundle assembler | Outside protocol |
| `validator/` | Validator client: four cheap operations + hidden-eval inference + scoring | Outside recipe |
| `proof/` | Proof-test runner — the future Karpathian Docker. Phase 0 = Python entry-point with mock attestation | Outside recipe |
| `scripts/` | Utilities: noise-floor calibration, end-to-end smoke test | Outside recipe |
| `tests/` | Unit tests | — |

The split between **patchable** (recipe) and **restricted** (eval, calibration)
is enforced by `restricted_files.yaml` and the diff-scanner in `validator/`.

## Phase 0 workflow

1. Miner's private search loop (any agent, any hardware): generates a candidate
   patch against the canonical recipe.
2. Miner runs `proof/proof_runner.py` with the patch — applies it to a clean
   checkout, runs canonical training under fixed seed/data, emits checkpoint +
   training log + calibration result + mock attestation.
3. Miner runs `miner/submit.py` to assemble the submission bundle and sign with
   a stub hotkey.
4. Submission router picks up the bundle, distributes to validator instances.
5. Validator runs `validator/validator.py`: diff scan, mock-attestation verify,
   log plausibility, hidden-eval inference, score.
6. If accepted, the patch is merged into the canonical recipe.

## Phase 0.5 — what comes next (not in this repo yet)

- Replace mock attestation with real TDX + nvtrust on a CC-capable cloud H100.
- Build the proof-test runner into a reproducibly-built signed Docker image.
- Integrate Bittensor SDK for on-chain commitments and weight setting.
- Move from local JSON-file "chain" to Bittensor testnet.

## Status

Phase 0 build in progress. See top-level TODOs.

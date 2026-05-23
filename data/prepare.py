"""
Prepare a tokenized data shard from a text source.

Usage:
    python -m data.prepare --source synthetic --out data/shards/ --shard-tokens 100000
    python -m data.prepare --source fineweb-edu --out data/shards/ --shard-tokens 10000000

The synthetic source is for CPU smoke tests — it generates a deterministic
small corpus from a seeded RNG over a small vocabulary, so the training loop
has something to chew on without downloading anything.

For real training, --source fineweb-edu streams HuggingFaceFW/fineweb-edu
(sample-10BT subset). Requires `datasets` package.
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from data.tokenizer import EOT_TOKEN, get_tokenizer
from data.manifest import DataManifest, build_manifest


def synthetic_stream(seed: int = 1337):
    """A small deterministic text corpus. Not real English — just stable bytes
    so the model has something to fit. Use only for CPU smoke tests."""
    rng = random.Random(seed)
    words = [
        "the", "cat", "sat", "on", "the", "mat", "and", "looked", "around",
        "quietly", "while", "rain", "tapped", "the", "tin", "roof",
        "Karpathian", "validates", "training", "recipes", "openly",
        "every", "epoch", "the", "container", "attests", "what", "it", "ran",
        "miners", "search", "patches", "validators", "score", "checkpoints",
    ]
    while True:
        sent_len = rng.randint(6, 18)
        yield " ".join(rng.choice(words) for _ in range(sent_len)) + "."


def fineweb_edu_stream():  # pragma: no cover - exercised only with `datasets` installed
    from datasets import load_dataset

    ds = load_dataset(
        "HuggingFaceFW/fineweb-edu",
        name="sample-10BT",
        split="train",
        streaming=True,
    )
    for row in ds:
        yield row["text"]


def tokenize_into_shards(
    out_dir: Path,
    shard_tokens: int,
    total_tokens: int,
    source: str = "synthetic",
    seed: int = 1337,
) -> list[Path]:
    tok = get_tokenizer()
    stream = synthetic_stream(seed) if source == "synthetic" else fineweb_edu_stream()
    out_dir.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []
    buf: list[int] = []
    written = 0
    shard_idx = 0
    for text in stream:
        if not text:
            continue
        ids = tok.encode_ordinary(text)
        buf.extend(ids)
        buf.append(EOT_TOKEN)
        while len(buf) >= shard_tokens:
            shard_path = out_dir / f"shard_{shard_idx:04d}.bin"
            arr = np.array(buf[:shard_tokens], dtype=np.uint16)
            arr.tofile(shard_path)
            paths.append(shard_path)
            shard_idx += 1
            written += shard_tokens
            buf = buf[shard_tokens:]
            if written >= total_tokens:
                return paths
    if buf:
        shard_path = out_dir / f"shard_{shard_idx:04d}.bin"
        np.array(buf, dtype=np.uint16).tofile(shard_path)
        paths.append(shard_path)
    return paths


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--source", choices=["synthetic", "fineweb-edu"], default="synthetic")
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--shard-tokens", type=int, default=100_000)
    p.add_argument("--total-tokens", type=int, default=500_000)
    p.add_argument("--track", default="llm-pretraining-launch")
    p.add_argument("--manifest", type=Path, default=None)
    p.add_argument("--seed", type=int, default=1337)
    args = p.parse_args()

    paths = tokenize_into_shards(
        args.out,
        shard_tokens=args.shard_tokens,
        total_tokens=args.total_tokens,
        source=args.source,
        seed=args.seed,
    )
    base_dir = args.out.parent
    manifest = build_manifest(
        track=args.track,
        tokenizer="gpt2",
        vocab_size=50257,
        dtype="uint16",
        shards=paths,
        base_dir=base_dir,
    )
    manifest_path = args.manifest if args.manifest else base_dir / "data_manifest.json"
    manifest.write(manifest_path)
    print(f"wrote {len(paths)} shards, {manifest.total_tokens():,} tokens total")
    print(f"manifest: {manifest_path}")
    print(f"manifest hash: {manifest.manifest_hash()[:16]}…")


if __name__ == "__main__":
    main()

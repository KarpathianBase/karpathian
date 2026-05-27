"""
Chain backend configuration.

Set AUTORALPH_CHAIN=bittensor to use real Bittensor chain, or
AUTORALPH_CHAIN=local (default) for JSON-file testing.

Reads from .env file if present (never committed to git).
"""

from __future__ import annotations

import os
from pathlib import Path

from .interface import ChainInterface


def _load_dotenv(autoralph_root: Path | None = None) -> None:
    """Load .env file into os.environ if it exists. Does not override
    existing env vars (explicit exports take precedence)."""
    candidates = []
    if autoralph_root:
        candidates.append(Path(autoralph_root) / ".env")
    candidates.append(Path.cwd() / ".env")
    for env_path in candidates:
        if env_path.exists():
            for line in env_path.read_text().splitlines():
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, _, value = line.partition("=")
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                if key and key not in os.environ:
                    os.environ[key] = value
            return


def get_chain(autoralph_root: Path | None = None) -> ChainInterface:
    """Factory: returns the configured chain backend."""
    _load_dotenv(autoralph_root)
    backend = os.environ.get("AUTORALPH_CHAIN", "local")

    if backend == "bittensor":
        from .bittensor_chain import BittensorChain
        return BittensorChain(
            network=os.environ.get("BT_NETWORK", "test"),
            netuid=int(os.environ.get("BT_NETUID", "1")),
            wallet_name=os.environ.get("BT_WALLET", "default"),
            wallet_hotkey=os.environ.get("BT_HOTKEY", "default"),
            chain_dir=Path(autoralph_root / "chain") if autoralph_root else None,
        )
    else:
        from .local import LocalChain
        chain_dir = Path(autoralph_root / "chain") if autoralph_root else Path("chain")
        return LocalChain(chain_dir)

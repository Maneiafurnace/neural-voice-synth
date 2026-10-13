"""TOML config loader with local-override merge.

Load order (later wins):
  1. config/default.toml
  2. config/local.toml   (gitignored, optional)
  3. explicit --config path
"""
from __future__ import annotations

import tomllib
from pathlib import Path

from src.config.schema import EngineConfig


def _merge(base: dict, overlay: dict) -> dict:
    out = dict(base)
    for k, v in overlay.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _merge(out[k], v)
        else:
            out[k] = v
    return out


def load_config(explicit: Path | None = None) -> EngineConfig:
    root = Path(__file__).resolve().parents[2] / "config"
    merged: dict = {}
    for candidate in (root / "default.toml", root / "local.toml", explicit):
        if candidate and candidate.exists():
            merged = _merge(merged, tomllib.loads(candidate.read_text("utf-8")))
    return EngineConfig.from_dict(merged)
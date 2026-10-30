# -*- coding: utf-8 -*-
"""Shared helpers. No third-party imports besides numpy/matplotlib when available."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

STATUS = "已整理，未运行验证"


def rng(seed: int = 0) -> np.random.Generator:
    return np.random.default_rng(seed)


def save_meta(path: Path, **kwargs) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"verification_status": STATUS, **kwargs}
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def try_savefig(path: Path):
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception:
        return None
    path.parent.mkdir(parents=True, exist_ok=True)
    return plt

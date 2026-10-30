#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from _common import save_meta  # noqa: E402


def main() -> None:
    cfg = json.loads((HERE / "config.json").read_text(encoding="utf-8"))
    rng = np.random.default_rng(cfg["seed"])
    n = cfg["n"]
    r = cfg["mu"] + cfg["sigma"] * rng.standard_normal(n)
    r += 0.002 * np.sin(2 * np.pi * np.arange(n) / cfg["cycle"])
    price = 100 * np.exp(np.cumsum(r))
    data = HERE / "data"
    data.mkdir(exist_ok=True)
    np.savez(data / "synth_price.npz", price=price, ret=r)
    save_meta(
        data / "README.json",
        source="synthetic_gbm_plus_sine",
        license="original schematic",
        units={"price": "dimensionless index", "ret": "log return per step"},
        sample_rate="1 step = 1 bar (not seconds)",
        not_market_data=True,
    )
    print("wrote", data)


if __name__ == "__main__":
    main()

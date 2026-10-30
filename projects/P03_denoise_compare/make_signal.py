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
    fs = float(cfg["fs"])
    n = int(round(cfg["duration_s"] * fs))
    t = np.arange(n) / fs
    clean = np.sin(2 * np.pi * cfg["sine_hz"] * t)
    clean[t >= 0.8] += 0.8
    clean[t >= 1.3] -= 0.8
    rng = np.random.default_rng(cfg["seed"])
    noisy = clean + cfg["noise_std"] * rng.standard_normal(n)
    data = HERE / "data"
    data.mkdir(exist_ok=True)
    np.savez(data / "block_sine.npz", t=t, clean=clean, noisy=noisy, fs=fs)
    save_meta(
        data / "README.json",
        source="synthetic",
        license="original schematic",
        units={"t": "s", "clean/noisy": "dimensionless", "fs": "Hz"},
        sample_rate_hz=fs,
        noise="iid gaussian",
    )
    print("wrote", data)


if __name__ == "__main__":
    main()

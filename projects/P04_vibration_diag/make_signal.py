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
    x = np.zeros(n)
    period = 1.0 / cfg["fault_hz"]
    k = 0
    while k * period < t[-1]:
        tau = t - k * period
        pulse = (tau >= 0).astype(float) * np.exp(-cfg["decay"] * np.clip(tau, 0, None))
        x += pulse * np.sin(2 * np.pi * cfg["carrier_hz"] * t)
        k += 1
    rng = np.random.default_rng(cfg["seed"])
    x += cfg["noise_std"] * rng.standard_normal(n)
    data = HERE / "data"
    data.mkdir(exist_ok=True)
    np.savez(data / "synthetic_bearing.npz", t=t, x=x, fs=fs)
    save_meta(
        data / "README.json",
        source="synthetic_not_cwru",
        license="original schematic",
        units={"t": "s", "x": "dimensionless accel", "fs": "Hz"},
        sample_rate_hz=fs,
        fault_hz=cfg["fault_hz"],
        warning="Not real bearing measurements",
    )
    print("wrote", data)


if __name__ == "__main__":
    main()

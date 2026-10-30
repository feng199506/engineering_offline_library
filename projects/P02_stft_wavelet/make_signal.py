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
    # linear chirp phase 2π (f0 t + (f1-f0) t^2 / (2T))
    T = t[-1] if t[-1] > 0 else 1.0
    phase = 2 * np.pi * (
        cfg["chirp_f0"] * t + (cfg["chirp_f1"] - cfg["chirp_f0"]) * t * t / (2 * T)
    )
    x = np.sin(phase)
    i0 = int(round(cfg["impulse_time_s"] * fs))
    if 0 <= i0 < n:
        x[i0] += cfg["impulse_amp"]
    rng = np.random.default_rng(cfg["seed"])
    x += cfg["noise_std"] * rng.standard_normal(n)
    data = HERE / "data"
    data.mkdir(exist_ok=True)
    np.savez(data / "chirp_impulse.npz", t=t, x=x, fs=fs)
    save_meta(
        data / "README.json",
        source="synthetic",
        license="original schematic",
        units={"t": "s", "x": "dimensionless", "fs": "Hz"},
        sample_rate_hz=fs,
        note="linear chirp plus one impulse; not field data",
    )
    print("wrote", data)


if __name__ == "__main__":
    main()

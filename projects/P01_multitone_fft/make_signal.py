#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Synthetic multi-tone signal. Schematic data only."""
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
    rng = np.random.default_rng(cfg["seed"])
    out = HERE / "data"
    out.mkdir(exist_ok=True)
    for T in cfg["durations_s"]:
        n = int(round(T * fs))
        t = np.arange(n) / fs
        x = np.zeros(n)
        for f, a in zip(cfg["tones_hz"], cfg["amps"]):
            x += a * np.sin(2 * np.pi * f * t)
        x += cfg["noise_std"] * rng.standard_normal(n)
        np.savez(out / f"multitone_{T:.0f}s.npz", t=t, x=x, fs=fs)
    save_meta(
        out / "README.json",
        source="synthetic",
        license="original schematic",
        units={"t": "s", "x": "dimensionless amplitude", "fs": "Hz"},
        sample_rate_hz=fs,
        tones_hz=cfg["tones_hz"],
    )
    print("wrote", out)


if __name__ == "__main__":
    main()

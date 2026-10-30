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
    fs = cfg["imu_hz"]
    n = int(cfg["duration_s"] * fs)
    t = np.arange(n) / fs
    # true trajectory: slow turn in 2D
    px = 10 * np.sin(0.15 * t)
    py = 4 * t
    vx = np.gradient(px, 1 / fs)
    vy = np.gradient(py, 1 / fs)
    ax = np.gradient(vx, 1 / fs)
    ay = np.gradient(vy, 1 / fs)
    rng = np.random.default_rng(cfg["seed"])
    imu = np.stack(
        [
            ax + cfg["bias"][0] + cfg["acc_noise_std"] * rng.standard_normal(n),
            ay + cfg["bias"][1] + cfg["acc_noise_std"] * rng.standard_normal(n),
        ],
        axis=1,
    )
    step = int(fs / cfg["gnss_hz"])
    g_idx = np.arange(0, n, step)
    gnss = np.stack(
        [
            px[g_idx] + cfg["gnss_std"] * rng.standard_normal(len(g_idx)),
            py[g_idx] + cfg["gnss_std"] * rng.standard_normal(len(g_idx)),
        ],
        axis=1,
    )
    data = HERE / "data"
    data.mkdir(exist_ok=True)
    np.savez(
        data / "synth_imu_gnss.npz",
        t=t,
        true_p=np.stack([px, py], axis=1),
        true_v=np.stack([vx, vy], axis=1),
        imu_acc=imu,
        gnss=gnss,
        gnss_idx=g_idx,
        fs=fs,
    )
    save_meta(
        data / "README.json",
        source="synthetic",
        license="original schematic",
        units={
            "t": "s",
            "true_p": "m",
            "true_v": "m/s",
            "imu_acc": "m/s^2 (corrupted)",
            "gnss": "m",
        },
        sample_rate_hz={"imu": fs, "gnss": cfg["gnss_hz"]},
        latency_s=0,
        note="Not real IMU/GNSS. delay=0. Not hardware.",
    )
    print("wrote", data)


if __name__ == "__main__":
    main()

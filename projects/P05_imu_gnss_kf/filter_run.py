#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Linear KF on 2D point mass + accel bias. Teaching model only."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent


def main() -> None:
    z = np.load(HERE / "data" / "synth_imu_gnss.npz")
    t = z["t"]
    imu = z["imu_acc"]
    gnss = z["gnss"]
    gidx = z["gnss_idx"]
    true_p = z["true_p"]
    dt = float(t[1] - t[0])
    n = len(t)
    # state: px py vx vy bx by
    F = np.eye(6)
    F[0, 2] = dt
    F[1, 3] = dt
    qv, qb = 0.2, 0.01
    Q = np.diag([1e-6, 1e-6, qv * dt, qv * dt, qb * dt, qb * dt])
    R = np.diag([1.5**2, 1.5**2])
    H = np.zeros((2, 6))
    H[0, 0] = H[1, 1] = 1.0
    x = np.zeros(6)
    P = np.eye(6) * 10
    filt = np.zeros((n, 6))
    gi = 0
    for k in range(n):
        acc = imu[k] - x[4:6]
        x = F @ x
        x[2:4] += acc * dt
        P = F @ P @ F.T + Q
        if gi < len(gidx) and gidx[gi] == k:
            y = gnss[gi]
            S = H @ P @ H.T + R
            K = P @ H.T @ np.linalg.inv(S)
            x = x + K @ (y - H @ x)
            P = (np.eye(6) - K @ H) @ P
            gi += 1
        filt[k] = x
    rmse_f = float(np.sqrt(np.mean((filt[:, :2] - true_p) ** 2)))
    out = HERE / "output"
    out.mkdir(exist_ok=True)
    np.savez(out / "kf_causal.npz", filt=filt, t=t)
    metrics = {
        "causal_position_rmse_m": rmse_f,
        "rts_not_run": True,
        "note": "RMSE is on synthetic data. Not hardware. RTS skipped by default (would use future).",
        "verification": "script executed locally if you see this file from a run",
    }
    (out / "metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print(metrics)


if __name__ == "__main__":
    main()

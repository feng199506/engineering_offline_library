#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
import json
import numpy as np

HERE = Path(__file__).resolve().parent
out = HERE / "output"
out.mkdir(exist_ok=True)
rng = np.random.default_rng(16)
n = 400
dt = 0.02
th = np.cumsum(0.4 * dt + 0.05 * rng.normal(size=n))
y = np.sin(th) + 0.05 * rng.normal(size=n)

# EKF 1D
x, P = 0.0, 1.0
q, r = 0.002, 0.05**2
ekf = np.zeros(n)
for k in range(n):
    x = x + 0.4 * dt
    P = P + q
    H = np.cos(x)
    S = H * P * H + r
    K = P * H / S
    x = x + K * (y[k] - np.sin(x))
    P = (1 - K * H) * P
    ekf[k] = x

# UKF 1D (kappa=0, alpha=1e-3, beta=2) simplified
x, P = 0.0, 1.0
ukf = np.zeros(n)
alpha, beta, kappa = 1e-3, 2.0, 0.0
l = alpha**2 * (1 + kappa) - 1
for k in range(n):
    x = x + 0.4 * dt
    P = P + q
    sig = np.array([x, x + np.sqrt((1 + l) * P), x - np.sqrt((1 + l) * P)])
    wm = np.array([l / (1 + l), 1 / (2 * (1 + l)), 1 / (2 * (1 + l))])
    wc = wm.copy()
    wc[0] += 1 - alpha**2 + beta
    ys = np.sin(sig)
    yhat = ys @ wm
    Pyy = np.sum(wc * (ys - yhat) ** 2) + r
    Pxy = np.sum(wc * (sig - x) * (ys - yhat))
    K = Pxy / Pyy
    x = x + K * (y[k] - yhat)
    P = P - K * Pyy * K
    ukf[k] = x

metrics = {
    "ekf_rmse": float(np.sqrt(np.mean((ekf - th) ** 2))),
    "ukf_rmse": float(np.sqrt(np.mean((ukf - th) ** 2))),
    "note": "1D synthetic. Not IMU hardware. Not a claim UKF always wins.",
}
(out / "metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
print(metrics)

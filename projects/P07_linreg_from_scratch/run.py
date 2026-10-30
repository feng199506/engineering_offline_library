#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
import json
import numpy as np

HERE = Path(__file__).resolve().parent
out = HERE / "output"
out.mkdir(exist_ok=True)
rng = np.random.default_rng(7)
n, p = 200, 5
true_w = np.array([1.0, -2.0, 0.5, 0.0, 3.0])
X = rng.normal(size=(n, p))
X[:, 4] = X[:, 0] + 1e-4 * rng.normal(size=n)  # collinear
y = X @ true_w + 0.1 * rng.normal(size=n)
w_ne = np.linalg.pinv(X.T @ X) @ X.T @ y
w_svd = np.linalg.lstsq(X, y, rcond=None)[0]
s = np.linalg.svd(X, compute_uv=False)
metrics = {
    "cond": float(s[0] / s[-1]),
    "ne_err": float(np.linalg.norm(w_ne - true_w)),
    "svd_err": float(np.linalg.norm(w_svd - true_w)),
    "data": "synthetic",
    "verification_status": "已整理，数字仅在运行后有效",
}
(out / "metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
print(metrics)

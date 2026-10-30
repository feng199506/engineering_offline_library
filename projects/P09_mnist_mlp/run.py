#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
import json
import numpy as np

HERE = Path(__file__).resolve().parent
out = HERE / "output"
out.mkdir(exist_ok=True)
rng = np.random.default_rng(9)
n = 400
x0 = rng.normal(loc=[-1, 0], scale=0.4, size=(n // 2, 2))
x1 = rng.normal(loc=[1, 0.2], scale=0.4, size=(n // 2, 2))
X = np.vstack([x0, x1])
y = np.array([0] * (n // 2) + [1] * (n // 2))
idx = rng.permutation(n)
X, y = X[idx], y[idx]
n_tr = 300
Xtr, ytr, Xte, yte = X[:n_tr], y[:n_tr], X[n_tr:], y[n_tr:]
# logistic
w = np.zeros(2)
b = 0.0
for _ in range(200):
    z = Xtr @ w + b
    p = 1 / (1 + np.exp(-z))
    w -= 0.1 * (Xtr.T @ (p - ytr) / len(ytr))
    b -= 0.1 * float(np.mean(p - ytr))
pred = (Xte @ w + b > 0).astype(int)
acc = float(np.mean(pred == yte))
metrics = {"test_acc_synthetic_blobs": acc, "note": "Not MNIST. Not verified beyond this script."}
(out / "metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
print(metrics)

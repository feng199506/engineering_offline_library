#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
import json
import numpy as np

HERE = Path(__file__).resolve().parent
out = HERE / "output"
out.mkdir(exist_ok=True)
rng = np.random.default_rng(19)
ang = np.linspace(0, 1.8 * np.pi, 40)
true = np.array([1.2, -0.4, 2.5])  # cx cy r
xy = np.stack([true[0] + true[2] * np.cos(ang), true[1] + true[2] * np.sin(ang)], axis=1)
xy += 0.05 * rng.normal(size=xy.shape)
p = np.array([0.0, 0.0, 1.0], dtype=float)
for _ in range(20):
    cx, cy, r = p
    f = np.sqrt((xy[:, 0] - cx) ** 2 + (xy[:, 1] - cy) ** 2) - r
    dx, dy = xy[:, 0] - cx, xy[:, 1] - cy
    d = np.sqrt(dx * dx + dy * dy) + 1e-12
    J = np.stack([-dx / d, -dy / d, -np.ones(len(xy))], axis=1)
    dp, *_ = np.linalg.lstsq(J, -f, rcond=None)
    p = p + dp
metrics = {"est": p.tolist(), "true": true.tolist(), "data": "synthetic"}
(out / "metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
print(metrics)

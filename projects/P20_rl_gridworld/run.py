#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
import json
import numpy as np

HERE = Path(__file__).resolve().parent
out = HERE / "output"
out.mkdir(exist_ok=True)
n = 5
goal = (4, 4)
rng = np.random.default_rng(20)
Q = np.zeros((n, n, 4))
acts = [(-1, 0), (1, 0), (0, -1), (0, 1)]
alpha, gamma, eps = 0.3, 0.95, 0.2
for _ in range(2000):
    s = (0, 0)
    for _t in range(50):
        a = int(rng.integers(4)) if rng.random() < eps else int(Q[s].argmax())
        ns = (min(max(s[0] + acts[a][0], 0), n - 1), min(max(s[1] + acts[a][1], 0), n - 1))
        r = 1.0 if ns == goal else -0.01
        Q[s][a] += alpha * (r + gamma * Q[ns].max() * (0.0 if ns == goal else 1.0) - Q[s][a])
        s = ns
        if s == goal:
            break
greedy = 0
s = (0, 0)
for _t in range(20):
    a = int(Q[s].argmax())
    s = (min(max(s[0] + acts[a][0], 0), n - 1), min(max(s[1] + acts[a][1], 0), n - 1))
    greedy += 1
    if s == goal:
        break
metrics = {"greedy_steps_or_cap": greedy, "reached": s == goal, "note": "tabular toy"}
(out / "metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
print(metrics)

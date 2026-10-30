#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
import json
import numpy as np

HERE = Path(__file__).resolve().parent
out = HERE / "output"
out.mkdir(exist_ok=True)
dt, T = 0.001, 2.0
n = int(T / dt)
# plant: omega_dot = -a omega + b u
a, b = 4.0, 20.0
kp, ki, kd = 0.8, 2.0, 0.02
omega = 0.0
integ = 0.0
prev_e = 0.0
ref = 10.0
traj = []
for k in range(n):
    e = ref - omega
    integ += e * dt
    de = (e - prev_e) / dt
    prev_e = e
    u = kp * e + ki * integ + kd * de
    u = float(np.clip(u, -12, 12))
    omega += dt * (-a * omega + b * u)
    traj.append(omega)
traj = np.array(traj)
metrics = {
    "final_omega": float(traj[-1]),
    "overshoot": float(traj.max() / ref - 1.0),
    "note": "Euler simulation only. Not hardware.",
}
(out / "metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
np.save(out / "omega.npy", traj)
print(metrics)

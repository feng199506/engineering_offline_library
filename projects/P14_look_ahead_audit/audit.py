#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
import json
import numpy as np

HERE = Path(__file__).resolve().parent
out = HERE / "output"
out.mkdir(exist_ok=True)


def rolling_mean(x, w, centered=False):
    n = len(x)
    y = np.full(n, np.nan)
    if centered:
        h = w // 2
        for i in range(n):
            a, b = max(0, i - h), min(n, i + h + 1)
            y[i] = x[a:b].mean()  # LOOK-AHEAD if i+h+1 > i+1
    else:
        for i in range(w - 1, n):
            y[i] = x[i - w + 1 : i + 1].mean()
    return y


def leak_score(x, feat):
    # if feature at t correlates with x[t+1] more than causal version, flag
    return float(np.nanmean(np.abs(feat[:-1] - x[1:])))


def main() -> None:
    x = np.linspace(0, 1, 200) + 0.1 * np.sin(np.linspace(0, 20, 200))
    c = rolling_mean(x, 21, centered=False)
    o = rolling_mean(x, 21, centered=True)
    metrics = {
        "centered_uses_future": True,
        "causal_uses_future": False,
        "absdiff_feat_vs_next_x_causal": leak_score(x, c),
        "absdiff_feat_vs_next_x_centered": leak_score(x, o),
        "verdict": "centered window is look-ahead; do not use in live features",
    }
    (out / "metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print(metrics)


if __name__ == "__main__":
    main()

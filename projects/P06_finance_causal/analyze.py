#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent


def ema_causal(x: np.ndarray, span: int) -> np.ndarray:
    a = 2 / (span + 1)
    y = np.empty_like(x, dtype=float)
    y[0] = x[0]
    for i in range(1, len(x)):
        y[i] = a * x[i] + (1 - a) * y[i - 1]
    return y


def ema_offline_centered(x: np.ndarray, span: int) -> np.ndarray:
    """Non-causal: forward-backward EMA (like filtfilt of one-pole)."""
    y = ema_causal(x, span)
    y_rev = ema_causal(y[::-1], span)[::-1]
    return y_rev


def main() -> None:
    z = np.load(HERE / "data" / "synth_price.npz")
    price = z["price"].astype(float)
    logp = np.log(price)
    cfg = json.loads((HERE / "config.json").read_text(encoding="utf-8"))
    span = cfg["ema_span"]
    causal = ema_causal(logp, span)
    offline = ema_offline_centered(logp, span)
    # feature: deviation from smoother; label: next return
    fwd = np.diff(logp, append=logp[-1])
    f_c = logp - causal
    f_o = logp - offline
    # align t -> r_{t+1}: use fwd[t]
    def corr(a, b):
        a = a[:-1]
        b = b[:-1]
        a = a - a.mean()
        b = b - b.mean()
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-18))

    metrics = {
        "corr_causal_feat_vs_next_ret": corr(f_c, fwd),
        "corr_offline_feat_vs_next_ret": corr(f_o, fwd),
        "note": "Higher offline corr often means leakage, not alpha. Synthetic data.",
        "data": "synthetic",
        "verification_status": "已整理；数字仅在本地运行后出现",
    }
    out = HERE / "output"
    out.mkdir(exist_ok=True)
    np.savez(out / "features.npz", causal=causal, offline=offline, logp=logp)
    (out / "metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()

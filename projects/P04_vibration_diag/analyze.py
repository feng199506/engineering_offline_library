#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent


def kurtosis(x: np.ndarray) -> float:
    x = x - np.mean(x)
    m2 = np.mean(x**2) + 1e-18
    m4 = np.mean(x**4)
    return float(m4 / m2**2)


def main() -> None:
    z = np.load(HERE / "data" / "synthetic_bearing.npz")
    x, fs = z["x"], float(z["fs"])
    out = HERE / "output"
    out.mkdir(exist_ok=True)
    # band-pass around carrier then envelope via Hilbert if scipy present
    env = np.abs(x)
    try:
        from scipy.signal import butter, hilbert, sosfiltfilt, welch

        sos = butter(4, [1500 / (fs / 2), 2500 / (fs / 2)], btype="band", output="sos")
        xf = sosfiltfilt(sos, x)
        env = np.abs(hilbert(xf))
        f, pxx = welch(env, fs=fs, nperseg=min(4096, len(env)))
        band = (f > 30) & (f < 50)
        peak = float(f[band][np.argmax(pxx[band])]) if np.any(band) else None
        note = "envelope via Hilbert after bandpass; filtfilt NONCAUSAL"
    except Exception as e:
        f = np.fft.rfftfreq(len(env), 1 / fs)
        pxx = np.abs(np.fft.rfft(env)) ** 2
        peak = None
        note = f"fallback FFT envelope of |x|: {e}"
    metrics = {
        "kurtosis_raw": kurtosis(x),
        "envelope_peak_30_50hz": peak,
        "note": note,
        "verification_status": "已整理，未运行验证" if False else "run-local",
    }
    # keep honest: this script running locally is still not hardware
    metrics["data"] = "synthetic"
    (out / "metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print(metrics)


if __name__ == "__main__":
    main()

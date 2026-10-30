#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Windowed FFT comparison. Not executed in this round."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from _common import try_savefig  # noqa: E402


def mag_db(x: np.ndarray, window: str, m: int) -> tuple[np.ndarray, np.ndarray]:
    try:
        from scipy.signal import get_window
    except Exception:
        wmap = {
            "boxcar": np.ones,
            "hann": np.hanning,
            "hamming": np.hamming,
            "blackman": np.blackman,
        }
        w = wmap[window](len(x))
    else:
        w = get_window(window, len(x), fftbins=True)
    xw = x * w
    n = len(xw)
    spec = np.fft.rfft(xw, n=m)
    mag = 20 * np.log10(np.maximum(np.abs(spec) / np.sum(w) * 2.0, 1e-12))
    freq = np.fft.rfftfreq(m, d=1.0)
    return freq, mag


def main() -> None:
    cfg = json.loads((HERE / "config.json").read_text(encoding="utf-8"))
    fs = float(cfg["fs"])
    m = int(cfg["zero_pad_to"])
    out = HERE / "output"
    out.mkdir(exist_ok=True)
    plt = try_savefig(out / "dummy.png")
    lines = ["# P01 运行记录", "", "verification: 若你看到本文件由 analyze.py 生成，则已在本机运行。", ""]
    for T in cfg["durations_s"]:
        z = np.load(HERE / "data" / f"multitone_{T:.0f}s.npz")
        x = z["x"]
        if plt is not None:
            import matplotlib.pyplot as plt  # noqa

            fig, ax = plt.subplots(figsize=(8, 4))
        for window in cfg["windows"]:
            freq, mag = mag_db(x, window, m)
            freq = freq * fs
            band = (freq >= 5) & (freq <= 15)
            f_peak = float(freq[band][np.argmax(mag[band])])
            lines.append(f"- T={T}s window={window} peak_in_5_15Hz={f_peak:.4f} Hz")
            if plt is not None:
                ax.plot(freq, mag, label=window, linewidth=1)
        if plt is not None:
            ax.set_xlim(0, 60)
            ax.set_xlabel("Hz")
            ax.set_ylabel("dB (window coherent-gain scaled, schematic)")
            ax.set_title(f"P01 duration={T}s (schematic)")
            ax.legend()
            ax.grid(True, alpha=0.3)
            fig.tight_layout()
            fig.savefig(out / f"spectrum_{T:.0f}s.png", dpi=120)
            plt.close(fig)
    (out / "metrics.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("wrote", out)


if __name__ == "__main__":
    main()

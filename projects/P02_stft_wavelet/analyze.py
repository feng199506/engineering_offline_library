#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from _common import try_savefig  # noqa: E402


def main() -> None:
    cfg = json.loads((HERE / "config.json").read_text(encoding="utf-8"))
    z = np.load(HERE / "data" / "chirp_impulse.npz")
    x, fs = z["x"], float(z["fs"])
    out = HERE / "output"
    out.mkdir(exist_ok=True)
    lines = ["# P02 摘要", "", "status: 仅在本机运行后才有实测图", ""]
    try:
        from scipy.signal import stft
    except Exception as e:
        (out / "metrics.md").write_text(f"scipy unavailable: {e}\n", encoding="utf-8")
        return
    plt = try_savefig(out / "x.png")
    for nperseg in cfg["stft_nperseg"]:
        f, tt, zxx = stft(x, fs=fs, nperseg=nperseg, noverlap=nperseg // 2)
        mag = np.abs(zxx)
        lines.append(f"- STFT nperseg={nperseg} shape={mag.shape}")
        if plt is not None:
            import matplotlib.pyplot as plt  # noqa

            fig, ax = plt.subplots(figsize=(8, 3.5))
            ax.pcolormesh(tt, f, mag, shading="auto")
            ax.set_title(f"STFT nperseg={nperseg} (schematic)")
            ax.set_ylabel("Hz")
            ax.set_xlabel("s")
            fig.tight_layout()
            fig.savefig(out / f"stft_{nperseg}.png", dpi=120)
            plt.close(fig)
    try:
        import pywt
    except Exception:
        lines.append("- CWT skipped: pywt not imported (未运行环境)")
    else:
        scales = np.arange(1, 64)
        coef, freqs = pywt.cwt(x, scales, "morl", sampling_period=1.0 / fs)
        lines.append(f"- CWT morlet coef shape={coef.shape}")
        if plt is not None:
            import matplotlib.pyplot as plt  # noqa

            fig, ax = plt.subplots(figsize=(8, 3.5))
            ax.imshow(
                np.abs(coef),
                aspect="auto",
                extent=[0, len(x) / fs, freqs[-1], freqs[0]],
            )
            ax.set_title("CWT morlet (schematic)")
            ax.set_ylabel("Hz (pywt scale map)")
            ax.set_xlabel("s")
            fig.tight_layout()
            fig.savefig(out / "cwt_morlet.png", dpi=120)
            plt.close(fig)
    (out / "metrics.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("wrote", out)


if __name__ == "__main__":
    main()

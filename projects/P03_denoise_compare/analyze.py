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


def snr(clean, est) -> float:
    num = np.sum(clean**2)
    den = np.sum((clean - est) ** 2) + 1e-18
    return float(10 * np.log10(num / den))


def edge_rmse(clean, est, fs) -> float:
    t = np.arange(len(clean)) / fs
    m = (t >= 0.75) & (t <= 0.90)
    return float(np.sqrt(np.mean((clean[m] - est[m]) ** 2)))


def main() -> None:
    z = np.load(HERE / "data" / "block_sine.npz")
    clean, noisy, fs = z["clean"], z["noisy"], float(z["fs"])
    out = HERE / "output"
    out.mkdir(exist_ok=True)
    rows = []

    def rec(name, est, causal):
        rows.append(
            {
                "name": name,
                "causal": causal,
                "snr_db": snr(clean, est),
                "rmse": float(np.sqrt(np.mean((clean - est) ** 2))),
                "edge_rmse": edge_rmse(clean, est, fs),
            }
        )
        return est

    estimates = {"noisy": rec("noisy", noisy, True)}
    try:
        from scipy.signal import butter, filtfilt, lfilter
    except Exception as e:
        (out / "metrics.json").write_text(json.dumps({"error": str(e)}), encoding="utf-8")
        return
    b, a = butter(4, 20 / (fs / 2), btype="low")
    estimates["iir_causal"] = rec("iir_lfilter", lfilter(b, a, noisy), True)
    estimates["iir_filtfilt"] = rec("iir_filtfilt_NONCAUSAL", filtfilt(b, a, noisy), False)
    try:
        import pywt

        w = pywt.Wavelet("db4")
        maxlev = pywt.dwt_max_level(len(noisy), w.dec_len)
        coeffs = pywt.wavedec(noisy, "db4", level=min(4, maxlev))
        sigma = np.median(np.abs(coeffs[-1])) / 0.6745
        thr = sigma * np.sqrt(2 * np.log(len(noisy)))
        recs = [coeffs[0]] + [pywt.threshold(c, thr, "soft") for c in coeffs[1:]]
        estimates["wavelet"] = rec("wavelet_soft", pywt.waverec(recs, "db4")[: len(noisy)], False)
    except Exception:
        rows.append({"name": "wavelet_soft", "causal": False, "snr_db": None, "note": "skipped"})
    try:
        from PyEMD import EMD

        imfs = EMD().emd(noisy, max_imf=6)
        # drop first IMF as "noise" — heuristic, not a law
        est = np.sum(imfs[1:], axis=0) if imfs.shape[0] > 1 else imfs[0]
        estimates["emd"] = rec("emd_drop_imf1_NONCAUSAL", est[: len(noisy)], False)
    except Exception:
        rows.append({"name": "emd", "causal": False, "snr_db": None, "note": "skipped"})

    (out / "metrics.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    plt = try_savefig(out / "cmp.png")
    if plt is not None:
        import matplotlib.pyplot as plt  # noqa

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(clean, label="clean", linewidth=1)
        ax.plot(noisy, label="noisy", alpha=0.4, linewidth=0.6)
        for k, v in estimates.items():
            if k == "noisy":
                continue
            ax.plot(v, label=k, linewidth=1)
        ax.legend(fontsize=8)
        ax.set_title("P03 schematic denoise (not a ranking)")
        fig.tight_layout()
        fig.savefig(out / "cmp.png", dpi=120)
        plt.close(fig)
    print("wrote", out)


if __name__ == "__main__":
    main()

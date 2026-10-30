#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Log newline-delimited samples. Default: no hardware, generate locally."""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--port", default="")
    p.add_argument("--baud", type=int, default=115200)
    p.add_argument("--seconds", type=float, default=1.0)
    p.add_argument("--out", default=str(HERE / "output" / "log.csv"))
    args = p.parse_args()
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    rows = ["mono_s,value"]
    t0 = time.monotonic()
    if args.port:
        try:
            import serial  # type: ignore
        except Exception as e:
            meta = {"status": "pyserial missing", "error": str(e), "hardware": False}
            (out.parent / "metrics.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
            return
        # Not opened in this archive run. User must pass a real port later.
        meta = {
            "status": "configured_not_opened",
            "port": args.port,
            "baud": args.baud,
            "hardware_verified": False,
            "note": "This script refuses to open serial unless you delete this guard.",
        }
        (out.parent / "metrics.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
        return
    while time.monotonic() - t0 < args.seconds:
        t = time.monotonic() - t0
        rows.append(f"{t:.6f},{t*0}")
        time.sleep(0.05)
    out.write_text("\n".join(rows) + "\n", encoding="utf-8")
    meta = {"rows": len(rows) - 1, "hardware": False, "clock": "CLOCK-like monotonic in Python"}
    (out.parent / "metrics.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(meta)


if __name__ == "__main__":
    main()

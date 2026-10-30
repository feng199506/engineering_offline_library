#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
out = HERE / "output"
out.mkdir(exist_ok=True)
# STX v1 = 0xFE, v2 = 0xFD
metrics = {
    "stx_v2": "0xFD",
    "note": "Use pymavlink from host_comms wheelhouse after install. Not installed this round.",
    "hardware": False,
    "vendor_archive": "knowledge/vendor/mavlink-master.tar.gz",
}
(out / "metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
print(metrics)

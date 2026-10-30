#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
import json
import time
import numpy as np

HERE = Path(__file__).resolve().parent
out = HERE / "output"
out.mkdir(exist_ok=True)


class Ring:
    def __init__(self, n):
        self.buf = np.zeros(n)
        self.ts = np.zeros(n)
        self.n = n
        self.w = 0
        self.drops = 0
        self.count = 0

    def push(self, v, t):
        if self.count == self.n:
            self.drops += 1
        else:
            self.count += 1
        self.buf[self.w] = v
        self.ts[self.w] = t
        self.w = (self.w + 1) % self.n

    def pop_block(self, m):
        if self.count < m:
            return None
        # naive: not matching real concurrent index logic
        self.count -= m
        return True


def main() -> None:
    rb = Ring(32)
    t0 = time.monotonic()
    for i in range(80):
        rb.push(i, time.monotonic() - t0)
        if i % 10 == 0:
            rb.pop_block(4)
    metrics = {
        "drops": rb.drops,
        "clock": "time.monotonic (host simulation)",
        "hardware_verified": False,
        "board": "none",
    }
    (out / "metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print(metrics)


if __name__ == "__main__":
    main()

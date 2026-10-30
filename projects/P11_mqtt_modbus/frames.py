#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
import json
import struct

HERE = Path(__file__).resolve().parent
out = HERE / "output"
out.mkdir(exist_ok=True)


def crc16_modbus(data: bytes) -> int:
    crc = 0xFFFF
    for b in data:
        crc ^= b
        for _ in range(8):
            crc = (crc >> 1) ^ 0xA001 if crc & 1 else crc >> 1
    return crc


def main() -> None:
    # Modbus RTU read holding registers addr=1, start=0, qty=2
    pdu = bytes([0x01, 0x03, 0x00, 0x00, 0x00, 0x02])
    crc = crc16_modbus(pdu)
    frame = pdu + struct.pack("<H", crc)
    metrics = {
        "modbus_rtu_hex": frame.hex(),
        "mqtt": "CONNECT binary not sent; see OASIS MQTT 5.0 PDF",
        "hardware": False,
    }
    (out / "metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print(metrics)


if __name__ == "__main__":
    main()

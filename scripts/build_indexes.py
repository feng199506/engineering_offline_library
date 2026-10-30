#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build catalog CSV and checksums from what is actually on disk."""
from __future__ import annotations

import csv
import hashlib
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INV = ROOT / "inventories"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def iter_files(base: Path):
    if not base.exists():
        return
    for p in base.rglob("*"):
        if p.is_file() and p.name not in {".DS_Store"}:
            yield p


def main() -> None:
    INV.mkdir(exist_ok=True)
    rows = []
    for label, rel, release in [
        ("public_original", "_public", "may_publish_if_license_ok"),
        ("vendor_source", "vendor", "may_publish_if_LICENSE_ok"),
        ("local_only", "_local_only", "DO_NOT_PUBLISH"),
        ("html_mirror", "docs_html", "DO_NOT_PUBLISH_default"),
        ("guides", "00_portal", "original_ok"),
        ("projects", "projects", "original_ok"),
    ]:
        base = ROOT / rel
        for p in iter_files(base):
            if p.name.endswith(".part"):
                continue
            st = p.stat()
            rows.append(
                {
                    "class": label,
                    "release": release,
                    "relpath": str(p.relative_to(ROOT)),
                    "bytes": st.st_size,
                    "sha256": sha256_file(p) if st.st_size <= 80 * 1024 * 1024 else "(skip_hash_gt_80MiB)",
                }
            )
    out = INV / "on_disk_files.csv"
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["class", "release", "relpath", "bytes", "sha256"])
        w.writeheader()
        w.writerows(rows)
    # domain coverage stub from download_log
    log = INV / "download_log.csv"
    by_domain = {}
    if log.exists():
        with log.open(newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                by_domain.setdefault(r.get("domain", ""), []).append(r)
    lines = ["domain,downloaded,failed,link_only,bytes_ok"]
    for d, items in sorted(by_domain.items()):
        dl = [i for i in items if i["status"] in {"downloaded", "already"}]
        fail = [i for i in items if i["status"] == "failed"]
        link = [i for i in items if i["status"] in {"link_only", "skipped"}]
        b = sum(int(i.get("bytes") or 0) for i in dl)
        lines.append(f"{d},{len(dl)},{len(fail)},{len(link)},{b}")
    (INV / "by_domain.csv").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("files", len(rows), "wrote", out)


if __name__ == "__main__":
    main()

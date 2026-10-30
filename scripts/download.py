#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Download catalogued materials. Does not install, flash, or deploy."""
from __future__ import annotations

import csv
import hashlib
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from catalog import CATALOG, HTML_MIRRORS  # noqa: E402

UA = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 "
    "OfflineStudyArchive/1.0"
)
LOG = ROOT / "inventories" / "download_log.csv"
TIMEOUT = 600


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def curl_download(url: str, dest: Path) -> tuple[int, str]:
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".part")
    cmd = [
        "curl",
        "-L",
        "--fail",
        "--retry",
        "3",
        "--retry-delay",
        "2",
        "--connect-timeout",
        "20",
        "--max-time",
        str(TIMEOUT),
        "-A",
        UA,
        "-o",
        str(tmp),
        "--",
        url,
    ]
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        if tmp.exists():
            tmp.unlink()
        err = (p.stderr or p.stdout or "")[-500:]
        return p.returncode, err.replace("\n", " ")
    if not tmp.exists() or tmp.stat().st_size == 0:
        if tmp.exists():
            tmp.unlink()
        return 1, "empty file"
    # Reject HTML error pages saved as PDF
    head = tmp.read_bytes()[:200].lower()
    binary_ext = {".pdf", ".zip", ".gz", ".bz2", ".xz", ".tgz"}
    looks_html = head.lstrip().startswith(b"<!doctype html") or head.lstrip().startswith(b"<html")
    if dest.suffix.lower() in binary_ext and looks_html:
        tmp.unlink()
        return 1, "got HTML instead of binary"
    tmp.replace(dest)
    return 0, "ok"


def wget_mirror(item: dict) -> tuple[int, str]:
    dest = ROOT / item["dest"]
    dest.mkdir(parents=True, exist_ok=True)
    cmd = [
        "wget",
        "--quiet",
        "--show-progress",
        "--progress=dot:giga",
        "-k",
        "-E",
        "-p",
        "-np",
        "-nH",
        "--cut-dirs=0",
        f"--accept={item.get('accept', 'html,htm,css,js,png,jpg,gif,svg,pdf')}",
        f"-l{item.get('depth', 1)}",
        "-e",
        "robots=off",
        "-U",
        UA,
        "-P",
        str(dest),
        "--timeout=20",
        "--tries=2",
        item["url"],
    ]
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        return p.returncode, (p.stderr or p.stdout or "")[-400:].replace("\n", " ")
    return 0, "ok"


def main() -> int:
    LOG.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "id",
        "domain",
        "title",
        "lang",
        "kind",
        "license",
        "release_class",
        "url",
        "dest",
        "status",
        "bytes",
        "sha256",
        "detail",
        "utc",
    ]
    rows = []
    existing = {}
    if LOG.exists():
        with LOG.open(newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                existing[r["id"]] = r

    for item in CATALOG:
        iid = item["id"]
        dest_rel = item.get("dest")
        dest = ROOT / dest_rel if dest_rel else None
        rec = {
            "id": iid,
            "domain": item.get("domain", ""),
            "title": item.get("title", ""),
            "lang": item.get("lang", ""),
            "kind": item.get("kind", ""),
            "license": item.get("license", ""),
            "release_class": item.get("release_class", ""),
            "url": item.get("url", ""),
            "dest": dest_rel or "",
            "status": "",
            "bytes": "0",
            "sha256": "",
            "detail": item.get("notes", ""),
            "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }
        if item.get("skip_download") or item.get("release_class") == "link" or not dest_rel:
            rec["status"] = "link_only" if item.get("release_class") == "link" or item.get("skip_download") else "skipped"
            if dest and dest.exists() and dest.stat().st_size > 0:
                rec["status"] = "already"
                rec["bytes"] = str(dest.stat().st_size)
                rec["sha256"] = sha256_file(dest)
            rows.append(rec)
            print(f"[{rec['status']}] {iid}", flush=True)
            continue
        if dest.exists() and dest.stat().st_size > 64:
            rec["status"] = "already"
            rec["bytes"] = str(dest.stat().st_size)
            rec["sha256"] = sha256_file(dest)
            rows.append(rec)
            print(f"[already {rec['bytes']}] {iid}", flush=True)
            continue
        print(f"[fetch] {iid} <- {item['url']}", flush=True)
        code, detail = curl_download(item["url"], dest)
        if code == 0:
            rec["status"] = "downloaded"
            rec["bytes"] = str(dest.stat().st_size)
            rec["sha256"] = sha256_file(dest)
            rec["detail"] = (rec["detail"] + " " + detail).strip()
        else:
            rec["status"] = "failed"
            rec["detail"] = detail[:800]
            print(f"[FAIL] {iid}: {detail[:200]}", flush=True)
        rows.append(rec)

    for item in HTML_MIRRORS:
        dest = ROOT / item["dest"]
        rec = {
            "id": item["id"],
            "domain": item.get("domain", ""),
            "title": item.get("title", ""),
            "lang": "en",
            "kind": "html_mirror",
            "license": "see original site",
            "release_class": item.get("release_class", "local"),
            "url": item["url"],
            "dest": item["dest"],
            "status": "",
            "bytes": "0",
            "sha256": "",
            "detail": "",
            "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }
        if dest.exists() and any(dest.rglob("*")):
            rec["status"] = "already"
            rec["bytes"] = str(sum(p.stat().st_size for p in dest.rglob("*") if p.is_file()))
            rows.append(rec)
            print(f"[already html] {item['id']}", flush=True)
            continue
        print(f"[mirror] {item['id']}", flush=True)
        code, detail = wget_mirror(item)
        rec["status"] = "downloaded" if code == 0 else "failed"
        rec["detail"] = detail[:800]
        if dest.exists():
            rec["bytes"] = str(sum(p.stat().st_size for p in dest.rglob("*") if p.is_file()))
        rows.append(rec)

    with LOG.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    ok = sum(1 for r in rows if r["status"] in {"downloaded", "already"})
    fail = sum(1 for r in rows if r["status"] == "failed")
    link = sum(1 for r in rows if r["status"] in {"link_only", "skipped"})
    print(f"DONE ok={ok} fail={fail} link_or_skip={link} total={len(rows)}", flush=True)
    return 0 if fail < 40 else 1


if __name__ == "__main__":
    raise SystemExit(main())

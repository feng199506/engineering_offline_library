#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Continue legal fetches into /root/engineering_offline_library. No install/flash."""
from __future__ import annotations

import csv
import hashlib
import re
import subprocess
import time
from pathlib import Path

ROOT = Path("/root/engineering_offline_library")
LOG = ROOT / "inventories" / "continue_fetch_log.csv"
UA = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

# dest relative to ROOT, urls, insecure
ITEMS = [
    (
        "vendor/linear-algebra-hefferon-master.tar.gz",
        [
            "https://gitlab.com/jim.hefferon/linear-algebra/-/archive/master/linear-algebra-master.tar.gz",
        ],
        False,
    ),
    (
        "_public/math/hefferon_linear_algebra.pdf",
        [
            "https://jheffero.w3.uvm.edu/linearalgebra/book.pdf",
            "https://www.cs.ox.ac.uk/files/12921/book.pdf",
        ],
        False,
    ),
    (
        "_public/math/hefferon_linear_algebra_answers.pdf",
        ["https://jheffero.w3.uvm.edu/linearalgebra/jhanswer.pdf"],
        False,
    ),
    (
        "_public/math/hefferon_linear_algebra_lab.pdf",
        ["https://jheffero.w3.uvm.edu/linearalgebra/lab.pdf"],
        False,
    ),
    (
        "_public/math/hefferon_linear_algebra_slides.zip",
        ["https://jheffero.w3.uvm.edu/linearalgebra/slides.zip"],
        False,
    ),
    (
        "_local_only/ai/hastie_esl.pdf",
        [
            # Live author PDF currently 404; IA snapshot of the author-posted file (personal use).
            "https://web.archive.org/web/20180928060423id_/https://web.stanford.edu/~hastie/Papers/ESLII.pdf",
        ],
        False,
    ),
    (
        "_local_only/ai/islp_python.pdf",
        [
            "https://drive.google.com/uc?export=download&id=1ajFkHO6zjrdGNqhqW1jKBZdiNGh_8YQ1",
            "https://hastie.su.domains/ISLP/ISLP_website.pdf.download.html",
        ],
        False,
    ),
    (
        "_local_only/ai/islr2.pdf",
        [
            "https://drive.google.com/uc?export=download&id=1--811-yIIvjT3dvnyFJM20rj_-tbB3bg",
        ],
        False,
    ),
    (
        "_local_only/control/tedrake_underactuated.pdf",
        [
            "https://github.com/RussTedrake/underactuated/releases/download/2023-03-24/book.pdf",
            "https://underactuated.mit.edu/underactuated.pdf",
        ],
        False,
    ),
    (
        "_local_only/ai/prince_understanding_deep_learning.pdf",
        [
            "https://github.com/udlbook/udlbook/releases/download/v2.05/UnderstandingDeepLearning_04_18_24_C.pdf",
        ],
        False,
    ),
    (
        "_local_only/ai/UDL_Answer_Booklet_Students.pdf",
        ["https://github.com/udlbook/udlbook/raw/main/UDL_Answer_Booklet_Students.pdf"],
        False,
    ),
    (
        "vendor/cvxbook_additional_exercises-main.tar.gz",
        [
            "https://github.com/cvxgrp/cvxbook_additional_exercises/archive/refs/heads/main.tar.gz",
        ],
        False,
    ),
    (
        "_public/math/numpy-user.pdf",
        ["https://numpy.org/doc/stable/numpy-user.pdf"],
        False,
    ),
    (
        "_local_only/embedded/LFS-BOOK.pdf",
        [
            "https://www.linuxfromscratch.org/lfs/downloads/13.1-systemd/LFS-SYSD-BOOK-13.1.pdf",
            "https://www.linuxfromscratch.org/lfs/downloads/12.3/LFS-BOOK-12.3.pdf",
        ],
        False,
    ),
    (
        "_local_only/embedded/BLFS-BOOK.pdf",
        [
            "https://www.linuxfromscratch.org/blfs/downloads/13.1-systemd/BLFS-SYSD-BOOK-13.1.pdf",
            "https://www.linuxfromscratch.org/blfs/downloads/12.4-systemd/BLFS-SYSD-BOOK-12.4.pdf",
            "https://www.linuxfromscratch.org/blfs/downloads/12.3/BLFS-BOOK-12.3.pdf",
        ],
        False,
    ),
    (
        "vendor/scikit-learn-1.5.2.tar.gz",
        ["https://github.com/scikit-learn/scikit-learn/archive/refs/tags/1.5.2.tar.gz"],
        False,
    ),
    (
        "vendor/pykalman-master.tar.gz",
        ["https://github.com/pykalman/pykalman/archive/refs/heads/master.tar.gz"],
        False,
    ),
    (
        "_public/engineering/progit2-src.tar.gz",
        ["https://github.com/progit/progit2/archive/refs/tags/2.1.441.tar.gz"],
        False,
    ),
    (
        "_local_only/papers/arxiv_1312.6114_vae.pdf",
        ["https://arxiv.org/pdf/1312.6114.pdf"],
        False,
    ),
    (
        "_local_only/papers/arxiv_1502.03167_batchnorm.pdf",
        ["https://arxiv.org/pdf/1502.03167.pdf"],
        False,
    ),
    (
        "_local_only/papers/arxiv_1412.6980_adam.pdf",
        ["https://arxiv.org/pdf/1412.6980.pdf"],
        False,
    ),
    (
        "_local_only/papers/arxiv_1706.03762_attention.pdf",
        ["https://arxiv.org/pdf/1706.03762.pdf"],
        False,
    ),
    (
        "_local_only/papers/arxiv_1512.03385_resnet.pdf",
        ["https://arxiv.org/pdf/1512.03385.pdf"],
        False,
    ),
    (
        "_local_only/papers/arxiv_1203.0734_particle_filter_tutorial.pdf",
        ["https://arxiv.org/pdf/1203.0734.pdf"],
        False,
    ),
    (
        "_local_only/papers/arxiv_1810.04805_bert.pdf",
        ["https://arxiv.org/pdf/1810.04805.pdf"],
        False,
    ),
    (
        "_public/rfcs/rfc7252.txt",
        ["https://www.rfc-editor.org/rfc/rfc7252.txt"],
        False,
    ),
    (
        "_public/rfcs/rfc6455.txt",
        ["https://www.rfc-editor.org/rfc/rfc6455.txt"],
        False,
    ),
    (
        "_public/rfcs/rfc8446.txt",
        ["https://www.rfc-editor.org/rfc/rfc8446.txt"],
        False,
    ),
    (
        "_public/rfcs/rfc8949.txt",
        ["https://www.rfc-editor.org/rfc/rfc8949.txt"],
        False,
    ),
    (
        "_public/specs/amqp-core-complete-v1.0.pdf",
        ["https://docs.oasis-open.org/amqp/core/v1.0/os/amqp-core-complete-v1.0-os.pdf"],
        False,
    ),
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def looks_html(data: bytes) -> bool:
    s = data.lstrip().lower()
    return s.startswith(b"<!doctype") or s.startswith(b"<html") or s.startswith(b"<html")


def gdrive_confirm(tmp: Path) -> str | None:
    text = tmp.read_text(errors="ignore")
    m = re.search(r"confirm=([0-9A-Za-z_]+)", text)
    if m:
        return m.group(1)
    m = re.search(r"name=\"confirm\"\s+value=\"([^\"]+)\"", text)
    if m:
        return m.group(1)
    return None


def fetch(url: str, dest: Path, insecure: bool) -> tuple[bool, str]:
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".part")
    cmd = [
        "curl",
        "-L",
        "--fail",
        "--retry",
        "1",
        "--connect-timeout",
        "15",
        "--max-time",
        "180",
        "-A",
        UA,
        "-o",
        str(tmp),
    ]
    if insecure:
        cmd.append("-k")
    if "drive.google.com" in url:
        cmd += ["-c", str(tmp) + ".cookies", "-b", str(tmp) + ".cookies"]
    cmd += ["--", url]
    p = subprocess.run(cmd, capture_output=True, text=True)
    cookies = Path(str(tmp) + ".cookies")
    if p.returncode != 0 or not tmp.exists() or tmp.stat().st_size < 400:
        err = (p.stderr or "")[-180:].replace("\n", " ")
        if tmp.exists():
            tmp.unlink()
        if cookies.exists():
            cookies.unlink()
        return False, f"rc={p.returncode} {err}"
    head = tmp.read_bytes()[:180]
    if dest.suffix.lower() in {".pdf", ".zip", ".gz", ".tgz"} and looks_html(head):
        confirm = None
        if "drive.google.com" in url:
            confirm = gdrive_confirm(tmp)
        if confirm and "id=" in url:
            fid = re.search(r"id=([^&]+)", url)
            if fid:
                tmp.unlink()
                url2 = (
                    "https://drive.google.com/uc?export=download&confirm="
                    f"{confirm}&id={fid.group(1)}"
                )
                return fetch(url2, dest, insecure)
        tmp.unlink()
        if cookies.exists():
            cookies.unlink()
        return False, "html_not_binary"
    if cookies.exists():
        cookies.unlink()
    tmp.replace(dest)
    return True, "ok"


def wget_page(url: str, dest: Path) -> tuple[bool, str]:
    dest.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "wget",
        "-q",
        "-k",
        "-E",
        "-p",
        "-np",
        "-nH",
        "-l1",
        "-e",
        "robots=off",
        "-U",
        UA,
        "-P",
        str(dest),
        "--timeout=20",
        "--tries=2",
        "--quota=80m",
        url,
    ]
    p = subprocess.run(cmd, capture_output=True, text=True)
    n = sum(1 for _ in dest.rglob("*") if _.is_file()) if dest.exists() else 0
    return (n > 0, f"files={n} rc={p.returncode}")


def main() -> None:
    LOG.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    extras_html = [
        ("docs_html/jos_filters", "https://ccrma.stanford.edu/~jos/filters/filters.html"),
        ("docs_html/jos_sasp", "https://ccrma.stanford.edu/~jos/sasp/sasp.html"),
        ("docs_html/underactuated_html", "https://underactuated.mit.edu/index.html"),
        ("docs_html/python_control", "https://python-control.readthedocs.io/en/0.10.2/"),
        ("docs_html/hefferon_la", "https://hefferon.net/linearalgebra/"),
        ("docs_html/udlbook", "https://udlbook.github.io/udlbook/"),
        ("docs_html/casadi", "https://web.casadi.org/docs/"),
        ("docs_html/esp_idf_get_started", "https://docs.espressif.com/projects/esp-idf/en/latest/esp32/get-started/index.html"),
        ("docs_html/yocto_brief", "https://docs.yoctoproject.org/brief-yoctoprojectqs/index.html"),
    ]

    for dest_rel, urls, insecure in ITEMS:
        dest = ROOT / dest_rel
        rec = {
            "dest": dest_rel,
            "status": "",
            "bytes": "0",
            "sha256": "",
            "url": urls[0] if urls else "",
            "detail": "",
            "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }
        if not urls:
            rec["status"] = "skipped"
            rows.append(rec)
            continue
        if dest.exists() and dest.stat().st_size > 2000:
            rec["status"] = "already"
            rec["bytes"] = str(dest.stat().st_size)
            rec["sha256"] = sha256_file(dest) if dest.stat().st_size < 80 * 1024 * 1024 else "skip_hash"
            print(f"[already] {dest_rel}", flush=True)
            rows.append(rec)
            continue
        ok = False
        last = ""
        for url in urls:
            print(f"[fetch] {dest_rel} <- {url}", flush=True)
            ok, last = fetch(url, dest, insecure)
            if ok:
                rec["status"] = "downloaded"
                rec["bytes"] = str(dest.stat().st_size)
                rec["url"] = url
                rec["sha256"] = sha256_file(dest) if dest.stat().st_size < 80 * 1024 * 1024 else "skip_hash"
                rec["detail"] = last
                print(f"  ok {dest.stat().st_size}", flush=True)
                break
            print(f"  fail {last[:160]}", flush=True)
        if not ok:
            rec["status"] = "failed"
            rec["detail"] = last[:500]
        rows.append(rec)

    for dest_rel, url in extras_html:
        dest = ROOT / dest_rel
        rec = {
            "dest": dest_rel,
            "status": "",
            "bytes": "0",
            "sha256": "",
            "url": url,
            "detail": "",
            "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }
        if dest.exists() and any(dest.rglob("*")):
            rec["status"] = "already"
            rec["bytes"] = str(sum(p.stat().st_size for p in dest.rglob("*") if p.is_file()))
            print(f"[already html] {dest_rel}", flush=True)
            rows.append(rec)
            continue
        print(f"[mirror] {dest_rel}", flush=True)
        ok, detail = wget_page(url, dest)
        rec["status"] = "downloaded" if ok else "failed"
        rec["detail"] = detail
        if dest.exists():
            rec["bytes"] = str(sum(p.stat().st_size for p in dest.rglob("*") if p.is_file()))
        rows.append(rec)

    with LOG.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["dest", "status", "bytes", "sha256", "url", "detail", "utc"])
        w.writeheader()
        w.writerows(rows)
    c = {}
    for r in rows:
        c[r["status"]] = c.get(r["status"], 0) + 1
    print("DONE", c, flush=True)


if __name__ == "__main__":
    main()

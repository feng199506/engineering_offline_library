#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Retry high-value failures with alternate URLs / insecure TLS when cert is the only issue."""
from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
LOG = ROOT / "inventories" / "retry_log.txt"

RETRIES = [
    # (urls, dest, insecure)
    (
        [
            "https://joshua.smcvt.edu/linearalgebra/book.pdf",
            "https://hefferon.net/linearalgebra/LinearAlgebra.pdf",
        ],
        "_public/math/hefferon_linear_algebra.pdf",
        False,
    ),
    (
        ["https://joshua.smcvt.edu/linearalgebra/jhanswer.pdf"],
        "_public/math/hefferon_linear_algebra_answers.pdf",
        False,
    ),
    (
        [
            "https://web.stanford.edu/~boyd/cvxbook/bv_cvxbook_extra_exercises.pdf",
            "https://stanford.edu/~boyd/cvxbook/bv_cvxbook_extra_exercises.pdf",
        ],
        "_local_only/math/boyd_cvx_additional_exercises.pdf",
        False,
    ),
    (
        [
            "https://www.cds.caltech.edu/~murray/books/AM08/pdf/fbs-public_24Jul2020.pdf",
            "https://fbswiki.org/wiki/index.php/Main_Page",
        ],
        "_local_only/control/astrom_murray_feedback_systems.pdf",
        True,
    ),
    (
        ["https://www.cds.caltech.edu/~murray/books/MLS/pdf/mls94-complete.pdf"],
        "_local_only/control/murray_li_sastry_robotic_manipulation.pdf",
        True,
    ),
    (
        [
            "https://underactuated.csail.mit.edu/underactuated.pdf",
            "https://underactuated.mit.edu/underactuated.pdf",
        ],
        "_local_only/control/tedrake_underactuated.pdf",
        False,
    ),
    (
        [
            "https://hastie.su.domains/Papers/ESLII.pdf",
            "https://hastie.su.domains/ElemStatLearn/printings/ESLII_print12.pdf",
        ],
        "_local_only/ai/hastie_esl.pdf",
        False,
    ),
    (
        [
            "https://www.statlearning.com/s/ISLP_python.pdf",
            "https://www.statlearning.com/s/ISLP.pdf",
        ],
        "_local_only/ai/islp_python.pdf",
        False,
    ),
    (
        [
            "https://github.com/udlbook/udlbook/releases/download/v4.01/UnderstandingDeepLearning_04_01_24_C.pdf",
            "https://udlbook.github.io/udlbook/UDLBook_2024_02_12.pdf",
        ],
        "_local_only/ai/prince_understanding_deep_learning.pdf",
        False,
    ),
    (
        [
            "https://web.stanford.edu/~jurafsky/slp3/ed3book.pdf",
            "https://web.stanford.edu/~jurafsky/slp3/ed3book_jan2023.pdf",
        ],
        "_local_only/ai/jurafsky_martin_slp3_draft.pdf",
        False,
    ),
    (
        ["https://www.cs.ucl.ac.uk/staff/d.barber/brml/brml-pdf.zip"],
        "_local_only/ai/barber_brml.zip",
        True,
    ),
    (
        [
            "https://greenteapress.com/wp/wp-content/uploads/2021/09/thinkbayes.pdf",
            "https://greenteapress.com/thinkbayes/thinkbayes.pdf",
        ],
        "_local_only/math/downey_thinkbayes.pdf",
        False,
    ),
    (
        [
            "https://docs.octave.org/octave.pdf",
            "https://docs.octave.org/v9.4.0/octave.pdf",
            "https://docs.octave.org/v8.4.0/octave.pdf",
        ],
        "_public/math/octave-manual.pdf",
        False,
    ),
    (
        [
            "https://docs.scipy.org/doc/scipy/scipy-ref.pdf",
            "https://docs.scipy.org/doc/scipy-1.13.1/scipy-ref.pdf",
        ],
        "_public/signal/scipy-ref.pdf",
        False,
    ),
    (
        [
            "https://modbus.org/docs/Modbus_Application_Protocol_V1_1b3.pdf",
            "https://www.modbus.org/docs/Modbus_Application_Protocol_V1_1b3.pdf",
        ],
        "_local_only/embedded/Modbus_Application_Protocol_V1_1b3.pdf",
        True,
    ),
    (
        ["https://www.modbus.org/docs/Modbus_over_serial_line_V1_02.pdf"],
        "_local_only/embedded/Modbus_over_serial_line_V1_02.pdf",
        True,
    ),
    (
        ["https://www.modbus.org/docs/Modbus_Messaging_Implementation_Guide_V1_0b.pdf"],
        "_local_only/embedded/Modbus_Messaging_Implementation_Guide_V1_0b.pdf",
        True,
    ),
    (
        [
            "https://www.linuxfromscratch.org/lfs/downloads/12.2/LFS-BOOK-12.2.pdf",
            "https://www.linuxfromscratch.org/lfs/downloads/stable-systemd/LFS-BOOK.pdf",
        ],
        "_local_only/embedded/LFS-BOOK.pdf",
        False,
    ),
    (
        ["https://ntrs.nasa.gov/api/citations/20040182410/downloads/20040182410.pdf"],
        "_local_only/papers/nasa_huang_hht.pdf",
        False,
    ),
    (
        ["https://github.com/lballabio/QuantLib-SWIG/archive/refs/heads/master.tar.gz"],
        "vendor/QuantLib-SWIG-master.tar.gz",
        False,
    ),
    (
        ["https://ccrma.stanford.edu/~jos/mdft/"],
        None,
        False,
    ),
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch(url: str, dest: Path, insecure: bool) -> bool:
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".part")
    cmd = [
        "curl",
        "-L",
        "--fail",
        "--retry",
        "2",
        "--connect-timeout",
        "20",
        "--max-time",
        "180",
        "-A",
        UA,
        "-o",
        str(tmp),
    ]
    if insecure:
        cmd.append("-k")
    cmd += ["--", url]
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0 or not tmp.exists() or tmp.stat().st_size < 1000:
        if tmp.exists():
            tmp.unlink()
        print(f"  fail {url} rc={p.returncode} {(p.stderr or '')[-120:]}")
        return False
    head = tmp.read_bytes()[:80].lower().lstrip()
    looks_html = head.startswith(b"<!doctype") or head.startswith(b"<html")
    if dest.suffix.lower() in {".pdf", ".zip", ".gz"} and looks_html:
        tmp.unlink()
        print(f"  html {url}")
        return False
    tmp.replace(dest)
    print(f"  ok {dest.name} {dest.stat().st_size}")
    return True


def mirror_jos() -> None:
    dest = ROOT / "docs_html" / "jos_mdft"
    dest.mkdir(parents=True, exist_ok=True)
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
        "https://ccrma.stanford.edu/~jos/mdft/mdft.html",
    ]
    subprocess.run(cmd)
    print("jos mirror files", sum(1 for _ in dest.rglob("*")))


def dspguide() -> None:
    dest_dir = ROOT / "_local_only" / "signal" / "dspguide"
    dest_dir.mkdir(parents=True, exist_ok=True)
    ok = 0
    for i in range(1, 35):
        dest = dest_dir / f"CH{i}.PDF"
        if dest.exists() and dest.stat().st_size > 1000:
            ok += 1
            continue
        for url in (
            f"https://www.dspguide.com/CH{i}.PDF",
            f"https://dspguide.com/CH{i}.PDF",
            f"http://www.dspguide.com/pdfbook{i}.htm",
        ):
            if url.endswith(".htm"):
                continue
            if fetch(url, dest, True):
                ok += 1
                break
    print("dspguide chapters ok", ok)
    # html book
    html = ROOT / "docs_html" / "dspguide"
    html.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
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
            str(html),
            "--timeout=20",
            "https://www.dspguide.com/pdfbook.htm",
        ]
    )


def main() -> None:
    LOG.write_text("", encoding="utf-8")
    for urls, dest_rel, insecure in RETRIES:
        if dest_rel is None:
            continue
        dest = ROOT / dest_rel
        if dest.exists() and dest.stat().st_size > 2000:
            print("skip existing", dest_rel)
            continue
        print("try", dest_rel)
        for url in urls:
            if dest.suffix.lower() not in {".pdf", ".zip", ".gz", ".txt"}:
                continue
            if fetch(url, dest, insecure):
                LOG.write_text(LOG.read_text(encoding="utf-8") + f"OK {dest_rel} {url}\n", encoding="utf-8")
                break
        else:
            LOG.write_text(LOG.read_text(encoding="utf-8") + f"FAIL {dest_rel}\n", encoding="utf-8")
    dspguide()
    mirror_jos()
    # extra arxiv teaching papers (local)
    extras = [
        ("https://arxiv.org/pdf/1703.01898.pdf", "_local_only/papers/arxiv_1703.01898_wavelet_overview.pdf"),
        ("https://arxiv.org/pdf/0912.2437.pdf", "_local_only/papers/arxiv_0912.2437.pdf"),
        ("https://arxiv.org/pdf/1506.03099.pdf", "_local_only/papers/arxiv_1506.03099.pdf"),
    ]
    for url, rel in extras:
        dest = ROOT / rel
        if dest.exists() and dest.stat().st_size > 1000:
            continue
        fetch(url, dest, False)


if __name__ == "__main__":
    main()

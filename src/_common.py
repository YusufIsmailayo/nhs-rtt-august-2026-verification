"""Shared helpers for the August 2026 RTT / Cancer Waiting Times verification.

I copy the RTT measure rules from Two Maps verbatim rather than inventing new
ones, because the whole point of this pipeline is that its figures line up with
the RTT pieces I have already published. If a rule here ever differs from
~/Two_maps/src/pipeline/_common.py, that is a measure change and it has to be
written up, not slipped in.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from datetime import date, datetime, timezone
from pathlib import Path

import requests

REPO_ROOT = Path(__file__).resolve().parents[1]
BRONZE_DIR = REPO_ROOT / "data" / "bronze"
SILVER_DIR = REPO_ROOT / "data" / "silver"
GOLD_DIR = REPO_ROOT / "data" / "gold"


# ------------------------------------------------------- the reporting month
#
# The month a run rebuilds is set here and nowhere else. Every notebook takes
# its file names, its comparison months and its labels from these values, so
# moving to a new month changes no analysis logic. The published August 2026
# article was built with "2026-08" (git tag august-2026-published). The
# environment variable overrides the default for a one-off run, which is how I
# prove the August outputs still reproduce exactly after this change.

#: The reporting month, "YYYY-MM".
REPORT_MONTH = os.environ.get("RTT_REPORT_MONTH", "2026-09")
assert re.fullmatch(r"20\d\d-(0[1-9]|1[0-2])", REPORT_MONTH), REPORT_MONTH

#: First month of every series (April 2025). An analysis anchor, not a setting:
#: it stays put whichever month is being reported.
FIRST_MONTH = "2025-04"


def shift_month(period: str, k: int) -> str:
    """'2026-09' shifted by k months, e.g. shift_month('2026-09', -12) -> '2025-09'."""
    y, m = map(int, period.split("-"))
    n = y * 12 + (m - 1) + k
    return f"{n // 12:04d}-{n % 12 + 1:02d}"


def months_from(start: str, end: str) -> list[str]:
    """Every month from start to end inclusive, as 'YYYY-MM'."""
    out, p = [], start
    while p <= end:
        out.append(p)
        p = shift_month(p, 1)
    return out


PREV_MONTH = shift_month(REPORT_MONTH, -1)
YEAR_AGO_MONTH = shift_month(REPORT_MONTH, -12)
SERIES_MONTHS = months_from(FIRST_MONTH, REPORT_MONTH)


def _first_day(period: str) -> date:
    y, m = map(int, period.split("-"))
    return date(y, m, 1)


# Labels in the forms NHS England uses in its file names and wording.
def mon_yy(period: str) -> str:      # 'Sep26'
    return _first_day(period).strftime("%b%y")


def mon(period: str) -> str:         # 'Sep'
    return _first_day(period).strftime("%b")


def mon_year(period: str) -> str:    # 'Sep 2026'
    return _first_day(period).strftime("%b %Y")


def month_name(period: str) -> str:  # 'September'
    return _first_day(period).strftime("%B")


def month_year(period: str) -> str:  # 'September 2026'
    return _first_day(period).strftime("%B %Y")


def bronze_file(pattern: str) -> Path:
    """The single Bronze file matching a glob under data/bronze.

    NHS England's file names carry random suffixes and change wording between
    releases, so I find each file by a pattern built from the month labels
    rather than typing its name. More or fewer than one match is an error: a
    pattern that quietly picked the wrong vintage would defeat the point.
    """
    hits = sorted(BRONZE_DIR.glob(pattern))
    assert len(hits) == 1, f"expected one Bronze file for {pattern!r}, found {[str(h.relative_to(BRONZE_DIR)) for h in hits]}"
    return hits[0]


#: The year-ago cancer month as FIRST published (provisional), for like-for-like
#: year-on-year comparison: (Bronze folder, layout). NHS England changed the
#: file layout in November 2025, so August 2025 is one CSV per standard and
#: September 2025 is the Combined CSV every later month uses.
YEAR_AGO_CWT_PROVISIONAL = {
    "2025-08": ("nhse_cwt_2025-08_provisional", "old_layout"),
    "2025-09": ("nhse_cwt_2025-09_provisional", "combined_csv"),
}

#: Two Maps' Bronze, which already holds April-July 2026 RTT extracts. I reuse
#: those bytes only when the SHA-256 matches what Two Maps recorded.
TWO_MAPS_BRONZE = Path.home() / "Two_maps" / "data" / "bronze"

USER_AGENT = "rtt-aug26-verification/0.1"


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def download(url: str, dest: Path, timeout: int = 600) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".part")
    with requests.get(url, stream=True, timeout=timeout, headers={"User-Agent": USER_AGENT}) as r:
        r.raise_for_status()
        with tmp.open("wb") as f:
            for chunk in r.iter_content(1 << 20):
                f.write(chunk)
    # I only rename once the whole payload has landed, so a dropped connection
    # can never leave a truncated file sitting in Bronze looking complete.
    tmp.rename(dest)
    return dest


def remote_size(url: str) -> int | None:
    """Content-Length the server reports for `url`, or None if it won't say."""
    r = requests.head(url, allow_redirects=True, timeout=60, headers={"User-Agent": USER_AGENT})
    r.raise_for_status()
    n = r.headers.get("Content-Length")
    return int(n) if n else None


def write_metadata(folder: Path, **fields) -> None:
    fields["written_at_utc"] = now_utc()
    (folder / "metadata.json").write_text(json.dumps(fields, indent=2))


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


# ---------------------------------------------------------------- RTT quirks
# Copied from Two Maps. Same rules, same reasons.

#: Commissioner code in the RTT full extract for activity with no identified
#: commissioner. NHS England's published Incomplete Provider workbook excludes
#: these rows. July 2026: 7,162,692 pathways with them, 7,131,685 without, and
#: the workbook says 7,131,685. I keep them in Bronze and drop them in Silver.
RTT_UNIDENTIFIED_COMMISSIONER = "NONC"

#: (old code, surviving code, first period the survivor carries the old trust).
#: North Bristol (RVJ) merged into Bristol NHS FT (RA7) on 1 July 2026.
#: Any further merger I find in the 2025-26 months goes here, dated, with the
#: evidence written next to it.
TRUST_SUCCESSIONS = [
    ("RVJ", "RA7", "2026-07"),
]

#: The two numbers that tie this pipeline to Two Maps. If my July 2026 rebuild
#: does not land on these exactly, I am not using the same measure.
TWO_MAPS_JUL26_TOTAL = 7_131_685
TWO_MAPS_JUL26_OVER_52 = 108_263


def apply_trust_successions(codes, period: str):
    """Map superseded trust codes to their successor, for one period."""
    mapping = {old: new for old, new, eff in TRUST_SUCCESSIONS if period >= eff}
    return codes.replace(mapping) if mapping else codes

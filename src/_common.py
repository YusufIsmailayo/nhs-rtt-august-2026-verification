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
from datetime import datetime, timezone
from pathlib import Path

import requests

REPO_ROOT = Path(__file__).resolve().parents[1]
BRONZE_DIR = REPO_ROOT / "data" / "bronze"
SILVER_DIR = REPO_ROOT / "data" / "silver"
GOLD_DIR = REPO_ROOT / "data" / "gold"

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

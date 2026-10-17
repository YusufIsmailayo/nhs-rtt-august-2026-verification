"""The claims under test, exactly as the secondary sources state them.

These are not inputs. Nothing in Silver or Gold reads a number from here;
they exist only so the gate can put each one next to what the primary files
say. Sources: BMA, 'NHS backlog data analysis' (8 Oct 2026), compiled from the
August 2026 RTT and Cancer Waiting Times releases; Healthcare Management,
'NHS waiting list rises fourth time in five months'.
"""

from __future__ import annotations

CLAIMS = [
    # (key, claimed value, unit, wording as quoted, source)
    ("rtt_incomplete_pathways", 7_370_000, "pathways", "7.37 million pathways", "BMA / Healthcare Management"),
    ("rtt_unique_patients", 6_240_000, "patients", "6.24 million patients", "BMA / Healthcare Management"),
    ("rtt_change_on_july", 41_848, "pathways", "up 41,848 on July", "Healthcare Management"),
    ("rtt_over_52_weeks", 113_000, "pathways", "~113,000 waiting more than a year", "BMA"),
    ("rtt_over_52_change", 7_000, "pathways", "+7,000 over 52 weeks (article title)", "article brief"),
    ("rtt_over_52_pct_change", 6.0, "%", "over-52-week group grew by roughly six per cent", "article brief"),
    ("rtt_total_pct_change", 1.0, "% (upper bound)", "list grew by well under one per cent", "article brief"),
    ("rtt_median_weeks", 12.2, "weeks", "median wait 12.2 weeks", "BMA"),
    ("cwt_62d_pct", 71.9, "%", "62-day performance 71.9 per cent", "BMA"),
    ("cwt_fds_pct", 78.6, "%", "28-day faster diagnosis 78.6 per cent", "BMA"),
]

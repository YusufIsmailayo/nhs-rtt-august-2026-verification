"""The source catalogue: every file this pipeline reads, and where it came from.

Every URL here I copied off NHS England's own statistical work area pages on
16 October 2026, with the browser open on the page. None of them come from the
BMA compilation or from Healthcare Management. Those two are the claims under
test, not sources.

NHS England puts random suffixes on its file URLs (…-vjgRdG.zip) and rotates
them when it revises a month. If one of these 404s, the file has moved: find
the month on the page named in `source_page` and update the URL here. The
SHA-256 in each metadata.json tells you whether you got the same bytes I did.
"""

from __future__ import annotations

NHSE = "https://www.england.nhs.uk/statistics/wp-content/uploads/sites/2"
RTT_2026_27 = "https://www.england.nhs.uk/statistics/statistical-work-areas/rtt-waiting-times/rtt-data-2026-27/"
RTT_2025_26 = "https://www.england.nhs.uk/statistics/statistical-work-areas/rtt-waiting-times/rtt-data-2025-26/"
CWT_MAIN = "https://www.england.nhs.uk/statistics/statistical-work-areas/cancer-waiting-times/"
CWT_2026_27 = "https://www.england.nhs.uk/statistics/2026-27-monthly-cancer-waiting-times-statistics/"

# ----------------------------------------------------------------------------
# RTT full CSV extracts, April 2025 - August 2026 (17 months).
# (period, URL, vintage note). The vintage comes from the 2025-26 page's
# revisions paragraph and from the upload folder in the URL. I use the latest
# vintage of every month, because that is what NHS England now says the month
# was. A revised month is a different number from the one first published.
# ----------------------------------------------------------------------------
RTT_FULL_CSV = [
    ("2025-04", f"{NHSE}/2026/02/Full-CSV-data-file-Apr25-ZIP-4M-revised.zip", "revised 12 Feb 2026"),
    ("2025-05", f"{NHSE}/2026/02/Full-CSV-data-file-May25-ZIP-4M-revised.zip", "revised 12 Feb 2026"),
    ("2025-06", f"{NHSE}/2026/02/Full-CSV-data-file-Jun25-ZIP-4M-revised.zip", "revised 12 Feb 2026"),
    ("2025-07", f"{NHSE}/2026/02/Full-CSV-data-file-Jul25-ZIP-4M-revised-2.zip", "revised 13 Nov 2025, again 12 Feb 2026"),
    ("2025-08", f"{NHSE}/2026/02/Full-CSV-data-file-Aug25-ZIP-4M-revised-2.zip", "revised 13 Nov 2025, again 12 Feb 2026"),
    ("2025-09", f"{NHSE}/2026/02/Full-CSV-data-file-Sep25-ZIP-4M-revised.zip", "revised 12 Feb 2026"),
    ("2025-10", f"{NHSE}/2025/12/Full-CSV-data-file-Oct25-ZIP-4M-SrRW6y.zip", "as first published"),
    ("2025-11", f"{NHSE}/2026/01/Full-CSV-data-file-Nov25-ZIP-4M-1Xmjkk.zip", "as first published"),
    ("2025-12", f"{NHSE}/2026/07/Full-CSV-data-file-Dec25-ZIP-3M-revised.zip", "revised 9 Jul 2026"),
    ("2026-01", f"{NHSE}/2026/03/Full-CSV-data-file-Jan26-ZIP-4M-WL5BiP.zip", "as first published"),
    ("2026-02", f"{NHSE}/2026/04/Full-CSV-data-file-Feb26-ZIP-4M-9j03fJT.zip", "as first published"),
    ("2026-03", f"{NHSE}/2026/07/Full-CSV-data-file-Mar26-ZIP-3M-revised.zip", "revised 9 Jul 2026"),
    ("2026-04", f"{NHSE}/2026/06/Full-CSV-data-file-Apr26-ZIP-3M-X7gGnn.zip", "as first published"),
    ("2026-05", f"{NHSE}/2026/07/Full-CSV-data-file-May26-ZIP-3M-3jBgba.zip", "as first published"),
    ("2026-06", f"{NHSE}/2026/08/Full-CSV-data-file-Jun26-ZIP-3M-6jPlxd.zip", "as first published"),
    ("2026-07", f"{NHSE}/2026/09/Full-CSV-data-file-Jul26-ZIP-4M-97ylx5.zip", "as first published"),
    ("2026-08", f"{NHSE}/2026/10/Full-CSV-data-file-Aug26-ZIP-3M-vjgRdG.zip", "as first published"),
]

SOURCES: list[dict] = []

for _period, _url, _vintage in RTT_FULL_CSV:
    SOURCES.append({
        "slug": f"nhse_rtt_{_period}",
        "publisher": "NHS England",
        "publication_name": f"Consultant-led Referral to Treatment Waiting Times - full CSV extract, {_period}",
        "source_page": RTT_2025_26 if _period < "2026-04" else RTT_2026_27,
        "vintage": _vintage,
        "files": [(_url.rsplit("/", 1)[-1], _url,
                   "Full extract: provider x commissioner x RTT part x treatment function x weekly wait bands (0-104+).")],
        "grain": "provider x commissioner x RTT part x treatment function",
        "primary": True,
        # Two Maps already holds April-July 2026 at these exact URLs.
        "reuse_from": f"nhse_rtt_{_period}" if "2026-04" <= _period <= "2026-07" else None,
    })

# ----------------------------------------------------------------------------
# Superseded vintages. NHS England revised December 2025 and March 2026 on
# 9 July 2026, and the 2025-26 page now links only the revised files. I found
# the original links on the Wayback Machine's copy of that page (snapshot
# 23 June 2026), but the files themselves still come from england.nhs.uk. I
# use them ONLY to measure what the revision changed. They never enter the
# Silver series, which always takes the latest vintage. The slug deliberately
# doesn't match the `nhse_rtt_YYYY-MM` pattern 02_silver_rtt globs for.
# ----------------------------------------------------------------------------
RTT_SUPERSEDED = [
    ("2025-12", f"{NHSE}/2026/02/Full-CSV-data-file-Dec25-ZIP-4M-6jPlxd.zip", "original, published Feb 2026; superseded 9 Jul 2026"),
    ("2026-03", f"{NHSE}/2026/05/Full-CSV-data-file-Mar26-ZIP-4M-Dc1i9U.zip", "original, published 14 May 2026; superseded 9 Jul 2026"),
]
for _period, _url, _vintage in RTT_SUPERSEDED:
    SOURCES.append({
        "slug": f"nhse_rtt_superseded_{_period}",
        "publisher": "NHS England",
        "publication_name": f"RTT full CSV extract, {_period} - ORIGINAL vintage (superseded)",
        "source_page": "https://web.archive.org/web/20260623114021/" + RTT_2025_26,
        "vintage": _vintage,
        "files": [(_url.rsplit("/", 1)[-1], _url,
                   "Superseded vintage, kept only to measure the July 2026 revision. Not used in any series.")],
        "grain": "provider x commissioner x RTT part x treatment function",
        "primary": True,
        "reuse_from": None,
    })

SOURCES += [
    {
        "slug": "nhse_rtt_published_2026-08",
        "publisher": "NHS England",
        "publication_name": "RTT Waiting Times, August 2026 - published workbooks and statistical press notice",
        "source_page": RTT_2026_27,
        "vintage": "as first published",
        "files": [
            ("Aug26-RTT-statistical-press-notice-PDF-389K-vjgRdG.pdf",
             f"{NHSE}/2026/10/Aug26-RTT-statistical-press-notice-PDF-389K-vjgRdG.pdf",
             "Statistical press notice: NHS England's own headline wording and figures (the gate's 'published headline')."),
            ("Incomplete-Provider-Aug26-XLSX-9M-vjgRdG.xlsx",
             f"{NHSE}/2026/10/Incomplete-Provider-Aug26-XLSX-9M-vjgRdG.xlsx",
             "Published provider-level incomplete pathways. Gate A target: my rebuild must match this provider by provider."),
            ("Incomplete-Provider-Jul26-XLSX-9M-97ylx5.xlsx",
             f"{NHSE}/2026/09/Incomplete-Provider-Jul26-XLSX-9M-97ylx5.xlsx",
             "July provider workbook: the Two Maps gate target, re-checked here so the two pipelines share one measure."),
            ("RTT-Overview-Timeseries-Including-Estimates-for-Missing-Trusts-Aug26-XLS-139K-vjgRdG.xlsx",
             f"{NHSE}/2026/10/RTT-Overview-Timeseries-Including-Estimates-for-Missing-Trusts-Aug26-XLS-139K-vjgRdG.xlsx",
             "England headline series, including NHS England's estimates for trusts that did not submit."),
            ("Missing-data-adjustments-to-Aug26-XLSX-109K-vjgRdG.xlsx",
             f"{NHSE}/2026/10/Missing-data-adjustments-to-Aug26-XLSX-109K-vjgRdG.xlsx",
             "The bridge between reported-provider totals and the headline: which trusts were estimated, and by how much."),
        ],
        "grain": "England / provider; headline and adjustments",
        "primary": True,
        "reuse_from": None,
    },
    {
        "slug": "nhse_wlmds_2026-08",
        "publisher": "NHS England",
        "publication_name": "Waiting List Minimum Data Set (WLMDS) summary, to 30 August 2026",
        "source_page": "https://www.england.nhs.uk/statistics/statistical-work-areas/rtt-waiting-times/wlmds/",
        "vintage": "management information (NHS England: 'should be treated with caution')",
        "files": [
            ("WLMDS-Summary-to-30-August-2026.xlsx",
             f"{NHSE}/2026/10/WLMDS-Summary-to-30-August-2026.xlsx",
             "Weekly patient-level collection, summarised: the source of the unique-patients-to-pathways ratio the RTT release applies."),
        ],
        "grain": "England / provider / treatment function x week ending",
        "primary": True,
        "reuse_from": None,
    },
    {
        "slug": "nhse_cwt_2026-08",
        "publisher": "NHS England",
        "publication_name": "Cancer Waiting Times, August 2026 (Provisional), released 8 October 2026",
        "source_page": CWT_2026_27,
        "vintage": "provisional",
        "files": [
            ("Cancer-Waiting-Times-Statistical-Release-August-2026-Provider-based-Provisional.pdf",
             f"{NHSE}/2026/10/Cancer-Waiting-Times-Statistical-Release-August-2026-Provider-based-Provisional.pdf",
             "Statistical release: NHS England's own headline for 62-day and 28-day FDS performance."),
            ("August-2026-Monthly-Combined-CSV-Provisional.csv",
             f"{NHSE}/2026/10/August-2026-Monthly-Combined-CSV-Provisional.csv",
             "Single-month Combined CSV: provider + commissioner x standard x cancer type x route x modality."),
            ("2026-27-Apr-Aug-Cumulative-Monthly-Combined-CSV-Provisional.csv",
             f"{NHSE}/2026/10/2026-27-Apr-Aug-Cumulative-Monthly-Combined-CSV-Provisional.csv",
             "April-August 2026 Combined CSV, same schema. Lets me check the single-month file against the cumulative one."),
            ("CWT-CRS-National-Time-Series-Oct-2009-Aug-2026-Provisional.xlsx",
             f"{NHSE}/2026/10/CWT-CRS-National-Time-Series-Oct-2009-Aug-2026-Provisional.xlsx",
             "NHS England's published national series: the second, independent target for the gate."),
        ],
        "grain": "basis (provider/commissioner) x org x standard x cancer type x route x modality x month",
        "primary": True,
        "reuse_from": None,
    },
    {
        # August 2025 as FIRST published (provisional, 9 Oct 2025), so year on
        # year can be compared like for like: provisional against provisional.
        # These are in the pre-November-2025 layout (one CSV per standard). The
        # page's "Monthly CSV" link is a format illustration NHS England says not
        # to analyse, so I deliberately don't take it.
        "slug": "nhse_cwt_2025-08_provisional",
        "publisher": "NHS England",
        "publication_name": "Cancer Waiting Times, August 2025 (Provisional), released 9 October 2025",
        "source_page": "https://www.england.nhs.uk/statistics/statistical-work-areas/cancer-waiting-times/monthly-data-and-summaries/2025-26-monthly-cancer-waiting-times-statistics/cancer-waiting-times-for-august-2025-26-provisional/",
        "vintage": "provisional (superseded by the 2025-26 Final file)",
        "files": [
            ("Cancer-Waiting-Times-Statistical-Release-August-2025-Provider-based-Provisional.pdf",
             f"{NHSE}/2025/10/Cancer-Waiting-Times-Statistical-Release-August-2025-Provider-based-Provisional.pdf",
             "Statistical release for August 2025 as first published."),
            ("2.-28-Day-Faster-Diagnosis-All-Routes-Provider-Data.csv",
             f"{NHSE}/2025/10/2.-28-Day-Faster-Diagnosis-All-Routes-Provider-Data.csv",
             "FDS, all routes, provider data, August 2025 provisional (old layout)."),
            ("7.-62-Day-Combined-All-Cancers-Provider-Data.csv",
             f"{NHSE}/2025/10/7.-62-Day-Combined-All-Cancers-Provider-Data.csv",
             "62-day combined, all cancers, provider data, August 2025 provisional (old layout)."),
        ],
        "grain": "provider x standard (all cancers / all routes)",
        "primary": True,
        "reuse_from": None,
    },
    {
        "slug": "nhse_cwt_2025-26",
        "publisher": "NHS England",
        "publication_name": "Cancer Waiting Times 2025-26, Apr-Mar Monthly Combined CSV (Final)",
        "source_page": CWT_MAIN,
        "vintage": "final",
        "files": [
            ("2025-26-Apr-Mar-Cumulative-Monthly-Combined-CSV-Final.csv",
             f"{NHSE}/2026/10/2025-26-Apr-Mar-Cumulative-Monthly-Combined-CSV-Final.csv",
             "Final 2025-26 months. Needed only for August 2025, so 'improved year on year' is tested rather than quoted."),
        ],
        "grain": "as above",
        "primary": True,
        "reuse_from": None,
    },
]

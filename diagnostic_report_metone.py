#!/usr/bin/env python3
"""
Week 5 Operational Diagnostics Report
Nairobi Throughput Shortfall — Root Cause & Recommendations
Prepared by Stanley Metone

This is a report-backed Python summary based on the supplied Week 5 PDF.
It does NOT recreate the underlying 2,920-row production analysis because
the raw dataset was not included with the PDF.

Run:
    python week5_diagnostics_report_stanley_metone.py
    python week5_diagnostics_report_stanley_metone.py --format markdown
    python week5_diagnostics_report_stanley_metone.py --format json
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from typing import Dict, List


@dataclass(frozen=True)
class Recommendation:
    number: int
    action: str
    why_it_matters: str


REPORT_META: Dict[str, object] = {
    "title": "Operational Diagnostics Report",
    "subtitle": "Nairobi Throughput Shortfall — Root Cause & Recommendations",
    "prepared_by": "Stanley Metone",
    "week": 5,
    "year": 2026,
    "records_reviewed": 2920,
    "machines": 13,
    "depots": 4,
    "expected_daily_throughput_barrels": {
        "low": 950,
        "high": 1050,
    },
}

ROOT_CAUSE = {
    "depot": "Nairobi",
    "machine_id": "NBI-P03",
    "issue_start": "February 2026",
    "missed_maintenance_rate": "over 90% of operating days since February",
    "throughput_when_maintenance_missed_barrels": 625,
    "healthy_throughput_barrels": "approximately 990–1,000",
    "shortfall_percent": 37,
    "estimated_2026_lost_barrels": 194_000,
    "share_of_incident_driven_losses": "approximately 88%",
}

CORRELATIONS = {
    "ambient_temperature_vs_throughput": 0.25,
    "voltage_vs_throughput": 0.04,
    "skipped_maintenance_vs_throughput": -0.85,
}

OPERATOR_EVIDENCE = {
    "operators_rostered_on_nbi_p03": 5,
    "missed_maintenance_rate_range": "92–95%",
    "interpretation": (
        "Rates are nearly identical across all five operators, supporting a "
        "machine/process issue rather than a single-operator issue."
    ),
}

ALTERNATIVE_EXPLANATIONS = [
    {
        "factor": "Weather / ambient temperature",
        "finding": (
            "Ambient temperature has only a weak relationship with throughput "
            "(correlation 0.25)."
        ),
        "ruled_out": True,
    },
    {
        "factor": "Power supply / voltage",
        "finding": (
            "Voltage has essentially no relationship with throughput "
            "(correlation 0.04)."
        ),
        "ruled_out": True,
    },
    {
        "factor": "One careless operator",
        "finding": (
            "All five operators assigned to NBI-P03 show similar missed-maintenance "
            "rates of 92–95%."
        ),
        "ruled_out": True,
    },
    {
        "factor": "Skipped maintenance",
        "finding": (
            "Skipped maintenance has a strong negative relationship with throughput "
            "(correlation -0.85), the strongest relationship reported."
        ),
        "ruled_out": False,
    },
]

RECOMMENDATIONS: List[Recommendation] = [
    Recommendation(
        number=1,
        action=(
            "Audit and reset NBI-P03's maintenance schedule this month. "
            "Assign a named owner accountable for sign-off after every service "
            "window, not just the technician on shift."
        ),
        why_it_matters=(
            "The failure is chronic and machine-specific, not a one-off skip. "
            "It needs a hard reset, not a reminder."
        ),
    ),
    Recommendation(
        number=2,
        action=(
            "Add a simple weekly maintenance-compliance report per machine "
            "(percentage of scheduled services completed on time), reviewed at "
            "the depot level."
        ),
        why_it_matters=(
            "The failure ran undetected for more than 10 months. A lightweight "
            "recurring check could have caught it in weeks rather than at year-end."
        ),
    ),
    Recommendation(
        number=3,
        action=(
            "Once NBI-P03 is back on schedule, re-baseline its expected throughput "
            "and monitor it for 60 days to confirm output returns to approximately "
            "990–1,000 barrels per day."
        ),
        why_it_matters=(
            "This confirms the fix worked and provides early warning if the issue recurs."
        ),
    ),
]

BOTTOM_LINE = (
    "The report identifies a fixable, process-level issue on one asset: NBI-P03. "
    "Weather, power, and individual operators were ruled out as the primary cause. "
    "Restoring maintenance discipline on NBI-P03 is the highest-leverage action "
    "recommended for the quarter."
)


def build_report_dict() -> Dict[str, object]:
    """Return the complete report summary as a JSON-serializable dictionary."""
    return {
        "report_meta": REPORT_META,
        "root_cause": ROOT_CAUSE,
        "correlations": CORRELATIONS,
        "operator_evidence": OPERATOR_EVIDENCE,
        "alternative_explanations": ALTERNATIVE_EXPLANATIONS,
        "recommendations": [asdict(item) for item in RECOMMENDATIONS],
        "bottom_line": BOTTOM_LINE,
        "source_note": (
            "This script summarizes the supplied PDF only. Exact raw-record "
            "reproduction requires the original production dataset."
        ),
    }


def as_text() -> str:
    """Build a readable terminal version of the report."""
    lines = [
        REPORT_META["title"],
        REPORT_META["subtitle"],
        f"Prepared by {REPORT_META['prepared_by']} | Week {REPORT_META['week']}",
        "",
        "CONTEXT",
        (
            f"The report reviewed {REPORT_META['records_reviewed']:,} daily records "
            f"covering {REPORT_META['machines']} machines across "
            f"{REPORT_META['depots']} depots."
        ),
        (
            "Expected daily throughput is "
            f"{REPORT_META['expected_daily_throughput_barrels']['low']:,}–"
            f"{REPORT_META['expected_daily_throughput_barrels']['high']:,} barrels."
        ),
        "",
        "ROOT CAUSE",
        (
            f"{ROOT_CAUSE['machine_id']} in {ROOT_CAUSE['depot']} is the identified "
            f"problem machine. Since {ROOT_CAUSE['issue_start']}, it has missed "
            f"scheduled maintenance on {ROOT_CAUSE['missed_maintenance_rate']}."
        ),
        (
            f"On missed-maintenance days, throughput falls to roughly "
            f"{ROOT_CAUSE['throughput_when_maintenance_missed_barrels']:,} barrels "
            f"from a healthy {ROOT_CAUSE['healthy_throughput_barrels']} barrels, "
            f"a {ROOT_CAUSE['shortfall_percent']}% shortfall."
        ),
        (
            f"Estimated 2026 production loss: "
            f"{ROOT_CAUSE['estimated_2026_lost_barrels']:,} barrels."
        ),
        "",
        "CORRELATIONS",
        (
            "Ambient temperature vs throughput: "
            f"{CORRELATIONS['ambient_temperature_vs_throughput']:.2f}"
        ),
        (
            "Voltage vs throughput: "
            f"{CORRELATIONS['voltage_vs_throughput']:.2f}"
        ),
        (
            "Skipped maintenance vs throughput: "
            f"{CORRELATIONS['skipped_maintenance_vs_throughput']:.2f}"
        ),
        "",
        "RECOMMENDATIONS",
    ]

    for rec in RECOMMENDATIONS:
        lines.extend(
            [
                f"{rec.number}. {rec.action}",
                f"   Why it matters: {rec.why_it_matters}",
            ]
        )

    lines.extend(["", "BOTTOM LINE", BOTTOM_LINE])
    return "\n".join(lines)


def as_markdown() -> str:
    """Build a GitHub-friendly Markdown version of the report."""
    low = REPORT_META["expected_daily_throughput_barrels"]["low"]
    high = REPORT_META["expected_daily_throughput_barrels"]["high"]

    lines = [
        f"# {REPORT_META['title']}",
        "",
        f"**{REPORT_META['subtitle']}**",
        "",
        (
            f"Prepared by **{REPORT_META['prepared_by']}** | "
            f"Week **{REPORT_META['week']}**"
        ),
        "",
        "## Context",
        "",
        (
            f"The report reviewed **{REPORT_META['records_reviewed']:,} daily records** "
            f"covering **{REPORT_META['machines']} machines** across "
            f"**{REPORT_META['depots']} depots**. Expected daily throughput is "
            f"**{low:,}–{high:,} barrels**."
        ),
        "",
        "## Root cause",
        "",
        (
            f"- Problem machine: **{ROOT_CAUSE['machine_id']}** "
            f"({ROOT_CAUSE['depot']})"
        ),
        f"- Issue begins: **{ROOT_CAUSE['issue_start']}**",
        f"- Missed maintenance: **{ROOT_CAUSE['missed_maintenance_rate']}**",
        (
            f"- Throughput on missed-maintenance days: "
            f"**~{ROOT_CAUSE['throughput_when_maintenance_missed_barrels']:,} barrels**"
        ),
        f"- Healthy output: **{ROOT_CAUSE['healthy_throughput_barrels']} barrels/day**",
        f"- Shortfall: **{ROOT_CAUSE['shortfall_percent']}%**",
        (
            f"- Estimated 2026 lost production: "
            f"**~{ROOT_CAUSE['estimated_2026_lost_barrels']:,} barrels**"
        ),
        (
            f"- Share of incident-driven losses: "
            f"**{ROOT_CAUSE['share_of_incident_driven_losses']}**"
        ),
        "",
        "## Evidence",
        "",
        "| Relationship | Correlation |",
        "|---|---:|",
        (
            "| Ambient temperature vs throughput | "
            f"{CORRELATIONS['ambient_temperature_vs_throughput']:.2f} |"
        ),
        (
            "| Voltage vs throughput | "
            f"{CORRELATIONS['voltage_vs_throughput']:.2f} |"
        ),
        (
            "| Skipped maintenance vs throughput | "
            f"{CORRELATIONS['skipped_maintenance_vs_throughput']:.2f} |"
        ),
        "",
        (
            f"All {OPERATOR_EVIDENCE['operators_rostered_on_nbi_p03']} operators "
            f"rostered on NBI-P03 show missed-maintenance rates of "
            f"**{OPERATOR_EVIDENCE['missed_maintenance_rate_range']}**, supporting "
            "a process/machine issue rather than an individual-operator issue."
        ),
        "",
        "## Recommendations",
        "",
    ]

    for rec in RECOMMENDATIONS:
        lines.extend(
            [
                f"### {rec.number}. Recommendation",
                "",
                rec.action,
                "",
                f"**Why it matters:** {rec.why_it_matters}",
                "",
            ]
        )

    lines.extend(
        [
            "## Bottom line",
            "",
            BOTTOM_LINE,
            "",
            "> Source note: this Python file summarizes the supplied Week 5 PDF. "
            "The raw production dataset was not included, so the original row-level "
            "analysis and charts are not recomputed here.",
        ]
    )

    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Print the Week 5 Nairobi throughput diagnostics report."
    )
    parser.add_argument(
        "--format",
        choices=("text", "markdown", "json"),
        default="text",
        help="Output format (default: text).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.format == "json":
        print(json.dumps(build_report_dict(), indent=2))
    elif args.format == "markdown":
        print(as_markdown())
    else:
        print(as_text())


if __name__ == "__main__":
    main()

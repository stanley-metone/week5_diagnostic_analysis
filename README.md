# Week 5: Operational Diagnostics Report & Stakeholder Defense

**Author:** Stanley Metone
**Pod:** Oil & Gas
**Dataset:** `Mystery_Ops.csv` — 2,920 daily production records across 4 depots (Mombasa, Kisumu, Nairobi, Eldoret), 13 machines, 2 shifts, full year 2026.

## TL;DR — The Finding

Nairobi's throughput has been inconsistent all year. The root cause is a single machine, **NBI-P03**, which has skipped scheduled maintenance on 90%+ of its operating days since **February 2026**. On affected days its output falls from a healthy ~990–1,000 barrels/day to ~625 barrels/day (a 37% shortfall). This one machine accounts for **~88% of all incident-driven throughput loss company-wide** in 2026 (~194,000 barrels).

Weather (r ≈ 0.25) and voltage/power supply (r ≈ 0.04) were ruled out as drivers. The issue is not operator-specific — all five operators rostered on NBI-P03 show nearly identical missed-maintenance rates (92–95%), pointing to a broken scheduling/asset-management process rather than individual error.

## Repo Contents

| File | Description |
|---|---|
| `week5_diagnostics_analysis.ipynb` | Full technical notebook: data profiling, univariate/bivariate analysis, IQR-based anomaly detection, drill-down (depot → machine → month), Pareto analysis, and correlation analysis. Includes 7 publication-quality charts (Seaborn/Matplotlib). |
| `Week5_Diagnostics_Report_Stanley Metone.pdf` | 2-page director-facing report: context, root-cause insight, and 3 actionable recommendations. |
| `Week5_Presentation_Stanley Metone.mp4` | 5–7 minute video presentation of the findings, including a simulated skeptical-Director Q&A segment. |
| `Week5_Presentation_Script.md` | Speaking script/outline used to record the video. |
| `pod_feedback.md` | Summary of feedback received during the peer pod "Sceptical Director" role-play, and how the argument was refined in response. |
| `hackathon_reflection.md` | ~200-word reflection on Hackathon #1: biggest technical hurdle, how it was resolved, and teamwork takeaways for next time. |

## How to Reproduce

```bash
# Clone the repo
git clone <this-repo-url>
cd <this-repo>

# Install dependencies
pip install pandas numpy matplotlib seaborn plotly jupyter

# Run the notebook
jupyter nbconvert --to notebook --execute --inplace week5_diagnostics_analysis.ipynb
```

The notebook reads `Mystery_Ops.csv` from the repo root — make sure the dataset is present alongside the notebook before running.

## Methodology Summary

1. **Data Profiling** — shape, dtypes, missing-value audit, summary statistics, and distribution plots for all numeric/categorical fields.
2. **Anomaly Detection** — IQR-based outlier flagging on throughput, visualized with box plots and a temperature-vs-throughput scatter colored by incident type.
3. **Root Cause / Drill-Down** — cross-tabs of incident type by depot, machine, and month isolate the problem to NBI-P03 in Nairobi, starting February 2026.
4. **Pareto Analysis** — quantifies missed maintenance as ~88% of total incident-driven barrel loss, versus equipment faults and operator errors combined.
5. **Correlation Analysis** — confirms maintenance flag (r ≈ -0.85) as the dominant driver, ruling out temperature and voltage/power supply.

## Recommendations (from the report)

1. Audit and reset NBI-P03's maintenance schedule immediately, with a named owner accountable for sign-off.
2. Add a weekly maintenance-compliance report per machine, reviewed at the depot level, to catch future lapses within weeks rather than a year.
3. Re-baseline NBI-P03's expected throughput once maintenance resumes and monitor for 60 days to confirm recovery.

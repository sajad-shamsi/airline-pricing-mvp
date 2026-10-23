# Airline Pricing Decision Support MVP

> **Status (23 Oct 2026):** Research-driven **scenario prototype** with BTS fare analysis, manual-demand assumptions, a capacity-capped pricing optimizer, and a Streamlit dashboard. **Not a trained revenue optimization product or deployed airline pricing system.**

## Mission and users
Provide route/flight Revenue Management (RM) analysts a **human-approved fare recommendation** supported by transparent historical context, demand assumptions, capacity constraints, and explainable revenue scenarios. Pilot focus: **single-leg/nonstop passenger flights**. **Revenue**, not profit, is the current objective; another workstream may later provide costs.

## What exists now
- BTS DB1C June 2026 data acquired and inspected via DuckDB/Pandas: Ticket **13,822,006 sampled records**, 39 columns, 65 reporting carrier codes; Market **57 columns**.
- Prepared American Airlines **ORD → LGA** nonstop market: **14,035 filtered historical records**; median market amount excluding taxes **$169.76**.
- Source scripts in `src/` for carrier/purchase-window/market EDA, `prepare_market.py`, `demand.py` and `optimizer.py`.
- `demand.py`: **isoelastic scenario** `Q(P)=Q0*(P/P0)**epsilon`, not a learned future-booking predictor.
- `optimizer.py`: compare **candidate fares ±20% of reference fare, at 5% increments**, with expected sales `min(demand, remaining_seats)`, rank by modeled *remaining-seat* revenue. These policy bounds are **illustrative**, not verified regulations.
- `app.py` Streamlit dashboard, initial `tests/` unit tests, `src/sensitivity_analysis.py` scenario experiment; Git and GitHub versioning.

## Architecture: target versus current implementation

| Area | Current MVP | Target / depends on airline data |
|---|---|---|
| Historical fare context | BTS Market Parquet | Airline sales/booking and fare-offer histories |
| Baseline demand | Manual `Q0` | Flight-level pickup forecast, then Lasso/other benchmarks |
| Price response | Assumed `epsilon` | Calibrated/causal price response; IV only if valid |
| Lost demand | Not implemented | Censoring detection and PD/EM where identifiable |
| Capacity | Manual seats + hard cap | Live inventory; EMSR when fare-class demand supports it |
| Risk/uncertainty | Basic input sensitivity | Forecast intervals + shock scenarios + expert input/audit |
| Optimization | Grid search | Feasible policy and risk-aware evaluation |
| Action | Human-readable suggestion | Human approval → later authorized airline-system publishing |

Two conceptual pipelines:

1. **Offline research/training:** authorized flight/booking/inventory data → clean/features/censoring → forecast & price-response estimation separately → chronological validation + versioned artifacts.
2. **Decision-time inference:** current flight state + policy + risk flags → demand, elasticity & optionally seat opportunity value → feasible optimizer → safety validation → human approval → outcome recording and feedback.

Our current Python MVP is only a **subset** of the second pipeline. View the architecture draft at `docs/architecture/airline_rm_architecture.html` (planned components in that HTML **are not implemented**).

## Stack and local setup
Windows / WSL2 **Ubuntu 24.04**, Python **3.12** in project-local `.venv`, **DuckDB**, Pandas, Parquet, Streamlit, `unittest`, Git/GitHub.

From the Linux project root (`~/projects/airline-pricing-mvp`):

```bash
source .venv/bin/activate                  # existing environment
python -m pip install -r requirements.txt # if environment needs packages
python src/prepare_market.py              # needs data/raw BTS Market Parquet
python -m unittest discover -s tests -v   # check actual tests; result not preclaimed
python -m src.optimizer                   # interactive command-line experiment
python -m src.sensitivity_analysis        # if present
python -m streamlit run app.py            # dashboard, http://localhost:8501
```

Raw data should be placed (downloaded from official BTS sources) under `data/raw/` with files:
`DB1C.MARKET.202606.16SEP2026.parquet` and `DB1C.TICKET.202606.16SEP2026.parquet`. Large Parquet files and `.venv` **are not tracked by Git**. Check `src/prepare_market.py` for its exact input and generated column names; do not infer missing file paths. No PII should be committed.

## How to reproduce the current example
Reference offered fare **$170**, assumed remaining future bookings **60**, assumed elasticity **−1.2**, remaining seats **45**. The price-grid recommendation from the existing example is **$204** and modeled future revenue **$9,180**. This is an **illustrative scenario**, not measured airline revenue gain. A BTS historical median is *not* a live offered fare and does not identify true demand.

## Documentation — only three maintained Markdown files
- **`README.md` (here)**: first read, how to run, architecture and status.
- **`docs/research_and_findings.md`**: all five reviewed studies, caveats, research-backed methods and backlog; scientific source of truth.
- **`docs/devlog.md`**: time-ordered verified engineering activity, Git milestones and next step.

Other assets go under `docs/architecture/` (HTML diagram); do not maintain duplicate research files. If current code disagrees with prose, **inspect code/tests** and update the docs. Do not silently change production policies based on examples in a paper.

## Immediate next milestone
1. Verify `git status`, tests and dashboard locally.
2. Agree on a privacy-safe **flight/day data contract** with Skytech advisors; request a pilot route's timestamped bookings, offered fares, inventory/fare closure snapshots and flight operation status, preferably 12+ months if available.
3. Benchmark historical pickup against Lasso using **time-based holdout**. Add PD/EM and dynamic price response only when valid raw data support them.
4. Consider Iran-specific crisis scenario gating **without** publishing fares for cancelled/suspended flights.

**Key validation rule:** academic revenue-lift numbers from Fan, Wang and Almasi/Bagherian are **not** projected Skytech results. Compare to the airline's *existing* policy using common, documented evaluation conditions.

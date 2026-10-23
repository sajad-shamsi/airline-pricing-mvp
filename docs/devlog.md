# Development Log — Airline Pricing MVP

> Chronological engineering record. Entries marked **reported** are based on terminal output provided by the developer; execution must be independently rechecked on the current machine. New activities go at the bottom, never rewrite history to make the project appear more mature.

## 2026-10-18 — Initial development checkpoint

### Research
- Studied airline RM architecture, demand forecasting, price elasticity, demand unconstraining, EMSR and numerical revenue optimization.
- Chose a **single-leg/nonstop, recommendation-only MVP** so the first working prototype would be achievable without full network RM integration.
- Four foundation papers: Fan (2026), Wang (2025), Mumbower (2014), Belobaba (2016). See `research_and_findings.md` for precise claims and page references.

### Environment
- Installed **WSL2 / Ubuntu 24.04** on Windows and opened project with VS Code WSL.
- Confirmed Python 3.12 and created/activated `.venv`.
- Installed DuckDB and Pandas in the local virtual environment.

### Data engineering
- Downloaded BTS DB1C **Ticket** and **Market** June 2026 Parquet data (large raw files excluded from Git).
- Inspected 39 Ticket and 57 Market fields.
- BTS Ticket sample: **13,822,006 records**, 65 reporting carriers; identified missing amount and tax-only records; checked unusually low and high fares.
- Analyzed purchase windows, carriers, market directions and nonstop/coupon conditions.
- Script `src/prepare_market.py` filtered **AA ORD→LGA nonstop**, saved `data/processed/aa_ord_lga_nonstop.parquet` with **14,035 records**, median ex-tax market amount **$169.76**. Processed rows are **sampled ticket records**, not distinct flights.

## 2026-10-20 — Scenario pricing MVP and reproducibility
- Wrote `src/demand.py`: assumed isoelastic response; demonstration at $150/$170/$190 relative to $170 and Q0=60.
- Wrote `src/optimizer.py`: capacity-limited pricing scenarios, **±20% / 5%-increment grid**; demo: $170 reference, Q0=60, epsilon −1.2, 45 seats ⇒ $204 recommended; modeled remaining-seat revenue $9,180, +20% *modeled scenario* versus reference.
- Added `src/__init__.py`, `app.py` Streamlit interface, and `tests/test_pricing.py` initial unit tests (do not claim green tests unless output confirmed).
- Git milestones reported: `50b559b` (`feat: establish BTS data analysis and preparation pipeline`) and `e4b223c` (`feat: add interactive pricing dashboard and model tests`), pushed to GitHub `origin/main` at the time.
- Added README and initial research/devlog documentation.
- **Not implemented:** trained booking demand prediction, causal fare elasticity, EM/PD, EMSR, cost optimization or external publishing.

## 2026-10-23 — Elasticity sensitivity and research consolidation
- Developer ran `python -m src.sensitivity_analysis` (reported success):

| Assumed elasticity | Recommended fare | Modeled remaining-seat revenue |
|---:|---:|---:|
| -0.6 | $204.00 | $9,180.00 |
| -1.0 | $204.00 | $9,180.00 |
| -1.2 | $204.00 | $9,180.00 |
| -1.5 | $204.00 | $9,180.00 |
| -2.0 | $195.50 | $8,797.50 |

- Reviewed all pages of four foundational papers (46 pages); documented limitations and recommended distinct forecast, price-response and optimization responsibilities.
- Reviewed **Almasi & Bagherian (2025), 28-page uncertain-programming paper** for Iranian volatility/data-scarcity applications. Proposal: crisis-sensitive operational gating, expert-elicitation audit and later risk-scenario comparison, **not a premature implementation of its formulas**.
- Reviewed uploaded **two-pipeline HTML architecture**. Appropriate as target architecture; requires mathematical and status-label corrections before presentation as implementation.
- Selected documentation convention: exactly three living Markdown docs (`README.md`, `docs/research_and_findings.md`, `docs/devlog.md`), with interactive HTML under `docs/architecture/`.

## Current next-step checkpoint
**First action:** copy this documentation pack into the local Git repo **only after backing up existing files and reviewing the diff**. Then run existing unit tests and dashboard (if accessible). Next research-engineering deliverable is a one-route **flight/day booking + inventory + offer-price data contract**; request CEO authorization for permitted, privacy-safe data access. Do not upload nonpublic airline data to GitHub or external AI services without clearance.

### Suggested verification commands
```bash
cd ~/projects/airline-pricing-mvp
git status --short
source .venv/bin/activate
python -m unittest discover -s tests -v
python -m src.sensitivity_analysis
python -m streamlit run app.py
```
After documentation review: `git add README.md docs/research_and_findings.md docs/devlog.md docs/architecture/airline_rm_architecture.html`, `git diff --cached --stat`, `git commit -m "docs: consolidate five-paper research and RM architecture"`, `git push origin main`.

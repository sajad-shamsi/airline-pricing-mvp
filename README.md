# Airline Pricing Decision Support MVP

A research-driven airline revenue management prototype
for evaluating ticket pricing decisions using historical
market data, demand scenarios, and capacity constraints.

## Project Objective

Develop a decision-support system that recommends ticket
prices to maximize expected remaining-seat revenue.

The MVP focuses on nonstop, single-leg flights.
Recommendations require human review.

## Technology Stack

- Python 3.12
- Ubuntu 24.04 / WSL 2
- DuckDB and Pandas
- Apache Parquet
- Streamlit
- Git and GitHub
- Python unittest

## Data Sources

US Bureau of Transportation Statistics (BTS)
DB1C Origin & Destination Survey, June 2026.

Ticket dataset:
- 13,822,006 sampled records
- 39 columns
- 65 reporting carrier codes

Market dataset:
- 57 columns
- Market origins, destinations, carriers, and fares

Selected analytical market:
- American Airlines (AA)
- Chicago O'Hare (ORD) to New York LaGuardia (LGA)
- Nonstop, single-leg journeys
- 14,035 filtered records
- Median market amount excluding taxes: $169.76

Raw and processed datasets are excluded from Git.

## Current Architecture

1. Historical data acquisition
2. Exploratory Data Analysis (EDA)
3. Data quality assessment and filtering
4. Market-level data preparation
5. Constant-elasticity demand scenario modeling
6. Capacity-constrained revenue optimization
7. Pricing recommendation dashboard

## Pricing Engine

The demand model uses a constant-elasticity equation:

    Q(p) = Q0 * (p / p0) ** elasticity

The optimizer:
- Tests candidate prices from -20% to +20% of the reference fare
- Uses 5% price increments
- Estimates demand at each candidate price
- Limits expected sales to remaining seat capacity
- Calculates expected remaining-seat revenue
- Selects the candidate with the highest expected revenue

## Project Structure

    airline-pricing-mvp/
    ├── app.py
    ├── src/
    │   ├── demand.py
    │   ├── optimizer.py
    │   ├── prepare_market.py
    │   └── analyze_markets.py
    ├── data/
    │   ├── raw/
    │   └── processed/
    ├── tests/
    ├── docs/
    │   └── devlog.md
    └── requirements.txt

## Running the MVP

Activate the virtual environment:

    source .venv/bin/activate

Install dependencies:

    python -m pip install -r requirements.txt

Prepare the selected market dataset:

    python src/prepare_market.py

Run automated tests:

    python -m unittest discover -s tests -v

Run the command-line optimizer:

    python -m src.optimizer

Launch the dashboard:

    python -m streamlit run app.py

The dashboard is available locally at:

    http://localhost:8501

## Current Limitations

This is a scenario-based prototype, not a validated
production demand forecasting system.

- Baseline future demand is currently assumed.
- Price elasticity is currently assumed.
- Available seats and current fare are manual inputs.
- Historical BTS data provides market fare benchmarks.
- Flight-level booking histories are not yet integrated.
- Demand unconstraining is not yet implemented.
- Revenue improvements are simulated, not realized.
- Operating costs are not yet included.

## Next Milestones

1. Validate and test the existing MVP.
2. Integrate actual airline booking and inventory data.
3. Implement demand unconstraining where supported.
4. Develop and validate demand forecasting models.
5. Estimate price elasticity using appropriate data.
6. Improve revenue optimization and business guardrails.
7. Integrate operating costs for profit optimization.
8. Prepare for airline system integration.

## Development History

See docs/devlog.md for research, development milestones,
engineering decisions, and implementation progress.

# Airline Pricing Decision Support MVP

A Python-based airline revenue management prototype
for analyzing historical fares and recommending ticket
prices under demand and capacity assumptions.

## Tech Stack
- Python 3.12
- DuckDB and Pandas
- Parquet
- Ubuntu 24.04 / WSL 2

## Data
BTS DB1C Ticket and Market datasets, June 2026.

## Current Progress
- Historical data exploration
- Data quality assessment
- Purchase-window and airline analysis
- Nonstop market data preparation
- AA ORD-LGA: 14,035 filtered records

## Next Milestones
- Demand scenario modeling
- Revenue optimization
- Interactive dashboard
- Model validation and CEO demonstration

## Limitations
Historical ticket samples do not contain complete
flight-level booking or inventory histories.
Initial pricing recommendations will use explicit
demand and elasticity assumptions.
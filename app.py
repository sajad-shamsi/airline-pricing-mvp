
from pathlib import Path

import duckdb
import pandas as pd
import streamlit as st

from src.demand import estimate_demand
from src.optimizer import optimize_price


DATA_FILE = (
    Path(__file__).resolve().parent
    / "data/processed/aa_ord_lga_nonstop.parquet"
)

st.set_page_config(
    page_title="Airline Pricing Agent",
    page_icon="✈️",
    layout="wide",
)


@st.cache_data
def load_market_summary(path: str):
    """Read a historical market summary only when needed."""
    with duckdb.connect() as con:
        return con.execute("""
            SELECT
                COUNT(*) AS records,
                MEDIAN(fare_ex_tax) AS median_fare
            FROM read_parquet(?)
        """, [path]).fetchone()


st.title("Airline Pricing Agent")
st.caption("Revenue Management MVP | Single-leg flights | June 2026 BTS data")

if not DATA_FILE.is_file():
    st.error("Processed dataset missing. Run: python src/prepare_market.py")
    st.stop()

records, historical_median = load_market_summary(str(DATA_FILE))

st.subheader("Historical Market Reference")

a, b, c = st.columns(3)
a.metric("Market", "ORD → LGA")
b.metric("Sampled records", f"{records:,}")
c.metric("Historical median fare", f"${historical_median:,.2f}")

st.caption(
    "American Airlines nonstop O&D records. "
    "Historical market amounts exclude reported taxes."
)

st.divider()
st.subheader("Future Flight Pricing Scenario")

st.sidebar.header("Scenario Inputs")
st.sidebar.caption("These values are assumptions, not BTS observations.")

current_price = st.sidebar.number_input(
    "Current offered fare ($)",
    min_value=1.0,
    value=170.0,
    step=5.0,
)

baseline_demand = st.sidebar.number_input(
    "Expected future bookings at current fare",
    min_value=0.0,
    value=60.0,
    step=5.0,
)

elasticity = st.sidebar.slider(
    "Assumed price elasticity",
    min_value=-3.0,
    max_value=0.0,
    value=-1.2,
    step=0.1,
)

remaining_seats = st.sidebar.number_input(
    "Remaining seats",
    min_value=1,
    max_value=500,
    value=45,
    step=1,
)

best = optimize_price(
    current_price=current_price,
    baseline_demand=baseline_demand,
    elasticity=elasticity,
    remaining_seats=remaining_seats,
)

baseline_sales = min(baseline_demand, remaining_seats)
baseline_revenue = current_price * baseline_sales

uplift = (
    (best["revenue"] / baseline_revenue - 1) * 100
    if baseline_revenue > 0
    else 0.0
)

a, b, c, d = st.columns(4)
a.metric("Current fare", f"${current_price:,.2f}")
b.metric("Recommended fare", f"${best['price']:,.2f}")
c.metric("Expected seats sold", f"{best['sales']:.1f}")
d.metric("Scenario revenue change", f"{uplift:+.1f}%")

st.write(
    f"Expected remaining-seat revenue: **${best['revenue']:,.2f}** "
    f"versus **${baseline_revenue:,.2f}** at the current fare."
)

st.subheader("Candidate Price Comparison")

rows = []
for change_pct in range(-20, 21, 5):
    price = round(current_price * (1 + change_pct / 100), 2)

    demand = estimate_demand(
        current_price,
        price,
        baseline_demand,
        elasticity,
    )

    sales = min(demand, remaining_seats)

    rows.append({
        "Fare ($)": price,
        "Expected Demand": round(demand, 1),
        "Expected Sales": round(sales, 1),
        "Expected Revenue ($)": round(price * sales, 2),
    })

options = pd.DataFrame(rows)

st.line_chart(
    options.set_index("Fare ($)")[["Expected Revenue ($)"]]
)

st.dataframe(options, hide_index=True, use_container_width=True)

if best["price"] >= round(current_price * 1.20, 2):
    st.info(
        "The selected fare reaches the +20% price-change limit. "
        "The optimum may depend on this guardrail."
    )

st.warning(
    "Research prototype: demand, elasticity, and seat availability "
    "are scenario assumptions. Revenue changes are simulated, "
    "not validated predictions or realized financial results."
)

with st.expander("How this recommendation is calculated"):
    st.write(
        "1. Start with assumed future bookings at the current fare.\n"
        "2. Estimate demand at each candidate fare using elasticity.\n"
        "3. Cap expected sales at remaining seat capacity.\n"
        "4. Multiply fare by expected sales.\n"
        "5. Choose the highest-revenue candidate within ±20%."
    )


from pathlib import Path

import duckdb

from src.demand import estimate_demand


def optimize_price(
    current_price: float,
    baseline_demand: float,
    elasticity: float,
    remaining_seats: int,
) -> dict:
    """Find the highest-revenue price within a 20% change limit."""

    if current_price <= 0 or remaining_seats <= 0:
        raise ValueError("Price and remaining seats must be positive")

    if baseline_demand < 0 or elasticity > 0:
        raise ValueError("Invalid demand or elasticity")

    best = None

    # Test price changes from -20% to +20%, in 5% steps.
    for change_pct in range(-20, 21, 5):
        price = round(current_price * (1 + change_pct / 100), 2)

        demand = estimate_demand(
            current_price,
            price,
            baseline_demand,
            elasticity,
        )

        sales = min(demand, remaining_seats)
        revenue = price * sales

        if best is None or revenue > best["revenue"]:
            best = {
                "price": price,
                "demand": demand,
                "sales": sales,
                "revenue": revenue,
            }

    return best


if __name__ == "__main__":
    data_file = (
        Path(__file__).resolve().parents[1]
        / "data/processed/aa_ord_lga_nonstop.parquet"
    )

    historical_median = duckdb.execute(
        "SELECT MEDIAN(fare_ex_tax) FROM read_parquet(?)",
        [str(data_file)],
    ).fetchone()[0]

    print(f"\nHistorical median (excluding tax): ${historical_median:.2f}")
    print("Enter assumptions for one future flight:\n")

    current_price = float(input("Current offered fare ($): "))
    baseline_demand = float(input("Expected future bookings at current fare: "))
    elasticity = float(input("Assumed elasticity (e.g. -1.2): "))
    remaining_seats = int(input("Remaining seats: "))

    result = optimize_price(
        current_price,
        baseline_demand,
        elasticity,
        remaining_seats,
    )

    baseline_revenue = current_price * min(
        baseline_demand, remaining_seats
    )

    uplift = (
        (result["revenue"] / baseline_revenue - 1) * 100
        if baseline_revenue > 0 else 0
    )

    print("\n--- PRICING RECOMMENDATION ---")
    print(f"Recommended price: ${result['price']:.2f}")
    print(f"Expected demand: {result['demand']:.1f}")
    print(f"Expected sales: {result['sales']:.1f}")
    print(f"Expected remaining-seat revenue: ${result['revenue']:.2f}")
    print(f"Scenario revenue improvement: {uplift:.1f}%")

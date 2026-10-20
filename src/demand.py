
def estimate_demand(
    reference_price: float,
    candidate_price: float,
    baseline_demand: float,
    elasticity: float,
) -> float:
    """Estimate demand under an assumed constant elasticity."""

    if reference_price <= 0 or candidate_price <= 0:
        raise ValueError("Prices must be positive")

    if baseline_demand < 0 or elasticity > 0:
        raise ValueError("Invalid demand or elasticity")

    return baseline_demand * (
        candidate_price / reference_price
    ) ** elasticity


if __name__ == "__main__":
    # All inputs below are illustrative scenarios.
    reference_price = 170.0
    baseline_demand = 60.0
    assumed_elasticity = -1.2

    for price in [150.0, 170.0, 190.0]:
        demand = estimate_demand(
            reference_price,
            price,
            baseline_demand,
            assumed_elasticity,
        )

        print(f"Price: ${price:.2f} | Expected demand: {demand:.1f}")

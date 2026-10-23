
from src.optimizer import optimize_price

reference_price = 170
baseline_demand = 60
remaining_seats = 45

print("ELASTICITY SENSITIVITY ANALYSIS")
print("Assumed elasticity | Recommended fare | Expected revenue")

for elasticity in [-0.6, -1.0, -1.2, -1.5, -2.0]:
    result = optimize_price(
        current_price=reference_price,
        baseline_demand=baseline_demand,
        elasticity=elasticity,
        remaining_seats=remaining_seats,
    )

    print(
        f"{elasticity:>18.1f} | "
        f"${result['price']:>15.2f} | "
        f"${result['revenue']:>15.2f}"
    )


import unittest

from src.demand import estimate_demand
from src.optimizer import optimize_price


class DemandTests(unittest.TestCase):

    def test_reference_price(self):
        demand = estimate_demand(170, 170, 60, -1.2)
        self.assertAlmostEqual(demand, 60)

    def test_price_increase_reduces_demand(self):
        demand = estimate_demand(170, 190, 60, -1.2)
        self.assertLess(demand, 60)

    def test_invalid_price(self):
        with self.assertRaises(ValueError):
            estimate_demand(0, 190, 60, -1.2)


class OptimizerTests(unittest.TestCase):

    def test_seat_capacity_and_revenue(self):
        result = optimize_price(170, 60, -1.2, 45)

        self.assertEqual(result["price"], 204)
        self.assertLessEqual(result["sales"], 45)
        self.assertAlmostEqual(result["revenue"], 9180)

    def test_elastic_demand_changes_decision(self):
        result = optimize_price(170, 60, -2.0, 100)

        self.assertEqual(result["price"], 136)


if __name__ == "__main__":
    unittest.main()

import unittest
from backend.salary_estimator import SalaryEstimator

class TestSalaryEstimator(unittest.TestCase):
    def setUp(self):
        self.estimator = SalaryEstimator()

    def test_junior_estimate(self):
        res = self.estimator.estimate_compensation("software_engineer", 0.0, "remote_us")
        self.assertGreater(res["median_salary"], 80000.0)
        self.assertLess(res["p25_salary"], res["median_salary"])
        self.assertGreater(res["p75_salary"], res["median_salary"])

    def test_senior_multiplier(self):
        jr = self.estimator.estimate_compensation("data_scientist", 1.0, "new_york")
        sr = self.estimator.estimate_compensation("data_scientist", 8.0, "new_york")
        self.assertGreater(sr["median_salary"], jr["median_salary"] * 1.4)

    def test_invalid_role(self):
        with self.assertRaises(ValueError):
            self.estimator.estimate_compensation("blacksmith", 2.0, "austin")

if __name__ == "__main__":
    unittest.main()

import unittest
from backend.certification_roi_calculator import CertificationRoiCalculator

class TestCertificationRoiCalculator(unittest.TestCase):
    def test_positive_roi(self):
        res = CertificationRoiCalculator.calculate_roi(
            exam_cost=300.0,
            prep_cost=200.0,
            study_hours=50,
            hourly_wage=25.0, # opp cost 1250, total = 1750
            annual_salary_lift=8000.0
        )
        self.assertEqual(res["total_investment"], 1750.0)
        self.assertLess(res["payback_period_months"], 3.0)
        self.assertGreater(res["first_year_roi_percent"], 300.0)

if __name__ == "__main__":
    unittest.main()

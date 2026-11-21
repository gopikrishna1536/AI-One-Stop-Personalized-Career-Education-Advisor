import unittest
from backend.internship_eligibility_checker import InternshipEligibilityChecker

class TestInternshipEligibility(unittest.TestCase):
    def test_eligible(self):
        res = InternshipEligibilityChecker.check_eligibility(gpa=3.5, completed_credits=45, is_full_time=True, is_international=False)
        self.assertTrue(res["eligible"])

    def test_ineligible_gpa(self):
        res = InternshipEligibilityChecker.check_eligibility(gpa=2.7, completed_credits=45, is_full_time=True, is_international=False)
        self.assertFalse(res["eligible"])
        self.assertIn("GPA must be at least 3.0", res["reasons"][0])

if __name__ == "__main__":
    unittest.main()

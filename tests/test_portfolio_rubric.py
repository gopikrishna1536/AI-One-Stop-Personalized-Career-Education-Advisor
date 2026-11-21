import unittest
from backend.portfolio_rubric_evaluator import PortfolioRubricEvaluator

class TestPortfolioRubricEvaluator(unittest.TestCase):
    def test_full_marks(self):
        meta = {
            "has_readme": True,
            "has_tests": True,
            "has_ci": True,
            "has_docker": True,
            "has_architecture_doc": True,
            "has_clean_license": True
        }
        res = PortfolioRubricEvaluator.evaluate_repo(meta)
        self.assertEqual(res["score"], 100)
        self.assertEqual(res["grade"], "A+")
        self.assertTrue(res["recruiter_ready"])

if __name__ == "__main__":
    unittest.main()

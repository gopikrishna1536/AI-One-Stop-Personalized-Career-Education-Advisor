import unittest
from backend.job_market_trend_analyzer import JobMarketTrendAnalyzer

class TestJobMarketTrendAnalyzer(unittest.TestCase):
    def test_trend_calculation(self):
        data = {
            "FastAPI": [1000, 1200, 1500],
            "jQuery": [5000, 4200, 3800]
        }
        res = JobMarketTrendAnalyzer.analyze_skills(data)
        self.assertEqual(res[0]["skill"], "FastAPI")
        self.assertEqual(res[0]["growth_percentage"], 50.0)
        self.assertEqual(res[0]["momentum_tier"], "High Growth")
        self.assertEqual(res[1]["momentum_tier"], "Declining")

if __name__ == "__main__":
    unittest.main()

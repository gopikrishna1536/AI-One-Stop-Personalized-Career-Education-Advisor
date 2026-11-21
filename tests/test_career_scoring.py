import unittest

class CareerRecommendationEngine:
    """
    Pure Python assessment and scoring logic for academic stream matching.
    """
    CATEGORIES = ("Analytical", "Technical", "Creative", "Healthcare", "Business")

    @staticmethod
    def calculate_stream_scores(responses):
        """
        Aggregates raw response weights across categories and computes percentage affinities.
        """
        scores = {cat: 0.0 for cat in CareerRecommendationEngine.CATEGORIES}
        max_possible = {cat: 0.0 for cat in CareerRecommendationEngine.CATEGORIES}

        for item in responses:
            cat = item.get("category")
            val = float(item.get("score", 0))
            max_val = float(item.get("max_score", 5))

            if cat in scores:
                scores[cat] += val
                max_possible[cat] += max_val

        affinities = {}
        for cat in CareerRecommendationEngine.CATEGORIES:
            denom = max_possible[cat]
            affinities[cat] = round((scores[cat] / denom * 100), 2) if denom > 0 else 0.0

        return affinities

    @staticmethod
    def recommend_top_streams(affinities, top_k=2):
        """
        Ranks categories by percentage affinity and returns top-k recommended streams.
        """
        ranked = sorted(affinities.items(), key=lambda kv: kv[1], reverse=True)
        return [cat for cat, score in ranked[:top_k]]


class TestCareerScoringEngine(unittest.TestCase):
    def test_analytical_dominant_profile(self):
        responses = [
            {"category": "Analytical", "score": 5, "max_score": 5},
            {"category": "Analytical", "score": 5, "max_score": 5},
            {"category": "Technical", "score": 4, "max_score": 5},
            {"category": "Creative", "score": 2, "max_score": 5},
            {"category": "Healthcare", "score": 1, "max_score": 5},
            {"category": "Business", "score": 3, "max_score": 5},
        ]

        affinities = CareerRecommendationEngine.calculate_stream_scores(responses)
        self.assertEqual(affinities["Analytical"], 100.0)
        self.assertEqual(affinities["Technical"], 80.0)
        self.assertEqual(affinities["Business"], 60.0)
        self.assertEqual(affinities["Creative"], 40.0)
        self.assertEqual(affinities["Healthcare"], 20.0)

        top_streams = CareerRecommendationEngine.recommend_top_streams(affinities, top_k=2)
        self.assertEqual(top_streams, ["Analytical", "Technical"])

    def test_empty_responses_handling(self):
        affinities = CareerRecommendationEngine.calculate_stream_scores([])
        for cat in CareerRecommendationEngine.CATEGORIES:
            self.assertEqual(affinities[cat], 0.0)

    def test_tied_scores_ranking(self):
        responses = [
            {"category": "Creative", "score": 4, "max_score": 5},
            {"category": "Business", "score": 4, "max_score": 5},
        ]
        affinities = CareerRecommendationEngine.calculate_stream_scores(responses)
        self.assertEqual(affinities["Creative"], 80.0)
        self.assertEqual(affinities["Business"], 80.0)

        top_streams = CareerRecommendationEngine.recommend_top_streams(affinities, top_k=2)
        self.assertEqual(len(top_streams), 2)
        self.assertIn("Creative", top_streams)
        self.assertIn("Business", top_streams)


if __name__ == "__main__":
    unittest.main()

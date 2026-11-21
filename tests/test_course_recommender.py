import unittest
from backend.course_recommender import CourseRecommender

class TestCourseRecommender(unittest.TestCase):
    def setUp(self):
        self.recommender = CourseRecommender()

    def test_recommendation_filtering(self):
        recs = self.recommender.recommend(["algorithms", "sql"], ["python"], max_hours_weekly=10)
        self.assertEqual(len(recs), 2)
        # Algorithms has prereq python (satisfied), SQL has no prereqs (satisfied)
        self.assertTrue(all(r["prerequisites_satisfied"] for r in recs))

    def test_prereq_penalty(self):
        recs = self.recommender.recommend(["scikit_learn"], ["python"], max_hours_weekly=5)
        # Missing numpy
        self.assertFalse(recs[0]["prerequisites_satisfied"])

if __name__ == "__main__":
    unittest.main()

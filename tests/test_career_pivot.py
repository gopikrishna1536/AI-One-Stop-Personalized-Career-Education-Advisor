import unittest
from backend.career_pivot_matrix import CareerPivotMatrix

class TestCareerPivotMatrix(unittest.TestCase):
    def test_pivot(self):
        res = CareerPivotMatrix.calculate_pivot_distance("qa_engineer", "devops_engineer")
        self.assertIn("git", res["transferable_skills"])
        self.assertIn("ci_cd", res["transferable_skills"])
        self.assertIn("kubernetes", res["skills_to_acquire"])
        self.assertLessEqual(res["transition_difficulty_score"], 10.0)

if __name__ == "__main__":
    unittest.main()

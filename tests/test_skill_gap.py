import unittest
from backend.skill_gap_engine import SkillGapEngine

class TestSkillGapEngine(unittest.TestCase):
    def setUp(self):
        self.engine = SkillGapEngine()

    def test_full_match(self):
        skills = ["python", "data_structures", "algorithms", "git", "sql", "docker", "fastapi", "linux", "testing", "ci_cd"]
        result = self.engine.analyze_gaps(skills, "software_engineer")
        self.assertEqual(result["readiness_score"], 100.0)
        self.assertEqual(len(result["missing_required"]), 0)

    def test_partial_match(self):
        skills = ["python", "git"]
        result = self.engine.analyze_gaps(skills, "software_engineer")
        self.assertIn("sql", result["missing_required"])
        self.assertIn("algorithms", result["missing_required"])
        self.assertLess(result["readiness_score"], 60.0)

    def test_invalid_role(self):
        with self.assertRaises(ValueError):
            self.engine.analyze_gaps(["python"], "astrophysicist")

if __name__ == "__main__":
    unittest.main()

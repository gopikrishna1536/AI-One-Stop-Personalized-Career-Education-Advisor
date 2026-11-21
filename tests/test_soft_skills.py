import unittest
from backend.soft_skills_assessor import SoftSkillsAssessor

class TestSoftSkillsAssessor(unittest.TestCase):
    def test_assessment_scoring(self):
        responses = [
            {"competency": "communication", "score": 5},
            {"competency": "communication", "score": 4},
            {"competency": "conflict_resolution", "score": 3},
            {"competency": "adaptability", "score": 4},
            {"competency": "leadership", "score": 5},
            {"competency": "time_management", "score": 2}
        ]
        res = SoftSkillsAssessor.score_assessment(responses)
        self.assertEqual(res["competency_breakdown"]["communication"], 4.5)
        self.assertEqual(res["growth_area"], "time_management")

if __name__ == "__main__":
    unittest.main()

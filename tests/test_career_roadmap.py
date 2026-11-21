import unittest
import sys
import os

# Add backend directory to module search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

from career_engine import CareerEngine

class TestCareerRoadmapEngine(unittest.TestCase):
    def test_aiml_roadmap_generation(self):
        roadmap = CareerEngine.generate_learning_roadmap("Technical", "AI/ML Engineer", "beginner")

        self.assertEqual(roadmap["stream"], "Technical")
        self.assertEqual(roadmap["target_role"], "AI/ML Engineer")
        self.assertEqual(roadmap["phases_count"], 3)
        self.assertEqual(roadmap["total_estimated_weeks"], 30)

        curriculum = roadmap["curriculum"]
        self.assertIn("Phase 1", curriculum[0]["phase"])
        self.assertIn("Linear Algebra", curriculum[0]["topics"])
        self.assertIn("PyTorch Foundations", curriculum[2]["topics"])

    def test_fullstack_roadmap_generation(self):
        roadmap = CareerEngine.generate_learning_roadmap("Technical", "Full-Stack Engineer", "intermediate")

        self.assertEqual(roadmap["stream"], "Technical")
        self.assertEqual(roadmap["target_role"], "Full-Stack Engineer")
        self.assertEqual(roadmap["phases_count"], 3)
        self.assertEqual(roadmap["total_estimated_weeks"], 24)

    def test_fallback_custom_role_roadmap(self):
        roadmap = CareerEngine.generate_learning_roadmap("Creative", "3D Animation Specialist")

        self.assertEqual(roadmap["phases_count"], 2)
        self.assertEqual(roadmap["total_estimated_weeks"], 18)
        self.assertIn("Creative Principles", roadmap["curriculum"][0]["topics"])

if __name__ == "__main__":
    unittest.main()

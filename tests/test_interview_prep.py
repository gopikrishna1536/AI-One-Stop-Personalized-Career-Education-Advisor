import unittest
from backend.interview_prep_generator import InterviewPrepGenerator

class TestInterviewPrepGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = InterviewPrepGenerator()

    def test_prep_package_generation(self):
        pkg = self.generator.get_prep_package(["python", "sql"])
        self.assertGreaterEqual(len(pkg["behavioral_questions"]), 2)
        self.assertEqual(len(pkg["technical_questions"]), 2)
        self.assertIn("star_framework_guide", pkg)

if __name__ == "__main__":
    unittest.main()

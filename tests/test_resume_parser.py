import unittest
from backend.resume_keyword_parser import ResumeKeywordParser

class TestResumeKeywordParser(unittest.TestCase):
    def setUp(self):
        self.parser = ResumeKeywordParser()

    def test_scoring(self):
        resume = "Experienced software engineer specializing in python, docker, fastAPI and distributed microservices with PostgreSQL."
        jd = "Seeking software engineer skilled in python, docker, PostgreSQL, kubernetes, AWS and CI/CD pipelines."
        res = self.parser.score_resume(resume, jd)
        self.assertIn("python", res["matched_keywords"])
        self.assertIn("docker", res["matched_keywords"])
        self.assertIn("kubernetes", res["missing_keywords"])
        self.assertGreater(res["ats_match_percentage"], 30.0)

if __name__ == "__main__":
    unittest.main()

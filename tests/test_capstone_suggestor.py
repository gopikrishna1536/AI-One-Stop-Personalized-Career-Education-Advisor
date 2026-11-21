import unittest
from backend.capstone_project_suggestor import CapstoneProjectSuggestor

class TestCapstoneSuggestor(unittest.TestCase):
    def test_suggestion(self):
        sugs = CapstoneProjectSuggestor.get_suggestions("software_engineer")
        self.assertEqual(len(sugs), 1)
        self.assertEqual(sugs[0]["title"], "High-Throughput Distributed Rate Limiter")

if __name__ == "__main__":
    unittest.main()

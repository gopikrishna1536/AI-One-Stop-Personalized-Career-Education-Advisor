import unittest
from backend.scholarship_finder import ScholarshipFinder

class TestScholarshipFinder(unittest.TestCase):
    def test_matching(self):
        matches = ScholarshipFinder.find_matches("computer_science", 3.8)
        self.assertEqual(len(matches), 3)
        self.assertEqual(matches[0]["amount"], 8000)

if __name__ == "__main__":
    unittest.main()

import unittest
from backend.mentorship_matcher import MentorshipMatcher

class TestMentorshipMatcher(unittest.TestCase):
    def test_stable_matching(self):
        mentees = {
            "Alice": ["Mentor_X", "Mentor_Y"],
            "Bob": ["Mentor_X", "Mentor_Y"]
        }
        mentors = {
            "Mentor_X": ["Alice", "Bob"],
            "Mentor_Y": ["Alice", "Bob"]
        }
        matches = MentorshipMatcher.stable_match(mentees, mentors)
        self.assertEqual(matches["Alice"], "Mentor_X")
        self.assertEqual(matches["Bob"], "Mentor_Y")

if __name__ == "__main__":
    unittest.main()

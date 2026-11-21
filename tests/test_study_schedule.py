import unittest
from backend.study_schedule_generator import StudyScheduleGenerator

class TestStudyScheduleGenerator(unittest.TestCase):
    def test_schedule_generation(self):
        topics = [{"name": "Python AsyncIO"}, {"name": "SQL Indexing"}]
        avail = {"Monday": 2.0, "Wednesday": 2.0, "Saturday": 4.0}
        res = StudyScheduleGenerator.generate_schedule(topics, avail)
        self.assertEqual(res["total_pomodoro_sessions"], 16)
        self.assertEqual(res["total_study_hours"], 8.0)
        self.assertEqual(len(res["weekly_schedule"]["Monday"]), 4)

if __name__ == "__main__":
    unittest.main()

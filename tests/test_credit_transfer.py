import unittest
from backend.academic_credit_transfer import AcademicCreditTransfer

class TestAcademicCreditTransfer(unittest.TestCase):
    def setUp(self):
        self.transfer = AcademicCreditTransfer()

    def test_transfer_acceptance(self):
        courses = [
            {"course_code": "CS-101", "grade": "A"},
            {"course_code": "MATH-201", "grade": "C"} # requires B-
        ]
        res = self.transfer.evaluate_transfers(courses)
        self.assertEqual(res["total_transferred_credits"], 4)
        self.assertEqual(len(res["transferred_courses"]), 1)
        self.assertEqual(len(res["rejected_courses"]), 1)

if __name__ == "__main__":
    unittest.main()

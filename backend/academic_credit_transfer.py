"""
Academic Credit Transfer & Articulation Evaluator
Determines course credit transferability between higher-education institutions.
"""
from typing import Dict, List, Any

class AcademicCreditTransfer:
    def __init__(self, articulation_agreements: Dict[str, Dict[str, str]] = None):
        self.agreements = articulation_agreements or {
            "CS-101": {"target_course": "ENGR-110", "credits": 4, "min_grade": "C"},
            "MATH-201": {"target_course": "MATH-240", "credits": 3, "min_grade": "B-"},
            "PHYS-101": {"target_course": "PHYS-150", "credits": 4, "min_grade": "C"}
        }

    GRADE_POINTS = {"A": 4.0, "A-": 3.7, "B+": 3.3, "B": 3.0, "B-": 2.7, "C+": 2.3, "C": 2.0, "D": 1.0, "F": 0.0}

    def evaluate_transfers(self, completed_courses: List[Dict[str, Any]]) -> Dict[str, Any]:
        transferred = []
        rejected = []
        total_transferred_credits = 0

        for c in completed_courses:
            code = c["course_code"]
            grade = c["grade"]
            if code in self.agreements:
                agr = self.agreements[code]
                min_gp = self.GRADE_POINTS.get(agr["min_grade"], 2.0)
                earned_gp = self.GRADE_POINTS.get(grade, 0.0)

                if earned_gp >= min_gp:
                    transferred.append({
                        "original": code,
                        "equivalent": agr["target_course"],
                        "credits": agr["credits"]
                    })
                    total_transferred_credits += agr["credits"]
                else:
                    rejected.append({
                        "course": code,
                        "reason": f"Grade {grade} below minimum requirement {agr['min_grade']}"
                    })
            else:
                rejected.append({
                    "course": code,
                    "reason": "No direct articulation agreement found"
                })

        return {
            "total_transferred_credits": total_transferred_credits,
            "transferred_courses": transferred,
            "rejected_courses": rejected
        }

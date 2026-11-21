"""
Scholarship & Academic Grant Matcher
Matches eligible educational grants based on academic achievement and field of study.
"""
from typing import Dict, List, Any

SCHOLARSHIPS = [
    {"name": "Women in STEM Tech Grant", "major": "computer_science", "min_gpa": 3.2, "amount": 5000},
    {"name": "Future Software Leaders Award", "major": "computer_science", "min_gpa": 3.7, "amount": 8000},
    {"name": "General Tech Diversity Fellowship", "major": "any", "min_gpa": 3.0, "amount": 4000}
]

class ScholarshipFinder:
    @staticmethod
    def find_matches(major: str, gpa: float) -> List[Dict[str, Any]]:
        matches = []
        for s in SCHOLARSHIPS:
            if (s["major"] == "any" or s["major"] == major.lower()) and gpa >= s["min_gpa"]:
                matches.append(s)
        matches.sort(key=lambda x: x["amount"], reverse=True)
        return matches

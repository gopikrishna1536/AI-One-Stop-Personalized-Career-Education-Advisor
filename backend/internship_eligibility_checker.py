"""
Student Internship Eligibility & Compliance Checker
Verifies academic standing, completed credits, and international student work requirements.
"""
from typing import Dict, Any

class InternshipEligibilityChecker:
    @staticmethod
    def check_eligibility(gpa: float, completed_credits: int, is_full_time: bool, is_international: bool, has_cpt_authorization: bool = True) -> Dict[str, Any]:
        reasons = []

        if gpa < 3.0:
            reasons.append("GPA must be at least 3.0 (current: {:.2f})".format(gpa))

        if completed_credits < 30:
            reasons.append("Must complete at least 30 credit hours prior to internship")

        if not is_full_time:
            reasons.append("Must maintain full-time student status")

        if is_international and not has_cpt_authorization:
            reasons.append("Requires valid Curricular Practical Training (CPT) authorization")

        eligible = len(reasons) == 0
        return {
            "eligible": eligible,
            "gpa": gpa,
            "credits": completed_credits,
            "reasons": reasons
        }

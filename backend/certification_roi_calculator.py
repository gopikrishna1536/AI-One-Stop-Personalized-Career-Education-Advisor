"""
Certification ROI & Payback Calculator
Estimates return on investment for professional certifications based on salary lift.
"""
from typing import Dict, Any

class CertificationRoiCalculator:
    @staticmethod
    def calculate_roi(exam_cost: float, prep_cost: float, study_hours: int, hourly_wage: float, annual_salary_lift: float) -> Dict[str, Any]:
        opportunity_cost = study_hours * hourly_wage
        total_investment = exam_cost + prep_cost + opportunity_cost

        if total_investment <= 0 or annual_salary_lift <= 0:
            return {
                "total_investment": total_investment,
                "first_year_net_gain": 0.0,
                "first_year_roi_percent": 0.0,
                "payback_period_months": 999.0
            }

        payback_months = round((total_investment / annual_salary_lift) * 12.0, 1)
        first_year_gain = annual_salary_lift - total_investment
        roi_percent = round((first_year_gain / total_investment) * 100.0, 1)

        return {
            "total_investment": round(total_investment, 2),
            "annual_salary_lift": round(annual_salary_lift, 2),
            "first_year_net_gain": round(first_year_gain, 2),
            "first_year_roi_percent": roi_percent,
            "payback_period_months": payback_months
        }

"""
Salary Estimation & Compensation Benchmarking Engine
Computes expected base compensation ranges with location cost-of-living adjustments.
"""
from typing import Dict, Any

ROLE_BASE_SALARIES: Dict[str, float] = {
    "software_engineer": 85000.0,
    "machine_learning_engineer": 95000.0,
    "data_scientist": 90000.0,
    "full_stack_developer": 82000.0,
    "devops_engineer": 88000.0
}

LOCATION_MULTIPLIERS: Dict[str, float] = {
    "san_francisco": 1.45,
    "new_york": 1.40,
    "seattle": 1.30,
    "austin": 1.15,
    "chicago": 1.10,
    "bengaluru": 0.40,
    "hyderabad": 0.38,
    "remote_us": 1.05,
    "remote_global": 0.90
}

class SalaryEstimator:
    def __init__(self, base_salaries: Dict[str, float] = None, multipliers: Dict[str, float] = None):
        self.base_salaries = base_salaries or ROLE_BASE_SALARIES
        self.multipliers = multipliers or LOCATION_MULTIPLIERS

    def estimate_compensation(self, role: str, years_exp: float, location: str, has_masters: bool = False) -> Dict[str, Any]:
        role_key = role.lower().replace(" ", "_")
        if role_key not in self.base_salaries:
            raise ValueError(f"Unknown role for compensation: {role}")

        loc_key = location.lower().replace(" ", "_")
        loc_mult = self.multipliers.get(loc_key, 1.0)
        base = self.base_salaries[role_key]

        # Experience multiplier: 8% compounding annual increase capped at 2.5x
        exp_mult = min(2.5, (1.08 ** min(years_exp, 15.0)))
        degree_mult = 1.07 if has_masters else 1.0

        median_salary = round(base * exp_mult * loc_mult * degree_mult, -2)
        p25_salary = round(median_salary * 0.88, -2)
        p75_salary = round(median_salary * 1.15, -2)

        return {
            "role": role,
            "years_experience": years_exp,
            "location": location,
            "currency": "USD",
            "p25_salary": p25_salary,
            "median_salary": median_salary,
            "p75_salary": p75_salary,
            "cost_of_living_multiplier": loc_mult
        }

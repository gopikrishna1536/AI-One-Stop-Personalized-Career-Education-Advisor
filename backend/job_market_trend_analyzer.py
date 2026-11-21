"""
Job Market Technology Demand Trend Analyzer
Computes demand momentum and compound growth rate across technology sectors.
"""
from typing import Dict, List, Any

class JobMarketTrendAnalyzer:
    @staticmethod
    def calculate_growth_rate(historical_postings: List[int]) -> float:
        if not historical_postings or len(historical_postings) < 2:
            return 0.0
        start = historical_postings[0]
        end = historical_postings[-1]
        if start <= 0:
            return 0.0
        return round(((end - start) / start) * 100.0, 2)

    @staticmethod
    def analyze_skills(skill_data: Dict[str, List[int]]) -> List[Dict[str, Any]]:
        results = []
        for skill, postings in skill_data.items():
            growth = JobMarketTrendAnalyzer.calculate_growth_rate(postings)
            momentum = "High Growth" if growth > 25.0 else ("Moderate" if growth >= 0 else "Declining")
            results.append({
                "skill": skill,
                "latest_volume": postings[-1] if postings else 0,
                "growth_percentage": growth,
                "momentum_tier": momentum
            })
        results.sort(key=lambda x: x["growth_percentage"], reverse=True)
        return results

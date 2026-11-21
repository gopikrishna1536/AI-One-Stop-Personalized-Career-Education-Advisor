"""
Soft Skills & Engineering Leadership Assessor
Scores situational scenario responses across 5 core professional competencies.
"""
from typing import Dict, List, Any

class SoftSkillsAssessor:
    COMPETENCIES = ["communication", "conflict_resolution", "adaptability", "leadership", "time_management"]

    @staticmethod
    def score_assessment(responses: List[Dict[str, Any]]) -> Dict[str, Any]:
        competency_scores = {c: [] for c in SoftSkillsAssessor.COMPETENCIES}

        for r in responses:
            comp = r.get("competency")
            rating = r.get("score", 0) # 1 to 5
            if comp in competency_scores:
                competency_scores[comp].append(rating)

        summary = {}
        for comp, scores in competency_scores.items():
            avg = sum(scores) / len(scores) if scores else 3.0
            summary[comp] = round(avg, 2)

        overall = round(sum(summary.values()) / len(summary), 2)
        return {
            "overall_soft_skill_rating": overall,
            "competency_breakdown": summary,
            "top_strength": max(summary.items(), key=lambda x: x[1])[0],
            "growth_area": min(summary.items(), key=lambda x: x[1])[0]
        }

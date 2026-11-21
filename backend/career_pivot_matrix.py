"""
Career Pivot & Transferable Skill Distance Matrix
Computes overlap and transition effort between two engineering career specializations.
"""
from typing import Dict, List, Set, Any

CAREER_TRACKS: Dict[str, Set[str]] = {
    "qa_engineer": {"python", "selenium", "pytest", "jira", "git", "ci_cd", "api_testing"},
    "devops_engineer": {"python", "docker", "kubernetes", "ci_cd", "git", "terraform", "linux", "aws"},
    "data_engineer": {"python", "sql", "spark", "airflow", "docker", "git", "data_warehousing"},
    "frontend_developer": {"javascript", "typescript", "react", "html", "css", "git", "tailwind"}
}

class CareerPivotMatrix:
    @staticmethod
    def calculate_pivot_distance(current_role: str, target_role: str) -> Dict[str, Any]:
        c_skills = CAREER_TRACKS.get(current_role.lower(), set())
        t_skills = CAREER_TRACKS.get(target_role.lower(), set())

        if not c_skills or not t_skills:
            raise ValueError("Role not recognized in career pivot matrix")

        transferable = sorted(list(c_skills & t_skills))
        skills_to_acquire = sorted(list(t_skills - c_skills))

        jaccard_similarity = len(transferable) / len(c_skills | t_skills)
        transition_difficulty = round((1.0 - jaccard_similarity) * 10, 1)

        return {
            "current_role": current_role,
            "target_role": target_role,
            "transferable_skills": transferable,
            "skills_to_acquire": skills_to_acquire,
            "jaccard_similarity": round(jaccard_similarity, 3),
            "transition_difficulty_score": transition_difficulty, # 1-10 scale
            "estimated_months": max(3, int(transition_difficulty * 1.2))
        }

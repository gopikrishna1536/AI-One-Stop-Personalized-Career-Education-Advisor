"""
Skill Gap Analysis Engine
Evaluates candidate skillsets against target engineering role competency models.
"""
from typing import Dict, List, Set, Any

ROLE_TAXONOMIES: Dict[str, Dict[str, List[str]]] = {
    "software_engineer": {
        "required": ["python", "data_structures", "algorithms", "git", "sql"],
        "recommended": ["docker", "fastapi", "linux", "testing", "ci_cd"]
    },
    "machine_learning_engineer": {
        "required": ["python", "numpy", "pandas", "scikit_learn", "linear_algebra"],
        "recommended": ["pytorch", "mlflow", "docker", "docker_compose", "statistics"]
    },
    "full_stack_developer": {
        "required": ["javascript", "typescript", "react", "node", "sql"],
        "recommended": ["tailwind", "docker", "graphql", "nextjs", "redis"]
    }
}

class SkillGapEngine:
    def __init__(self, taxonomies: Dict[str, Dict[str, List[str]]] = None):
        self.taxonomies = taxonomies or ROLE_TAXONOMIES

    def analyze_gaps(self, candidate_skills: List[str], target_role: str) -> Dict[str, Any]:
        role_key = target_role.lower().replace(" ", "_").replace("-", "_")
        if role_key not in self.taxonomies:
            raise ValueError(f"Unknown target role: {target_role}")

        taxonomy = self.taxonomies[role_key]
        candidate_set: Set[str] = {s.lower().strip() for s in candidate_skills}
        required_set: Set[str] = {s.lower() for s in taxonomy.get("required", [])}
        recommended_set: Set[str] = {s.lower() for s in taxonomy.get("recommended", [])}

        missing_required = sorted(list(required_set - candidate_set))
        matched_required = sorted(list(required_set & candidate_set))
        missing_recommended = sorted(list(recommended_set - candidate_set))
        matched_recommended = sorted(list(recommended_set & candidate_set))

        req_score = (len(matched_required) / len(required_set)) * 100 if required_set else 100.0
        rec_score = (len(matched_recommended) / len(recommended_set)) * 100 if recommended_set else 100.0
        composite_score = round(req_score * 0.7 + rec_score * 0.3, 1)

        return {
            "target_role": target_role,
            "readiness_score": composite_score,
            "required_match_percentage": round(req_score, 1),
            "matched_required": matched_required,
            "missing_required": missing_required,
            "matched_recommended": matched_recommended,
            "missing_recommended": missing_recommended,
            "priority_actions": [f"Learn required skill: {s}" for s in missing_required]
        }

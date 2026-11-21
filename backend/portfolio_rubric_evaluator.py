"""
Portfolio Rubric & Recruiter Readiness Evaluator
Scores developer repositories on production engineering best practices.
"""
from typing import Dict, Any

class PortfolioRubricEvaluator:
    @staticmethod
    def evaluate_repo(repo_meta: Dict[str, Any]) -> Dict[str, Any]:
        score = 0
        feedback = []

        if repo_meta.get("has_readme", False):
            score += 20
        else:
            feedback.append("Missing README.md documentation")

        if repo_meta.get("has_tests", False):
            score += 25
        else:
            feedback.append("Missing automated unit test suite")

        if repo_meta.get("has_ci", False):
            score += 20
        else:
            feedback.append("Missing GitHub Actions CI workflow")

        if repo_meta.get("has_docker", False):
            score += 15
        else:
            feedback.append("Missing Dockerfile containerization")

        if repo_meta.get("has_architecture_doc", False):
            score += 10
        else:
            feedback.append("Missing architecture or system design diagram")

        if repo_meta.get("has_clean_license", False):
            score += 10
        else:
            feedback.append("Missing open-source LICENSE")

        grade = "A+" if score >= 90 else ("A" if score >= 80 else ("B" if score >= 65 else "Needs Improvement"))

        return {
            "score": score,
            "max_score": 100,
            "grade": grade,
            "feedback": feedback,
            "recruiter_ready": score >= 75
        }

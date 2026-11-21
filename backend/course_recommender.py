"""
Course Recommendation Engine
Ranks curriculum modules based on student skill gaps, study hours, and prerequisites.
"""
from typing import List, Dict, Any

class CourseRecommender:
    def __init__(self, catalog: List[Dict[str, Any]] = None):
        self.catalog = catalog or [
            {"id": "CS101", "title": "Data Structures & Algorithms", "skill": "algorithms", "prereqs": ["python"], "hours": 40, "rating": 4.8},
            {"id": "PY201", "title": "Advanced Python & AsyncIO", "skill": "fastapi", "prereqs": ["python"], "hours": 30, "rating": 4.7},
            {"id": "DB101", "title": "Relational Databases & SQL Masterclass", "skill": "sql", "prereqs": [], "hours": 25, "rating": 4.6},
            {"id": "DOCK101", "title": "Docker Containers & Kubernetes Fundamentals", "skill": "docker", "prereqs": ["linux"], "hours": 20, "rating": 4.9},
            {"id": "ML101", "title": "Applied Machine Learning with Scikit-Learn", "skill": "scikit_learn", "prereqs": ["python", "numpy"], "hours": 45, "rating": 4.8}
        ]

    def recommend(self, missing_skills: List[str], known_skills: List[str], max_hours_weekly: int = 10) -> List[Dict[str, Any]]:
        known_set = {s.lower() for s in known_skills}
        missing_set = {s.lower() for s in missing_skills}
        recommendations = []

        for course in self.catalog:
            skill = course["skill"].lower()
            if skill in missing_set:
                prereqs = [p.lower() for p in course.get("prereqs", [])]
                prereqs_met = all(p in known_set for p in prereqs)
                weeks_to_finish = round(course["hours"] / max(1, max_hours_weekly), 1)

                score = course["rating"] * (1.5 if prereqs_met else 0.8)

                recommendations.append({
                    "course_id": course["id"],
                    "title": course["title"],
                    "target_skill": course["skill"],
                    "prerequisites_satisfied": prereqs_met,
                    "estimated_weeks": weeks_to_finish,
                    "relevance_score": round(score, 2)
                })

        recommendations.sort(key=lambda x: (x["prerequisites_satisfied"], x["relevance_score"]), reverse=True)
        return recommendations

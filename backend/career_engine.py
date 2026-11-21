"""
Career Recommendation and Personalized Learning Roadmap Engine.
Analyzes student aptitudes, computes domain affinities, and generates milestone-driven curricula.
"""
from typing import Dict, List, Any, Optional

ROADMAP_TEMPLATES = {
    "Technical": {
        "AI/ML Engineer": [
            {
                "phase": "Phase 1: Mathematical Foundations & Python Mastery",
                "duration_weeks": 8,
                "topics": ["Linear Algebra", "Multivariate Calculus", "NumPy & Pandas", "Data Structures in Python"],
                "deliverable": "Custom matrix operations library and EDA project on real-world datasets"
            },
            {
                "phase": "Phase 2: Classical Machine Learning & Feature Engineering",
                "duration_weeks": 10,
                "topics": ["Scikit-Learn", "Regression & Classification", "Random Forests & XGBoost", "Model Evaluation & Cross-Validation"],
                "deliverable": "End-to-end predictive model pipeline deployed with FastAPI"
            },
            {
                "phase": "Phase 3: Deep Learning, NLP & LLMs",
                "duration_weeks": 12,
                "topics": ["PyTorch Foundations", "Transformers Architecture", "HuggingFace Ecosystem", "RAG & Vector Databases"],
                "deliverable": "Production Retrieval-Augmented Generation (RAG) assistant containerized with Docker"
            }
        ],
        "Full-Stack Engineer": [
            {
                "phase": "Phase 1: Modern Web Core & TypeScript",
                "duration_weeks": 6,
                "topics": ["HTML5/CSS3 Grid & Flexbox", "Modern JavaScript (ES6+)", "TypeScript Types & Generics", "Git & GitHub Workflows"],
                "deliverable": "Responsive component library and interactive portfolio"
            },
            {
                "phase": "Phase 2: Frontend Architecture & React",
                "duration_weeks": 8,
                "topics": ["React 19 / Next.js", "State Management (Zustand/Redux)", "Tailwind CSS", "REST & GraphQL Integration"],
                "deliverable": "Dynamic multi-tenant SaaS dashboard with authentication"
            },
            {
                "phase": "Phase 3: Backend Services & Cloud Deployment",
                "duration_weeks": 10,
                "topics": ["Node.js / Express & FastAPI", "PostgreSQL & Prisma ORM", "Docker Containerization", "CI/CD with GitHub Actions"],
                "deliverable": "Full-stack microservices architecture deployed to AWS or Railway"
            }
        ]
    },
    "Analytical": {
        "Data Analyst": [
            {
                "phase": "Phase 1: Advanced SQL & Database Querying",
                "duration_weeks": 6,
                "topics": ["Complex Joins & Window Functions", "CTEs & Subqueries", "Query Optimization & Indexing", "PostgreSQL/BigQuery"],
                "deliverable": "Cohort retention and churn analysis SQL script suite"
            },
            {
                "phase": "Phase 2: Business Intelligence & Dashboarding",
                "duration_weeks": 8,
                "topics": ["PowerBI / Tableau", "Data Modeling (Star Schema)", "DAX / Calculated Measures", "Executive Storytelling"],
                "deliverable": "Interactive executive KPI dashboard with automated refreshes"
            },
            {
                "phase": "Phase 3: Statistical Analysis & Python Automation",
                "duration_weeks": 8,
                "topics": ["Hypothesis Testing & A/B Experiments", "Python (Pandas, Seaborn)", "Automated Reporting Pipelines"],
                "deliverable": "A/B test statistical significance calculator and automated report generator"
            }
        ]
    }
}

class CareerEngine:
    CATEGORIES = ("Analytical", "Technical", "Creative", "Healthcare", "Business")

    @staticmethod
    def calculate_stream_scores(responses: List[Dict[str, Any]]) -> Dict[str, float]:
        """
        Aggregates raw response weights across categories and computes percentage affinities.
        """
        scores = {cat: 0.0 for cat in CareerEngine.CATEGORIES}
        max_possible = {cat: 0.0 for cat in CareerEngine.CATEGORIES}

        for item in responses:
            cat = item.get("category")
            val = float(item.get("score", 0))
            max_val = float(item.get("max_score", 5))

            if cat in scores:
                scores[cat] += val
                max_possible[cat] += max_val

        affinities = {}
        for cat in CareerEngine.CATEGORIES:
            denom = max_possible[cat]
            affinities[cat] = round((scores[cat] / denom * 100), 2) if denom > 0 else 0.0

        return affinities

    @staticmethod
    def recommend_top_streams(affinities: Dict[str, float], top_k: int = 2) -> List[str]:
        """
        Ranks categories by percentage affinity and returns top-k recommended streams.
        """
        ranked = sorted(affinities.items(), key=lambda kv: kv[1], reverse=True)
        return [cat for cat, score in ranked[:top_k]]

    @staticmethod
    def generate_learning_roadmap(stream: str, target_role: str, experience_level: str = "beginner") -> Dict[str, Any]:
        """
        Generates a phased curriculum roadmap for a given stream and target role.
        """
        stream_data = ROADMAP_TEMPLATES.get(stream, {})
        phases = stream_data.get(target_role)

        if not phases:
            # Fallback generic structured roadmap
            phases = [
                {
                    "phase": f"Phase 1: Core Fundamentals in {stream}",
                    "duration_weeks": 8,
                    "topics": [f"{stream} Principles", "Industry Standard Tools", "Foundational Problem Solving"],
                    "deliverable": "Foundational portfolio project"
                },
                {
                    "phase": f"Phase 2: Applied {target_role} Skillsets",
                    "duration_weeks": 10,
                    "topics": ["Intermediate Workflows", "Team Collaboration", "Domain Best Practices"],
                    "deliverable": "Comprehensive capstone project demonstrating end-to-end execution"
                }
            ]

        total_weeks = sum(p["duration_weeks"] for p in phases)

        return {
            "stream": stream,
            "target_role": target_role,
            "experience_level": experience_level,
            "total_estimated_weeks": total_weeks,
            "phases_count": len(phases),
            "curriculum": phases
        }

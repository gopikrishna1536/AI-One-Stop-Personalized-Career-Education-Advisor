"""
Industry-Aligned Capstone Project Suggestion Engine
Generates portfolio project specifications tailored to student career aspirations.
"""
from typing import Dict, List, Any

CAPSTONES = {
    "software_engineer": [
        {
            "title": "High-Throughput Distributed Rate Limiter",
            "stack": ["Python", "FastAPI", "Redis", "Docker"],
            "features": ["Token bucket algorithm", "Sliding window counter", "Prometheus metrics export"]
        }
    ],
    "machine_learning_engineer": [
        {
            "title": "Real-Time Fraud Detection Pipeline",
            "stack": ["Python", "Kafka", "Scikit-Learn", "FastAPI"],
            "features": ["Streaming feature extraction", "LightGBM inference", "Drift monitoring"]
        }
    ]
}

class CapstoneProjectSuggestor:
    @staticmethod
    def get_suggestions(role: str) -> List[Dict[str, Any]]:
        role_k = role.lower().replace(" ", "_")
        return CAPSTONES.get(role_k, [])

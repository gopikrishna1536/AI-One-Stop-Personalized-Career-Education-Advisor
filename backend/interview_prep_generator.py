"""
Interview Preparation Question Generator
Provides targeted behavioral (STAR) and technical questions with evaluation rubrics.
"""
from typing import List, Dict, Any

INTERVIEW_BANK = {
    "behavioral": [
        {
            "id": "BEH-01",
            "category": "conflict_resolution",
            "prompt": "Describe a situation where you had a technical disagreement with a team member. How did you resolve it?",
            "rubric": ["Identified root technical cause", "Listened actively to peer perspective", "Evaluated trade-offs with objective benchmarks", "Reached collaborative consensus"]
        },
        {
            "id": "BEH-02",
            "category": "ownership",
            "prompt": "Tell me about a time an unexpected production outage occurred under your watch. What did you do?",
            "rubric": ["Immediate incident triage", "Clear stakeholder communication", "Root-cause post-mortem", "Preventative automated testing or monitoring added"]
        }
    ],
    "technical": {
        "python": [
            {
                "id": "TECH-PY-01",
                "question": "Explain the difference between threading, multiprocessing, and asyncio in Python. When would you use each?",
                "rubric": ["GIL implications on CPU-bound vs I/O-bound", "Memory overhead comparison", "Event loop architecture in asyncio"]
            }
        ],
        "sql": [
            {
                "id": "TECH-SQL-01",
                "question": "How do B-tree indexes improve query performance, and what are the trade-offs on write-heavy tables?",
                "rubric": ["Logarithmic lookup complexity O(log N)", "Index maintenance cost during INSERT/UPDATE", "Covering index concept"]
            }
        ]
    }
}

class InterviewPrepGenerator:
    def __init__(self, bank: Dict[str, Any] = None):
        self.bank = bank or INTERVIEW_BANK

    def get_prep_package(self, skills: List[str]) -> Dict[str, Any]:
        tech_questions = []
        for s in skills:
            k = s.lower().strip()
            if k in self.bank.get("technical", {}):
                tech_questions.extend(self.bank["technical"][k])

        return {
            "behavioral_questions": self.bank.get("behavioral", []),
            "technical_questions": tech_questions,
            "star_framework_guide": {
                "S": "Situation - Set the context and business problem",
                "T": "Task - Specify your individual responsibility",
                "A": "Action - Explain technical steps taken and tooling used",
                "R": "Result - Quantify positive outcome with metrics (latency, revenue, bug reduction)"
            }
        }

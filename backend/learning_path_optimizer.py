"""
Learning Path DAG Optimizer
Uses topological sorting to schedule curriculum milestones respecting prerequisite dependencies.
"""
from typing import Dict, List, Any
from collections import deque

class LearningPathOptimizer:
    def __init__(self, course_graph: Dict[str, List[str]] = None):
        # Maps course -> list of prerequisite courses that must precede it
        self.course_graph = course_graph or {
            "python_basics": [],
            "data_structures": ["python_basics"],
            "algorithms": ["data_structures"],
            "databases_sql": ["python_basics"],
            "web_frameworks": ["python_basics", "databases_sql"],
            "system_design": ["algorithms", "databases_sql", "web_frameworks"],
            "cloud_deployment": ["web_frameworks"]
        }

    def generate_path(self, target_courses: List[str]) -> List[str]:
        # Collect all required nodes in subgraph
        required_nodes = set()
        def collect(node: str):
            if node not in required_nodes and node in self.course_graph:
                required_nodes.add(node)
                for prereq in self.course_graph[node]:
                    collect(prereq)

        for target in target_courses:
            collect(target)

        # Build in-degree map for required nodes
        in_degree = {n: 0 for n in required_nodes}
        adj = {n: [] for n in required_nodes}

        for node in required_nodes:
            for prereq in self.course_graph.get(node, []):
                if prereq in required_nodes:
                    adj[prereq].append(node)
                    in_degree[node] += 1

        queue = deque([n for n, deg in in_degree.items() if deg == 0])
        ordered_path = []

        while queue:
            curr = queue.popleft()
            ordered_path.append(curr)
            for neighbor in adj[curr]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        if len(ordered_path) != len(required_nodes):
            raise ValueError("Cyclic dependency detected in course curriculum graph!")

        return ordered_path

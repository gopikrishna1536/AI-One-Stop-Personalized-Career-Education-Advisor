import unittest
from backend.learning_path_optimizer import LearningPathOptimizer

class TestLearningPathOptimizer(unittest.TestCase):
    def setUp(self):
        self.optimizer = LearningPathOptimizer()

    def test_topological_sequence(self):
        path = self.optimizer.generate_path(["system_design"])
        self.assertIn("python_basics", path)
        self.assertIn("system_design", path)
        # python_basics must precede algorithms
        self.assertLess(path.index("python_basics"), path.index("algorithms"))
        # algorithms and web_frameworks must precede system_design
        self.assertLess(path.index("algorithms"), path.index("system_design"))
        self.assertLess(path.index("web_frameworks"), path.index("system_design"))

if __name__ == "__main__":
    unittest.main()

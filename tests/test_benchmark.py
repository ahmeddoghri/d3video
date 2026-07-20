import unittest
import d3video

class BenchmarkTest(unittest.TestCase):
    def test_research_method_clears_baseline(self):
        result = d3video.run()
        self.assertGreaterEqual(result["accuracy_gain_pct"], 25)

if __name__ == "__main__":
    unittest.main()

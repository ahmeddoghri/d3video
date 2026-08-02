import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import d3video
from adversarial import HOLDOUT_SEEDS, TUNING_SEEDS
from eval_v2 import run_stress, summarize


class AdversarialTest(unittest.TestCase):
    def test_holdout_disjoint_from_tuning(self):
        self.assertTrue(set(TUNING_SEEDS).isdisjoint(HOLDOUT_SEEDS))

    def test_original_benchmark_still_reproduces_exactly(self):
        result = d3video.run()
        self.assertEqual(result["first_order_accuracy"], 0.46)
        self.assertEqual(result["second_order_accuracy"], 1.0)
        self.assertEqual(result["accuracy_gain_pct"], 54.0)

    def test_published_artifact_shape_is_near_worst_case_for_the_filter(self):
        """d3video.py's injected artifact alternates sign every single
        frame at full amplitude (.15) -- close to the literal highest
        frequency a discrete sequence can carry, which is what a two-tap
        second-difference filter is maximally sensitive to. Confirmed
        directly: second_order_accuracy sits at ~1.0 across many seeds."""
        accs = [run_stress(seed, 0.15, "alternate")["second_order_accuracy"] for seed in TUNING_SEEDS[:10]]
        self.assertGreater(sum(accs) / len(accs), 0.99)

    def test_less_tailored_artifact_shows_the_headline_number_is_best_case(self):
        """A less favorable but equally plausible artifact (half the
        amplitude, per-frame random sign instead of perfect alternation)
        drops second_order_accuracy well below the published 1.0."""
        result = summarize(TUNING_SEEDS)
        self.assertLess(result["mean_second_order_accuracy"], 0.85)

    def test_second_order_advantage_survives_under_the_stress_shape_on_tuning_seeds(self):
        result = summarize(TUNING_SEEDS)
        self.assertGreater(result["min_gain_pct"], 5)

    def test_second_order_advantage_survives_under_the_stress_shape_on_frozen_holdout_seeds(self):
        result = summarize(HOLDOUT_SEEDS)
        self.assertGreater(result["min_gain_pct"], 5)

    def test_original_module_untouched(self):
        import inspect

        source = inspect.getsource(d3video.run)
        self.assertIn(".15 if t%2 else -.15", source)

    def test_report_is_reproducible(self):
        a = summarize(TUNING_SEEDS[:5])
        b = summarize(TUNING_SEEDS[:5])
        self.assertEqual(a, b)


if __name__ == "__main__":
    unittest.main()

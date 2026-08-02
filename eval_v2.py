"""Stress-test d3video's claim against a less favorable, but still
plausible, injected-artifact shape.

This is not a bug fix -- d3video.py's mechanism and published numbers are
correct and reproduce exactly. This checks whether the claim generalizes
past the one artifact shape (perfect, maximal-amplitude, alternating-every-
frame) the benchmark ships with, which happens to be close to the
best-case input for a second-difference filter."""
import json
import math
import random
import statistics as st

from adversarial import HOLDOUT_SEEDS, STRESS_AMPLITUDE, STRESS_MODE, TUNING_SEEDS
from d3video import accuracy, first_order_score, second_order_score


def make_stress_sequences(seed, amplitude, mode):
    rng = random.Random(seed)
    sequences = []
    for fake in (0, 1):
        for _ in range(100):
            phase = rng.random() * 6
            seq = [t * .8 + 2 * math.sin(t / 7 + phase) + rng.gauss(0, .08) for t in range(30)]
            if fake:
                if mode == "alternate":
                    seq = [x + (amplitude if t % 2 else -amplitude) for t, x in enumerate(seq)]
                elif mode == "random_sign":
                    seq = [x + amplitude * rng.choice([-1, 1]) for x in seq]
            sequences.append((seq, fake))
    return sequences


def run_stress(seed, amplitude=STRESS_AMPLITUDE, mode=STRESS_MODE):
    sequences = make_stress_sequences(seed, amplitude, mode)
    first, _ = accuracy([(first_order_score(s), y) for s, y in sequences])
    second, threshold = accuracy([(second_order_score(s), y) for s, y in sequences])
    return {
        "first_order_accuracy": round(first, 3),
        "second_order_accuracy": round(second, 3),
        "accuracy_gain_pct": round(100 * (second - first), 1),
        "threshold": round(threshold, 3),
    }


def summarize(seeds):
    results = [run_stress(seed) for seed in seeds]
    gains = [r["accuracy_gain_pct"] for r in results]
    seconds = [r["second_order_accuracy"] for r in results]
    return {
        "n": len(seeds),
        "mean_gain_pct": round(st.mean(gains), 1),
        "min_gain_pct": min(gains),
        "mean_second_order_accuracy": round(st.mean(seconds), 3),
    }


def main():
    print("d3video eval_v2: published artifact shape vs. a less favorable, still-plausible one")
    print(f"published (seed=31, alternate, amp=0.15): {run_stress(31, 0.15, 'alternate')}")
    print(f"stress (seed=31, {STRESS_MODE}, amp={STRESS_AMPLITUDE}): {run_stress(31)}")
    for label, seeds in (("tuning", TUNING_SEEDS), ("holdout", HOLDOUT_SEEDS)):
        print(f"\n{label} ({len(seeds)} seeds) at stress artifact shape:")
        print(json.dumps(summarize(seeds), indent=2))


if __name__ == "__main__":
    main()

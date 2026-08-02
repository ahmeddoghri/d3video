"""Adversarial seeds for the artifact-shape generalization stress test.

d3video.py's injected "fake" artifact is `+.15 if t%2 else -.15` --
a perfect, maximal-amplitude, alternating-every-frame square wave. That's
close to the literal worst-case (best-case for the detector) input for a
second-difference filter: alternating sign at the highest frequency a
discrete sequence can represent is exactly what two-tap differencing is
most sensitive to. It is not obviously representative of what a real
video generator's second-order artifact would look like.

STRESS_AMPLITUDE / STRESS_MODE describe a more modest, less-tailored
artifact: half the amplitude, and a per-frame *random* sign instead of a
perfect alternation -- still a plausible stand-in for "frame-level noise
a generator introduces," just not hand-picked to maximize the second-
difference filter's response.

TUNING_SEEDS: used to characterize d3video's generalization under a less
favorable, but still plausible, artifact shape.
HOLDOUT_SEEDS: disjoint, evaluated exactly once after characterization.
"""

STRESS_AMPLITUDE = 0.06
STRESS_MODE = "random_sign"

TUNING_SEEDS = list(range(1, 41))
HOLDOUT_SEEDS = list(range(1000, 1030))

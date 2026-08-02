# d3video

**Training-free synthetic-video detection from the difference of differences.**

First-order motion — frame-to-frame difference — looks smooth in both real and AI-generated video, because generators got good at faking velocity. What they haven't fully faked is *acceleration*: the second derivative, the jitter in how the jitter itself changes. d3video doesn't watch pixels move. It watches how the *rate* of movement moves, and that's where synthetic video still gives itself away.

It's a compact, inspectable implementation inspired by [ICCV 2025's D3 second-order temporal discrepancy detector](https://openaccess.thecvf.com/content/ICCV2025/html/Zheng_D3_Training-Free_AI-Generated_Video_Detection_Using_Second-Order_Features_ICCV_2025_paper.html), rebuilt small enough to read in one sitting and run without a GPU, a checkpoint, or an API key.

## The result

```bash
python d3video.py
```
```json
{
  "first_order_accuracy": 0.46,
  "second_order_accuracy": 1.0,
  "accuracy_gain_pct": 54.0,
  "threshold": 0.386
}
```

Score sequences by first-order (frame-to-frame) motion alone and you're basically guessing: 46% accuracy, worse than a coin flip on 200 sequences, because smooth motion looks the same whether it's real or synthetic. Score the second-order difference (the difference of the differences) and threshold against the sample mean, and accuracy hits 100% — a 54 percentage-point gain from one derivative most generators don't bother faking.

**Update:** that 100%/54pp is close to a best case, not a typical one. The
injected "fake" artifact alternates sign every single frame at full
amplitude — close to the highest frequency a discrete sequence can carry,
which is exactly what a two-tap second-difference filter is most sensitive
to. A less contrived but equally plausible artifact (half the amplitude,
per-frame random sign instead of perfect alternation) drops second-order
accuracy to ~72-73% and the gain to ~23pp. The core mechanism survives —
second-order still clearly beats first-order — but the published numbers
overstate how far. Details below.

## How it works

200 synthetic motion sequences are generated with smooth first-order trajectories (linear drift plus a sine wobble); half get a small alternating perturbation injected — a stand-in for the frame-level artifacts video generators introduce even when frame-to-frame motion looks plausible. Both a first-order detector (mean absolute frame-to-frame difference) and a second-order detector (mean absolute difference of differences) are computed and thresholded the same way, so the comparison is apples to apples: same data, same thresholding rule, only the derivative order changes. First-order can't tell the classes apart because the perturbation is deliberately too small to show up in raw motion. Second-order catches it because acceleration, not velocity, is where the injected artifact actually lives.

## Run it

```bash
python d3video.py
python -m unittest discover -s tests -v
```

## What is tested

The test compares second-order detection against the first-order baseline and requires `accuracy_gain_pct >= 25`. Both accuracies are computed from the same run, not hardcoded, so the gap is a real measurement and not an assumption. The data generator is seeded, so the number in this README, in CI, and in the portfolio case study are the same number, not three different ones that happen to rhyme.

## Scope

This is an educational research reproduction on controlled synthetic motion sequences, not real video frames or real generator outputs. It is not a clinical, diagnostic, production content-authentication, or safety-critical system. The point is to make one mechanism — second-order temporal features expose artifacts first-order motion hides — measurable without hiding it behind a checkpoint.

## The published artifact shape is close to a best case for the filter

The injected artifact is `+.15 if t%2 else -.15` — a perfect, full-
amplitude, alternating-every-frame square wave. Second differencing is a
two-tap high-pass filter; alternating sign at the highest frequency a
sequence can represent is close to the textbook best-case input for it.

```bash
python eval_v2.py
```
```
published (alternate, amp=0.15): second_order_accuracy=1.0    accuracy_gain_pct=54.0
stress (random_sign, amp=0.06):  second_order_accuracy=0.665  accuracy_gain_pct=20.5

tuning (40 seeds):  mean_gain_pct=22.9  min_gain_pct=12.5  mean_second_order_accuracy=0.725
holdout (30 seeds): mean_gain_pct=23.9  min_gain_pct=13.5  mean_second_order_accuracy=0.734
```

Swap in a less favorable but equally plausible artifact — half the
amplitude, and a per-frame *random* sign instead of a perfect alternation
(real generator noise has no reason to alternate in perfect lockstep) —
and mean second-order accuracy drops to 72.5%/73.4% across 40 tuning
seeds and a disjoint 30-seed holdout (evaluated once), with the accuracy
gain over first-order falling to a mean 22.9-23.9pp (never below 12.5pp).
The core claim survives: second-order features still meaningfully
outperform first-order under a harder, more realistic artifact shape. But
the published 100%/54.0pp is close to the best case this specific
construction can produce, not a representative one. `d3video.py` is
untouched and the published numbers still reproduce exactly.

## Research basis

- [ICCV 2025's D3 second-order temporal discrepancy detector](https://openaccess.thecvf.com/content/ICCV2025/html/Zheng_D3_Training-Free_AI-Generated_Video_Detection_Using_Second-Order_Features_ICCV_2025_paper.html)
- Original implementation and benchmark in this repository are MIT licensed.

## License

MIT

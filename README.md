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
  "first_order_accuracy": 0.5,
  "second_order_accuracy": 1.0,
  "accuracy_gain_pct": 50.0,
  "threshold": 1.386
}
```

A first-order signal has nothing to threshold against here — it's a coin flip, 50% accuracy, because smooth frame-to-frame motion looks identical whether it's real or synthetic. Score the second-order difference (the difference of the differences) and threshold against the sample mean, and accuracy hits 100% across 200 sequences — a 50 percentage-point gain from one derivative nobody bothered faking.

## How it works

200 synthetic motion sequences are generated with smooth first-order trajectories (linear drift plus a sine wobble); half get a small alternating perturbation injected — a stand-in for the frame-level artifacts that video generators introduce even when frame-to-frame motion looks plausible. The detector computes the second difference of each sequence and averages its absolute magnitude. Real sequences cluster low, perturbed ones cluster high, and a single threshold (the dataset mean) separates them cleanly. No CNN, no frame classifier — just arithmetic on differences, made explicit.

## Run it

```bash
python d3video.py
python -m unittest discover -s tests -v
```

## What is tested

The test compares second-order detection against the first-order (chance-level) baseline and requires `accuracy_gain_pct >= 25`. The data generator is seeded, so the number in this README, in CI, and in the portfolio case study are the same number, not three different ones that happen to rhyme.

## Scope

This is an educational research reproduction on controlled synthetic motion sequences, not real video frames or real generator outputs. It is not a clinical, diagnostic, production content-authentication, or safety-critical system. The point is to make one mechanism — second-order temporal features expose artifacts first-order motion hides — measurable without hiding it behind a checkpoint.

## Research basis

- [ICCV 2025's D3 second-order temporal discrepancy detector](https://openaccess.thecvf.com/content/ICCV2025/html/Zheng_D3_Training-Free_AI-Generated_Video_Detection_Using_Second-Order_Features_ICCV_2025_paper.html)
- Original implementation and benchmark in this repository are MIT licensed.

## License

MIT

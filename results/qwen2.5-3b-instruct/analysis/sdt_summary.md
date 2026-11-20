# POST-HOC signal-detection analysis: Qwen/Qwen2.5-3B-Instruct

> **POST-HOC (exploratory): added after the results were seen; not pre-registered in the HW1 proposal.**

- Signal = Entailment. H = P(pred=E | gold=E); F = P(pred=E | gold=N).
- d' = z(H) − z(F): discrimination, higher is better.
- c = −(z(H) + z(F)) / 2: **c > 0 = bias toward Non-entailment; c < 0 = bias toward Entailment; c = 0 = unbiased**.
- Invalid outputs are excluded per prompt (counts below).
- Log-linear correction (Hautus, 1995): every rate is (count + 0.5) / (n + 1), in every condition.
- 95% CIs: 2000 bootstrap resamples stratified by HANS subcase, numpy default_rng(42); paired contrasts reuse the same resamples for both prompts.

## Per prompt

| Prompt | Valid gold E / N | Excluded invalid (gold E / N) | Hits: pred E, gold E | False alarms: pred E, gold N | H (corr.) | F (corr.) | d' [95% CI] | c [95% CI] |
|---|---|---|---|---|---|---|---|---|
| P1 Basic | 150 / 150 | 0 (0 / 0) | 96/150 | 22/150 | 0.639 | 0.149 | +1.40 [+1.18, +1.62] | +0.34 [+0.23, +0.46] |
| P2 General reasoning | 150 / 150 | 0 (0 / 0) | 56/150 | 7/150 | 0.374 | 0.050 | +1.33 [+1.07, +1.71] | +0.98 [+0.85, +1.17] |
| P3 Structure-aware | 147 / 147 | 6 (3 / 3) | 102/147 | 18/147 | 0.693 | 0.125 | +1.65 [+1.40, +1.96] | +0.32 [+0.20, +0.47] |
| P4 Nonstructural control | 149 / 150 | 1 (1 / 0) | 85/149 | 16/150 | 0.570 | 0.109 | +1.41 [+1.17, +1.68] | +0.53 [+0.40, +0.67] |

## Paired contrasts (first prompt minus second)

Δc < 0: the first prompt is less biased toward Non-entailment than the second (or more toward Entailment).

| Contrast | Δd' [95% CI] | Δc [95% CI] |
|---|---|---|
| P3-P2 | +0.33 [-0.12, +0.70] | -0.66 [-0.89, -0.48] |
| P3-P4 | +0.25 [-0.09, +0.58] | -0.20 [-0.38, -0.04] |
| P3-P1 | +0.26 [-0.03, +0.57] | -0.02 [-0.16, +0.14] |
| P2-P1 | -0.07 [-0.37, +0.33] | +0.64 [+0.49, +0.83] |

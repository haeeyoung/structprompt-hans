# POST-HOC signal-detection analysis: Qwen/Qwen2.5-1.5B-Instruct

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
| P1 Basic | 150 / 150 | 0 (0 / 0) | 89/150 | 42/150 | 0.593 | 0.281 | +0.81 [+0.61, +1.02] | +0.17 [+0.07, +0.28] |
| P2 General reasoning | 150 / 150 | 0 (0 / 0) | 27/150 | 17/150 | 0.182 | 0.116 | +0.29 [+0.06, +0.52] | +1.05 [+0.94, +1.17] |
| P3 Structure-aware | 124 / 131 | 45 (26 / 19) | 68/124 | 45/131 | 0.548 | 0.345 | +0.52 [+0.27, +0.78] | +0.14 [+0.00, +0.28] |
| P4 Nonstructural control | 150 / 150 | 0 (0 / 0) | 0/150 | 0/150 | 0.003 | 0.003 | +0.00 [+0.00, +0.00] | +2.72 [+2.72, +2.72] |

## Paired contrasts (first prompt minus second)

Δc < 0: the first prompt is less biased toward Non-entailment than the second (or more toward Entailment).

| Contrast | Δd' [95% CI] | Δc [95% CI] |
|---|---|---|
| P3-P2 | +0.23 [-0.09, +0.55] | -0.91 [-1.08, -0.75] |
| P3-P4 | +0.52 [+0.27, +0.78] | -2.58 [-2.71, -2.44] |
| P3-P1 | -0.29 [-0.61, +0.03] | -0.03 [-0.20, +0.14] |
| P2-P1 | -0.52 [-0.80, -0.25] | +0.88 [+0.75, +1.03] |

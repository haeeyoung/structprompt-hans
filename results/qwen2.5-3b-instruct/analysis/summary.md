# Results: Qwen/Qwen2.5-3B-Instruct

Accuracy in %, [95% stratified bootstrap CI]. Conflicting = gold non-entailment; consistent = gold entailment.

| Prompt | Conflicting | Consistent | Overall | Non-ent. predicted | Invalid | Overall (lenient parse) | Mean new tokens | Hit 128 | Label first |
|---|---|---|---|---|---|---|---|---|---|
| P1 Basic | 85.3 [81.3, 89.3] | 64.0 [58.7, 69.3] | 74.7 [71.0, 78.0] | 60.7 [57.3, 64.3] | 0 | 74.7 | 7.2 | 0 | 0.0 |
| P2 General reasoning | 95.3 [92.7, 98.0] | 37.3 [31.3, 42.7] | 66.3 [63.0, 69.7] | 79.0 [75.7, 82.3] | 0 | 66.3 | 62.0 | 0 | 0.0 |
| P3 Structure-aware | 86.0 [81.3, 90.7] | 68.0 [62.0, 74.0] | 77.0 [73.0, 80.7] | 58.0 [54.3, 61.7] | 6 | 77.0 | 95.1 | 9 | 0.0 |
| P4 Nonstructural control | 89.3 [85.3, 93.3] | 56.7 [50.0, 62.7] | 73.0 [69.3, 76.7] | 66.0 [62.3, 69.7] | 1 | 73.0 | 68.7 | 0 | 0.0 |

## By heuristic (accuracy %)

| Prompt | LO confl. | SUB confl. | CON confl. | LO cons. | SUB cons. | CON cons. |
|---|---|---|---|---|---|---|
| P1 | 100.0 | 68.0 | 88.0 | 50.0 | 92.0 | 50.0 |
| P2 | 100.0 | 86.0 | 100.0 | 30.0 | 50.0 | 32.0 |
| P3 | 100.0 | 74.0 | 84.0 | 60.0 | 88.0 | 56.0 |
| P4 | 98.0 | 78.0 | 92.0 | 48.0 | 86.0 | 36.0 |

## Paired comparisons (percentage points)

| Comparison | Subset | Role | Diff | 95% CI | first right & second wrong / reverse | McNemar p |
|---|---|---|---|---|---|---|
| P3-P2 | conflicting | H1 (primary) | -9.3 | [-14.7, -4.0] | 4/18 | 0.004 |
| P3-P4 | conflicting | control (secondary) | -3.3 | [-8.7, +1.3] | 7/12 | 0.359 |
| P3-P1 | conflicting | exploratory | +0.7 | [-4.0, +5.3] | 9/8 | 1.000 |
| P2-P1 | conflicting | exploratory | +10.0 | [+6.0, +14.0] | 15/0 | 0.000 |
| P4-P2 | conflicting | exploratory | -6.0 | [-9.3, -2.7] | 0/9 | 0.004 |
| P3-P2 | consistent | loss check | +30.7 | [+23.3, +37.3] | 53/7 | 0.000 |
| P3-P4 | consistent | loss check | +11.3 | [+4.0, +18.7] | 28/11 | 0.009 |
| P3-P1 | consistent | loss check | +4.0 | [-3.3, +11.3] | 24/18 | 0.441 |
| P3-P2 | all | overall | +10.7 | [+6.0, +15.0] | 57/25 | 0.001 |
| P3-P4 | all | overall | +4.0 | [-0.7, +8.3] | 35/23 | 0.148 |

Shift in non-entailment prediction rate, P3-P2 (all items): -21.0 pp [-25.7, -16.7]

## Hypotheses

- **H1** (P3 > P2 on conflicting items): diff -9.3 pp, CI [-14.7, -4.0] -> **not supported** (CI includes or is below zero)
- **H2** (exploratory; LO gain minus mean SUB/CON gain): +14.0 pp, CI [+6.0, +22.0] -> CI entirely above zero
  - P3-P2 gain on conflicting items by heuristic: LO +0.0 [+0.0, +0.0], SUB -12.0 [-26.0, +0.0], CON -16.0 [-26.0, -8.0]


# Results: Qwen/Qwen2.5-1.5B-Instruct

Accuracy in %, [95% stratified bootstrap CI]. Conflicting = gold non-entailment; consistent = gold entailment.

| Prompt | Conflicting | Consistent | Overall | Non-ent. predicted | Invalid | Overall (lenient parse) | Mean new tokens | Hit 128 | Label first |
|---|---|---|---|---|---|---|---|---|---|
| P1 Basic | 72.0 [66.7, 76.7] | 59.3 [53.3, 65.3] | 65.7 [61.7, 69.3] | 56.3 [52.7, 60.0] | 0 | 65.7 | 7.1 | 0 | 0.0 |
| P2 General reasoning | 88.7 [85.3, 91.3] | 18.0 [14.0, 22.7] | 53.3 [50.7, 56.0] | 85.3 [82.7, 88.0] | 0 | 53.3 | 65.2 | 0 | 100.0 |
| P3 Structure-aware | 57.3 [50.7, 64.0] | 45.3 [38.0, 52.0] | 51.3 [46.7, 56.0] | 47.3 [42.3, 52.7] | 45 | 55.0 | 88.9 | 38 | 0.0 |
| P4 Nonstructural control | 100.0 [100.0, 100.0] | 0.0 [0.0, 0.0] | 50.0 [50.0, 50.0] | 100.0 [100.0, 100.0] | 0 | 50.0 | 102.6 | 80 | 98.7 |

## By heuristic (accuracy %)

| Prompt | LO confl. | SUB confl. | CON confl. | LO cons. | SUB cons. | CON cons. |
|---|---|---|---|---|---|---|
| P1 | 100.0 | 74.0 | 42.0 | 32.0 | 72.0 | 74.0 |
| P2 | 100.0 | 94.0 | 72.0 | 16.0 | 16.0 | 22.0 |
| P3 | 84.0 | 56.0 | 32.0 | 44.0 | 32.0 | 60.0 |
| P4 | 100.0 | 100.0 | 100.0 | 0.0 | 0.0 | 0.0 |

## Paired comparisons (percentage points)

| Comparison | Subset | Role | Diff | 95% CI | first right & second wrong / reverse | McNemar p |
|---|---|---|---|---|---|---|
| P3-P2 | conflicting | H1 (primary) | -31.3 | [-38.0, -24.7] | 2/49 | 0.000 |
| P3-P4 | conflicting | control (secondary) | -42.7 | [-49.3, -36.0] | 0/64 | 0.000 |
| P3-P1 | conflicting | exploratory | -14.7 | [-22.0, -6.7] | 11/33 | 0.001 |
| P2-P1 | conflicting | exploratory | +16.7 | [+11.3, +22.0] | 25/0 | 0.000 |
| P4-P2 | conflicting | exploratory | +11.3 | [+8.7, +14.7] | 17/0 | 0.000 |
| P3-P2 | consistent | loss check | +27.3 | [+19.3, +34.7] | 46/5 | 0.000 |
| P3-P4 | consistent | loss check | +45.3 | [+38.0, +52.0] | 68/0 | 0.000 |
| P3-P1 | consistent | loss check | -14.0 | [-23.3, -5.3] | 22/43 | 0.013 |
| P3-P2 | all | overall | -2.0 | [-6.7, +3.0] | 48/54 | 0.621 |
| P3-P4 | all | overall | +1.3 | [-3.3, +6.0] | 68/64 | 0.794 |

Shift in non-entailment prediction rate, P3-P2 (all items): -38.0 pp [-43.3, -32.3]

## Hypotheses

- **H1** (P3 > P2 on conflicting items): diff -31.3 pp, CI [-38.0, -24.7] -> **not supported** (CI includes or is below zero)
- **H2** (exploratory; LO gain minus mean SUB/CON gain): +23.0 pp, CI [+10.0, +36.0] -> CI entirely above zero
  - P3-P2 gain on conflicting items by heuristic: LO -16.0 [-26.0, -6.0], SUB -38.0 [-52.0, -24.0], CON -40.0 [-52.0, -28.0]


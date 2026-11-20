# Structure-aware prompting on HANS

Code and data for *Does Structure-Aware Prompting Reduce Shortcut Reliance in Natural Language Inference?*

We compare four prompts on the same 300 HANS pairs with Qwen2.5-3B-Instruct
(Qwen2.5-1.5B-Instruct as a robustness check):

| | Prompt | Instruction (after a shared task description) |
|---|---|---|
| P1 | Basic | answer directly, no explanation |
| P2 | General reasoning | think carefully, explain in 1–2 sentences |
| P3 | Structure-aware | examine who performs / receives each action and how clauses affect meaning |
| P4 | Nonstructural control | examine topic, vocabulary, style and tone (length-matched to P3) |

Exact wording: [prompts.py](prompts.py).

## Quick start (Google Colab, T4 GPU)

Open [colab_run.ipynb](colab_run.ipynb) in Colab
([direct link](https://colab.research.google.com/github/haeeyoung/structprompt-hans/blob/main/colab_run.ipynb)),
set **Runtime → Change runtime type → T4 GPU**, then **Runtime → Run all**.
It reruns every step below, optionally runs the greedy-decoding check (`tests/check_greedy.py`),
and downloads `results.zip` at the end: raw model responses, run metadata (library versions, GPU,
decoding settings), every table, the figure, the example and annotation sheets, and `env/`
(`pip freeze`, `nvidia-smi`).

## Environment

| | Main experiments | Pipeline tests |
|---|---|---|
| Hardware | Google Colab, NVIDIA T4 (16 GB) | laptop CPU, no GPU |
| Python | Colab default (logged in `run_meta_eval.json`) | 3.13 |
| torch | Colab preinstalled CUDA build (logged) | 2.15.0+cpu |
| transformers / accelerate | 4.57.1 / 1.11.0 | 4.57.1 / 1.11.0 |
| Precision | float16 | float32 |

```bash
pip install -r requirements.txt   # plus a torch build for your machine
```

## Reproducing each result

| Output | Command | Writes |
|---|---|---|
| Evaluation sample (300 pairs) and pilot set (12 pairs) | `python sample_hans.py --verify` | checks `data/*.jsonl` against HANS |
| Instruction token lengths (P3 vs P4) | `python check_prompts.py --tag qwen2.5-3b-instruct` | `results/<tag>/prompt_lengths.json` |
| Pilot format check | `python run_inference.py --tag qwen2.5-3b-instruct --split pilot` | `results/<tag>/pilot_predictions.jsonl` |
| Raw predictions (1,200) | `python run_inference.py --tag qwen2.5-3b-instruct --split eval` | `results/<tag>/predictions.jsonl` |
| Table 1: accuracy by heuristic and label | `python analyze.py --tag qwen2.5-3b-instruct` | `results/<tag>/analysis/table_main.tex` |
| Table 2: H1/H2 tests, bootstrap CIs, McNemar | same command | `results/<tag>/analysis/table_tests.tex` |
| Figure: accuracy and non-entailment rate | same command | `results/<tag>/analysis/fig_accuracy.pdf` |
| Appendix: per-subcase accuracy | same command | `results/<tag>/analysis/table_subcase.tex` |
| Sampled examples and P2→P3 flips | same command | `random_examples.md`, `flips_P2_P3.md` |
| Robustness model | the last three commands with `--tag qwen2.5-1.5b-instruct` | `results/qwen2.5-1.5b-instruct/` |

`summary.md` in each analysis folder collects every number used in the paper.

## Seeds and fixed settings

| What | Setting |
|---|---|
| HANS source | [tommccoy1/hans](https://github.com/tommccoy1/hans) at commit `7299f6f`, SHA-256 checked in `sample_hans.py` |
| Evaluation sample | 10 pairs per subcase × 30 subcases, `random.Random(42)` |
| Pilot set | 2 pairs per heuristic × label from the HANS **training** file, seed 42, no overlap with the evaluation set |
| Model checkpoints | pinned HuggingFace commits in `common.py` (`MODELS`) |
| Decoding | greedy, `max_new_tokens=128`, `repetition_penalty=1.0` (the checkpoint's sampling defaults are overridden), batch size 16 |
| Conversation | one single-turn conversation per item; Qwen's default system prompt; no examples in the prompt |
| Label parsing | last `Final label: …` line; anything else is invalid and counted as incorrect (`common.parse_label`) |
| Bootstrap | 2,000 paired resamples, stratified by HANS subcase, `numpy.random.default_rng(42)` |
| Example sampling | `random.Random(42)` for flips, random examples, and the annotation sheet |

## Changes from the proposal (HW1), all made before any evaluation run

- The output format `Final label: [label]` became `'Final label: Entailment' or 'Final label: Non-entailment'`
  in P2–P4, as in P1, because a small model can copy the literal `[label]`.
- Greedy decoding is made explicit by setting `repetition_penalty=1.0`; Qwen2.5 ships with 1.05.

## Testing without a GPU

```bash
python tests/test_parse.py                      # label parser
python tests/make_fake_predictions.py           # synthetic predictions
python analyze.py --pred results/_fake/predictions.jsonl
python run_inference.py --tag qwen2.5-0.5b-instruct --split pilot --limit 4 --out_dir results/_smoke
```

On a GPU, `python tests/check_greedy.py --tag qwen2.5-3b-instruct` confirms that `generate()` with our
settings matches a hand-written argmax loop token for token (`results/<tag>/greedy_check.json`).

## Files

```
sample_hans.py       build the evaluation and pilot sets from HANS
prompts.py           the four prompt conditions
check_prompts.py     token lengths of the instructions
run_inference.py     generation (resumable)
analyze.py           tables, tests, figure, example sheets
common.py            I/O, model registry, label parser
colab_run.ipynb      one-click Colab run
data/                hans_eval_sample300.jsonl, hans_pilot12.jsonl
tests/               parser tests and a synthetic-prediction generator
```

HANS is distributed under the MIT License by its authors (McCoy, Pavlick, and Linzen, 2019).

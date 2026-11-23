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
It reruns every pre-registered step below (the post-hoc scripts run on the committed predictions without a GPU),
optionally runs the greedy-decoding check (`tests/check_greedy.py`),
and downloads `results.zip` at the end: raw model responses, run metadata (library versions, GPU,
decoding settings), every table, the figure, the example and annotation sheets, and `env/`
(`pip freeze`, `nvidia-smi`).

## Environment

| | Main experiments (logged in `results/*/run_meta_eval.json`, `results/env/`) | Pipeline tests and re-analysis |
|---|---|---|
| Hardware | Google Colab, Tesla T4 (14.6 GB usable) | laptop CPU, no GPU |
| Python | 3.13.16 | 3.13 |
| torch / CUDA | 2.14.1+cu130 / 13.0 | 2.15.0+cpu |
| transformers / accelerate | 4.57.1 / 1.11.0 | 4.57.1 / 1.11.0 |
| numpy / pandas / scipy | 2.4.6 / 2.2.3 / 1.16.3 | 2.5.5 / 3.1.1 / 1.18.1 |
| Precision | float16 | float32 |

Re-running `analyze.py` on the committed predictions with the local versions reproduces every table and
example file byte for byte; CSV files differ only in Windows line endings, and `summary.json` only in the
16th significant digit of one p-value.

```bash
pip install -r requirements.txt   # plus a torch build for your machine
```

## Reproducing each result

Run every command from the repository root. Only `run_inference.py` needs a GPU; everything else reads the
committed predictions. `<tag>` is `qwen2.5-3b-instruct` (main model) or `qwen2.5-1.5b-instruct` (second model).

### Data and predictions

| Step | Command | Writes |
|---|---|---|
| Check the evaluation sample (300 pairs) and pilot set (12 pairs) against HANS | `python sample_hans.py --verify` | nothing; prints whether `data/*.jsonl` match |
| Rebuild that sample from HANS (overwrites `data/*.jsonl` with identical files) | `python sample_hans.py` | `data/hans_eval_sample300.jsonl`, `data/hans_pilot12.jsonl` |
| Pilot format check | `python run_inference.py --tag <tag> --split pilot` | `results/<tag>/pilot_predictions.jsonl` |
| Raw predictions (1,200 per model) | `python run_inference.py --tag <tag> --split eval` | `results/<tag>/predictions.jsonl`, `run_meta_eval.json` |

### Paper tables and figure

| Paper | Content | Command | Source file |
|---|---|---|---|
| Table 1 | Prompting conditions and instruction lengths | `python check_prompts.py --tag qwen2.5-3b-instruct` | `results/qwen2.5-3b-instruct/prompt_lengths.json`; wording in `prompts.py` |
| Table 2 | 3B accuracy by heuristic and gold label | `python analyze.py --tag qwen2.5-3b-instruct` | `results/qwen2.5-3b-instruct/analysis/table_main.tex` |
| Table 3 | Paired comparisons and hypothesis tests (H1, H2) | same as Table 2 | `results/qwen2.5-3b-instruct/analysis/table_tests.tex` |
| Table 4 | 1.5B accuracy | `python analyze.py --tag qwen2.5-1.5b-instruct` | `results/qwen2.5-1.5b-instruct/analysis/table_main.tex`; label-first rate in `summary.md` |
| Table 5 | **Post-hoc** signal detection (d′, c) | `python sdt_analysis.py --tag qwen2.5-3b-instruct` | `results/qwen2.5-3b-instruct/analysis/table_sdt.tex` |
| Table 6 | **Post-hoc** explanation-cue analysis | `python extra_analysis.py results/qwen2.5-3b-instruct/predictions.jsonl` | printed to stdout |
| Table 7 | Reproducibility settings | none | `common.py` (`MODELS`), `results/<tag>/run_meta_eval.json`, `results/env/`, [Seeds and fixed settings](#seeds-and-fixed-settings) |
| Table 8 | Per-subcase results | same as Table 2 | `results/qwen2.5-3b-instruct/analysis/table_subcase.tex` |
| Figure 1 | 3B accuracy and non-entailment rate by heuristic | same as Table 2 | `results/qwen2.5-3b-instruct/analysis/fig_accuracy.pdf` |

Numbers quoted only in the text come from the same runs:

| Text | Command | Source file |
|---|---|---|
| 1.5B signal-detection numbers | `python sdt_analysis.py --tag qwen2.5-1.5b-instruct` | `results/qwen2.5-1.5b-instruct/analysis/sdt_summary.md` |
| P4−P2 on all items | the Table 6 command | printed to stdout |
| Explanation cues for the 1.5B model | `python extra_analysis.py results/qwen2.5-1.5b-instruct/predictions.jsonl` | printed to stdout |
| Randomly sampled examples and P2→P3 flips | same as Table 2 | `random_examples.md`, `flips_P2_P3.md` |
| P3 annotation counts | command under [Post-hoc analyses](#post-hoc-analyses-not-pre-registered) | `annotation_sheet_P3_filled.csv` |

`summary.md` in each analysis folder collects every pre-registered number with its CI; `sdt_summary.md` holds the
post-hoc signal-detection numbers. The predictions and analysis outputs of the reported runs are committed under
`results/`, so every table can be regenerated without a GPU.

## Post-hoc analyses (not pre-registered)

Both analyses below were added after the results were seen and are reported as exploratory.

**Signal detection (`sdt_analysis.py`).** Entailment is the signal.

| Quantity | Definition |
|---|---|
| hit rate H | P(pred = Entailment \| gold = Entailment) |
| false-alarm rate F | P(pred = Entailment \| gold = Non-entailment) |
| d′ | z(H) − z(F); discrimination, higher is better |
| c | −(z(H) + z(F)) / 2; **c > 0 = bias toward Non-entailment**, c < 0 = bias toward Entailment, c = 0 = unbiased |
| Δd′, Δc | first prompt minus second, for P3−P2, P3−P4, P3−P1, P2−P1 |

Invalid outputs are excluded from the SDT computation per prompt, and the number excluded is reported.
All rates use the log-linear correction of Hautus (1995), (count + 0.5) / (n + 1), in every condition.
95% CIs come from the subcase-stratified paired bootstrap described under
[Seeds and fixed settings](#seeds-and-fixed-settings), with the same item resamples shared by both prompts of a contrast.

**Explanation cues (`extra_analysis.py`).** Share of explanations containing *simplif*, *subset* or *omit*
(cue list chosen after reading sampled outputs) and accuracy with and without the cue, plus the P4−P2
contrast on all items with the same bootstrap.

**Annotation of P3 explanations** (`results/qwen2.5-3b-instruct/analysis/annotation_sheet_P3_filled.csv`).
The 45 P3 outputs in `annotation_sheet_P3.csv` (15 per heuristic, 24 gold Non-entailment and 21 gold Entailment,
sampled by `analyze.py` with seed 42) are coded for two properties, with a short rationale in `notes`:

| Column | 1 means |
|---|---|
| `roles_correct` | every agent–patient relation the explanation states is correct |
| `label_follows` | the explanation supports the final label that follows it |

Annotator: Claude (Anthropic), following this rubric. This is not an independent human annotation
(see the paper's Limitations and AI-usage appendix). Counts reported in the paper:

```bash
python -c "import pandas as pd; f=pd.read_csv('results/qwen2.5-3b-instruct/analysis/annotation_sheet_P3_filled.csv', encoding='utf-8-sig'); print(f[['roles_correct','label_follows']].sum()); print(pd.crosstab(f.roles_correct, f.P3_correct))"
```

## Seeds and fixed settings

**All bootstrap seeds are 42:** every bootstrap in `analyze.py`, `sdt_analysis.py` and `extra_analysis.py` draws 2,000 paired resamples stratified by HANS subcase with `numpy.random.default_rng(42)`.

| What | Setting |
|---|---|
| HANS source | [tommccoy1/hans](https://github.com/tommccoy1/hans) at commit `7299f6f`, SHA-256 checked in `sample_hans.py` |
| Evaluation sample | 10 pairs per subcase × 30 subcases, `random.Random(42)` |
| Pilot set | 2 pairs per heuristic × label from the HANS **training** file, seed 42, no overlap with the evaluation set |
| Model checkpoints | pinned HuggingFace commits in `common.py` (`MODELS`) |
| Decoding | greedy, `max_new_tokens=128`, `repetition_penalty=1.0` (the checkpoint's sampling defaults are overridden), batch size 16 |
| Conversation | one single-turn conversation per item; Qwen's default system prompt; no examples in the prompt |
| Label parsing | last `Final label: …` line; anything else is invalid and counted as incorrect (`common.parse_label`) |
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
analyze.py           tables, tests, figure, example sheets (pre-registered analyses)
sdt_analysis.py      post-hoc signal-detection analysis (d', c)
extra_analysis.py    post-hoc explanation-cue analysis
common.py            I/O, model registry, label parser
colab_run.ipynb      one-click Colab run
data/                hans_eval_sample300.jsonl, hans_pilot12.jsonl
results/             predictions, run metadata, analysis outputs of the reported runs; env/ = pip freeze, nvidia-smi
tests/               parser tests, synthetic-prediction generator, greedy-decoding check
```

HANS is distributed under the MIT License by its authors (McCoy, Pavlick, and Linzen, 2019).

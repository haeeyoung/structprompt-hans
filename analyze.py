"""Turn raw predictions into the paper's tables, tests, figure, and example sheets.

    python analyze.py --tag qwen2.5-3b-instruct

Reads   results/<tag>/predictions.jsonl
Writes  results/<tag>/analysis/
          summary.md, summary.json            all numbers in one place
          table_main.tex                      accuracy by heuristic and gold label (Table 1)
          table_tests.tex                     paired differences, bootstrap CIs, McNemar (Table 2)
          table_subcase.tex                   per-subcase accuracy (appendix)
          fig_accuracy.pdf / .png             accuracy and non-entailment rate (Figure)
          flips_P2_P3.md                      randomly sampled P2->P3 improvements and losses
          random_examples.md                  randomly sampled items with all four outputs
          annotation_sheet_P3.csv             45 P3 explanations for manual annotation
          item_level.csv                      one row per item, every condition

Definitions
  heuristic-conflicting = gold non-entailment (the heuristic wrongly predicts entailment)
  heuristic-consistent  = gold entailment     (the heuristic happens to be right)
  An output without a parseable 'Final label' line counts as incorrect.
"""
import argparse
import json
import os
import random

import numpy as np
import pandas as pd
from scipy.stats import binomtest

from common import HEURISTIC_SHORT, HEURISTICS, label_first, parse_label, parse_label_lenient, read_jsonl
from prompts import CONDITION_NAMES, CONDITIONS

N_BOOT = 2000
SEED = 42
SUBSETS = {"conflicting": "non-entailment", "consistent": "entailment"}

# (a, b, subset, role) -> report a - b
COMPARISONS = [
    ("P3", "P2", "conflicting", "H1 (primary)"),
    ("P3", "P4", "conflicting", "control (secondary)"),
    ("P3", "P1", "conflicting", "exploratory"),
    ("P2", "P1", "conflicting", "exploratory"),
    ("P4", "P2", "conflicting", "exploratory"),
    ("P3", "P2", "consistent", "loss check"),
    ("P3", "P4", "consistent", "loss check"),
    ("P3", "P1", "consistent", "loss check"),
    ("P3", "P2", "all", "overall"),
    ("P3", "P4", "all", "overall"),
]

# Figure colors: categorical slots 1-4 of the validated default palette, fixed per condition.
COLORS = {"P1": "#2a78d6", "P2": "#eb6834", "P3": "#1baf7a", "P4": "#eda100"}
INK, INK2, MUTED, GRID, AXIS = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"


# ----------------------------------------------------------------------------- data
def load(pred_path, data_path):
    items = read_jsonl(data_path)
    latest = {(p["item_id"], p["condition"]): p for p in read_jsonl(pred_path)}
    missing = [(it["item_id"], c) for it in items for c in CONDITIONS if (it["item_id"], c) not in latest]
    if missing:
        raise SystemExit(f"{len(missing)} predictions missing, e.g. {missing[:3]}; finish run_inference.py first")
    rows = []
    for it in items:
        row = {k: it[k] for k in ("item_id", "heuristic", "subcase", "gold", "premise", "hypothesis")}
        for c in CONDITIONS:
            p = latest[(it["item_id"], c)]
            pred = parse_label(p["output"])
            row[f"out_{c}"] = p["output"]
            row[f"pred_{c}"] = pred if pred else "invalid"
            row[f"ok_{c}"] = int(pred == it["gold"])
            row[f"okl_{c}"] = int(parse_label_lenient(p["output"]) == it["gold"])
            row[f"ne_{c}"] = int(pred == "non-entailment")
            row[f"inv_{c}"] = int(pred is None)
            row[f"lf_{c}"] = int(label_first(p["output"]))
            row[f"tok_{c}"] = p["n_new_tokens"]
            row[f"max_{c}"] = int(p["hit_max"])
        rows.append(row)
    return pd.DataFrame(rows)


def subset(df, name):
    return df if name == "all" else df[df["gold"] == SUBSETS[name]]


# ------------------------------------------------------------------------ bootstrap
def boot_indices(strata, seed=SEED, n_boot=N_BOOT):
    """Stratified resampling: items are redrawn with replacement within each HANS subcase,
    and one index is shared by all conditions, so predictions on a pair stay together."""
    rng = np.random.default_rng(seed)
    strata = np.asarray(strata)
    blocks = []
    for s in sorted(set(strata)):
        members = np.flatnonzero(strata == s)
        blocks.append(members[rng.integers(0, len(members), size=(n_boot, len(members)))])
    return np.concatenate(blocks, axis=1)


def ci95(values):
    lo, hi = np.percentile(values, [2.5, 97.5])
    return float(lo), float(hi)


def mean_ci(x, strata):
    x = np.asarray(x, dtype=float)
    idx = boot_indices(strata)
    return float(x.mean()), *ci95(x[idx].mean(axis=1))


def paired(df, a, b, metric="ok"):
    xa, xb = df[f"{metric}_{a}"].to_numpy(float), df[f"{metric}_{b}"].to_numpy(float)
    d = xa - xb
    idx = boot_indices(df["subcase"])
    lo, hi = ci95(d[idx].mean(axis=1))
    gain = int(((xa == 1) & (xb == 0)).sum())   # b wrong -> a right
    loss = int(((xa == 0) & (xb == 1)).sum())   # b right -> a wrong
    p = binomtest(min(gain, loss), gain + loss, 0.5).pvalue if gain + loss else 1.0
    return {"diff": float(d.mean()), "lo": lo, "hi": hi, "gain": gain, "loss": loss, "mcnemar_p": float(p),
            "n": int(len(d))}


def h2_test(df):
    """Exploratory H2: (P3-P2 gain on lexical overlap) - mean(gain on subsequence, gain on constituent),
    on heuristic-conflicting items."""
    sub = subset(df, "conflicting")
    d = (sub["ok_P3"] - sub["ok_P2"]).to_numpy(float)
    heur = sub["heuristic"].to_numpy()
    idx = boot_indices(sub["subcase"])
    col_heur = heur[idx[0]]  # resampling stays inside a subcase, so each column keeps its heuristic
    res = d[idx]
    g = {h: res[:, col_heur == h].mean(axis=1) for h in HEURISTICS}
    stat_boot = g["lexical_overlap"] - 0.5 * (g["subsequence"] + g["constituent"])
    point = {h: float(d[heur == h].mean()) for h in HEURISTICS}
    stat = point["lexical_overlap"] - 0.5 * (point["subsequence"] + point["constituent"])
    per_heur = {h: (point[h], *ci95(g[h])) for h in HEURISTICS}
    return {"stat": stat, "lo": ci95(stat_boot)[0], "hi": ci95(stat_boot)[1], "per_heuristic": per_heur}


# --------------------------------------------------------------------------- tables
def pct(x):
    return f"{100 * x:.1f}"


def tex_escape(s):
    return s.replace("\\", r"\textbackslash{}").replace("_", r"\_").replace("&", r"\&").replace("%", r"\%")


def accuracy_grid(df):
    """acc[cond][subset][heuristic or 'all'] = (mean, lo, hi)."""
    grid = {}
    for c in CONDITIONS:
        grid[c] = {}
        for sname in ("conflicting", "consistent"):
            sub = subset(df, sname)
            cells = {h: mean_ci(sub.loc[sub.heuristic == h, f"ok_{c}"], sub.loc[sub.heuristic == h, "subcase"])
                     for h in HEURISTICS}
            cells["all"] = mean_ci(sub[f"ok_{c}"], sub["subcase"])
            grid[c][sname] = cells
        grid[c]["overall"] = mean_ci(df[f"ok_{c}"], df["subcase"])
        grid[c]["nonent_rate"] = mean_ci(df[f"ne_{c}"], df["subcase"])
        grid[c]["nonent_rate_by_heuristic"] = {
            h: mean_ci(df.loc[df.heuristic == h, f"ne_{c}"], df.loc[df.heuristic == h, "subcase"]) for h in HEURISTICS}
        grid[c]["invalid"] = int(df[f"inv_{c}"].sum())
        grid[c]["overall_lenient"] = float(df[f"okl_{c}"].mean())
        grid[c]["mean_new_tokens"] = float(df[f"tok_{c}"].mean())
        grid[c]["label_first_rate"] = float(df[f"lf_{c}"].mean())
        grid[c]["hit_max"] = int(df[f"max_{c}"].sum())
    return grid


def table_main(grid, model_name):
    cols = [HEURISTIC_SHORT[h] for h in HEURISTICS] + ["All"]
    head = " & ".join(cols)
    lines = [
        r"\begin{table*}[t]", r"\centering", r"\small",
        r"\begin{tabular}{l cccc cccc c c c}", r"\toprule",
        r" & \multicolumn{4}{c}{Heuristic-conflicting (gold: non-ent.)} & \multicolumn{4}{c}{Heuristic-consistent (gold: ent.)} & & & \\",
        r"\cmidrule(lr){2-5}\cmidrule(lr){6-9}",
        rf"Prompt & {head} & {head} & Overall & NE\% & Inv. \\", r"\midrule",
    ]
    for c in CONDITIONS:
        g = grid[c]
        cells = [pct(g["conflicting"][k][0]) for k in list(HEURISTICS) + ["all"]]
        cells += [pct(g["consistent"][k][0]) for k in list(HEURISTICS) + ["all"]]
        cells += [pct(g["overall"][0]), pct(g["nonent_rate"][0]), str(g["invalid"])]
        lines.append(f"{c} {CONDITION_NAMES[c]} & " + " & ".join(cells) + r" \\")
    lines += [
        r"\bottomrule", r"\end{tabular}",
        rf"\caption{{Accuracy (\%) of {tex_escape(model_name)} on 300 HANS pairs (50 per heuristic and gold label). "
        r"LO = lexical overlap, SUB = subsequence, CON = constituent. NE\% = share of all 300 predictions that are "
        r"Non-entailment; Inv. = outputs without a valid final label (counted as incorrect).}",
        r"\label{tab:main}", r"\end{table*}",
    ]
    return "\n".join(lines) + "\n"


def table_tests(tests, h2):
    lines = [
        r"\begin{table}[t]", r"\centering", r"\small",
        r"\begin{tabular}{llrcrr}", r"\toprule",
        r"Comparison & Subset & $\Delta$ (pp) & 95\% CI & $+$/$-$ & $p$ \\", r"\midrule",
    ]
    for t in tests:
        lines.append(
            f"{t['a']}$-${t['b']} & {t['subset']} & {100 * t['diff']:+.1f} & "
            f"[{100 * t['lo']:+.1f}, {100 * t['hi']:+.1f}] & {t['gain']}/{t['loss']} & {t['mcnemar_p']:.3f} \\\\")
    lines += [
        r"\midrule",
        f"H2: LO gain $-$ mean(SUB, CON) & conflicting & {100 * h2['stat']:+.1f} & "
        f"[{100 * h2['lo']:+.1f}, {100 * h2['hi']:+.1f}] & -- & -- \\\\",
        r"\bottomrule", r"\end{tabular}",
        r"\caption{Paired accuracy differences in percentage points. CIs: stratified paired bootstrap "
        rf"({N_BOOT} resamples within HANS subcases). $+$/$-$: items that the first prompt gets right and the second "
        r"wrong, and the reverse; $p$: exact McNemar test.}",
        r"\label{tab:tests}", r"\end{table}",
    ]
    return "\n".join(lines) + "\n"


def table_subcase(df):
    lines = [
        r"\begin{table}[t]", r"\centering", r"\scriptsize",
        r"\begin{tabular}{ll" + "r" * len(CONDITIONS) + "}", r"\toprule",
        "Gold & Subcase & " + " & ".join(CONDITIONS) + r" \\", r"\midrule",
    ]
    for h in HEURISTICS:
        for gold in ("entailment", "non-entailment"):
            for sc in sorted(df.loc[(df.heuristic == h) & (df.gold == gold), "subcase"].unique()):
                part = df[df.subcase == sc]
                accs = " & ".join(f"{int(part[f'ok_{c}'].sum())}" for c in CONDITIONS)
                lines.append(f"{'E' if gold == 'entailment' else 'N'} & {tex_escape(sc)} & {accs} \\\\")
        lines.append(r"\midrule" if h != HEURISTICS[-1] else r"\bottomrule")
    lines += [
        r"\end{tabular}",
        r"\caption{Correct predictions out of 10 per HANS subcase. E/N: gold entailment / non-entailment.}",
        r"\label{tab:subcase}", r"\end{table}",
    ]
    return "\n".join(lines) + "\n"


# --------------------------------------------------------------------------- figure
def figure(grid, out_base, model_name):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    panels = [
        ("Heuristic-consistent\n(gold: entailment)", lambda c, h: grid[c]["consistent"][h], "accuracy"),
        ("Heuristic-conflicting\n(gold: non-entailment)", lambda c, h: grid[c]["conflicting"][h], "accuracy"),
        ("Non-entailment predictions\n(all items)", lambda c, h: grid[c]["nonent_rate_by_heuristic"][h], "rate"),
    ]
    plt.rcParams.update({"font.family": "sans-serif", "font.size": 8, "axes.edgecolor": AXIS,
                         "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2})
    fig, axes = plt.subplots(1, 3, figsize=(6.6, 2.3), sharey=True)
    width = 0.19
    x = np.arange(len(HEURISTICS))
    for ax, (title, getter, kind) in zip(axes, panels):
        for k, c in enumerate(CONDITIONS):
            vals = [getter(c, h) for h in HEURISTICS]
            mean = np.array([v[0] for v in vals]) * 100
            err = np.array([[v[0] - v[1], v[2] - v[0]] for v in vals]).T * 100
            ax.bar(x + (k - 1.5) * width, mean, width, color=COLORS[c], edgecolor="white", linewidth=0.8,
                   label=f"{c} {CONDITION_NAMES[c]}", zorder=2)
            ax.errorbar(x + (k - 1.5) * width, mean, yerr=err, fmt="none", ecolor=INK2, elinewidth=0.6,
                        capsize=1.5, zorder=3)
        ax.axhline(50, color=MUTED, linewidth=0.6, linestyle=(0, (3, 3)), zorder=1)
        ax.set_xticks(x, [HEURISTIC_SHORT[h] for h in HEURISTICS])
        ax.set_title(title, fontsize=8, color=INK)
        ax.set_ylim(0, 100)
        ax.yaxis.grid(True, color=GRID, linewidth=0.5, zorder=0)
        ax.set_axisbelow(True)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        ax.tick_params(length=0)
    axes[0].set_ylabel("% of items")
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", ncol=4, frameon=False, bbox_to_anchor=(0.5, 1.04),
               fontsize=7.5, handlelength=1.0, columnspacing=1.2)
    fig.tight_layout(rect=(0, 0, 1, 0.9))
    fig.savefig(out_base + ".pdf", bbox_inches="tight")
    fig.savefig(out_base + ".png", dpi=200, bbox_inches="tight")
    plt.close(fig)


# ------------------------------------------------------------------------- examples
def fmt_example(r, conds):
    lines = [f"**{r['item_id']}** · {r['heuristic']} / {r['subcase']} · gold: **{r['gold']}**",
             f"- Premise: {r['premise']}", f"- Hypothesis: {r['hypothesis']}"]
    for c in conds:
        mark = "correct" if r[f"ok_{c}"] else "WRONG"
        text = r[f"out_{c}"].replace("\n", " / ")
        lines.append(f"- {c} ({r[f'pred_{c}']}, {mark}): {text}")
    return "\n".join(lines)


def flips(df, k=5):
    rng = random.Random(SEED)
    improved = df[(df.ok_P2 == 0) & (df.ok_P3 == 1)]
    worsened = df[(df.ok_P2 == 1) & (df.ok_P3 == 0)]
    out = ["# P2 -> P3 flips (random sample, seed 42)", "",
           f"Improved (P2 wrong, P3 right): {len(improved)} items. Worsened (P2 right, P3 wrong): {len(worsened)} items.",
           "Up to %d of each, drawn uniformly at random from the item list in file order." % k, ""]
    for title, part in (("Improved", improved), ("Worsened", worsened)):
        out.append(f"## {title}\n")
        ids = list(part.item_id)
        for item_id in sorted(rng.sample(ids, min(k, len(ids))), key=ids.index):
            out.append(fmt_example(part[part.item_id == item_id].iloc[0], ["P2", "P3"]) + "\n")
    return "\n".join(out)


def random_examples(df, k=8):
    rng = random.Random(SEED)
    ids = list(df.item_id)
    picked = sorted(rng.sample(ids, k), key=ids.index)
    out = ["# Randomly sampled items (seed 42), all four prompts", ""]
    for item_id in picked:
        out.append(fmt_example(df[df.item_id == item_id].iloc[0], CONDITIONS) + "\n")
    return "\n".join(out)


def annotation_sheet(df):
    """45 P3 explanations: 15 per heuristic (8 conflicting + 7 consistent), seed 42."""
    rng = random.Random(SEED)
    rows = []
    for h in HEURISTICS:
        for gold, n in (("non-entailment", 8), ("entailment", 7)):
            ids = list(df.loc[(df.heuristic == h) & (df.gold == gold), "item_id"])
            rows += sorted(rng.sample(ids, n), key=ids.index)
    sheet = df.set_index("item_id").loc[rows].reset_index()
    sheet = sheet[["item_id", "heuristic", "subcase", "gold", "premise", "hypothesis", "out_P3", "pred_P3", "ok_P3"]]
    sheet = sheet.rename(columns={"out_P3": "P3_output", "pred_P3": "P3_label", "ok_P3": "P3_correct"})
    # Filled in by hand (Y/N, or NA if the explanation does not mention roles at all):
    sheet["roles_correct"] = ""        # agent/patient and clause structure described correctly?
    sheet["label_follows"] = ""        # does the final label follow from the explanation?
    sheet["notes"] = ""
    return sheet


# ----------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", default="qwen2.5-3b-instruct")
    ap.add_argument("--pred", default=None, help="default: results/<tag>/predictions.jsonl")
    ap.add_argument("--data", default=os.path.join("data", "hans_eval_sample300.jsonl"))
    ap.add_argument("--out_dir", default=None, help="default: results/<tag>/analysis")
    args = ap.parse_args()

    pred_path = args.pred or os.path.join("results", args.tag, "predictions.jsonl")
    out_dir = args.out_dir or os.path.join(os.path.dirname(pred_path), "analysis")
    os.makedirs(out_dir, exist_ok=True)
    meta_path = os.path.join(os.path.dirname(pred_path), "run_meta_eval.json")
    model_name = json.load(open(meta_path, encoding="utf-8"))["model"] if os.path.exists(meta_path) else args.tag

    df = load(pred_path, args.data)
    grid = accuracy_grid(df)
    tests = [{"a": a, "b": b, "subset": s, "role": role, **paired(subset(df, s), a, b)}
             for a, b, s, role in COMPARISONS]
    h2 = h2_test(df)
    ne_shift = paired(df, "P3", "P2", metric="ne")

    h1 = tests[0]
    h1_supported = h1["lo"] > 0
    h2_supported = h2["lo"] > 0

    df.to_csv(os.path.join(out_dir, "item_level.csv"), index=False, encoding="utf-8-sig")
    for name, text in (("table_main.tex", table_main(grid, model_name)),
                       ("table_tests.tex", table_tests(tests, h2)),
                       ("table_subcase.tex", table_subcase(df)),
                       ("flips_P2_P3.md", flips(df)),
                       ("random_examples.md", random_examples(df))):
        with open(os.path.join(out_dir, name), "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
    annotation_sheet(df).to_csv(os.path.join(out_dir, "annotation_sheet_P3.csv"), index=False, encoding="utf-8-sig")
    figure(grid, os.path.join(out_dir, "fig_accuracy"), model_name)

    import platform

    import matplotlib
    import scipy
    versions = {"python": platform.python_version(), "numpy": np.__version__, "pandas": pd.__version__,
                "scipy": scipy.__version__, "matplotlib": matplotlib.__version__}
    summary = {"model": model_name, "analysis_env": versions, "n_items": int(len(df)), "n_boot": N_BOOT, "seed": SEED,
               "accuracy": grid, "tests": tests, "h2": h2, "nonent_shift_P3_minus_P2": ne_shift,
               "h1_supported": h1_supported, "h2_supported": h2_supported}
    with open(os.path.join(out_dir, "summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    md = [f"# Results: {model_name}", "",
          "Accuracy in %, [95% stratified bootstrap CI]. Conflicting = gold non-entailment; consistent = gold entailment.", "",
          "| Prompt | Conflicting | Consistent | Overall | Non-ent. predicted | Invalid | Overall (lenient parse) | Mean new tokens | Hit 128 | Label first |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    for c in CONDITIONS:
        g = grid[c]
        cell = lambda v: f"{pct(v[0])} [{pct(v[1])}, {pct(v[2])}]"
        md.append(f"| {c} {CONDITION_NAMES[c]} | {cell(g['conflicting']['all'])} | {cell(g['consistent']['all'])} | "
                  f"{cell(g['overall'])} | {cell(g['nonent_rate'])} | {g['invalid']} | {pct(g['overall_lenient'])} | "
                  f"{g['mean_new_tokens']:.1f} | {g['hit_max']} | {pct(g['label_first_rate'])} |")
    md += ["", "## By heuristic (accuracy %)", "", "| Prompt | " + " | ".join(
        f"{HEURISTIC_SHORT[h]} confl." for h in HEURISTICS) + " | " + " | ".join(
        f"{HEURISTIC_SHORT[h]} cons." for h in HEURISTICS) + " |", "|---" * 7 + "|"]
    for c in CONDITIONS:
        g = grid[c]
        md.append(f"| {c} | " + " | ".join(pct(g["conflicting"][h][0]) for h in HEURISTICS) + " | "
                  + " | ".join(pct(g["consistent"][h][0]) for h in HEURISTICS) + " |")
    md += ["", "## Paired comparisons (percentage points)", "",
           "| Comparison | Subset | Role | Diff | 95% CI | first right & second wrong / reverse | McNemar p |",
           "|---|---|---|---|---|---|---|"]
    for t in tests:
        md.append(f"| {t['a']}-{t['b']} | {t['subset']} | {t['role']} | {100 * t['diff']:+.1f} | "
                  f"[{100 * t['lo']:+.1f}, {100 * t['hi']:+.1f}] | {t['gain']}/{t['loss']} | {t['mcnemar_p']:.3f} |")
    md += ["", f"Shift in non-entailment prediction rate, P3-P2 (all items): {100 * ne_shift['diff']:+.1f} pp "
               f"[{100 * ne_shift['lo']:+.1f}, {100 * ne_shift['hi']:+.1f}]", "",
           "## Hypotheses", "",
           f"- **H1** (P3 > P2 on conflicting items): diff {100 * h1['diff']:+.1f} pp, CI "
           f"[{100 * h1['lo']:+.1f}, {100 * h1['hi']:+.1f}] -> "
           + ("**supported** (CI entirely above zero)" if h1_supported else "**not supported** (CI includes or is below zero)"),
           f"- **H2** (exploratory; LO gain minus mean SUB/CON gain): {100 * h2['stat']:+.1f} pp, CI "
           f"[{100 * h2['lo']:+.1f}, {100 * h2['hi']:+.1f}] -> "
           + ("CI entirely above zero" if h2_supported else "CI includes or is below zero"),
           "  - P3-P2 gain on conflicting items by heuristic: " + ", ".join(
               f"{HEURISTIC_SHORT[h]} {100 * v[0]:+.1f} [{100 * v[1]:+.1f}, {100 * v[2]:+.1f}]"
               for h, v in h2["per_heuristic"].items()), ""]
    with open(os.path.join(out_dir, "summary.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(md) + "\n")
    print("\n".join(md))
    print(f"\nwrote analysis files to {out_dir}")


if __name__ == "__main__":
    main()

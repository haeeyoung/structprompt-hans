"""POST-HOC signal-detection analysis (exploratory; not pre-registered in the HW1 proposal).

Separates discrimination (d') from response bias (c) for each prompt, with Entailment as the signal:
    H  = P(pred = Entailment | gold = Entailment)        hit rate
    F  = P(pred = Entailment | gold = Non-entailment)    false-alarm rate
    d' = z(H) - z(F)                                     discrimination (higher = better)
    c  = -(z(H) + z(F)) / 2                              bias: c > 0 toward Non-entailment, c < 0 toward Entailment
Invalid outputs (no parseable final label) are excluded per prompt and counted.
Every rate uses the log-linear correction of Hautus (1995), (count + 0.5) / (n + 1), in every condition.
CIs: 2,000 bootstrap resamples stratified by HANS subcase, numpy default_rng(0), percentile 95%.
Paired differences reuse the same item resamples for both prompts.

    python sdt_analysis.py --tag qwen2.5-3b-instruct

Reads   results/<tag>/predictions.jsonl
Writes  results/<tag>/analysis/sdt_summary.md, sdt_summary.json, table_sdt.tex
"""
import argparse
import json
import os
import sys

import numpy as np
from scipy.stats import norm

from analyze import boot_indices, load
from prompts import CONDITION_NAMES, CONDITIONS

N_BOOT = 2000
SEED = 0
CONTRASTS = [("P3", "P2"), ("P3", "P4"), ("P3", "P1"), ("P2", "P1")]
NOTE = ("POST-HOC (exploratory): added after the results were seen; not pre-registered in the HW1 proposal.")
SIGN = "c > 0 = bias toward Non-entailment; c < 0 = bias toward Entailment; c = 0 = unbiased"


def sdt(gold_e, pred_e, valid, idx=None):
    """d', c, corrected H and F. With idx of shape (B, n), returns arrays over resamples."""
    if idx is not None:
        gold_e, pred_e, valid = gold_e[idx], pred_e[idx], valid[idx]
    signal, noise = gold_e & valid, ~gold_e & valid
    h = ((pred_e & signal).sum(-1) + 0.5) / (signal.sum(-1) + 1)
    f = ((pred_e & noise).sum(-1) + 0.5) / (noise.sum(-1) + 1)
    zh, zf = norm.ppf(h), norm.ppf(f)
    return zh - zf, -(zh + zf) / 2, h, f


def ci(values):
    lo, hi = np.percentile(values, [2.5, 97.5])
    return float(lo), float(hi)


def fmt(point, interval, digits=2):
    return f"{point:+.{digits}f} [{interval[0]:+.{digits}f}, {interval[1]:+.{digits}f}]"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", default="qwen2.5-3b-instruct")
    ap.add_argument("--data", default=os.path.join("data", "hans_eval_sample300.jsonl"))
    ap.add_argument("--seed", type=int, default=SEED)
    args = ap.parse_args()

    pred_path = os.path.join("results", args.tag, "predictions.jsonl")
    out_dir = os.path.join("results", args.tag, "analysis")
    os.makedirs(out_dir, exist_ok=True)
    meta_path = os.path.join("results", args.tag, "run_meta_eval.json")
    model = json.load(open(meta_path, encoding="utf-8"))["model"] if os.path.exists(meta_path) else args.tag

    df = load(pred_path, args.data)
    gold_e = df["gold"].eq("entailment").to_numpy()
    idx = boot_indices(df["subcase"], seed=args.seed, n_boot=N_BOOT)

    per, boot = {}, {}
    for c in CONDITIONS:
        pred = df[f"pred_{c}"]
        pred_e, valid = pred.eq("entailment").to_numpy(), pred.ne("invalid").to_numpy()
        d, cc, h, f = sdt(gold_e, pred_e, valid)
        d_b, c_b, _, _ = sdt(gold_e, pred_e, valid, idx)
        boot[c] = (d_b, c_b)
        per[c] = {
            "valid_gold_E": int((gold_e & valid).sum()), "valid_gold_N": int((~gold_e & valid).sum()),
            "excluded_invalid": int((~valid).sum()),
            "excluded_gold_E": int((gold_e & ~valid).sum()), "excluded_gold_N": int((~gold_e & ~valid).sum()),
            "hits": int((pred_e & gold_e & valid).sum()), "false_alarms": int((pred_e & ~gold_e & valid).sum()),
            "H_corrected": float(h), "F_corrected": float(f),
            "d_prime": float(d), "d_prime_ci": ci(d_b), "c": float(cc), "c_ci": ci(c_b),
        }
    contrasts = []
    for a, b in CONTRASTS:
        dd, dc = boot[a][0] - boot[b][0], boot[a][1] - boot[b][1]
        contrasts.append({
            "contrast": f"{a}-{b}",
            "delta_d_prime": per[a]["d_prime"] - per[b]["d_prime"], "delta_d_prime_ci": ci(dd),
            "delta_c": per[a]["c"] - per[b]["c"], "delta_c_ci": ci(dc),
        })

    definitions = {
        "signal": "Entailment",
        "H": "P(pred=Entailment | gold=Entailment)", "F": "P(pred=Entailment | gold=Non-entailment)",
        "d_prime": "z(H) - z(F)", "c": "-(z(H) + z(F)) / 2", "c_sign": SIGN,
        "correction": "log-linear (Hautus, 1995): (count + 0.5) / (n + 1), all conditions",
        "invalid": "outputs without a parseable final label are excluded per prompt",
        "bootstrap": f"{N_BOOT} resamples stratified by HANS subcase, numpy default_rng({args.seed}), "
                     "percentile 95% CI; paired contrasts reuse the same resamples",
    }
    with open(os.path.join(out_dir, "sdt_summary.json"), "w", encoding="utf-8") as fh:
        json.dump({"post_hoc": True, "note": NOTE, "model": model, "definitions": definitions,
                   "seed": args.seed, "n_boot": N_BOOT, "per_prompt": per, "contrasts": contrasts}, fh, indent=2)

    md = [
        f"# POST-HOC signal-detection analysis: {model}", "",
        f"> **{NOTE}**", "",
        "- Signal = Entailment. H = P(pred=E | gold=E); F = P(pred=E | gold=N).",
        "- d' = z(H) − z(F): discrimination, higher is better.",
        f"- c = −(z(H) + z(F)) / 2: **{SIGN}**.",
        "- Invalid outputs are excluded per prompt (counts below).",
        "- Log-linear correction (Hautus, 1995): every rate is (count + 0.5) / (n + 1), in every condition.",
        f"- 95% CIs: {N_BOOT} bootstrap resamples stratified by HANS subcase, numpy default_rng({args.seed}); "
        "paired contrasts reuse the same resamples for both prompts.", "",
        "## Per prompt", "",
        "| Prompt | Valid gold E / N | Excluded invalid (gold E / N) | Hits: pred E, gold E | "
        "False alarms: pred E, gold N | H (corr.) | F (corr.) | d' [95% CI] | c [95% CI] |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for c in CONDITIONS:
        p = per[c]
        md.append(f"| {c} {CONDITION_NAMES[c]} | {p['valid_gold_E']} / {p['valid_gold_N']} | "
                  f"{p['excluded_invalid']} ({p['excluded_gold_E']} / {p['excluded_gold_N']}) | "
                  f"{p['hits']}/{p['valid_gold_E']} | {p['false_alarms']}/{p['valid_gold_N']} | "
                  f"{p['H_corrected']:.3f} | {p['F_corrected']:.3f} | "
                  f"{fmt(p['d_prime'], p['d_prime_ci'])} | {fmt(p['c'], p['c_ci'])} |")
    md += ["", "## Paired contrasts (first prompt minus second)", "",
           "Δc < 0: the first prompt is less biased toward Non-entailment than the second (or more toward Entailment).", "",
           "| Contrast | Δd' [95% CI] | Δc [95% CI] |", "|---|---|---|"]
    for t in contrasts:
        md.append(f"| {t['contrast']} | {fmt(t['delta_d_prime'], t['delta_d_prime_ci'])} | "
                  f"{fmt(t['delta_c'], t['delta_c_ci'])} |")
    with open(os.path.join(out_dir, "sdt_summary.md"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(md) + "\n")

    tex = [
        r"\begin{table}[t]", r"\centering", r"\small",
        r"\begin{tabular}{lrcc}", r"\toprule",
        r"Prompt & Excl. & $d'$ [95\% CI] & $c$ [95\% CI] \\", r"\midrule",
    ]
    for c in CONDITIONS:
        p = per[c]
        tex.append(f"{c} {CONDITION_NAMES[c]} & {p['excluded_invalid']} & "
                   f"{fmt(p['d_prime'], p['d_prime_ci'])} & {fmt(p['c'], p['c_ci'])} \\\\")
    tex += [r"\midrule", r"Contrast & & $\Delta d'$ [95\% CI] & $\Delta c$ [95\% CI] \\", r"\midrule"]
    for t in contrasts:
        tex.append(f"{t['contrast'].replace('-', '$-$')} & & {fmt(t['delta_d_prime'], t['delta_d_prime_ci'])} & "
                   f"{fmt(t['delta_c'], t['delta_c_ci'])} \\\\")
    tex += [
        r"\bottomrule", r"\end{tabular}",
        r"\caption{\textbf{Post-hoc} signal-detection analysis with Entailment as the signal: "
        r"$H = P(\hat{y}{=}\mathrm{E}\mid y{=}\mathrm{E})$, $F = P(\hat{y}{=}\mathrm{E}\mid y{=}\mathrm{N})$, "
        r"$d' = z(H) - z(F)$, $c = -\tfrac{1}{2}(z(H) + z(F))$; $c > 0$ indicates a bias toward Non-entailment. "
        r"Invalid outputs are excluded (Excl.). Rates use the log-linear correction of \citet{hautus1995corrections}. "
        rf"CIs: {N_BOOT} paired bootstrap resamples stratified by HANS subcase.}}",
        r"\label{tab:sdt}", r"\end{table}",
    ]
    with open(os.path.join(out_dir, "table_sdt.tex"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(tex) + "\n")
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # Windows consoles default to cp1252
    print("\n".join(md))


if __name__ == "__main__":
    main()

"""Exploratory post-hoc analysis (Section 6 of the paper): how often explanations
frame the hypothesis as a reduced copy of the premise, and how accurate those
items are. The cue list was defined AFTER reading sampled outputs, so this is
reported as exploratory.

Usage:
    python extra_analysis.py results/qwen2.5-3b-instruct/predictions.jsonl
"""
import re
import sys

import pandas as pd

CUE = re.compile(r"simplif|subset|omit", re.IGNORECASE)

d = pd.read_json(sys.argv[1], lines=True)
d["correct"] = d["pred"] == d["gold"]
d["cue"] = d["output"].str.contains(CUE)
rows = []
for c in ["P2", "P3", "P4"]:
    s = d[d.condition == c]
    conf = s[s.gold == "non-entailment"]
    rows.append({
        "condition": c,
        "cue_rate_%": round(100 * s.cue.mean(), 1),
        "pred_E_given_cue_%": round(100 * (s[s.cue].pred == "entailment").mean(), 1),
        "conf_n_cue": int(conf.cue.sum()),
        "conf_acc_cue_%": round(100 * conf[conf.cue].correct.mean(), 1),
        "conf_n_nocue": int((~conf.cue).sum()),
        "conf_acc_nocue_%": round(100 * conf[~conf.cue].correct.mean(), 1),
    })
print(pd.DataFrame(rows).to_string(index=False))

# --- Secondary contrast cited in Discussion: P4 - P2 on all items ---
import numpy as np
from scipy.stats import binomtest

d["c"] = d["correct"].astype(int)
w = d.pivot_table(index=["item_id", "subcase"], columns="condition", values="c").reset_index()
x = (w["P4"] - w["P2"]).to_numpy(float)
strata = w["subcase"].to_numpy()
groups = [np.where(strata == u)[0] for u in np.unique(strata)]
rng = np.random.default_rng(42)
bs = [x[np.concatenate([rng.choice(g, len(g)) for g in groups])].mean() for _ in range(2000)]
n01 = int(((w.P4 == 1) & (w.P2 == 0)).sum()); n10 = int(((w.P4 == 0) & (w.P2 == 1)).sum())
lo, hi = np.percentile(bs, [2.5, 97.5])
print(f"\nP4-P2 (all items): {100*x.mean():+.1f} pp, 95% CI [{100*lo:+.1f}, {100*hi:+.1f}], "
      f"+/- {n01}/{n10}, McNemar p={binomtest(n01, n01+n10).pvalue:.3f}")

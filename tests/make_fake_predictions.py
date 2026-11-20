"""Write synthetic predictions so analyze.py can be tested without a GPU.

    python tests/make_fake_predictions.py
    python analyze.py --pred results/_fake/predictions.jsonl

The numbers mean nothing; they only exercise every code path (including
invalid outputs and markdown-formatted labels).
"""
import json
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import read_jsonl  # noqa: E402

# P(predict entailment | condition, gold)
P_ENT = {
    "P1": {"entailment": 0.97, "non-entailment": 0.85},
    "P2": {"entailment": 0.90, "non-entailment": 0.65},
    "P3": {"entailment": 0.85, "non-entailment": 0.45},
    "P4": {"entailment": 0.92, "non-entailment": 0.70},
}
P_INVALID = 0.02
TEMPLATES = ["Final label: {}", "The roles stay the same.\nFinal label: {}", "**Final label:** {}",
             "Final label: {}\n\nThe premise and hypothesis share their words."]


def main():
    rng = random.Random(0)
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    items = read_jsonl(os.path.join(root, "data", "hans_eval_sample300.jsonl"))
    out_dir = os.path.join(root, "results", "_fake")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "predictions.jsonl"), "w", encoding="utf-8", newline="\n") as f:
        for c, probs in P_ENT.items():
            for it in items:
                if rng.random() < P_INVALID:
                    text = "I cannot determine this."
                else:
                    label = "Entailment" if rng.random() < probs[it["gold"]] else "Non-entailment"
                    text = rng.choice(TEMPLATES).format(label)
                f.write(json.dumps({
                    "item_id": it["item_id"], "condition": c, "heuristic": it["heuristic"],
                    "subcase": it["subcase"], "gold": it["gold"], "premise": it["premise"],
                    "hypothesis": it["hypothesis"], "output": text, "pred": None,
                    "n_prompt_tokens": 100, "n_new_tokens": 5 if c == "P1" else 60, "hit_max": False,
                }) + "\n")
    print(f"wrote {out_dir}/predictions.jsonl")


if __name__ == "__main__":
    main()

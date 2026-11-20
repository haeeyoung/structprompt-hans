"""Measure instruction and full-prompt token lengths with the model tokenizer.

The proposal requires P4 (nonstructural control) to be approximately
length-matched to P3 (structure-aware) in instruction tokens.

    python check_prompts.py --tag qwen2.5-3b-instruct
"""
import argparse
import json
import os
import statistics

from transformers import AutoTokenizer

from common import MODELS, read_jsonl
from prompts import CONDITIONS, INSTRUCTIONS, build_messages


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", default="qwen2.5-3b-instruct", choices=sorted(MODELS))
    ap.add_argument("--data", default=os.path.join("data", "hans_eval_sample300.jsonl"))
    args = ap.parse_args()

    name, revision = MODELS[args.tag]
    tok = AutoTokenizer.from_pretrained(name, revision=revision)
    items = read_jsonl(args.data)

    report = {"model": name, "revision": revision, "instruction_tokens": {}, "prompt_tokens_mean": {}}
    print(f"tokenizer: {name}@{revision[:8]}\n")
    print("instruction-only token counts")
    for c in CONDITIONS:
        n = len(tok(INSTRUCTIONS[c], add_special_tokens=False)["input_ids"])
        report["instruction_tokens"][c] = n
        print(f"  {c}: {n:3d}  {INSTRUCTIONS[c]}")
    gap = report["instruction_tokens"]["P4"] - report["instruction_tokens"]["P3"]
    report["p4_minus_p3"] = gap
    print(f"\nP4 - P3 instruction tokens: {gap:+d}")

    print("\nmean full prompt length (chat template applied), evaluation set")
    for c in CONDITIONS:
        lens = [
            len(tok.apply_chat_template(build_messages(it["premise"], it["hypothesis"], c),
                                        add_generation_prompt=True, tokenize=True))
            for it in items
        ]
        report["prompt_tokens_mean"][c] = round(statistics.mean(lens), 1)
        print(f"  {c}: {statistics.mean(lens):.1f} (min {min(lens)}, max {max(lens)})")

    example = tok.apply_chat_template(build_messages(items[0]["premise"], items[0]["hypothesis"], "P3"),
                                      add_generation_prompt=True, tokenize=False)
    print("\nexample formatted prompt (P3, first item):\n" + example)

    out = os.path.join("results", args.tag, "prompt_lengths.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()

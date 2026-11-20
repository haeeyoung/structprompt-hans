"""Check that run_inference.py decodes with plain greedy search: argmax at every step,
no repetition penalty or sampling warpers. Also reports whether batching with left
padding changes any output (informational; small float16 differences are possible).

Uses the same checkpoint, dtype and generation settings as run_inference.py. The
reference decoder is a hand-written argmax loop that reuses the KV cache, so it runs
the same forward computations as generate() and differs only in logit processing.

    python tests/check_greedy.py --tag qwen2.5-3b-instruct      # writes results/<tag>/greedy_check.json
"""
import argparse
import json
import os
import sys

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import MODELS, read_jsonl  # noqa: E402
from prompts import CONDITIONS, build_messages  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", default="qwen2.5-3b-instruct", choices=sorted(MODELS))
    ap.add_argument("--max_new_tokens", type=int, default=128)
    ap.add_argument("--dtype", default="auto", choices=["auto", "float16", "bfloat16", "float32"])
    args = ap.parse_args()

    name, revision = MODELS[args.tag]
    device = "cuda" if torch.cuda.is_available() else "cpu"
    dtype = {"auto": torch.float16 if device == "cuda" else torch.float32,
             "float16": torch.float16, "bfloat16": torch.bfloat16, "float32": torch.float32}[args.dtype]
    tok = AutoTokenizer.from_pretrained(name, revision=revision, padding_side="left")
    model = AutoModelForCausalLM.from_pretrained(name, revision=revision, dtype=dtype).to(device).eval()

    gc = model.generation_config  # identical overrides to run_inference.py
    gc.do_sample, gc.num_beams, gc.temperature, gc.top_p, gc.top_k = False, 1, None, None, None
    gc.repetition_penalty, gc.max_new_tokens, gc.pad_token_id = 1.0, args.max_new_tokens, tok.pad_token_id
    eos = set(gc.eos_token_id if isinstance(gc.eos_token_id, list) else [gc.eos_token_id])

    # Two pilot pairs per condition (pilot pairs come from the HANS training file).
    items = read_jsonl(os.path.join("data", "hans_pilot12.jsonl"))
    cases = [(items[k], c) for c in CONDITIONS for k in (CONDITIONS.index(c), CONDITIONS.index(c) + 6)]
    prompts = [tok.apply_chat_template(build_messages(it["premise"], it["hypothesis"], c),
                                       add_generation_prompt=True, tokenize=False) for it, c in cases]

    def trim(ids):
        ids = ids.tolist()
        return ids[: next((k for k, t in enumerate(ids) if t in eos), len(ids))]

    def manual_greedy(prompt):
        ids = tok(prompt, return_tensors="pt", add_special_tokens=False)["input_ids"].to(device)
        out, past, step_in = [], None, ids
        for _ in range(args.max_new_tokens):
            res = model(input_ids=step_in, past_key_values=past, use_cache=True)
            nxt = int(res.logits[0, -1].argmax())
            if nxt in eos:
                break
            out.append(nxt)
            past, step_in = res.past_key_values, torch.tensor([[nxt]], device=device)
        return out

    rows = []
    with torch.inference_mode():
        for (it, c), prompt in zip(cases, prompts):
            enc = tok(prompt, return_tensors="pt", add_special_tokens=False).to(device)
            single = trim(model.generate(**enc, generation_config=gc)[0, enc["input_ids"].shape[1]:].cpu())
            rows.append({"item_id": it["item_id"], "condition": c, "manual": manual_greedy(prompt), "single": single})
        enc = tok(prompts, return_tensors="pt", padding=True, add_special_tokens=False).to(device)
        gen = model.generate(**enc, generation_config=gc)[:, enc["input_ids"].shape[1]:].cpu()
        for row, ids in zip(rows, gen):
            row["batched"] = trim(ids)

    report = {"model": name, "revision": revision, "dtype": str(dtype), "device": device,
              "gpu": torch.cuda.get_device_name(0) if device == "cuda" else None,
              "repetition_penalty": gc.repetition_penalty, "cases": []}
    for r in rows:
        case = {"item_id": r["item_id"], "condition": r["condition"],
                "generate_equals_manual_argmax": r["single"] == r["manual"],
                "batched_equals_single": r["batched"] == r["single"],
                "output": tok.decode(r["single"], skip_special_tokens=True)}
        report["cases"].append(case)
        print(f"{r['condition']} {r['item_id']:<18} generate==argmax: {case['generate_equals_manual_argmax']!s:<5} "
              f"batched==single: {case['batched_equals_single']}")
    report["greedy_ok"] = all(c["generate_equals_manual_argmax"] for c in report["cases"])
    report["batched_matches"] = sum(c["batched_equals_single"] for c in report["cases"])

    out = os.path.join("results", args.tag, "greedy_check.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print(("greedy check PASSED" if report["greedy_ok"] else "greedy check FAILED")
          + f"; batched output identical for {report['batched_matches']}/{len(rows)} prompts; wrote {out}")


if __name__ == "__main__":
    main()

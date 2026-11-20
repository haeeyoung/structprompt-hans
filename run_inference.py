"""Run every (item, condition) pair through the model and save raw outputs.

Each item is its own single-turn conversation; the model never sees other items.
Decoding is greedy (no sampling, no repetition penalty) with at most 128 new tokens.
Output is appended after every batch, so an interrupted run resumes where it stopped.

    python run_inference.py --tag qwen2.5-3b-instruct --split pilot   # format check, 48 calls
    python run_inference.py --tag qwen2.5-3b-instruct --split eval    # main run, 1,200 calls
"""
import argparse
import json
import os
import platform
import time
from collections import Counter, defaultdict

import accelerate
import torch
import transformers
from transformers import AutoModelForCausalLM, AutoTokenizer

from common import MODELS, parse_label, read_jsonl
from prompts import CONDITIONS, build_messages

SPLITS = {
    "eval": (os.path.join("data", "hans_eval_sample300.jsonl"), "predictions.jsonl"),
    "pilot": (os.path.join("data", "hans_pilot12.jsonl"), "pilot_predictions.jsonl"),
}


def load_done(path):
    if not os.path.exists(path):
        return set()
    with open(path, encoding="utf-8") as f:
        return {(r["item_id"], r["condition"]) for r in map(json.loads, filter(str.strip, f))}


def summarize(path):
    rows = read_jsonl(path)
    by_cond = defaultdict(list)
    for r in rows:
        by_cond[r["condition"]].append(r)
    print(f"\nsummary of {path}")
    print("  cond     n  valid  hit_max  mean_new_tok  label counts")
    for c in CONDITIONS:
        rs = by_cond.get(c, [])
        if not rs:
            continue
        labels = Counter(parse_label(r["output"]) for r in rs)
        valid = sum(v for k, v in labels.items() if k is not None)
        mean_tok = sum(r["n_new_tokens"] for r in rs) / len(rs)
        print(f"  {c}  {len(rs):5d}  {valid:5d}  {sum(r['hit_max'] for r in rs):7d}  {mean_tok:12.1f}  "
              f"{dict(labels)}")
        if valid < 0.9 * len(rs):
            print(f"  WARNING: {c} has many unparseable outputs; inspect them before the main run.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", default="qwen2.5-3b-instruct", choices=sorted(MODELS))
    ap.add_argument("--split", default="eval", choices=sorted(SPLITS))
    ap.add_argument("--conditions", default=",".join(CONDITIONS))
    ap.add_argument("--batch_size", type=int, default=16)
    ap.add_argument("--max_new_tokens", type=int, default=128)
    ap.add_argument("--dtype", default="auto", choices=["auto", "float16", "bfloat16", "float32"],
                    help="auto = float16 on GPU, float32 on CPU")
    ap.add_argument("--limit", type=int, default=None, help="only the first N items (smoke tests)")
    ap.add_argument("--out_dir", default=None, help="default: results/<tag>")
    args = ap.parse_args()

    name, revision = MODELS[args.tag]
    data_path, out_name = SPLITS[args.split]
    out_dir = args.out_dir or os.path.join("results", args.tag)
    out_path = os.path.join(out_dir, out_name)
    os.makedirs(out_dir, exist_ok=True)

    items = read_jsonl(data_path)[: args.limit]
    conditions = args.conditions.split(",")
    done = load_done(out_path)
    todo = [(it, c) for c in conditions for it in items if (it["item_id"], c) not in done]
    print(f"{len(items)} items x {len(conditions)} conditions; {len(done)} already done, {len(todo)} to run")
    if not todo:
        summarize(out_path)
        return

    device = "cuda" if torch.cuda.is_available() else "cpu"
    dtype = {"auto": torch.float16 if device == "cuda" else torch.float32,
             "float16": torch.float16, "bfloat16": torch.bfloat16, "float32": torch.float32}[args.dtype]
    torch.manual_seed(0)

    tok = AutoTokenizer.from_pretrained(name, revision=revision, padding_side="left")
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    model = AutoModelForCausalLM.from_pretrained(name, revision=revision, dtype=dtype).to(device)
    model.eval()

    # Pure greedy decoding. Overwrite the checkpoint's sampling defaults
    # (Qwen2.5 ships temperature/top_p/top_k and repetition_penalty=1.05) so that
    # nothing but argmax decoding is applied.
    gc = model.generation_config
    gc.do_sample = False
    gc.num_beams = 1
    gc.temperature = None
    gc.top_p = None
    gc.top_k = None
    gc.repetition_penalty = 1.0
    gc.max_new_tokens = args.max_new_tokens
    gc.pad_token_id = tok.pad_token_id
    eos_ids = gc.eos_token_id if isinstance(gc.eos_token_id, list) else [gc.eos_token_id]

    meta = {
        "model": name, "revision": revision, "split": args.split, "conditions": conditions,
        "n_items": len(items), "batch_size": args.batch_size, "dtype": str(dtype), "device": device,
        "gpu": torch.cuda.get_device_name(0) if device == "cuda" else None,
        "gpu_memory_gb": round(torch.cuda.get_device_properties(0).total_memory / 2**30, 1) if device == "cuda" else None,
        "cuda": torch.version.cuda,
        "decoding": {k: getattr(gc, k) for k in ("do_sample", "num_beams", "temperature", "top_p", "top_k",
                                                 "repetition_penalty", "max_new_tokens", "eos_token_id",
                                                 "pad_token_id")},
        "torch": torch.__version__, "transformers": transformers.__version__, "accelerate": accelerate.__version__,
        "python": platform.python_version(), "started": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    with open(os.path.join(out_dir, f"run_meta_{args.split}.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, default=str)

    # Batch items of the same condition, ordered by prompt length to limit padding.
    jobs = []
    for it, c in todo:
        prompt = tok.apply_chat_template(build_messages(it["premise"], it["hypothesis"], c),
                                         add_generation_prompt=True, tokenize=False)
        jobs.append((it, c, prompt))
    jobs.sort(key=lambda j: (conditions.index(j[1]), len(j[2])))

    t0 = time.time()
    with open(out_path, "a", encoding="utf-8", newline="\n") as fout:
        for start in range(0, len(jobs), args.batch_size):
            batch = jobs[start: start + args.batch_size]
            enc = tok([j[2] for j in batch], return_tensors="pt", padding=True, add_special_tokens=False).to(device)
            with torch.inference_mode():
                gen = model.generate(**enc, generation_config=gc)
            new = gen[:, enc["input_ids"].shape[1]:].cpu()
            prompt_lens = enc["attention_mask"].sum(dim=1).tolist()
            for (it, c, prompt), row_ids, n_prompt in zip(batch, new, prompt_lens):
                ids = row_ids.tolist()
                stop = next((k for k, t in enumerate(ids) if t in eos_ids), None)
                n_new = stop if stop is not None else len(ids)
                text = tok.decode(ids[:n_new], skip_special_tokens=True).strip()
                fout.write(json.dumps({
                    "item_id": it["item_id"], "condition": c,
                    "heuristic": it["heuristic"], "subcase": it["subcase"], "gold": it["gold"],
                    "premise": it["premise"], "hypothesis": it["hypothesis"],
                    "output": text, "pred": parse_label(text),
                    "n_prompt_tokens": int(n_prompt),
                    "n_new_tokens": n_new, "hit_max": stop is None,
                }, ensure_ascii=False) + "\n")
            fout.flush()
            n_done = start + len(batch)
            rate = (time.time() - t0) / n_done
            print(f"  {n_done}/{len(jobs)}  ({rate:.2f}s per call, ~{rate * (len(jobs) - n_done) / 60:.1f} min left)",
                  flush=True)

    meta["finished"] = time.strftime("%Y-%m-%d %H:%M:%S")
    meta["seconds"] = round(time.time() - t0, 1)
    with open(os.path.join(out_dir, f"run_meta_{args.split}.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, default=str)
    summarize(out_path)


if __name__ == "__main__":
    main()

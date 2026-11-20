"""Build the evaluation sample (300 pairs) and the pilot set (12 pairs) from HANS.

Evaluation: 10 pairs from each of the 30 HANS evaluation subcases (seed 42),
            i.e. 50 entailment + 50 non-entailment pairs per heuristic.
Pilot:      2 pairs per (heuristic, gold label) from the HANS *training* file,
            each from a different subcase, so no pilot pair is an evaluation pair.

    python sample_hans.py            # download HANS (pinned commit) and write data/*.jsonl
    python sample_hans.py --verify   # re-sample and check it matches the committed files
"""
import argparse
import hashlib
import os
import random
import sys
import urllib.request

from common import HEURISTICS, LABELS, detokenize, read_jsonl, write_jsonl

HANS_COMMIT = "7299f6f657089ce06a0f98e7e81f8d0f5b7741ce"  # github.com/tommccoy1/hans
HANS_FILES = {
    "heuristics_evaluation_set.txt": "c55b62feef9913070e88f38938dc2492018c945ac81f70139346472494124e79",
    "heuristics_train_set.txt": "49245bd5fdb0b185dcbfbf48f0f16513c62ad5bc9fad0b8800dc48d6818ee5cf",
}
RAW_DIR = os.path.join("data", "raw")
EVAL_OUT = os.path.join("data", "hans_eval_sample300.jsonl")
PILOT_OUT = os.path.join("data", "hans_pilot12.jsonl")
SEED = 42
PER_SUBCASE = 10


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch(name):
    path = os.path.join(RAW_DIR, name)
    if not os.path.exists(path):
        os.makedirs(RAW_DIR, exist_ok=True)
        url = f"https://raw.githubusercontent.com/tommccoy1/hans/{HANS_COMMIT}/{name}"
        print(f"downloading {url}")
        urllib.request.urlretrieve(url, path)
    digest = sha256(path)
    if digest != HANS_FILES[name]:
        sys.exit(f"checksum mismatch for {path}: {digest}")
    return path


def load_hans(path, split):
    rows = []
    with open(path, encoding="utf-8") as f:
        header = f.readline().rstrip("\n").split("\t")
        for line in f:
            r = dict(zip(header, line.rstrip("\n").split("\t")))
            rows.append({
                "item_id": f"hans-{split}-{r['pairID']}",
                "pairID": r["pairID"],
                "heuristic": r["heuristic"],
                "subcase": r["subcase"],
                "template": r["template"],
                "gold": r["gold_label"],
                "premise": detokenize(r["sentence1"]),
                "hypothesis": detokenize(r["sentence2"]),
            })
    return rows


def pair_num(row):
    return int(row["pairID"].lstrip("ex"))


def sort_key(row):
    return (HEURISTICS.index(row["heuristic"]), LABELS.index(row["gold"]), row["subcase"], pair_num(row))


def sample_eval(rows):
    rng = random.Random(SEED)
    by_subcase = {}
    for r in rows:
        by_subcase.setdefault(r["subcase"], []).append(r)
    picked = []
    for subcase in sorted(by_subcase):
        pool = sorted(by_subcase[subcase], key=pair_num)
        picked.extend(rng.sample(pool, PER_SUBCASE))
    return sorted(picked, key=sort_key)


def sample_pilot(train_rows, eval_rows):
    rng = random.Random(SEED)
    eval_pairs = {(r["premise"], r["hypothesis"]) for r in eval_rows}
    picked = []
    for h in HEURISTICS:
        for lab in LABELS:
            subcases = sorted({r["subcase"] for r in train_rows if r["heuristic"] == h and r["gold"] == lab})
            for subcase in rng.sample(subcases, 2):
                pool = sorted(
                    (r for r in train_rows
                     if r["subcase"] == subcase and (r["premise"], r["hypothesis"]) not in eval_pairs),
                    key=pair_num,
                )
                picked.append(rng.choice(pool))
    return sorted(picked, key=sort_key)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--verify", action="store_true", help="check the committed files instead of writing them")
    args = ap.parse_args()

    eval_all = load_hans(fetch("heuristics_evaluation_set.txt"), "eval")
    train_all = load_hans(fetch("heuristics_train_set.txt"), "train")
    eval_rows = sample_eval(eval_all)
    pilot_rows = sample_pilot(train_all, eval_all)

    assert len(eval_rows) == 300 and len(pilot_rows) == 12
    eval_texts = {(r["premise"], r["hypothesis"]) for r in eval_all}
    assert not any((r["premise"], r["hypothesis"]) in eval_texts for r in pilot_rows)

    if args.verify:
        ok = read_jsonl(EVAL_OUT) == eval_rows and read_jsonl(PILOT_OUT) == pilot_rows
        print("sample matches committed files" if ok else "MISMATCH with committed files")
        sys.exit(0 if ok else 1)

    write_jsonl(EVAL_OUT, eval_rows)
    write_jsonl(PILOT_OUT, pilot_rows)
    print(f"wrote {EVAL_OUT} ({len(eval_rows)}) and {PILOT_OUT} ({len(pilot_rows)})")
    for h in HEURISTICS:
        counts = {lab: sum(r["heuristic"] == h and r["gold"] == lab for r in eval_rows) for lab in LABELS}
        print(f"  {h:16s} {counts}")


if __name__ == "__main__":
    main()

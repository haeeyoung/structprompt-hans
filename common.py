"""Shared helpers: file I/O, HANS text cleanup, model registry, label parsing."""
import json
import os
import re

LABELS = ("entailment", "non-entailment")

# HuggingFace checkpoints used in the paper, pinned to the commit that was
# current when the experiments were set up (2026-11-20).
MODELS = {
    "qwen2.5-3b-instruct": ("Qwen/Qwen2.5-3B-Instruct", "aa8e72537993ba99e69dfaafa59ed015b17504d1"),
    "qwen2.5-1.5b-instruct": ("Qwen/Qwen2.5-1.5B-Instruct", "989aa7980e4cf806f80c7fef2b1adb7bc71aa306"),
    "qwen2.5-0.5b-instruct": ("Qwen/Qwen2.5-0.5B-Instruct", "7ae557604adf67be50417f59c2c2f167def9a775"),
}

HEURISTICS = ("lexical_overlap", "subsequence", "constituent")
HEURISTIC_SHORT = {"lexical_overlap": "LO", "subsequence": "SUB", "constituent": "CON"}


def read_jsonl(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def write_jsonl(path, rows):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def detokenize(s):
    """HANS sentences are whitespace-tokenized ('the doctor .'); restore normal spacing."""
    s = re.sub(r"\s+([.,])", r"\1", s.strip())
    return re.sub(r"\s+", " ", s)


# ---------------------------------------------------------------- label parsing
# Strict rule (primary analysis): the label must follow an explicit "Final label"
# marker. The last such marker in the output wins. Markdown emphasis, quotes and
# brackets around the label are tolerated; anything else counts as invalid.
_DASH = r"[\s\-‐‑‒–—_]*"
_STRICT = re.compile(
    r"final\s*label\s*[:：]?\s*[\*\"'`\[\(\s]*(non" + _DASH + r"entailment|entailment)",
    re.IGNORECASE,
)
# Lenient rule (sensitivity analysis only): last label-like word anywhere.
_LENIENT = re.compile(
    r"(non" + _DASH + r"entailment|not\s+(?:an\s+)?entailment|does\s+not\s+entail|entailment)",
    re.IGNORECASE,
)


def _norm(word):
    w = word.lower()
    return "entailment" if w == "entailment" else "non-entailment"


def parse_label(text):
    """Return 'entailment', 'non-entailment', or None (invalid) under the strict rule."""
    hits = list(_STRICT.finditer(text or ""))
    return _norm(hits[-1].group(1)) if hits else None


def label_first(text):
    """True if the output opens with its final label and explains afterwards, i.e. the
    explanation cannot have informed the label (the prompts ask for the reverse order)."""
    hits = list(_STRICT.finditer(text or ""))
    if not hits:
        return False
    before = text[: hits[-1].start()].strip(" \t\n*#`\"'")
    after = text[hits[-1].end():].strip(" \t\n*`\"'].)")
    return before == "" and after != ""


def parse_label_lenient(text):
    hit = parse_label(text)
    if hit is not None:
        return hit
    hits = list(_LENIENT.finditer(text or ""))
    return _norm(hits[-1].group(1)) if hits else None

"""Label-parsing checks. Run: python tests/test_parse.py"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import detokenize, label_first, parse_label, parse_label_lenient  # noqa: E402

CASES = [
    ("Final label: Entailment", "entailment"),
    ("Final label: Non-entailment", "non-entailment"),
    ("final label: non entailment", "non-entailment"),
    ("Final Label: Nonentailment", "non-entailment"),
    ("**Final label:** Non-entailment", "non-entailment"),
    ("Final label: **Entailment**", "entailment"),
    ("Final label: [Non-entailment]", "non-entailment"),
    ("Final label: 'Entailment'", "entailment"),
    ("Final label: Non‑entailment", "non-entailment"),
    ("The doctor is the agent.\nFinal label: Entailment\n\nFinal label: Non-entailment", "non-entailment"),
    ("The roles are swapped, so this is non-entailment.", None),
    ("Final label: [label]", None),
    ("Final label: Contradiction", None),
    ("", None),
]

LENIENT = [
    ("The roles are swapped, so this is non-entailment.", "non-entailment"),
    ("This is not entailment.", "non-entailment"),
    ("The premise does not entail the hypothesis.", "non-entailment"),
    ("Entailment", "entailment"),
    ("No label here.", None),
]


def main():
    bad = 0
    for text, want in CASES:
        got = parse_label(text)
        if got != want:
            bad += 1
            print(f"FAIL strict  {text!r}: got {got!r}, want {want!r}")
    for text, want in LENIENT:
        got = parse_label_lenient(text)
        if got != want:
            bad += 1
            print(f"FAIL lenient {text!r}: got {got!r}, want {want!r}")
    assert detokenize("The doctor , who ran , slept .") == "The doctor, who ran, slept."
    assert label_first("Final label: Entailment\n\nThe premise states that the doctor ran.")
    assert label_first("**Final label:** Non-entailment\nExplanation: roles are swapped.")
    assert not label_first("The roles are swapped.\nFinal label: Non-entailment")
    assert not label_first("Final label: Entailment")
    assert not label_first("Final label: **Entailment**")
    assert not label_first("No label.")
    print(f"{len(CASES) + len(LENIENT) - bad}/{len(CASES) + len(LENIENT)} parsing checks passed")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()

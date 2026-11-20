"""The four prompting conditions (paper Appendix B).

Every condition shares the same task description, label definitions and
Premise/Hypothesis block; only the final instruction differs.

Deviation from the HW1 proposal, fixed before any evaluation run:
the proposal wrote the output format as 'Final label: [label]'. A small model can
copy the literal string "[label]", so P2-P4 now spell out both allowed labels,
exactly as P1 already did.
"""

CONDITIONS = ("P1", "P2", "P3", "P4")

CONDITION_NAMES = {
    "P1": "Basic",
    "P2": "General reasoning",
    "P3": "Structure-aware",
    "P4": "Nonstructural control",
}

TASK = (
    "Determine whether the hypothesis follows from the premise. "
    "Use Entailment only if the hypothesis must be true when the premise is true; "
    "otherwise use Non-entailment."
)

FORMAT = "'Final label: Entailment' or 'Final label: Non-entailment'"

INSTRUCTIONS = {
    "P1": f"Give no explanation. Output only {FORMAT}.",
    "P2": (
        "Think carefully about whether the hypothesis necessarily follows. "
        f"Explain your decision in one or two sentences, then give a final line in the format {FORMAT}."
    ),
    "P3": (
        "Examine who performs each action, who receives it, and how clauses affect meaning. "
        "Explain these grammatical relationships in one or two sentences, "
        f"then give a final line in the format {FORMAT}."
    ),
    "P4": (
        "Examine the general topic, vocabulary, and writing style of both sentences, including their tone. "
        "Describe these features in one or two sentences, "
        f"then give a final line in the format {FORMAT}."
    ),
}


def build_user_message(premise, hypothesis, condition):
    return (
        f"{TASK}\n\n"
        f"Premise: {premise}\n"
        f"Hypothesis: {hypothesis}\n\n"
        f"{INSTRUCTIONS[condition]}"
    )


def build_messages(premise, hypothesis, condition):
    # No system message: the Qwen2.5 chat template then inserts its default system
    # prompt, identically for every condition.
    return [{"role": "user", "content": build_user_message(premise, hypothesis, condition)}]

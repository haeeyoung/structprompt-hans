# P2 -> P3 flips (random sample, seed 42)

Improved (P2 wrong, P3 right): 48 items. Worsened (P2 right, P3 wrong): 54 items.
Up to 5 of each, drawn uniformly at random from the item list in file order.

## Improved

**hans-eval-ex6273** · lexical_overlap / le_around_prepositional_phrase · gold: **entailment**
- Premise: The senator in front of the author introduced the lawyer.
- Hypothesis: The senator introduced the lawyer.
- P2 (non-entailment, WRONG): Final label: Non-entailment /  / Explanation: The premise states that the senator introduced the lawyer, but it does not specify that the senator was in front of the author. Therefore, the hypothesis that the senator introduced the lawyer is not necessarily true based on the given premise.
- P3 (entailment, correct): In the premise, "The senator in front of the author introduced the lawyer," the senator performs the action of introducing the lawyer. The author receives this introduction. The hypothesis states, "The senator introduced the lawyer." Here, the senator performs the action of introducing the lawyer, and the lawyer is the recipient.  /  / Final label: Entailment

**hans-eval-ex8332** · lexical_overlap / le_conjunction · gold: **entailment**
- Premise: The authors and the artist supported the athlete.
- Hypothesis: The authors supported the athlete.
- P2 (non-entailment, WRONG): Final label: Non-entailment /  / Explanation: The premise states that both the authors and the artist supported the athlete, while the hypothesis only mentions the authors supporting the athlete. The hypothesis does not necessarily follow from the premise because the premise includes the artist as well, who is not mentioned in the hypothesis.
- P3 (entailment, correct): In the premise, "The authors and the artist supported the athlete," the authors and the artist both supported the athlete. In the hypothesis, "The authors supported the athlete," only the authors supported the athlete. The hypothesis is a subset of the premise, so the hypothesis follows from the premise. /  / Final label: Entailment

**hans-eval-ex19161** · subsequence / se_PP_on_obj · gold: **entailment**
- Premise: The athlete introduced the artists next to the tourist.
- Hypothesis: The athlete introduced the artists.
- P2 (non-entailment, WRONG): Final label: Non-entailment /  / Explanation: The hypothesis "The athlete introduced the artists" is a subset of the premise "The athlete introduced the artists next to the tourist." While the hypothesis is true when the premise is true, it does not necessarily follow because the premise specifies that the introduction occurred "next to the tourist," which is not mentioned in the hypothesis. Therefore, the hypothesis does not have to be true for the premise to be true.
- P3 (entailment, correct): In the premise, the athlete introduces the artists next to the tourist. In the hypothesis, the athlete introduces the artists. The athlete is the one performing the action of introducing the artists. The tourist is the one receiving the action of being introduced by the athlete. The clause "next to the tourist" in the premise does not affect the meaning of the hypothesis. Therefore, the hypothesis is entailed by the premise. /  / Final label: Entailment

**hans-eval-ex25828** · constituent / ce_embedded_under_since · gold: **entailment**
- Premise: Though the professor thanked the doctors, the lawyers ran.
- Hypothesis: The professor thanked the doctors.
- P2 (non-entailment, WRONG): Final label: Non-entailment /  / Explanation: The premise states that the professor thanked the doctors, but it does not provide any information about whether the lawyers ran. Therefore, the hypothesis that "The professor thanked the doctors" does not necessarily follow from the premise.
- P3 (entailment, correct): In the premise, "Though the professor thanked the doctors, the lawyers ran," the professor thanked the doctors, and the lawyers ran. The hypothesis states, "The professor thanked the doctors."  /  / The professor thanked the doctors in the premise, and the hypothesis also states that the professor thanked the doctors. Therefore, the hypothesis is entailed by the premise. /  / Final label: Entailment

**hans-eval-ex20721** · constituent / cn_embedded_under_if · gold: **non-entailment**
- Premise: If the authors admired the tourists, the senator slept.
- Hypothesis: The authors admired the tourists.
- P2 (entailment, WRONG): Final label: Entailment /  / Explanation: The premise states that if the authors admired the tourists, then the senator slept. The hypothesis directly states that the authors admired the tourists. Since the premise implies admiration of the tourists, the hypothesis must be true when the premise is true. Therefore, the hypothesis necessarily follows from the premise.
- P3 (non-entailment, correct): In the given premise, the action "admired" is performed by the authors, and the action "slept" is performed by the senator. The hypothesis states that the authors admired the tourists.  /  / Final label: Non-entailment /  / The premise indicates that the authors admired the tourists, but it does not specify that the authors performed the action of admiring. The hypothesis only states that the authors admired the tourists, which is a subset of the information provided in the premise. Therefore, the hypothesis does not necessarily follow from the premise.

## Worsened

**hans-eval-ex3438** · lexical_overlap / ln_passive · gold: **non-entailment**
- Premise: The president was recognized by the managers.
- Hypothesis: The president recognized the managers.
- P2 (non-entailment, correct): Final label: Non-entailment /  / Explanation: The premise states that the president was recognized by the managers, but it does not specify whether the recognition was mutual or one-sided. Therefore, we cannot conclude that the hypothesis "The president recognized the managers" necessarily follows from the premise.
- P3 (invalid, WRONG): In the premise, "The president was recognized by the managers," the president is the one performing the action of being recognized. The managers are the ones receiving the recognition. /  / In the hypothesis, "The president recognized the managers," the president is the one receiving the recognition, and the managers are the ones performing the action. /  / The final label is: Non-entailment.

**hans-eval-ex2065** · lexical_overlap / ln_relative_clause · gold: **non-entailment**
- Premise: The authors who the athlete encouraged introduced the tourists.
- Hypothesis: The tourists introduced the athlete.
- P2 (non-entailment, correct): Final label: Non-entailment /  / Explanation: The premise states that the authors who the athlete encouraged introduced the tourists. This implies that the authors were the ones who introduced the tourists to the athlete. However, the hypothesis claims that the tourists introduced the athlete. These two statements are contradictory, so the hypothesis does not necessarily follow from the premise.
- P3 (invalid, WRONG): In the premise, the authors who the athlete encouraged introduced the tourists. In the hypothesis, the tourists introduced the athlete. /  / The premise states that the authors who the athlete encouraged introduced the tourists. The hypothesis states that the tourists introduced the athlete. /  / The relationship between the authors who the athlete encouraged and the tourists is that the authors introduced the tourists. The relationship between the tourists and the athlete is that the tourists introduced the athlete. /  / The hypothesis is not entailed by the premise because the actions are reversed. The premise states that the authors introduced the tourists, but the hypothesis states that the tourists introduced the athlete. Therefore, the hypothesis does not follow from

**hans-eval-ex10246** · subsequence / sn_NP/S · gold: **non-entailment**
- Premise: The president believed the lawyers waited.
- Hypothesis: The president believed the lawyers.
- P2 (non-entailment, correct): Final label: Non-entailment /  / Explanation: The premise states that the president believed the lawyers waited, but it does not specify that the president believed the lawyers themselves. The hypothesis only states that the president believed the lawyers, which is a more general statement than the premise. Therefore, the hypothesis does not necessarily follow from the premise.
- P3 (entailment, WRONG): In the premise, "The president believed the lawyers waited," the president is the one who believed something. The lawyers are the ones who waited. The hypothesis states, "The president believed the lawyers," which is a simpler version of the premise. The president is still the one who believed the lawyers, but the lawyers are not explicitly mentioned. Therefore, the hypothesis is entailed by the premise. /  / Final label: Entailment

**hans-eval-ex10314** · subsequence / sn_NP/S · gold: **non-entailment**
- Premise: The doctor believed the president admired the professors.
- Hypothesis: The doctor believed the president.
- P2 (non-entailment, correct): Final label: Non-entailment /  / Explanation: The premise states that the doctor believed the president admired the professors, but it does not provide any information about whether the doctor believed the president. Therefore, the hypothesis "The doctor believed the president" is not necessarily true based on the given premise.
- P3 (entailment, WRONG): In the given premise and hypothesis, the doctor is the one who believes the president admires the professors. The doctor's belief is directed towards the president, who is the one who admires the professors. The hypothesis states that the doctor believes the president, which is a subset of the doctor's belief in the premise. Therefore, the hypothesis is entailed by the premise. /  / Final label: Entailment

**hans-eval-ex20046** · constituent / cn_embedded_under_if · gold: **non-entailment**
- Premise: If the scientist advised the actor, the artist called the secretaries.
- Hypothesis: The scientist advised the actor.
- P2 (non-entailment, correct): Final label: Non-entailment /  / Explanation: The premise states that if the scientist advised the actor, the artist called the secretaries. This means that the scientist advising the actor is a necessary condition for the artist to call the secretaries. However, the hypothesis only states that the scientist advised the actor, which is a sufficient condition but not a necessary one. Therefore, the hypothesis does not necessarily follow from the premise.
- P3 (entailment, WRONG): In the premise, the scientist advises the actor. In the hypothesis, the scientist advises the actor. The clause "If the scientist advised the actor" implies that the scientist advised the actor. Therefore, the hypothesis is entailed by the premise. /  / Final label: Entailment

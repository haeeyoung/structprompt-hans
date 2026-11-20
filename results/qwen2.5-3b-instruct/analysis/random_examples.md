# Randomly sampled items (seed 42), all four prompts

**hans-eval-ex7250** · lexical_overlap / le_around_relative_clause · gold: **entailment**
- Premise: The judge that danced helped the professors.
- Hypothesis: The judge helped the professors.
- P1 (entailment, correct): Final label: Entailment
- P2 (non-entailment, WRONG): The premise states that "The judge that danced helped the professors," which implies that the judge's dancing action led to the professors being helped. The hypothesis simplifies this to "The judge helped the professors," which is a more general statement that does not contradict the premise but is not necessarily implied by it. The premise specifies an action (dancing) that led to the help, while the hypothesis only states that the judge helped the professors without specifying the means. /  / Final label: Non-entailment
- P3 (entailment, correct): In the premise, "The judge that danced helped the professors," the judge is the subject performing the action of dancing, and the professors are the recipients of the action of helping. The hypothesis, "The judge helped the professors," simplifies this to just the judge helping the professors without specifying the dancing action. The dancing action does not negate or alter the fact that the judge helped the professors. Therefore, the hypothesis must be true if the premise is true. /  / Final label: Entailment
- P4 (entailment, correct): Both sentences discuss a judge's actions and their impact on professors. The premise provides more specific information about the judge dancing, while the hypothesis simplifies this to just the judge helping the professors. The hypothesis is a direct and necessary simplification of the premise, as the premise's additional detail (dancing) does not contradict the core action (helping). /  / Final label: Entailment

**hans-eval-ex4252** · lexical_overlap / ln_conjunction · gold: **non-entailment**
- Premise: The secretaries encouraged the managers and the tourist.
- Hypothesis: The managers encouraged the tourist.
- P1 (non-entailment, correct): Final label: Non-entailment
- P2 (non-entailment, correct): The premise states that secretaries encouraged the managers and the tourist, but it does not specify who encouraged whom. Therefore, we cannot conclude that the managers encouraged the tourist.  /  / Final label: Non-entailment
- P3 (non-entailment, correct): In the premise, the secretaries are the ones encouraging both the managers and the tourists. The hypothesis only mentions the managers encouraging the tourists. The premise does not provide information about the managers encouraging the tourists directly; it only states that the secretaries encouraged both groups. Therefore, the hypothesis cannot be concluded from the premise. /  / Final label: Non-entailment
- P4 (non-entailment, correct): The premise states that secretaries encouraged both managers and tourists, while the hypothesis focuses on managers encouraging the tourist. The premise does not provide any information about the managers encouraging the tourist directly; it only mentions that secretaries encouraged both groups. The tone is informative and straightforward, with no emotional or persuasive elements. /  / Final label: Non-entailment

**hans-eval-ex4658** · lexical_overlap / ln_conjunction · gold: **non-entailment**
- Premise: The artists and the scientist recognized the senators.
- Hypothesis: The scientist recognized the artists.
- P1 (non-entailment, correct): Final label: Non-entailment
- P2 (non-entailment, correct): The premise states that the artists and the scientist recognized the senators, but it does not specify who recognized whom among the artists and the scientist. Therefore, the hypothesis that "The scientist recognized the artists" cannot be concluded from the given premise.  /  / Final label: Non-entailment
- P3 (non-entailment, correct): In the premise, the action "recognized" is performed by the scientists and received by the artists and the senators. In the hypothesis, the action "recognized" is performed by the scientist and received by the artists. The roles of the scientist and the artists are reversed between the premise and the hypothesis. Therefore, the hypothesis cannot be true if the premise is true, as the premise states that the scientists recognized the artists, not the other way around. /  / Final label: Non-entailment
- P4 (non-entailment, correct): The premise states that both artists and scientists recognized the senators, while the hypothesis claims that the scientist recognized the artists. The premise does not provide any information about the recognition of artists by scientists. The tone is neutral and factual, focusing on the recognition of senators by both groups.  /  / Final label: Non-entailment

**hans-eval-ex1093** · lexical_overlap / ln_preposition · gold: **non-entailment**
- Premise: The professors called the bankers next to the student.
- Hypothesis: The bankers called the professors.
- P1 (non-entailment, correct): Final label: Non-entailment
- P2 (non-entailment, correct): The premise states that professors called the bankers, not the other way around. Therefore, the hypothesis that the bankers called the professors cannot be true if the premise is true. Final label: Non-entailment
- P3 (non-entailment, correct): In the premise, the action "called" is performed by "the professors" and is directed towards "the bankers." The hypothesis reverses these roles, stating that "the bankers called the professors." The premise does not provide any information about the bankers calling anyone, and the hypothesis introduces a new action that is not supported by the original statement. Therefore, the hypothesis cannot be concluded as true based on the given premise. /  / Final label: Non-entailment
- P4 (non-entailment, correct): The premise describes a sequence of actions where professors are the initiators of a call to bankers, while the hypothesis reverses this action, suggesting the bankers called the professors. The premise does not provide any information about the bankers calling the professors, and in fact, the premise implies the opposite. The tone is straightforward and factual, with no emotional or persuasive elements. /  / Final label: Non-entailment

**hans-eval-ex16736** · subsequence / se_adjective · gold: **entailment**
- Premise: Famous secretaries saw the senator.
- Hypothesis: Secretaries saw the senator.
- P1 (entailment, correct): Final label: Entailment
- P2 (non-entailment, WRONG): The premise states that "Famous secretaries saw the senator," which implies that there were secretaries who were famous and who saw the senator. The hypothesis simplifies this to "Secretaries saw the senator," which is a more general statement that does not require the secretaries to be famous. Therefore, the hypothesis does not necessarily follow from the premise. /  / Final label: Non-entailment
- P3 (entailment, correct): In the premise, "Famous secretaries saw the senator," the subject "secretaries" performs the action "saw" on the object "the senator." The hypothesis, "Secretaries saw the senator," omits the adjective "famous" but maintains the same subject and action. The omission of "famous" does not change the core meaning that secretaries saw the senator. Therefore, the hypothesis must be true if the premise is true. /  / Final label: Entailment
- P4 (entailment, correct): Both sentences discuss secretaries and the senator, with the premise providing additional context about their being "famous." The hypothesis is a simplified version of the premise, omitting the adjective "famous." The tone is straightforward and factual in both sentences. /  / Final label: Entailment

**hans-eval-ex15640** · subsequence / se_conjunction · gold: **entailment**
- Premise: The managers thanked the senator and the tourists.
- Hypothesis: The managers thanked the senator.
- P1 (entailment, correct): Final label: Entailment
- P2 (non-entailment, WRONG): The premise states that the managers thanked both the senator and the tourists. This does not necessarily mean that the managers only thanked the senator; they could have also thanked the tourists. Therefore, the hypothesis that "The managers thanked the senator" does not follow from the premise. /  / Final label: Non-entailment
- P3 (non-entailment, WRONG): In the premise, the managers thank both the senator and the tourists. The hypothesis only mentions the managers thanking the senator. The action of thanking the senator is a part of the overall action described in the premise, but the premise also includes the action of thanking tourists, which is not mentioned in the hypothesis. Therefore, the hypothesis is a subset of the information provided in the premise. /  / Final label: Non-entailment
- P4 (non-entailment, WRONG): Both sentences discuss a scenario where managers express gratitude. The premise provides more specific information, mentioning both the senator and tourists, while the hypothesis focuses solely on the managers thanking the senator. The tone in both sentences is neutral and informative. /  / Final label: Non-entailment

**hans-eval-ex17000** · subsequence / se_understood_object · gold: **entailment**
- Premise: The presidents paid the scientists.
- Hypothesis: The presidents paid.
- P1 (entailment, correct): Final label: Entailment
- P2 (entailment, correct): The premise states that "The presidents paid the scientists," which implies that the presidents did indeed pay someone (the scientists). Therefore, the hypothesis "The presidents paid" must be true if the premise is true.  /  / Final label: Entailment
- P3 (entailment, correct): In the premise, "The presidents paid the scientists," the action of paying is performed by "the presidents" and received by "the scientists." The hypothesis "The presidents paid" is a simplified version of the premise, omitting the recipients of the action. The hypothesis does not contradict the premise but is a subset of the information provided. The action (paying) is still performed by the presidents, and the hypothesis must be true if the premise is true. /  / Final label: Entailment
- P4 (entailment, correct): The premise states an action where presidents paid scientists, while the hypothesis simplifies this to just stating that presidents paid. The premise provides more specific information, but the hypothesis is a logical consequence of the premise. The tone is straightforward and factual. /  / Final label: Entailment

**hans-eval-ex23906** · constituent / cn_disjunction · gold: **non-entailment**
- Premise: The actors slept, or the judges shouted.
- Hypothesis: The judges shouted.
- P1 (non-entailment, correct): Final label: Non-entailment
- P2 (non-entailment, correct): The premise states that either the actors slept or the judges shouted. This does not guarantee that the judges shouted; they could have slept instead. Therefore, the hypothesis that "The judges shouted" does not necessarily follow from the premise. /  / Final label: Non-entailment
- P3 (non-entailment, correct): In the premise, the actions "slept" and "shouted" are attributed to "the actors" and "the judges" respectively. The hypothesis states that "the judges shouted." The premise does not provide enough information to conclude that the judges shouted; it only states that either the actors slept or the judges shouted. Therefore, the hypothesis could be true even if the actors slept, making it possible that the judges did not shout.  /  / Final label: Non-entailment
- P4 (non-entailment, correct): The premise and hypothesis are both presented in a simple, declarative style with a straightforward tone. The premise states a conditional relationship between two actions (actors sleeping or judges shouting), while the hypothesis focuses solely on one of these actions (judges shouting).  /  / Final label: Non-entailment

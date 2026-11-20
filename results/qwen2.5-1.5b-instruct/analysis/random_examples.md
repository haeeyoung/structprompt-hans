# Randomly sampled items (seed 42), all four prompts

**hans-eval-ex7250** · lexical_overlap / le_around_relative_clause · gold: **entailment**
- Premise: The judge that danced helped the professors.
- Hypothesis: The judge helped the professors.
- P1 (entailment, correct): Final label: Entailment
- P2 (non-entailment, WRONG): Final label: Non-entailment /  / Explanation: The premise states that the judge who danced helped the professors. The hypothesis simply states that the judge helped the professors. While the hypothesis is true if the premise is true, it is not necessarily true. The premise specifies that the judge who danced helped the professors, but it does not provide any information about the judge who did not dance. Therefore, the hypothesis does not necessarily follow from the premise.
- P3 (non-entailment, WRONG): In the premise, "The judge that danced helped the professors," the judge is the one who danced and the professors are the ones who received the help. In the hypothesis, "The judge helped the professors," the judge is the one who helped the professors.  /  / Final label: Non-entailment.
- P4 (non-entailment, WRONG): **Final label: Non-entailment** /  / **Explanation:** / - **General Topic:** Both sentences discuss a judge helping professors. / - **Vocabulary:** The vocabulary is similar, with "judge" and "professors" being the main terms. / - **Writing Style:** The tone is formal and informative in both sentences. / - **Tone:** The tone is neutral and objective in both sentences. / - **Final label:** Since the hypothesis is a subset of the premise and does not necessarily have to be true when the premise is true (the judge who danced could be different from the judge who helped the professors), the final label

**hans-eval-ex4252** · lexical_overlap / ln_conjunction · gold: **non-entailment**
- Premise: The secretaries encouraged the managers and the tourist.
- Hypothesis: The managers encouraged the tourist.
- P1 (non-entailment, correct): Final label: Non-entailment
- P2 (non-entailment, correct): Final label: Non-entailment /  / Explanation: The premise states that the secretaries encouraged both the managers and the tourist. However, the hypothesis claims that the managers encouraged the tourist. This is not necessarily true because the premise does not provide any information about the managers' actions towards the tourist. Therefore, the hypothesis does not necessarily follow from the premise.
- P3 (non-entailment, correct): In the premise, the secretaries encouraged the managers, and the managers encouraged the tourist. The hypothesis states that the managers encouraged the tourist.  /  / Final label: Non-entailment /  / Explanation: The premise indicates that the secretaries encouraged the managers, and the managers encouraged the tourist. The hypothesis, however, suggests that the managers encouraged the tourist, which contradicts the information provided in the premise. Therefore, the hypothesis does not follow from the premise.
- P4 (non-entailment, correct): **Final label: Non-entailment** /  / **Explanation:** / The premise states that "The secretaries encouraged the managers and the tourist." This implies a hierarchical relationship where secretaries are encouraging both managers and a tourist. The hypothesis, "The managers encouraged the tourist," does not necessarily follow from this premise because the premise does not specify that managers are encouraging the tourist. The premise only mentions that secretaries encouraged both managers and the tourist, but it does not provide information about the relationship between managers and the tourist. Therefore, the hypothesis is not entailed by the premise.

**hans-eval-ex4658** · lexical_overlap / ln_conjunction · gold: **non-entailment**
- Premise: The artists and the scientist recognized the senators.
- Hypothesis: The scientist recognized the artists.
- P1 (non-entailment, correct): Final label: Non-entailment
- P2 (non-entailment, correct): Final label: Non-entailment /  / Explanation: The premise states that both the artists and the scientist recognized the senators. However, the hypothesis claims that only the scientist recognized the artists. This is not necessarily true because the premise does not provide any information about the relationship between the artists and the scientist. They could have recognized each other, but the hypothesis does not specify this. Therefore, the hypothesis does not necessarily follow from the premise.
- P3 (non-entailment, correct): In the premise, the artists and the scientist recognize the senators. In the hypothesis, the scientist recognizes the artists. The key difference is that in the premise, the artists are recognized by the scientist, while in the hypothesis, the scientist recognizes the artists. /  / Final label: Non-entailment
- P4 (non-entailment, correct): **Final label: Non-entailment** /  / **Explanation:** / The premise states that both the artists and the scientist recognized the senators. This implies that the recognition occurred simultaneously between the two groups. The hypothesis, however, suggests that the scientist recognized the artists, which contradicts the premise. Therefore, the hypothesis does not follow from the premise.

**hans-eval-ex1093** · lexical_overlap / ln_preposition · gold: **non-entailment**
- Premise: The professors called the bankers next to the student.
- Hypothesis: The bankers called the professors.
- P1 (non-entailment, correct): Final label: Non-entailment
- P2 (non-entailment, correct): Final label: Non-entailment /  / Explanation: The hypothesis states that the bankers called the professors, but the premise only mentions that the professors called the bankers. These are two different actions, so the hypothesis does not necessarily follow from the premise.
- P3 (non-entailment, correct): In the premise, the professors are the ones calling the bankers. The bankers are the ones receiving the call. The hypothesis states that the bankers are the ones calling the professors. This is the opposite of what the premise states. Therefore, the hypothesis does not follow from the premise. /  / Final label: Non-entailment
- P4 (non-entailment, correct): **Final label: Non-entailment** /  / **Explanation:** / The premise states that the professors called the bankers next to the student. The hypothesis, however, claims that the bankers called the professors. These two statements are contradictory because they describe opposite actions. Therefore, the hypothesis does not follow from the premise.

**hans-eval-ex16736** · subsequence / se_adjective · gold: **entailment**
- Premise: Famous secretaries saw the senator.
- Hypothesis: Secretaries saw the senator.
- P1 (entailment, correct): Final label: Entailment
- P2 (entailment, correct): Final label: Entailment /  / Explanation: The hypothesis "Secretaries saw the senator" is a simplified version of the premise "Famous secretaries saw the senator." Since the premise specifies that famous secretaries saw the senator, it logically follows that all secretaries saw the senator. Therefore, the hypothesis necessarily follows from the premise.
- P3 (entailment, correct): In the premise, "Famous secretaries saw the senator," the subject is "Famous secretaries," and the verb is "saw." In the hypothesis, "Secretaries saw the senator," the subject is "Secretaries," and the verb is "saw." The subject in the premise is performing the action of seeing, while the subject in the hypothesis is receiving the action of seeing. The verb "saw" is the same in both sentences, indicating that the action is the same. Therefore, the hypothesis follows from the premise. /  / Final label: Entailment
- P4 (non-entailment, WRONG): **Final label: Non-entailment** /  / **Explanation:** / - **General Topic:** Both sentences discuss secretaries and a senator. / - **Vocabulary:** The vocabulary is similar, with "secretary" and "senator" being the same in both sentences. / - **Writing Style and Tone:** The tone is neutral and informative in both sentences. However, the premise uses the word "famous," which might imply a more positive or attention-grabbing context, while the hypothesis is straightforward and neutral. /  / Despite the similarities in topic, vocabulary, and writing style, the hypothesis does not necessarily follow from the premise because the premise

**hans-eval-ex15640** · subsequence / se_conjunction · gold: **entailment**
- Premise: The managers thanked the senator and the tourists.
- Hypothesis: The managers thanked the senator.
- P1 (non-entailment, WRONG): Final label: Non-entailment
- P2 (non-entailment, WRONG): Final label: Non-entailment /  / Explanation: The premise states that the managers thanked the senator and the tourists, while the hypothesis only mentions the managers thanking the senator. The hypothesis does not necessarily follow from the premise because it omits the part about the tourists.
- P3 (non-entailment, WRONG): In the premise, the managers thanked the senator and the tourists. In the hypothesis, the managers thanked the senator. The managers are the ones performing the action of thanking, and the senator is the one receiving the thank. The tourists are not mentioned in the hypothesis, so we cannot assume they were thanked. The presence of the tourists in the premise does not necessarily mean they were thanked in the hypothesis. Therefore, the hypothesis is not entailed by the premise. /  / Final label: Non-entailment
- P4 (non-entailment, WRONG): **Final label: Non-entailment** /  / **Explanation:** / The premise states that the managers thanked both the senator and the tourists. The hypothesis only mentions that the managers thanked the senator. The hypothesis is a subset of the information provided in the premise, but it does not capture the additional detail about the tourists. Therefore, the hypothesis does not necessarily follow from the premise.

**hans-eval-ex17000** · subsequence / se_understood_object · gold: **entailment**
- Premise: The presidents paid the scientists.
- Hypothesis: The presidents paid.
- P1 (non-entailment, WRONG): Final label: Non-entailment
- P2 (non-entailment, WRONG): Final label: Non-entailment /  / Explanation: The premise states that the presidents paid the scientists, but it does not specify that the presidents paid the scientists directly. The hypothesis only states that the presidents paid, which is a more general statement than the premise. Therefore, the hypothesis does not necessarily follow from the premise.
- P3 (non-entailment, WRONG): In the premise, "The presidents paid the scientists," the subject is "The presidents" and the action is "paid." In the hypothesis, "The presidents paid," the subject is "The presidents" and the action is "paid." The hypothesis is a simplified version of the premise, omitting the object "the scientists."  /  / Final label: Non-entailment.
- P4 (non-entailment, WRONG): **Final label: Non-entailment** /  / **Explanation:** / The premise states that "The presidents paid the scientists," which implies a specific action (payment) between two parties (presidents and scientists). The hypothesis, "The presidents paid," is a more general statement that does not necessarily require the payment to the scientists. It could be that the presidents paid for something else, or they did not pay at all. Therefore, the hypothesis does not necessarily follow from the premise.

**hans-eval-ex23906** · constituent / cn_disjunction · gold: **non-entailment**
- Premise: The actors slept, or the judges shouted.
- Hypothesis: The judges shouted.
- P1 (non-entailment, correct): Final label: Non-entailment
- P2 (non-entailment, correct): Final label: Non-entailment /  / Explanation: The premise states that either the actors slept or the judges shouted. The hypothesis only mentions that the judges shouted. While the hypothesis is a subset of the information given in the premise, it does not necessarily follow because the premise allows for the possibility that the actors slept instead of the judges shouting.
- P3 (entailment, WRONG): In the premise, "The actors slept" and "the judges shouted" are two separate actions performed by different entities. The premise states that either one of these actions occurs, but not both simultaneously. The hypothesis, "The judges shouted," is a subset of the premise's second clause. Since the premise allows for the possibility that the judges shouted, the hypothesis is entailed by the premise. /  / Final label: Entailment
- P4 (non-entailment, correct): **Final label: Non-entailment** /  / **Explanation:** / The premise states that either the actors slept or the judges shouted. The hypothesis specifically claims that the judges shouted. While the premise does not explicitly state that the judges shouted, it does not contradict the possibility that they shouted. Therefore, the hypothesis is not necessarily true based solely on the given premise.

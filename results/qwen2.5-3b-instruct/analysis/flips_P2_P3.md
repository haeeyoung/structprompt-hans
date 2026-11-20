# P2 -> P3 flips (random sample, seed 42)

Improved (P2 wrong, P3 right): 57 items. Worsened (P2 right, P3 wrong): 25 items.
Up to 5 of each, drawn uniformly at random from the item list in file order.

## Improved

**hans-eval-ex6214** · lexical_overlap / le_around_prepositional_phrase · gold: **entailment**
- Premise: The tourist next to the scientists admired the judge.
- Hypothesis: The tourist admired the judge.
- P2 (non-entailment, WRONG): The premise states that the tourist admired the judge, but it does not specify that the tourist was next to the scientists. The hypothesis only mentions the tourist admiring the judge without the additional context. Therefore, the hypothesis does not necessarily follow from the premise. /  / Final label: Non-entailment
- P3 (entailment, correct): In the premise, "The tourist next to the scientists" is the subject performing the action of admiring, and "the judge" is the object receiving the admiration. The hypothesis simplifies this to "The tourist admired the judge," removing the context of the scientists and the relative position. The core action and the object of admiration remain the same, but the premise provides additional context that is not necessary for the hypothesis to be true. /  / Final label: Entailment

**hans-eval-ex7175** · lexical_overlap / le_around_relative_clause · gold: **entailment**
- Premise: The manager who the artists introduced thanked the doctors.
- Hypothesis: The manager thanked the doctors.
- P2 (non-entailment, WRONG): The premise states that the manager thanked the doctors because they were introduced by the artists. This implies that the introduction by the artists was a condition for the manager's gratitude, but it does not necessarily mean that the manager would have thanked the doctors without the introduction. Therefore, the hypothesis is not guaranteed to be true based solely on the premise. /  / Final label: Non-entailment
- P3 (entailment, correct): In the premise, the manager is the one who performs the action of thanking, and the doctors are the ones who receive the action. The hypothesis simplifies this by omitting the actor (the artists) and the receiver (the artists) and directly stating the manager's action towards the doctors. The hypothesis does not contradict the premise but is a more concise version of the same action. Therefore, the hypothesis must be true if the premise is true. /  / Final label: Entailment

**hans-eval-ex8786** · lexical_overlap / le_conjunction · gold: **entailment**
- Premise: The professors and the athletes encouraged the tourists.
- Hypothesis: The professors encouraged the tourists.
- P2 (non-entailment, WRONG): The premise states that both professors and athletes encouraged the tourists, but it does not specify that only the professors encouraged the tourists. The athletes could have encouraged the tourists as well. Therefore, the hypothesis is not necessarily true based on the given premise. /  / Final label: Non-entailment
- P3 (entailment, correct): In the premise, "The professors and the athletes encouraged the tourists," the action of encouraging is performed by "the professors and the athletes" and received by "the tourists." The hypothesis, "The professors encouraged the tourists," is a subset of the premise, focusing only on the professors performing the action. The athletes are not mentioned in the hypothesis, but their involvement does not negate the professors' action. Therefore, the hypothesis must be true if the premise is true. /  / Final label: Entailment

**hans-eval-ex10899** · subsequence / sn_NP/S · gold: **non-entailment**
- Premise: The authors believed the senators resigned.
- Hypothesis: The authors believed the senators.
- P2 (entailment, WRONG): The premise states that the authors believed the senators resigned, which implies they believed the senators did something (resigned). The hypothesis simply states that the authors believed the senators, which is a more general statement. The resignation is a specific action, so the belief in resignation necessarily includes the belief in the senators. Therefore, the hypothesis must be true if the premise is true. /  / Final label: Entailment
- P3 (non-entailment, correct): In the premise, "The authors believed the senators resigned," the action "believed" is performed by the authors towards the senators' resignation. The hypothesis, "The authors believed the senators," simplifies this to just the authors' belief about the senators without specifying the action. The premise includes a specific action (resigned) that the hypothesis does not mention, but the core subject (the senators) remains the same.  /  / Final label: Non-entailment

**hans-eval-ex29654** · constituent / ce_adverb · gold: **entailment**
- Premise: Without a doubt the professor stopped the presidents.
- Hypothesis: The professor stopped the presidents.
- P2 (non-entailment, WRONG): The premise "Without a doubt the professor stopped the presidents" is an expression of certainty, but it does not provide evidence that the action actually occurred. The hypothesis "The professor stopped the presidents" is a statement of fact that could be true or false based on the premise. Since the premise does not guarantee the truth of the hypothesis, the hypothesis does not necessarily follow from the premise. /  / Final label: Non-entailment
- P3 (entailment, correct): In the premise, "the professor stopped the presidents" is a complete statement indicating an action performed by the professor on the presidents. The hypothesis "The professor stopped the presidents" omits the word "without a doubt," which does not change the core action but adds a degree of certainty. However, the hypothesis does not include the certainty expressed in the premise. Therefore, the hypothesis must be true if the premise is true, but the premise does not necessitate the certainty expressed in the hypothesis. /  / Final label: Entailment

## Worsened

**hans-eval-ex5217** · lexical_overlap / le_relative_clause · gold: **entailment**
- Premise: The manager who the secretary called advised the judge.
- Hypothesis: The secretary called the manager.
- P2 (entailment, correct): The premise states that the secretary called the manager, and the hypothesis states that the secretary called the manager. These are the same statement, just phrased differently. Therefore, the hypothesis must be true if the premise is true. /  / Final label: Entailment
- P3 (non-entailment, WRONG): In the premise, the secretary is the one who performs the action of calling, and the manager is the one who receives the call. The hypothesis reverses these roles, stating that the secretary called the manager. The premise does not provide information about the secretary calling the manager; it only states that the manager was advised by the person the secretary called. Therefore, the hypothesis cannot be concluded from the premise. /  / Final label: Non-entailment

**hans-eval-ex10245** · subsequence / sn_NP/S · gold: **non-entailment**
- Premise: The athletes heard the senator admired the lawyers.
- Hypothesis: The athletes heard the senator.
- P2 (non-entailment, correct): The premise states that the athletes heard the senator admired the lawyers, which does not provide any information about whether the athletes heard the senator directly. The hypothesis only claims that the athletes heard the senator, which could be true based on the premise, but it is not necessarily true. The premise does not guarantee the hypothesis. /  / Final label: Non-entailment
- P3 (entailment, WRONG): In the premise, "The athletes heard the senator admired the lawyers," the action of hearing is performed by the athletes, and the action of admiring is performed by the senator towards the lawyers. The hypothesis "The athletes heard the senator" is a simplified version of the premise, omitting the specific action of admiring. The athletes still hear the senator, which is a necessary condition for the hypothesis to be true given the premise. Therefore, the hypothesis must be true if the premise is true. /  / Final label: Entailment

**hans-eval-ex14545** · subsequence / sn_NP/Z · gold: **non-entailment**
- Premise: When the actors paid the author encouraged the artist.
- Hypothesis: The actors paid the author.
- P2 (non-entailment, correct): The premise states that when the actors paid the author, the author encouraged the artist. This does not necessarily mean that the actors paid the author in all cases. The hypothesis only asserts that the actors paid the author, but it does not specify that this occurred when the actors paid the author. Therefore, the hypothesis does not necessarily follow from the premise. /  / Final label: Non-entailment
- P3 (entailment, WRONG): In the premise, "the actors paid the author" is a complete action where the actors are performing the action of paying, and the author is the recipient. The hypothesis "The actors paid the author" is a simplified version of this action, omitting the verb "encouraged" and the recipient "the artist." The premise does not contradict the hypothesis; it merely provides additional context. The hypothesis is a subset of the information given in the premise. /  / Final label: Entailment

**hans-eval-ex20296** · constituent / cn_embedded_under_if · gold: **non-entailment**
- Premise: Unless the banker thanked the secretary, the senators called the manager.
- Hypothesis: The banker thanked the secretary.
- P2 (non-entailment, correct): The premise states a condition under which the senators called the manager, but it does not provide any information about whether the banker thanked the secretary. The hypothesis about the banker thanking the secretary is not necessarily true based on the given premise. Therefore, the hypothesis does not follow from the premise. /  / Final label: Non-entailment
- P3 (invalid, WRONG): In the premise, the action "thanked the secretary" is part of a condition that must be met for the subsequent action "the senators called the manager" to occur. The hypothesis states that "the banker thanked the secretary," which is the exact action that needs to be true for the premise to hold. However, the premise does not state that the banker thanked the secretary; it only states that if the banker did not thank the secretary, then the senators would call the manager. Therefore, the hypothesis does not have to be true for the premise to be true, as the premise could still be true even if the banker did not thank

**hans-eval-ex22379** · constituent / cn_embedded_under_verb · gold: **non-entailment**
- Premise: The scientist thought that the student performed.
- Hypothesis: The student performed.
- P2 (non-entailment, correct): The premise states that the scientist thought the student performed, but it does not necessarily mean that the student actually performed. The scientist's thought does not guarantee the truth of the hypothesis. /  / Final label: Non-entailment
- P3 (entailment, WRONG): In the premise, "The scientist thought that the student performed," the scientist is the one who thinks, and the student is the one who performed. The hypothesis "The student performed" is a simplified version of the premise, omitting the scientist's thought. The hypothesis does not contradict the premise but is a more direct statement of the action performed by the student. The scientist's thought does not negate or affect the truth of the student's performance. /  / Final label: Entailment

---
status: draft spec
last_update: 2026-05-02
---

# 20 Questions stimulus type

## Role in the design

The 20 Questions condition is the **validation bridge** between the paper's motivating phenomenon (multi-turn epistemic reasoning in dialogue) and the experimental design (single-turn matched-pair stimuli for mechanistic-interpretability tractability). It is *not* part of the primary three-condition matrix used to discriminate A/B/C; it is run alongside as a construct-validity check.

If the candidate shared circuit identified via the primary conditions also engages on 20Q-derived stimuli, with stance-sensitivity in the theoretically expected direction, that is evidence the construct generalises from experimental design to motivating phenomenon. If not, that is itself an informative finding — the design tests something narrower than the original framing claims, and the paper should report so rather than minimise it.

## Stimulus form

A single-turn input containing four parts:

1. **Stance framing.** A natural-language description of the answerer's stance.
2. **Transcript.** A short 20Q dialogue history (4–6 turns) consistent with the stance framing.
3. **Probe question.** A next-turn question from the questioner.
4. **Output to score.** The model's prediction of the answerer's response (predicted text and predicted informativeness profile).

## Stance variants

Three stance framings, all consistent with "playing 20 Questions correctly":

### Variant A — Collaborative

> "Player B has chosen an object. Player B is trying to help Player A find it efficiently within the twenty-question budget. Player B answers truthfully and volunteers helpful detail when a strict yes/no would otherwise mislead Player A or waste a question."

### Variant B — Strictly correctness-oriented

> "Player B has chosen an object. Player B answers each question with a strict yes or no. No elaboration, no volunteered detail, no choice between competing interpretations of an ambiguous question."

### Variant C — Adversarial within the rules

> "Player B has chosen an object. Player B answers truthfully and minimally. Where a question is ambiguous (e.g. category-boundary cases such as 'is a tomato a fruit?'), Player B chooses the interpretation least helpful to Player A's hypothesis-narrowing — without lying."

The transcript content is held constant across the three variants; only the stance framing and the corresponding answer style in the transcript change. The probe question is identical across variants.

## What is being probed

The model's prediction of the answerer's response, holding question constant, varying stance:

- **Stance-sensitive prediction (consistent with B1 or B2):** predicted answers shift in the theoretically expected direction across stance variants — collaborative answers more informative; strict-correctness answers minimal; adversarial answers truthful-but-misleading on ambiguous probes.
- **Stance-insensitive prediction (consistent with C):** predicted answers do not shift, or shift in non-systematic directions across stance variants.

This is a *related* primitive to false-belief tracking, not the same one. Sally-Anne / State-Rollback / novel conditions probe representation of *divergent state* between agents and reality. The 20Q condition probes representation of an *answerer's utility function* and pragmatic update of expected behaviour conditional on it. Both involve representing another agent's epistemic position; if a single shared primitive handles "represent another agent's mental state generally", it could plausibly engage across both.

## Connection to the recursive OOD probe

If the cross-bot review (P3) selects "pragmatic-stance distance" as an independent axis (IA-ε in `prereg/notes/p3-cross-bot-prompt.md`), the 20Q condition is also the natural test bed for the recursive probe itself. In that case:

- **B1 prediction.** Stance-sensitive computation engages similarly across stance variants close to the modal training distribution; informative breakdowns when stance combinations exceed compositional limits of pragmatic reasoning (e.g. nested stance: *"Player B believes Player A is being adversarial and adapts accordingly"*).
- **B2 prediction.** Smooth degradation of stance-sensitivity as stance moves further from typical-collaborative-respondent (which is presumably the modal training distribution for 20Q-like dialogues); no informative breakpoints.

Whether IA-ε is selected for the recursive probe is a P3 cross-bot output. If selected, the 20Q condition is promoted from validation-only to a primary test bed for B1/B2 discrimination.

## Scoring

Per stimulus, score:

- **Lexical content match** against canonical answer(s) for the stance variant.
- **Length / informativeness match** — collaborative answers should be longer and more informative than strict-correctness answers.
- **Interpretation choice on ambiguous probes** — for designed-in concept-boundary questions (e.g. "is it a fruit?" with object = tomato), does the model select the helpful or the unhelpful interpretation, conditioned on stance?

Composite scoring TBD; pre-registered alongside the primary three conditions.

## Structural invariants across paraphrases

Hold across ≥50 variants per stance:

- 4–6 turns of transcript history.
- One canonical chosen object per transcript; objects drawn from a controlled pool with matched training-distribution frequency (per the corpus frequency analysis).
- Question complexity and sentence length matched.
- One ambiguous probe (concept-boundary) and one unambiguous probe per stimulus, where applicable.

## Frequency analysis status

Subject to the same corpus-prevalence check as the other conditions. Expected status: **in-distribution**. 20Q transcripts and stance-of-respondent discussions are well-represented in training corpora (online forums, game-theory texts, pragmatic-reasoning literature, cooperative-AI work). The 20Q condition's role is *validation*, not OOD-probe-via-rarity.

## Open questions

- **Exact stance phrasings.** The three variants above are first-pass; piloting will reveal whether the framings produce the expected behavioural separation. If the model is insensitive to the framing wording but sensitive to in-transcript demonstration of the stance, the framing role weakens and the in-transcript signal carries.
- **Fourth variant: deceptive within the rules.** A *deceptive* stance — answering untruthfully where strategic and not caught — would test whether the model can represent non-truthful utility functions, a stronger ToM signal but a more contested stimulus design (introduces lying as a confound and stretches "playing 20 Questions correctly").
- **Hand-authored vs model-generated transcripts.** Hand-authored is cleaner but less naturalistic. Model-generated is naturalistic but introduces confounds (the generating model's own stance bleeds into the data). Likely answer: hand-authored for the controlled experiment, model-generated only for ecological-validity supplements.
- **Object-selection control.** Tomato is a salient example because of the fruit/vegetable boundary; not all objects offer the ambiguous-interpretation handle. The object pool needs to balance "objects with concept-boundary ambiguity available" against "objects with no such ambiguity" so the adversarial-stance variant has something to operate on.

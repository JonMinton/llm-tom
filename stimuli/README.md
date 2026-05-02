---
status: scaffold
last_update: 2026-05-02
---

# Stimuli

Three-way comparison structure. Each subdirectory holds the variants for one condition and a `spec.md` documenting the structural feature being probed.

```
stimuli/
├── README.md             # this file
├── psychological/        # Sally-Anne variants
├── technical/            # State-Rollback variants
├── novel/                # Combinatorially novel stimuli (form not yet finalised)
└── twenty-questions/     # 20Q-derived validation bridge (see twenty-questions/spec.md)
```

## Design principles

- **Matched pairs.** Each stimulus comes with a structurally-near control (false-belief / true-belief; divergent-state / non-divergent). The pair differs only in the structural feature of interest (epistemic divergence) — surface form, length, character/entity count, event count are matched.
- **Equivalent across conditions.** Where possible, control variables are matched not just within-pair but across conditions: a "complex" psychological stimulus has a counterpart "complex" technical stimulus.
- **OOD-in-the-right-way for the novel condition.** Surface notation tricks fail because early layers translate alien notation back to standard semantics before reaching the bottleneck. Non-standard update rules fail because they reduce to compositions of well-trained primitives. The novel condition must achieve *structural composition the model couldn't have abstracted from training*.

## Condition 1 — Psychological

Classical false-belief / true-belief Sally-Anne narratives. See `psychological/spec.md` (TBD) for the matched-variable schema.

## Condition 2 — Technical (State-Rollback)

System snapshot at T1, hidden migration at T2, recovery protocol at T3 must determine which server to query. Mathematically isomorphic to false-belief but in non-psychological domain.

The case for "in-distribution" here: distributed-systems texts, devops post-mortems, and database-recovery documentation are well-represented in training corpora. The frequency analysis (`analysis/frequency_analysis/`) is the empirical check on this case.

## Validation bridge — 20 Questions

A single-turn input combining a stance framing, a 4–6-turn transcript, and a probe question. Three stance variants (collaborative / strictly correctness-oriented / adversarial-within-rules) test whether the model's prediction of the answerer's response is sensitive to the answerer's utility function in the theoretically expected direction. **Not part of the primary three-condition matrix** that adjudicates A/B/C; run alongside as a construct-validity check that the candidate primitive identified via the primary conditions also engages on the motivating phenomenon. See `twenty-questions/spec.md` for full specification.

If the cross-bot review (P3) selects "pragmatic-stance distance" as the recursive-probe independent axis, 20Q is promoted from validation-only to a primary test bed for B1/B2 discrimination.

## Condition 3 — Combinatorially novel

**Form not yet finalised.** Leading candidate: cellular-automata-as-belief-systems, where cell states encode beliefs about neighbouring cells' states, updated by non-trivial rules, with divergent-state structure emerging from automaton dynamics rather than narrative specification.

Candidates considered and rejected:

- *Surface notation variants* — fail because early layers translate alien notation back to standard semantics before reaching the bottleneck (defeats the OOD claim).
- *Non-standard update rules* — fail because they reduce to compositions of well-trained primitives (negation, belief-attribution); the model can solve them by composing trained primitives, not by learning a new structural primitive.

This decision is **not yet locked**. Per `CLAUDE.md`, do not unilaterally pick a form — argue for the choice in this README and in `novel/spec.md`, and have the choice challenged before finalising.

## Variant generation

For each condition, generate ≥50 paraphrased variants for the frequency analysis (see `analysis/frequency_analysis/README.md`). Variants share structure; surface form (names, settings, narrative wrapping) varies.

When ready, store as plain Markdown or JSON, one stimulus per file, with metadata frontmatter capturing: condition, type (false/true-belief), structural feature, character count, syntactic complexity score.

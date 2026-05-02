---
status: scaffold
last_update: 2026-05-02
---

# Stimuli

Three-way comparison structure. Each subdirectory holds the variants for one condition and a `spec.md` documenting the structural feature being probed.

```
stimuli/
├── README.md            # this file
├── psychological/       # Sally-Anne variants
├── technical/           # State-Rollback variants
└── novel/               # Combinatorially novel stimuli (form not yet finalised)
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

## Condition 3 — Combinatorially novel

**Form not yet finalised.** Leading candidate: cellular-automata-as-belief-systems, where cell states encode beliefs about neighbouring cells' states, updated by non-trivial rules, with divergent-state structure emerging from automaton dynamics rather than narrative specification.

Candidates considered and rejected:

- *Surface notation variants* — fail because early layers translate alien notation back to standard semantics before reaching the bottleneck (defeats the OOD claim).
- *Non-standard update rules* — fail because they reduce to compositions of well-trained primitives (negation, belief-attribution); the model can solve them by composing trained primitives, not by learning a new structural primitive.

This decision is **not yet locked**. Per `CLAUDE.md`, do not unilaterally pick a form — argue for the choice in this README and in `novel/spec.md`, and have the choice challenged before finalising.

## Variant generation

For each condition, generate ≥50 paraphrased variants for the frequency analysis (see `analysis/frequency_analysis/README.md`). Variants share structure; surface form (names, settings, narrative wrapping) varies.

When ready, store as plain Markdown or JSON, one stimulus per file, with metadata frontmatter capturing: condition, type (false/true-belief), structural feature, character count, syntactic complexity score.

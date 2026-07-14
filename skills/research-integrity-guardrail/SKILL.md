---
name: research-integrity-guardrail
description: >-
  Mechanical pre-submission audit. Finds and locates errors; never rewrites. Checks that numbers
  in the abstract agree with the tables, that figure and reference cross-references survived
  renumbering, that every reference is both cited and listed, that percentages add up, that
  P-values carry the right test label. Runs the executable gates in `gates/`. Not for: judgment on
  novelty or scientific merit → nature-reviewer. 触发：一致性核查、核对数字、对不对得上、引了没列、列了没引、编号错位、交叉引用、终稿核对。
  Triggers: do the numbers match, are all figures cited, consistency check, cross-reference audit.
---

# Research Integrity Guardrail

## Principle

Use this skill to prevent real research-quality failures, not to evade detectors or disguise AI-written work. If the user frames the request as hiding automation, bypassing an Anti-Autoresearch detector, or covering tracks, redirect to a substantive integrity audit and revision plan.

For every research-facing task, preserve traceability: claims must point to evidence, numbers must reconcile, methods must be reproducible, and novelty must be bounded by related work.

## Default Workflow

1. Identify the artifact type: abstract, intro, related work, method, experiments, appendix, rebuttal, grant text, or full manuscript.
2. Run the red-flag audit below before polishing style.
3. Create an evidence ledger for risky claims when the task involves claims, results, or novelty:

| Claim/result | Evidence source | Numbers/tables/figures | Status | Required fix |
| --- | --- | --- | --- | --- |
|  |  |  | Supported / weak / missing / inconsistent |  |

4. Fix substance first: data, citations, logic, limitations, reproducibility, and consistency.
5. Polish language only after the evidence chain is sound.
6. In the final response, call out unresolved risks instead of smoothing them over.

## Red-Flag Audit

Check for these common low-quality research artifacts:

- Over-defensive patch writing: minor points get repeated explanations or local add-ons while the global story, hypothesis, and contribution become incoherent.
- Invented or unnecessary terminology: new coined phrases, broken abbreviations, awkward hyphenation, sudden bolding, fragmented abstracts, or jargon that does not buy precision.
- Numeric inconsistency: counts, percentages, ratios, table entries, figure labels, appendix values, and text claims do not reconcile.
- Suspicious number patterns: the same number or same digit multiples recur too often, especially after long-distance editing or across unrelated sections.
- Novelty overclaim: the method claims to be first, new, universal, or superior without careful comparison to related work.
- Related-work and citation errors: missing close baselines, miscited papers, citations that do not support the sentence, or unsupported contrastive claims.
- Ground-truth problems: undefined labels, questionable evaluation datasets, mismatch between appendix experiments and main-text experiments, or unclear provenance.
- Selective reporting: only favorable metrics appear; failed settings, excluded data, negative cases, variance, confidence intervals, and ablations are absent without explanation.
- Phantom or impossible results: results appear in text without an experiment path, code path, data path, table, figure, appendix entry, or reproducible calculation.
- Circular proof: the appendix only rephrases the claim or proves assumptions with outputs from the same method instead of independent validation.
- Trivial A-plus-B framing: the idea is merely a combination of two known components, with no clear mechanism, non-obvious insight, or empirical justification.

## Audit Actions

When drafting or revising:

- Replace vague novelty language with bounded claims: "we evaluate", "we extend", "we adapt", "we observe", or "under these settings".
- Add the closest related work before making comparative claims.
- Require each key result to trace to a table, figure, dataset, script, appendix item, or calculation.
- Recalculate percentages from raw counts and check that rounding rules are consistent.
- Cross-check every number that appears in multiple places.
- Mark unknowns explicitly instead of inventing ground truth, datasets, baselines, or citations.
- Include limitations, failure cases, and selection criteria when they materially affect interpretation.
- Keep terminology stable; define necessary terms once and remove decorative formatting.
- Make appendix material support the main text with independent detail: protocols, prompts, parameters, data splits, ablations, statistics, or reproducibility notes.

When reviewing:

- Lead with integrity risks before prose suggestions.
- Separate "unsupported", "inconsistent", "overclaimed", and "unclear" findings.
- Ask for raw evidence only when the answer cannot be verified from the available artifact.
- Do not recommend superficial humanizing, paraphrasing, or stylistic camouflage as a substitute for fixing evidence, logic, or reproducibility.

## Output Formats

For a quick audit, use:

```markdown
**Integrity Check**
- Supported:
- Needs Evidence:
- Numeric/Logic Issues:
- Overclaim/Related Work:
- Reproducibility Gaps:
- Priority Fixes:
```

For a deep audit, use:

```markdown
**Findings**
1. [Severity] Issue - location - why it matters - concrete fix.

**Evidence Ledger**
| Claim/result | Evidence source | Numbers/tables/figures | Status | Required fix |
| --- | --- | --- | --- | --- |

**Ready Criteria**
- All key claims have sources.
- All repeated numbers reconcile.
- Novelty is bounded and related work is represented.
- Methods and evaluation can be reproduced from the paper plus appendix.
- Limitations and exclusions are disclosed.
```

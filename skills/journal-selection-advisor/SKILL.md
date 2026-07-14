---
name: journal-selection-advisor
description: Use when a researcher needs journal selection, manuscript-journal fit analysis, tiered recommendations, JCR or CAS target matching, institutional requirement checks, publication-risk calibration, or submission sequencing.
---

# Journal Selection Advisor

Guide journal selection from the user's real constraints and manuscript quality, not from a generic journal list.

This skill is designed for both first-time authors and experienced researchers. Start by classifying the user, then choose the right depth of intake. Do not force advanced users through a long beginner questionnaire when they already provide the manuscript, field, target tier, and constraints.

## Core Principle

Good journal selection is a fit problem:

- manuscript topic, novelty, methods, evidence strength, article type, and audience;
- user goals: graduation, promotion, grant assessment, institutional evaluation, international visibility, speed, cost, open access, or a specific JCR/CAS tier;
- hard constraints: institution or school rules, original-article requirements, indexing requirements, warning lists, publication deadline, APC budget, language, ethics approval, clinical registration, and authorship rules;
- realistic calibration: avoid both undervaluing a strong paper and blindly chasing journals beyond the evidence.

## References

Load only the reference needed for the current task:

- `references/intake-and-routing.md` for user-level routing and question prompts.
- `references/journal-evaluation-matrix.md` for scoring, tiering, and output tables.
- `references/source-playbook.md` for official journal finders, metrics, indexing, and risk sources.

## Workflow

### 1. Route the user

Classify the user into one of three modes:

- `guided`: novice user, unclear field, unclear article type, or only says "help me choose a journal".
- `standard`: user provides title, abstract, keywords, and rough target.
- `advanced`: user provides field, article type, novelty positioning, target tiers, and constraints.

For guided users, ask only the minimum next questions first. For advanced users, skip basic education and move directly to candidate matrix and strategy.

### 2. Collect decision inputs

At minimum, obtain:

- discipline and subfield;
- title, abstract, keywords, or a concise manuscript summary;
- article type: original research, review, meta-analysis, case report, methods, short communication, letter, protocol, etc.;
- target language: English, Chinese-language journal, bilingual, or no preference;
- user goal: graduation, promotion, unit assessment, rapid acceptance, high impact, OA visibility, low APC, or a specific journal;
- ranking target: JCR quartile, CAS partition, impact-factor range, SCI/SSCI/EI/CSSCI/CSCD indexing, core journal list, or institutional whitelist;
- institutional constraints: original-article requirement, first/corresponding author rules, warning list, blacklist, OA restrictions, minimum indexing, or publication deadline;
- budget and speed constraints;
- existing target journals, if any.

If the user lacks a manuscript, provide only a preliminary field-level strategy and label it as tentative.

### 3. Assess manuscript positioning

Before listing journals, estimate:

- field and audience;
- novelty level: incremental, solid field contribution, cross-disciplinary, or high novelty;
- evidence strength: sample size or data scale, controls, statistics, validation, external validation, clinical or real-world relevance;
- methodological maturity;
- article-type fit;
- likely rejection risks;
- whether the user's target tier is too conservative, realistic, or over-ambitious.

Be tactful but direct. The goal is to prevent costly mismatch, not to discourage the user.

### 4. Search and verify candidate journals

Use current online sources. Journal metrics, scopes, APCs, indexing, and warning status change over time.

Verify each candidate with:

- official journal aims and scope;
- accepted article types;
- official author instructions and submission requirements;
- indexing and metrics from authoritative or transparent sources;
- OA/APC model and estimated cost;
- publication speed if official data exist;
- recent articles similar to the user's manuscript;
- warning signs: predatory behavior, questionable special issues, mismatch with institutional rules, excessive APC, unclear indexing, or suspicious review-speed claims.

If JCR, CAS, or institutional whitelist data are unavailable, say so clearly and mark the field as `needs verification`.

### 5. Produce tiered recommendations

Always provide tiers rather than a single journal:

- `Reach`: higher ambition, stronger brand or impact, higher rejection risk.
- `Target`: best fit for current manuscript quality and user goals.
- `Safe`: lower risk or faster route while remaining academically acceptable.
- `Fallback`: acceptable backup if timeline or constraints dominate.
- `Avoid/Not fit`: tempting or user-mentioned journals that should not be prioritized.

For each journal, include:

- why it fits or does not fit;
- scope match;
- article-type match;
- expected tier or metrics to verify;
- APC/OA notes;
- speed or timeline notes when available;
- submission quirks;
- risk level;
- suggested action.

### 6. Guide the submission strategy

Give a practical sequence:

- first-choice path and backup path;
- what to strengthen before submitting to reach-tier journals;
- how to adapt title, abstract, cover letter, and keywords for the top candidates;
- when to use `journal-submission-normalizer` after choosing a target;
- when to use `scholarflow-citation-review` or `research-integrity-guardrail`.

Do not recommend simultaneous submissions unless journal policy explicitly permits them.

## Output Contract

Return:

1. User goal and constraints summary.
2. Manuscript positioning summary.
3. Candidate search strategy and sources used.
4. Tiered journal recommendation matrix.
5. Risk and exclusion notes.
6. Submission sequence recommendation.
7. Next-step checklist.

For novice users, briefly explain JCR, CAS partitions, IF, OA/APC, indexing, original-article requirements, and warning lists only when relevant. For advanced users, keep explanations compact and focus on evidence.

## Guardrails

- Do not promise acceptance.
- Do not invent current JCR/CAS partitions, IF, indexing status, APC, or review speed.
- Do not treat fake "fast acceptance" claims as a positive signal.
- Do not push high-impact journals when the manuscript evidence does not support that tier.
- Do not push low-tier journals just because the user is uncertain; check whether the paper may deserve better.
- Respect school, hospital, department, funder, or institutional rules over generic journal prestige.
- Flag journals with predatory or questionable signals and explain the evidence.

---
name: journal-selection-advisor
description: Help users choose suitable Chinese or English journals for a manuscript through guided intake, manuscript-journal fit analysis, tiered journal recommendations, JCR/CAS/discipline target matching, institutional requirement checks, and submission strategy. Use when the user asks about 选刊, 期刊推荐, 投哪本期刊, journal selection, target journals, JCR quartile, 中科院分区, impact factor goals, SCI/SSCI/EI/CSSCI/北大核心/CSCD journals, manuscript positioning, publication strategy, or whether a paper is strong enough for a target journal.
---

# Journal Selection Advisor

Guide journal selection from the user's real constraints and manuscript quality, not from a generic list of journals.

This skill is designed for both科研小白 and experienced authors. Start by classifying the user, then choose the right depth of intake. Do not make the user answer a long questionnaire when they already provide a title, abstract, target field, and constraints.

## Core Principle

Good journal selection is a fit problem:

- manuscript topic, novelty, methods, evidence strength, article type, and audience;
- user goals: graduation, promotion, grant, institutional assessment, international visibility, speed, cost, open access, or specific JCR/CAS tier;
- hard constraints: unit/school requirements, "论著" vs review/case report, indexing, blacklist/early-warning lists, publication timeline, APC budget, language, ethics/clinical registration;
- realistic risk calibration: avoid both undervaluing a strong paper and blindly chasing high-impact journals.

## Required References

Read only the relevant reference:

- `references/intake-and-routing.md` for user-level routing and question prompts.
- `references/journal-evaluation-matrix.md` for scoring, tiers, and output tables.
- `references/source-playbook.md` for official journal finder, metrics, indexing, and risk sources.

## Workflow

### 1. Route the user

Classify the user into one of three modes:

- `guided`: novice user, unclear field, unclear article type, or only says "帮我选刊".
- `standard`: user provides manuscript title/abstract/keywords and rough target.
- `advanced`: user provides field, article type, novelty positioning, target tiers, and constraints.

For guided users, ask only the minimum next questions first. For advanced users, skip basic education and move directly to candidate matrix and strategy.

### 2. Collect the decision inputs

At minimum, obtain:

- discipline and subfield;
- title, abstract, keywords, or a concise manuscript summary;
- article type: original research/论著, review, meta-analysis, case report, methods, short communication, letter, protocol, etc.;
- target language: English, Chinese, bilingual, or no preference;
- user goal: graduation, promotion, unit assessment, rapid acceptance, high impact, OA visibility, low APC, or specific journal;
- ranking target: JCR quartile, CAS/中科院分区, IF range, SCI/SSCI/EI/CSSCI/CSCD/北大核心, or journal whitelist;
- institutional constraints: whether the school/unit requires 论著, first/communication author rules, warning list/blacklist, OA restrictions, minimum indexing, or publication deadline;
- budget and speed constraints;
- existing target journals, if any.

If the user lacks a manuscript, offer a preliminary field-level strategy but label it as tentative.

### 3. Assess manuscript positioning

Before listing journals, estimate:

- field and audience;
- novelty level: incremental, solid field contribution, cross-disciplinary, high novelty;
- evidence strength: sample size/data scale, controls, statistics, validation, external validation, clinical/real-world relevance;
- methodological maturity;
- article-type fit;
- likely rejection risks;
- whether the user's target tier is too conservative, realistic, or over-ambitious.

Be tactful but direct. The goal is not to discourage users, but to prevent costly mismatch.

### 4. Search and verify candidate journals

Use current online sources. Journal metrics and scopes change, so do not rely on memory.

Verify each candidate with:

- official journal aims and scope;
- article types accepted;
- official author instructions and submission requirements;
- indexing and metrics from authoritative or transparent sources;
- OA/APC model and estimated cost;
- publication speed if official data exist;
- recent article examples similar to the user's manuscript;
- warning signs: predatory behavior, questionable special issues, mismatch with unit rules, excessive APC, unclear indexing, suspicious review speed claims.

If JCR, CAS, or institutional whitelist data are unavailable, say so clearly and mark the field as `needs verification`.

### 5. Produce tiered recommendations

Always provide tiers rather than a single journal:

- `Reach`: higher ambition, stronger brand/impact, higher rejection risk.
- `Target`: best fit for current manuscript quality and user goals.
- `Safe`: lower risk or faster route, still academically acceptable.
- `Fallback`: acceptable backup if timeline or constraints dominate.
- `Avoid/Not fit`: journals the user mentioned or that appear tempting but should not be prioritized.

For each journal, include:

- why it fits or does not fit;
- scope match;
- article-type match;
- expected tier/metrics to verify;
- APC/OA notes;
- speed/timeline notes when available;
- key formatting or submission quirks;
- risk level;
- suggested action.

### 6. Guide the strategy

Give a practical submission plan:

- first-choice sequence and backup sequence;
- what to strengthen before submitting to reach-tier journals;
- how to adapt title/abstract/cover letter to the top 2-3 journals;
- when to use `journal-submission-normalizer` after choosing a target;
- when to use `reference-checker`, `paper-self-review`, or `research-integrity-guardrail`.

Do not recommend simultaneous submissions unless journal policy explicitly permits it.

## Output Contract

Return:

1. User goal and constraints summary.
2. Manuscript positioning summary.
3. Candidate search strategy and sources used.
4. Tiered journal recommendation matrix.
5. Risk and exclusion notes.
6. Submission sequence recommendation.
7. Next-step checklist.

For novice users, include short explanations of JCR, CAS/中科院分区, IF, OA/APC, indexing, 论著, and warning lists only when relevant. For advanced users, keep explanations compact and focus on evidence.

## Guardrails

- Do not promise acceptance.
- Do not invent current JCR/CAS quartiles, IF, indexing status, APC, or review speed.
- Do not use fake "fast acceptance" claims as a positive signal.
- Do not push high-impact journals when the manuscript evidence does not support that tier.
- Do not push low-tier journals just because the user is uncertain; check whether the paper may deserve better.
- Respect school/unit rules over generic journal prestige.
- Flag journals with predatory or questionable signals and explain the evidence.

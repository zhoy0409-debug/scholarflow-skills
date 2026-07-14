---
name: scholarflow-literature-monitor
description: Use when a researcher needs a bounded, repeatable literature-monitoring workflow with explicit sources, screening rules, delivery format, and review cadence.
---

# ScholarFlow Literature Monitor

ScholarFlow Literature Monitor helps a researcher keep up with a defined topic
without turning an alert feed into unreviewed evidence. It designs a monitoring
routine, screens incoming records consistently, and returns a compact research
brief with provenance and limits.

## Establish the Monitoring Brief

Before proposing automation, confirm or state the following assumptions:

- research topic, population or system, and key concepts;
- priority sources and permitted evidence types;
- date window, language limits, and exclusion rules;
- delivery cadence and preferred output format;
- whether the goal is discovery, grant intelligence, methods tracking, or a
  living review;
- the maximum number of records that can be meaningfully reviewed per cycle.

Use [scoring-system.md](references/scoring-system.md) to define transparent
screening rules. Use [gap-analysis.md](references/gap-analysis.md) when the
user needs recurring synthesis rather than a list of new papers.

## Default Workflow

1. Build a reproducible query and source plan. Use
   [ScholarFlow Literature Search](../scholarflow-literature-search/SKILL.md)
   for the baseline search or for any ad hoc deep dive.
2. Retrieve only the sources the active environment can access. Record the
   source, query, date, identifier, and any coverage limitation for each record.
3. Deduplicate records without losing their original source provenance.
4. Apply the agreed screening criteria. Separate high-priority records from
   background leads and uncertain items.
5. Produce a compact brief using
   [literature-push-template.md](templates/literature-push-template.md), with
   a clear recommendation for the next human review action.
6. Archive the queries, screened identifiers, and decisions so that the next
   cycle is comparable with the previous one.

## Optional Scheduling

Scheduling is opt-in. Do not create a cron job, messaging integration, or
external alert without the user's explicit approval and the required local
credentials. When requested, use [cron-setup.md](references/cron-setup.md) to
provide a platform-appropriate configuration that the user can inspect before
enabling.

The monitor may prepare content for an existing email, chat, or note-taking
workflow, but it must not claim to have delivered a message unless the active
environment actually completed that action.

## Per-Cycle Output

Return, at minimum:

1. search scope, sources, dates, and query changes;
2. screened records with stable identifiers and a short relevance rationale;
3. priority signals, gaps, or contradictions that require human attention;
4. excluded and uncertain leads when they prevent repeated work;
5. coverage limits and the next review action.

An alert is a discovery aid, not a substitute for critical reading or evidence
appraisal.

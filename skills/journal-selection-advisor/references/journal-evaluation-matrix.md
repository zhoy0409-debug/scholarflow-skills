# Journal Evaluation Matrix

Use this matrix to compare candidates.

## Candidate Matrix

| Tier | Journal | Publisher | Scope fit | Article type fit | Target metrics | Indexing | APC/OA | Speed | Fit rationale | Main risk | Action |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Reach |  |  | High/Med/Low |  | JCR/CAS/IF to verify |  |  |  |  |  |  |
| Target |  |  |  |  |  |  |  |  |  |  |  |
| Safe |  |  |  |  |  |  |  |  |  |  |  |
| Fallback |  |  |  |  |  |  |  |  |  |  |  |
| Avoid |  |  |  |  |  |  |  |  |  |  |  |

## Scoring Dimensions

Use scores only as decision support, not as absolute truth.

| Dimension | Weight | How to judge |
|---|---:|---|
| Scope match | 25 | Aims/scope, recent articles, audience fit |
| Article type match | 10 | Accepts original research/review/case/meta/etc. |
| Evidence-level match | 20 | Novelty, sample size, validation, methods, story strength |
| User goal match | 15 | Graduation/promotion/IF/CAS/JCR/speed/cost |
| Institutional fit | 15 | Unit whitelist/blacklist, required indexing, 论著 rule |
| Practical feasibility | 10 | APC, timeline, submission complexity, language |
| Risk | -15 | Predatory signals, poor fit, metric uncertainty, special issue risks |

## Tier Logic

- `Reach`: high scope fit but evidence/novelty may be near the lower edge for the journal.
- `Target`: best balance of fit, quality, and user goals.
- `Safe`: strong fit and lower risk, but lower prestige or broader scope.
- `Fallback`: acceptable if deadline, budget, or repeated rejection becomes dominant.
- `Avoid`: poor scope fit, policy conflict, questionable quality, or user-goal mismatch.

## Output Summary Template

```markdown
# Journal Selection Report

## User goal and constraints

...

## Manuscript positioning

...

## Recommended submission sequence

1. ...
2. ...
3. ...

## Candidate matrix

<table>

## Why these journals

...

## Not recommended / avoid

...

## What to improve before submission

- ...

## Next steps

- Use `journal-submission-normalizer` after choosing the target journal.
- Use `reference-checker` for references.
- Use `paper-self-review` for final quality check.
```

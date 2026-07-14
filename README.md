<div align="right"><a href="README.zh-CN.md">中文</a></div>

# ScholarFlow

**Other skill collections hand the model a prompt. ScholarFlow hands it a gate.**

A prompt says *"check the panel alignment before you deliver."*
The model says "checked" and gives you a crooked figure.

A gate says `BLOCK: panel label off the shared grid` — and exits 2.

Every gate in this repo came from a failure that actually happened. None of them are hypothetical.

```bash
/plugin marketplace add zhoy0409-debug/scholarflow-skills
/plugin install scholarflow
```

---

## The gates

```bash
python3 gates/gate_checks.py data      --file raw.xlsx
python3 gates/gate_checks.py claims    --claims c.csv --evidence e.csv --manuscript draft.md
python3 gates/gate_checks.py narrative --matrix slides.csv
```

Exit code 2 means a gate fired. 14 tests, each pinned to the incident it came from.

### `data` — the one that matters most

```
BLOCK filename_not_mock       PCa_Mock_Data_320_Final.csv
BLOCK missingness_plausible   320 × 191, zero missing cells
```

A dataset was about to be analysed and written up as a real 320-patient cohort, with an ethics
approval number and a funding line attached. The filename said `Mock`. The matrix had **zero
missing cells** — a real questionnaire study never does.

Both were caught because someone happened to read carefully. That is not a control. That is luck.

Now it is a gate.

### `claims` — no ledger, no sentence

```
BLOCK claims_have_sources   C002 has no source
BLOCK certainty_in_enum     'candidate_supported_moderate_to_strong' is not in the controlled vocabulary
BLOCK no_orphan_citation    the text cites [C777]; the ledger has no C777
BLOCK no_unused_claim       C005 sits in the ledger and appears nowhere in the text
```

Build the ledger first, then generate sentences from it. Not the other way around.

Writing prose first and hunting for citations afterwards *manufactures* unsourced claims — and
quietly pushes you toward whichever source agrees with the sentence you already wrote.

`certainty_in_enum` exists because one free-text value (`candidate_supported_moderate_to_strong`)
silently disabled every automated check downstream. A controlled enum **and** a free-text note
column. Never one field doing both jobs.

### `narrative` — one slide, one step forward

```
BLOCK no_duplicate_advance   "CRAB definition" is introduced on both P5 and P6
```

Four separate lab-meeting decks failed the same way: every slide re-told the whole story from the
beginning.

The fix is counter-intuitive. The slide that *looks* redundant is usually not the one at fault —
**a claim belongs to the first slide that can land it properly, and every earlier slide must give
it up.**

---

## Also in the box

**`shared/core/`** — the same failures, as loadable guidance:

| | |
|---|---|
| `figure-qa.md` | *Code ran ≠ figure is right.* matplotlib does not raise when a label is clipped. Open the PNG. Look at it at final insertion size. Then embed it in the real document and look again. |
| `integrity-gates.md` | A qPCR report claimed 2× upregulation. The raw Ct hadn't moved, and the housekeeping control had drifted 1.5 Ct across groups. The 2× was an artefact of normalisation. |
| `visual-honesty.md` | An AI-generated slide illustration depicted *A. baumannii* as a soil "natural decomposer" — contested in the literature, and indefensible at a defence. If you can't answer *"is there a citation for that?"*, the image doesn't ship. |
| `claim-ledger.md` · `narrative-advance.md` · `preflight.md` | |

**`skills/nature-*`** — manuscript drafting, polishing, figures, decks, referee simulation,
reviewer response. Declarative manifests: each skill loads only the fragments the request needs,
not its whole library.

**`skills/bio-*`** (130) and the tool references (samtools, bcftools, Prokka, Bakta…) — a bundled
bioinformatics library. Useful. Not what makes this repo different.

---

## The repo defends itself

Six CI checks. **Each one corresponds to a bug that shipped.**

| Check | The bug it exists for |
|---|---|
| `check_health` | 15 skills had their SKILL.md regenerated from a template. The manifests survived; 400 KB of references survived; **not one line told the model to load them.** The skills were hollow, and nothing noticed. Then a second sweep found 14 more — because the first version of this check only looked at the skills I remembered to look at. **A CI that checks only where you thought to look is worse than no CI: it gives you false confidence.** |
| `check_xrefs` | Skills name each other in their own bodies. Delete a skill and those names dangle — **and the model will happily go call a skill that no longer exists.** This check caught `journal-selection-advisor` pointing at a skill deleted one commit earlier. |
| `check_docs` | After 11 skills were removed, the README still told people to use them. |
| `sync_shared` | `shared/` and `skills/_shared/` were nine byte-identical copies. Editing one meant editing nine. |
| `gen_index` | A hand-written index goes stale. A generated one cannot. |
| `pytest gates/tests` | The gates themselves can break. |

All six are **statically checkable**. They should have been caught by a machine, not found months
later by a human reading the repo.

---

## Boundaries

Download only what you're authorised to access. Mark unverifiable citations as unverifiable
instead of hiding it. Results, statistics and experimental data come from *your* materials — never
invented. File deletion, overwrite and external publication require your confirmation. Statistical
conclusions, mechanistic claims, clinical meaning and journal fit stay conservative.

## Docs

[SKILL_INDEX](SKILL_INDEX.md) (generated) · [Architecture](docs/ARCHITECTURE.md) ·
[Where each gate came from](docs/INSIGHTS.md) · [Routing eval](docs/EVAL.md)

MIT.

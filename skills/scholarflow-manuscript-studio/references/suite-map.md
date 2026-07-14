# Suite Map

ScholarFlow Manuscript Studio is split into task-focused skills:

| Skill | Responsibility |
|---|---|
| `manuscript-studio` | route the workflow |
| `manuscript-studio-ui` | launch external terminal configuration UI |
| `manuscript-studio-intake` | collect configuration |
| `manuscript-studio-research` | index local references, research target scene, and learn examples |
| `manuscript-studio-citation` | build citation support candidates |
| `manuscript-studio-rewrite` | rewrite an existing draft |
| `manuscript-studio-build` | build from a materials folder |
| `manuscript-studio-latex` | assemble and guard LaTeX |
| `manuscript-studio-translate` | produce complete translation_zh/ with row-by-row translation |
| `manuscript-studio-humanize` | reduce AI detection patterns via tiered stylistic constraints |
| `manuscript-studio-audit` | check completeness, integrity audit, structured review, and translation coverage |

Use the orchestrator for end-to-end tasks. Use a child skill directly when the
user asks for that stage only.

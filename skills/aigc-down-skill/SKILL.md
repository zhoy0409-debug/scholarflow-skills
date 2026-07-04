---
name: aigc-down-skill
description: Reduce AIGC-like writing artifacts in academic text by routing to paper-spine-humanize and nature-polishing, with a change matrix and preservation of scientific meaning.
---

# AIGC Down Router

Use this alias when the user asks to reduce AIGC-like style, lower AI-writing signals, or make academic prose read more human.

## Route

1. Load `paper-spine-humanize` for the diagnostic matrix and tiered rewrite constraints.
2. Load `nature-polishing` for Nature-style prose after the diagnostic pass.
3. Keep all claims, data, citations, and technical meaning intact.
4. Record material changes when the task is manuscript-facing.

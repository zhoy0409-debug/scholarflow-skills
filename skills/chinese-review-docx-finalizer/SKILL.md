---
name: chinese-review-docx-finalizer
description: Use when doing targeted pre-submission revision or final formatting of Chinese academic review manuscripts in Word DOCX, especially preserving an established structure while synchronizing abstracts, removing AI/process wording, renumbering references, checking figure/table captions, table pagination, footnotes, images, and DOCX QA.
---

# Chinese Review DOCX Finalizer

Use this skill for Chinese-language review manuscripts in Word format when the user asks for structural polish, second/third/final revision, reference renumbering, figure/table cleanup, or submission formatting. It is especially useful for Chinese core journal style reviews where the section structure is already approved and the work must be conservative.

For DOCX editing tasks, also use the available `documents:documents` skill or bundled document runtime when rendering, inspecting, or validating Word output.

## Operating Principles

1. Preserve scope first. If the user says the structure is fixed, do not add or remove first-level headings, restore deleted sections, rewrite the article, or add unverified literature.
2. Preserve scientific content. Do not change checked drug names, models, doses, indicators, conclusions, or reference details unless the user provides corrected information.
3. Work from the existing DOCX. Make a copy in the workspace, edit the copy, and leave the source file intact.
4. Prefer deterministic edits. Use `python-docx` and XML inspection for formatting and numbering; use manual prose edits only where needed.
5. Keep a revision note. Record what changed, what was checked, and what still needs human final review.

## Standard Workflow

1. Inventory the document before editing:
   - Headings and their order.
   - Chinese and English abstracts/keywords.
   - Figure captions, table captions, and first in-text mentions.
   - Table count and table row/header pagination settings.
   - Reference list entries, body citations, and table citations.
   - Front matter fields, visible `footnoteRef` text, and hidden Word footnote-reference XML.
   - Embedded image pixel dimensions and effective DPI if available.

2. Confirm the protected structure:
   - Compare current headings with the user's required heading list.
   - If the structure is fixed, edit only wording, citations, captions, and formatting.
   - Do not reintroduce older sections such as deleted "problems and prospects" sections unless explicitly asked.

3. Revise text conservatively:
   - Synchronize Chinese and English abstracts with the current body structure only when asked.
   - Remove process residue such as `本节宜`, `正式发表研究显示`, `提示词式表达`, `AI式表达`, and similar drafting instructions.
   - Cool down project-report wording such as `作用边界`, `重要切入点`, and `延伸研究方向` when it reads unnatural; replace with journal-style terms such as `应用定位`, `机制环节`, `研究内容`, or `研究线索`.
   - Avoid overstating traditional Chinese medicine efficacy, clinical translation, cancer prevention, or evidence from in vitro and animal studies.

## Reference Renumbering

Use reference renumbering only when the user's request or citation order requires it.

1. Parse the reference list as grouped entries:
   - A new entry starts with a paragraph matching `^[n]`.
   - Bilingual continuation paragraphs without a new number stay attached to the preceding entry.
   - Preserve the original text of each entry unless the user supplies corrected bibliographic information.

2. Build an explicit old-to-new map:
   - Example: old `[39]` becomes new `[19]`; old `[19]` to `[38]` shift to `[20]` to `[39]`.
   - Apply the map to body paragraphs, table cells, captions, and reference-list numbering.
   - Update summary tables even when their internal order is not strictly ascending.

3. Avoid accidental bracket damage:
   - Normalize citation brackets to `[1]`, `[1-2]`, `[3-6]`.
   - Do not treat `[J]`, `[D]`, `[M]`, or journal abbreviations as numeric citations.
   - After editing, search for mixed brackets such as `[1]］`, `[2］`, `［1]`, and visible Word residue.

4. Validate after renumbering:
   - Every cited numeric reference should exist in the reference list.
   - No reference-list number should be duplicated or skipped.
   - Check special sentences for repeated same-sentence citations, such as `Jiang等[33]研究显示...缓解[33]`.
   - If a summary table remains non-monotonic because of its topic grouping, report it for human final review rather than rearranging scientific content.

## Figures, Tables, and Captions

1. Captions:
   - Put Chinese and English captions on separate paragraphs.
   - Use stable caption formats, for example `图 1 ...` and `Figure 1 ...`, `表 1 ...` and `Table 1 ...`.
   - Ensure the first in-text mention appears before the corresponding figure or table caption.

2. Figures:
   - Inspect embedded image size and effective DPI.
   - Replace low-resolution images only when a reliable high-resolution source file exists in the same folder and clearly represents the same scientific figure.
   - If no high-resolution source is available, do not redraw or regenerate figures; state that 300 dpi or vector figures should be reinserted before submission.

3. Tables:
   - Set every row to not split across pages by adding `w:cantSplit`.
   - Set the header row to repeat on each page by adding `w:tblHeader`.
   - Keep table captions with the following table when possible.
   - For long tables, set cell paragraph spacing before/after to 0 and line spacing to single; reduce font size slightly only when needed.
   - If a long table still creates a single-character orphan line, start the table on a new page rather than deleting columns or content.

## Front Matter and Footnotes

1. Check title, authors, affiliations, funding, first author, corresponding author, English title, English authors, English affiliations, abstracts, and keywords for visible residue.
2. Remove visible text such as `姓名[footnoteRef:0]` or `Name[footnoteRef:1]`.
3. Inspect `word/document.xml` for hidden `<w:footnoteReference>` elements in front matter. Remove only clearly erroneous front-matter footnote runs; do not remove legitimate academic footnotes unless requested.

## Final QA

1. Run the bundled QA script if available:

```bash
python scripts/docx_review_qa.py manuscript.docx
```

2. Attempt to render the DOCX to images/PDF using the document runtime or `documents:documents` instructions. If LibreOffice or `soffice` is unavailable, say that visual rendering could not be completed in the environment.
3. Re-open the edited DOCX programmatically and confirm it is readable.
4. Provide the edited DOCX path and a concise revision note covering:
   - Reference ordering and special renumbering.
   - Updated or completed reference entries.
   - Table pagination and caption checks.
   - Figure clarity and whether high-resolution figures are still needed.
   - Footnote residue cleanup.
   - Remaining items requiring human final review.


---
name: chinese-docx-reference-unifier
description: Use when revising a Chinese Word manuscript to standardize in-text citation superscripts and end-reference formatting for journal submission, especially for Chinese journals such as 中国实验方剂学杂志; preserves non-reference content and produces an audit report.
---

# Chinese DOCX Reference Unifier

Use this skill when the user asks to revise only the in-text citation markers and the end-reference list in a `.docx` manuscript. It is meant for Chinese journal submissions where citations are numbered in order of appearance and displayed as Word superscript markers.

## Core Principle

Only change reference-related content unless the user explicitly expands the scope. Preserve the title, abstract, author information, body wording, figures, tables, and non-reference formatting.

Work from a copy of the input file and produce both:

- a revised `.docx`
- a Markdown audit report

When available, combine this skill with `documents:documents` for DOCX/PDF handling, `chinese-review-docx-finalizer` for Chinese manuscript formatting patterns, and `reference-checker` for bibliographic verification.

## Workflow

1. Locate the reference section.
   Find the paragraph headed `参考文献` or the closest journal-specific equivalent. Treat all numbered paragraphs after this heading as the reference block. Bilingual translation lines that follow a Chinese reference are continuation lines, not new references, unless they begin with a new `[n]`.

2. Inventory references and citations.
   Parse end references as `[1]`, `[2]`, etc. Collect all citation markers before the reference section, including body text, captions, footnotes, and tables. Separately record table citation columns such as `文献`.

3. Preserve numbering.
   Do not reorder citations or references unless the user explicitly asks. Check that end-reference numbers are continuous and unique. Never set end-reference list numbers `[1]`, `[2]` as superscript.

4. Set in-text citation markers.
   Convert body and caption markers such as `[1]`, `[1-2]`, `[3-6]`, `[8-11,14]`, `[23,35]` to Word superscript. Keep table `文献` column markers as plain text by default for readability, unless the whole table already uses superscript cleanly and can remain uniform.

5. Normalize author rules.
   For Chinese references, list up to three authors and use `，等` when there are more than three. For English references, choose one policy and apply it consistently, usually `，et al.` for English-language references. If using `et al.` while the target journal says `等`, state this in the report and ask the author to confirm current journal practice.

6. Normalize reference formats.
   Use these patterns unless the target journal gives a stricter rule:

   ```text
   [n] 中文作者1，中文作者2，中文作者3，等. 中文题名[J]. 刊名，年，卷（期）：起页-止页.
   [n] AUTHOR A A，AUTHOR B B，AUTHOR C C，et al. English title[J]. Journal，Year，Volume（Issue）：Start-End.
   [n] 作者. 题名[D]. 城市：学校，年.
   [n] AUTHOR A A. English title[D]. City：University，Year.
   ```

   For article-number references, keep the article number instead of inventing pages:

   ```text
   Journal，Year，Volume（Issue）：ArticleNumber.
   ```

   For Epub ahead of print records, preserve DOI, article number, Epub status, and PMID:

   ```text
   [n] Authors. Title[J]. Journal，Year：ArticleNumber. doi：xxxxx. Epub ahead of print. PMID：xxxxx.
   ```

7. Keep bilingual translation lines stable.
   If Chinese references already include English translation lines, keep them unnumbered, directly under the Chinese item, with no blank paragraph between the pair. Format them consistently with the reference block. Do not delete translation lines unless the user asks.

8. Apply reference-block style only to reference paragraphs.
   Use 10.5 pt, black, paragraph spacing before/after 0, single line spacing, and a hanging indent if the journal wants aligned wrap lines. Use Chinese font for CJK text and Times New Roman for Latin text where the DOCX tooling supports split font settings. Remove hyperlink styling, underline, field-code residues, and automatic URL styling in the reference block.

## Verification

Use authoritative sources when network access is available:

- PubMed for biomedical records, especially generic titles and guideline updates.
- Crossref for DOI, journal, volume, issue, page, and article-number metadata.
- Journal pages, CNKI, Wanfang, VIP, or official publisher pages for Chinese-language references.

Do not trust the first Crossref hit blindly. Cross-check title, year, journal, author list, volume/issue, pages or article number, and DOI. If the source cannot be verified, do not invent missing metadata; mark it as `需作者人工核对`.

Useful lessons from prior work:

- Generic titles such as `Gastric cancer` can return multiple plausible Crossref matches; use PubMed or DOI confirmation.
- Guideline references may have old and new versions with similar titles; verify exact year, journal, volume, issue, and pages.
- Open-access journals often use article numbers, not page ranges; keep article numbers and flag them for author confirmation.
- Missing issue numbers can sometimes be resolved from Crossref or PubMed, but never fill them without a source.
- A Word font table may list unused fonts; inspect applied run fonts rather than treating every font-table entry as active formatting.

## Required Audit Report

The Markdown report should include:

- Input and output file names.
- Completed edits: citation superscripts, reference numbering continuity, author rule, punctuation, font/size/color, hyperlink cleanup, and translation-line handling.
- Changed reference items with before/after details and verification source.
- Article-number references that need author confirmation.
- Missing issue/page/DOI items or records that could not be verified.
- Epub ahead of print records and whether DOI/PMID/article number were preserved.
- Citation cross-check: body/table citation numbers not found in references and references not cited in body/table.
- Rendering or visual QA status. If `soffice`, `pdftoppm`, or another renderer is unavailable, state that visual rendering could not be completed.

## Quality Gate

Before finishing:

1. Compare all paragraph text before the reference heading between input and output. It should be unchanged except citation run styling.
2. Compare all table text between input and output. It should be unchanged unless the user explicitly requested table citation styling.
3. Confirm all in-text citation markers are superscript where required.
4. Confirm end-reference list numbers are not superscript.
5. Confirm reference numbers are continuous and no reference line was accidentally split into a new numbered item.
6. Confirm no DOI, PMID, article number, or `Epub ahead of print` text was removed.
7. Open or render the resulting `.docx` when possible; otherwise report the tooling limitation clearly.

## Implementation Notes

Use structured DOCX tooling such as `python-docx` plus direct OOXML edits for superscript, font, field, and hyperlink cleanup. Avoid broad text replacement across the whole document. When scripting in PowerShell or Python on Windows, be careful with Chinese paths and encoding; prefer passing paths as arguments or copying the source to an ASCII workspace alias before processing.

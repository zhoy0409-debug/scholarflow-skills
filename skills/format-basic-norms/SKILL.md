---
name: format-basic-norms
description: Universal baseline academic formatting and reference-integrity standard. Use automatically for every conversation involving drafting, rewriting, translation, polishing, review, editing, formatting, or checking Chinese or English academic/scientific text, manuscripts, abstracts, titles, figures, tables, legends, theses, reports, grants, cover letters, reviewer responses, or reference lists. Apply this as a default final quality-control pass even when the user does not explicitly ask for formatting checks.
---

# Format Basic Norms

## Non-Negotiable Default

Treat this skill as the baseline formatting layer for academic work. Before finalizing any academic/scientific text, run a proportional check for typography, statistical symbols, gene/protein notation, abbreviations, superscripts/subscripts, capitalization, and reference-citation integrity.

If target journal, institution, thesis, grant, or publisher instructions are provided, follow those instructions first and use this skill for unresolved baseline issues. Do not silently overwrite a journal-specific convention.

When the user provides only a fragment, check only the visible fragment and state what requires the full manuscript, tables, figures, or reference list.

## Default Workflow

1. Identify language, field, document type, target style, and whether the text contains references, tables, figures, equations, genes/proteins, organisms, chemicals, or statistics.
2. Apply baseline format rules silently while editing. Preserve meaning and do not invent missing data.
3. Check reference integrity whenever in-text citations or a reference list are present.
4. Return the corrected text first when the user asked for editing or polishing.
5. Add a concise "格式核查" note only for important fixes, unresolved ambiguities, missing source data, or style conflicts.

## Typography And Fonts

- Use SimSun/Songti as the default Chinese font and Times New Roman as the default English, number, Latin-symbol, and reference-list font unless a template or journal says otherwise.
- Keep Chinese and English punctuation style consistent with the sentence language.
- Use a single spacing convention consistently: Chinese body text may keep Chinese/English and Chinese/number spacing according to the required template; English text should use standard spaces around words, values, and units.
- Use SI units and standard unit symbols. Put a space between number and unit in English text, such as `5 mg`, `37 °C`, and `10 min`; keep `%` attached to the number unless the target style says otherwise.
- Use real mathematical operators where possible: `±`, `×`, `<`, `>`, `≤`, `≥`, and avoid replacing multiplication with lowercase `x`.

## Statistical Symbols

- Italicize Latin-letter statistical variables and test statistics: *P* or *p*, *n*/*N*, *t*, *F*, *r*, *R*, *R*², *z*, *U*, *H*, *Q*, *β*, *SE* only if the target style treats it as a variable. Keep common abbreviations roman unless the journal says otherwise: SD, SEM, CI, OR, RR, HR, AUC, ANOVA.
- Use one convention for significance values throughout: `P < 0.05`, `p = 0.032`, or the journal-required form. Do not mix uppercase and lowercase P/p in the same manuscript.
- Report exact P values when available. Use threshold forms only when appropriate, such as `P < 0.001`.
- Keep spaces around comparison operators in English academic style: `P < 0.05`, `95% CI: 1.12-2.45`.
- Make statistical reporting internally complete: test name, statistic, degrees of freedom when relevant, sample size, effect size or estimate, CI, and P value.

## Gene, Protein, Species, And Variant Names

- Italicize gene symbols; keep protein names and protein symbols roman/non-italic unless the target style says otherwise.
- Follow organism conventions where known: human genes are usually all caps italic, such as *TP53*; mouse/rat genes usually use initial cap plus lowercase italic, such as *Trp53*; bacterial genes are commonly lowercase italic, such as *lacZ*.
- Keep protein symbols in roman type and usually uppercase for human proteins, such as TP53 protein, p53, EGFR, and IL-6.
- Italicize Latin binomials for species names, such as *Escherichia coli*. Spell out genus at first mention and abbreviate later when unambiguous, such as *E. coli*.
- Check gene/protein capitalization carefully because capitalization can change meaning across species.
- Use HGVS-style variant notation when applicable and do not improvise variants: *TP53* c.743G>A, p.Arg248Gln. Flag uncertain or nonstandard variant expressions for verification.

## Abbreviations

- Define an abbreviation at first appearance: English full term (ABBR); Chinese text usually uses Chinese full term（英文 full term, ABBR）or Chinese full term（ABBR）, depending on field and journal style.
- Define abbreviations independently in title/abstract, main text, tables, and figure legends when those sections may stand alone.
- Do not introduce an abbreviation that is used only once or twice unless it is a standard field term or improves readability.
- Use one abbreviation form consistently after definition. Do not alternate between full term, synonym, and abbreviation unless needed for clarity.
- Check plural, hyphenation, and capitalization of abbreviations: qRT-PCR vs RT-qPCR, RNA-seq vs RNA sequencing, COVID-19, SARS-CoV-2, mRNA, miRNA.

## Superscripts, Subscripts, Equations, And Symbols

- Use subscripts for chemical formulas and molecular notation: H₂O, CO₂, O₂, Ca²⁺ where the final format supports it.
- Use superscripts for charges, isotopes, powers, footnote markers, and statistical annotations when required: m², 10⁶, ¹⁴C, a/b/c table notes.
- Keep mathematical variables italic and operators/functions roman where possible: *x*, *y*, *P*; log, ln, sin, max.
- Make table significance markers consistent and explain them in table notes: `* P < 0.05`, `** P < 0.01`, `*** P < 0.001`.
- Avoid ambiguous plain-text substitutes when rich formatting is expected. If the final medium cannot preserve superscript/subscript, flag the items that need manual formatting.

## Capitalization, Headings, And Terms

- Match heading style to the target template: sentence case, title case, numbered headings, or Chinese numbered hierarchy.
- Keep technical terms consistently capitalized. Do not mix "Western blot", "western blot", and "Western Blot" unless a style guide requires it.
- Capitalize taxonomic ranks and names correctly: family/order names are roman; genus/species binomials are italic.
- Keep product names, database names, software names, packages, and instruments in their official capitalization when known.
- Use "et al." consistently in English references and text, with punctuation matching the target style.

## Reference And Citation Integrity

Always check references when the manuscript or fragment contains in-text citations or a reference list.

For numeric citation styles:

- Confirm the first in-text appearance follows ascending order: [1], [2], [3] or superscript 1, 2, 3.
- Detect skipped numbers, duplicated numbers, citations first appearing out of order, and references cited in text but missing from the list.
- Detect reference-list items that are never cited in text.
- Check citation ranges and groups: `[3-5]` must include 3, 4, and 5; grouped citations should be ascending and nonduplicated.
- Renumber only when the full citation context is available. If not, flag the affected locations.

For author-year styles:

- Confirm every in-text author-year citation has a matching reference-list entry and every listed reference is cited.
- Check spelling of author names, publication year, `et al.` usage, and 2020a/2020b disambiguation.
- Confirm reference-list ordering follows the required style, commonly alphabetical by first author.

For all styles:

- Keep reference-list format uniform: author order, initials, article title capitalization, journal/book title style, year, volume, issue, pages or article number, DOI/URL, punctuation, and journal abbreviation/full title.
- Check completeness: missing authors, year, title, source, volume/issue/pages, DOI, publisher, preprint server, access date when required.
- Flag likely duplicates, inconsistent journal names, suspicious years, incomplete DOI strings, broken numbering, and references that look unrelated to the cited claim.
- Do not fabricate missing bibliographic details. Verify from DOI, PubMed, Crossref, publisher pages, or the user's source files when accuracy matters or when the user asks for completion.

## Output Pattern

For editing tasks, prefer:

1. Corrected text.
2. Brief format notes only for material changes or unresolved issues.
3. A reference-check summary if citations or a reference list were present.

For review-only tasks, use this compact structure:

- `必须修改`: errors that affect correctness, journal compliance, or citation integrity.
- `建议统一`: consistency issues.
- `需全文核查`: items that require the complete manuscript, tables, figures, or reference list.

Keep the report practical and avoid overwhelming the user with minor style trivia unless they requested a full line-by-line audit.

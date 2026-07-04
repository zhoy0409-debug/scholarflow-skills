# Intake and Routing

Use this reference to choose how much guidance the user needs.

## User Modes

| Mode | Signs | Approach |
|---|---|---|
| guided | "帮我选刊", no abstract, unclear discipline, does not know JCR/CAS/论著 | Ask 5-7 essential questions, explain terms only when needed. |
| standard | Has title/abstract, knows field, has rough target tier or deadline | Build manuscript positioning and candidate matrix. |
| advanced | Provides target tier, article type, metrics, institutional constraints, known candidates | Skip basic explanations; verify data and compare candidates. |

## Minimum Questions for Guided Users

Ask in a friendly, non-judgmental tone:

1. 你的文章属于什么专业或研究方向？如果不确定，可以发题目/摘要/关键词。
2. 这篇文章是什么类型：论著/原创研究、综述、Meta 分析、病例报告、方法学、短文、Letter，还是其他？
3. 你的主要目标是什么：毕业、职称、基金结题、单位考核、尽快见刊、高影响力、低版面费，还是特定分区？
4. 学校或单位有没有硬性要求：SCI/SSCI/EI/CSSCI/北大核心/CSCD、中科院几区、JCR 几区、必须论著、预警期刊限制、通讯/第一作者要求？
5. 是否有时间限制和版面费/APC 预算？
6. 文章目前有什么材料：题目、摘要、全文、图表、数据、投稿信、已有目标期刊？
7. 你愿意走更稳妥路线，还是可以接受更高拒稿风险去冲更高档次？

## Fast Intake for Advanced Users

Use this compact prompt:

```text
请给我：题目/摘要/关键词、文章类型、目标领域、希望的 JCR/CAS/IF/索引要求、单位硬性要求、时间/APC限制、已有候选期刊。我会直接做候选期刊矩阵和投稿顺序建议。
```

## User Goal Labels

- `graduation`: prioritize rule compliance, acceptable indexing, realistic timeline.
- `promotion`: prioritize institutional recognition, quartile/indexing, author-position rules.
- `high-impact`: prioritize scope/novelty fit and evidence strength; warn about rejection risk.
- `fast-publication`: prioritize speed only after excluding questionable journals.
- `low-cost`: prioritize non-OA/hybrid no-fee routes or APC waivers.
- `Chinese-core`: prioritize CSSCI/CSCD/北大核心/科技核心 and unit rules.
- `international-visibility`: prioritize WoS/Scopus/PubMed/field audience and journal reputation.

## Tone

Assume the user may not know journal publishing terminology. Explain without condescension. If the user overestimates or underestimates the paper, calibrate with evidence: methods, dataset, novelty, validation, and match to recent articles.

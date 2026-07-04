# JL Skill Collection

把科研、写作、文献、图表、生信分析和交付流程，变成 Agent 可以稳定复用的实用工具。

## 别再从零教 AI 做科研

真正消耗时间的，往往不是某一个问题，而是每次都要重新解释流程：

- 查文献时，要说明检索源、筛选标准、引用格式和 Zotero 入库方式。
- 写论文时，要反复强调不能编引用、不能过度声称、结果要和证据对齐。
- 做图时，要先确认结论、panel 逻辑、统计标注和投稿导出格式。
- 做生信时，要在工具、参数、输入输出、QC 和报告解释之间来回切换。
- 做 PPT / Word / PDF 时，要检查格式、溢出、渲染、路径和可编辑性。

JL Skill Collection 把这些重复流程封装成可安装的 Agent Skills。每个 skill 都是一套明确的工作方法：什么时候用、怎么做、读哪些参考、调用哪些脚本、输出什么、如何检查质量。

本发布包只收录 JL Skill Collection 的自有工作流和自研封装。底层公开软件、数据库、期刊平台和外部服务只作为用户环境中的可调用工具，不随本包分发，也不归属本产品。

## 它适合谁

- 研究生：快速完成文献精读、论文初稿、图表、引用核查和组会汇报。
- PI / 课题负责人：审稿、看稿、拆解审稿意见、判断文献价值、准备基金/专利/PPT。
- 生信和组学分析者：把 FASTQ、BAM、VCF、宏基因组、系统发育和论文报告串起来。
- 科研助理：管理 Zotero、PDF、PPT、Word、Excel、图表和交付检查。
- 内容创作者和创业者：把模糊问题变成清晰诊断、内容策略和可复盘决策。
- Agent 重度用户：把长期形成的方法论沉淀为稳定工具，而不是每次重新提示。

## 八条产品线

| 产品线 | 解决什么 |
|---|---|
| Nature Research Suite | 文献检索、论文精读、Nature 风格写作、图表、审稿回复 |
| PaperSpine & Literature Ops | 论文脊柱、证据链、文献入库、稿件重建 |
| Academic Writing & Integrity | 引用核查、论文自审、AI 痕迹、研究诚信质量门 |
| Bio & Omics Toolkit | 生信/组学分析全链条，从数据处理到论文解释 |
| Delivery Stack | PPT、PDF、DOCX、XLSX、截图和可交付文件 |
| DBS Business Toolkit | 商业诊断、内容策略、目标澄清、决策沉淀 |
| Agent Ops & Governance | skill 写作、安全审计、任务计划、会话交接 |
| Content & Knowledge Work | AI 资讯、知识库问答、内容研究和长文写作 |

## 典型使用场景

### 文献太多，真正值得读的太少

使用：

- `nature-academic-search`
- `nature-literature-pipeline`
- `nature-reader`
- `zotero-lit-fetch`
- `reference-checker`

得到：检索策略、候选文献、精读稿、引用文件、Zotero 入库和投稿前引用核查。

### 论文不是不会写，是缺少清晰脊柱

使用：

- `paper-spine`
- `nature-writing`
- `nature-polishing`
- `research-integrity-guardrail`
- `paper-self-review`
- `nature-response`

得到：研究动机、证据链、段落功能、Nature 风格表达、自审报告和审稿回复。

### 图表不像投稿图

使用：

- `nature-figure`
- `sci-figure-composer`
- `bio-data-visualization-*`

得到：先定义结论，再构建 panel、统计标注、颜色、导出格式和视觉 QA。

### 生信流程到处断点

使用：

- `samtools-bam-processing`
- `bcftools-variant-manipulation`
- `snpeff-variant-annotation`
- `bakta-genome-annotation`
- `bio-metagenomics-*`
- `bio-phylo-*`
- `omics-analysis`

得到：工具选择、参数解释、QC 逻辑、结果解读和论文级报告路径。

### 交付物总在最后拖慢进度

使用：

- `ppt`
- `ppt-html-authoring`
- `nature-paper2ppt`
- `pdf-guide`
- `local-md-mermaid-pdf`
- `chinese-docx-reference-unifier`
- `screenshot-docs`

得到：可编辑 PPT、可渲染 PDF、规范 Word 引用、Markdown 图表导出和 README 截图。

### Agent 很强，但需要工作纪律

使用：

- `skill-writing-guide`
- `securityauditor`
- `planning-with-files`
- `session-handoff`
- `artifact-staging-and-render-qa`

得到：可维护 skill、安全审计、长任务落盘、会话交接和交付前检查。

## 三分钟上手

把需要的 skill 文件夹复制到你的 Agent skills 目录，然后直接用自然语言开始：

```text
帮我读这篇论文，做中英文对照精读，保留图表逻辑。
```

```text
这篇稿子投稿前帮我检查引用、过度声称、AI 味和逻辑漏洞。
```

```text
我有一批 FASTQ，想做变异分析，并把结果写进论文。
```

```text
把这个 Markdown 里的 Mermaid 图导出成 PDF。
```

Agent 会根据 `name`、`description` 和 `agents/openai.yaml` 选择合适的 skill，并按该 skill 的工作流执行。

## 为什么它好用

- 场景清楚：每个 skill 只解决一类具体问题。
- 流程稳定：步骤、参考文件、脚本和质量门写在 skill 里。
- 输出明确：从精读稿、引用核查、PPT、PDF 到生信报告，都有交付形态。
- 边界清晰：授权文献访问、引用真实性、文件写入和安全审计都有明确规则。
- 易于扩展：复杂知识放在 `references/`，确定性操作放在 `scripts/`。

## 安装结构

```text
jl-skill-collection-release-20260704/
  skills/
    nature-reader/
      SKILL.md
      agents/openai.yaml
      references/
      scripts/
    ...
  README.md
  GETTING_STARTED.md
  SKILL_INDEX.md
```

## 一句话

**JL Skill Collection 把科研里最耗时间、最容易返工、最需要经验的步骤，变成 Agent 可以稳定复用的工作流工具。**

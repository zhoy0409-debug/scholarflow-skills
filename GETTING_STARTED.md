# Getting Started with ScholarFlow Skills

## 安装

选择需要的 skill 文件夹，复制到你的 Agent skills 目录。

常见目录：

```text
~/.codex/skills/
~/.claude/skills/
```

每个 skill 是一个独立文件夹，最少包含：

```text
skill-name/
  SKILL.md
  agents/openai.yaml
```

复杂 skill 还会包含：

```text
references/
scripts/
assets/
```

## 选择工具

按任务选择，不需要记完整列表。

| 你想做什么 | 优先使用 |
|---|---|
| 查文献、做综述、核引用 | `nature-academic-search`, `reference-checker` |
| 精读论文、中英文对照 | `nature-reader` |
| 写论文、改论文、润色英文 | `nature-writing`, `nature-polishing`, `paper-spine` |
| 投稿前质量检查 | `journal-submission-normalizer`, `research-integrity-guardrail`, `paper-self-review` |
| 做论文图表 | `nature-figure`, `sci-figure-composer` |
| 做组会/汇报 PPT | `nature-paper2ppt`, `ppt` |
| 做生信/组学分析 | `omics-analysis`, `bio-*`, `samtools-bam-processing`, `bcftools-variant-manipulation` |
| 转 PDF / DOCX / PPTX / XLSX | `pdf-guide`, `local-md-mermaid-pdf`, `ppt`, `chinese-docx-reference-unifier` |
| 写或审计自己的 skill | `skill-writing-guide`, `securityauditor` |
| 长任务防止上下文丢失 | `planning-with-files`, `session-handoff` |

## 推荐开场白

### 论文精读

```text
请用 nature-reader 的方式读这篇论文，输出中英文对照精读，保留图表逻辑、核心贡献、方法路线和可引用要点。
```

### 论文写作

```text
请把这些结果和图表整理成论文 Results 和 Discussion，先搭建论证结构，再写正文。
```

### 投稿前检查

```text
请对这篇稿子做投稿前质量检查，重点看引用真实性、过度声称、结果一致性、AI 写作痕迹和审稿风险。
```

### 期刊格式规范化

```text
请用 journal-submission-normalizer 先联网检索目标期刊的官方投稿要求，再把这篇稿件按字体、字号、行距、标题层级、图表、上下标、参考文献和声明部分逐项规范化，并输出投稿合规报告。
```

### 科研作图

```text
请用 nature-figure 工作流帮我做这张图。先确认图的核心结论、证据链、panel 结构和导出格式，再开始写代码。
```

### 生信分析

```text
我有一批测序数据，目标是完成变异分析并写进论文。请先给出完整工作流、质控节点、关键参数和结果解释框架。
```

### PPT 交付

```text
请把这篇论文做成组会汇报 PPT，保留研究问题、方法、关键图表、主要结论和讨论问题。
```

## 好结果长什么样

一个成熟 skill 不只给答案，还会给：

- 当前阶段判断
- 输入要求
- 操作步骤
- 输出文件或报告
- 质量检查
- 风险边界
- 下一步建议

例如，`reference-checker` 不只是“看起来引用没问题”，而是逐条核对标题、作者、期刊、年份、DOI、PubMed/Crossref/出版社来源和格式一致性。

`nature-figure` 不只是“画图”，而是先确认核心结论、证据逻辑、统计标注、panel 结构和导出格式。

`paper-spine` 不只是“润色论文”，而是先建立动机、证据、SOTA、段落功能和引用支撑。

## 使用习惯

最好的提问方式是给目标、材料和交付形式：

```text
目标：投稿前检查
材料：main.docx 和 references.docx
交付：问题清单 + 修改优先级 + 可直接改的建议
```

或者：

```text
目标：把论文做成 15 页组会 PPT
材料：paper.pdf
交付：可编辑 PPTX，中文讲述逻辑，保留关键图表
```

## 安全边界

- 文献下载只处理用户已授权访问的内容。
- 引用和事实不确定时必须标注，不编造。
- 文件删除、覆盖和外部写入必须由用户确认。
- 外部软件、联网脚本和高权限操作应先用 `securityauditor` 审计。
- 研究结果、统计结论和实验数据以用户材料为准。

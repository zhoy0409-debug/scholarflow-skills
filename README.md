# ScholarFlow Skills

ScholarFlow Skills 是一套面向科研场景的 Agent Skills。

我做这套 skills，是因为在真实科研工作中反复遇到同一类问题：很多任务并不是完全不会做，而是每次都要重新告诉 AI 背景、流程、标准和边界。查文献时，要说明检索源、筛选标准和引用格式；读论文时，要提醒它不要只总结摘要，而要保留图表逻辑和证据链；写论文时，又要反复约束引用真实性、论证边界、段落功能和语气强度。到了科研作图、生信分析、PPT、PDF、Word 排版和投稿前检查，真正消耗时间的往往不是某一个单点任务，而是这些流程总要从头解释。

ScholarFlow Skills 的目标，就是把这些已经在科研工作中反复使用、反复修正过的流程，沉淀成可以复用的 Agent Skills。

它不是一组零散提示词，而是一套可安装、可调用、可扩展的科研工作流组件。每个 skill 都尽量说明：适合什么场景、需要什么输入、如何执行、交付什么结果，以及哪些边界不能越过。

本仓库由 Zhoy 发布和维护，只发布 ScholarFlow Skills 的自有工作流和自研封装。底层公开软件、数据库、期刊平台和外部服务只作为用户环境中的可调用工具，不随本包分发，也不归属本产品。

## 为什么不是又一个 skill 列表

现在已经有很多通用 skill 仓库、跨平台 skill 格式、自动生成器和配置校验器。它们很有价值，可以让 skill 更容易创建、安装、迁移和检查。

ScholarFlow Skills 不重复这类基础设施，而是专注于一个更具体、也更容易出问题的场景：科研用户如何把 AI 稳定地带进文献检索、论文精读、学术写作、科研作图、生信分析和交付物整理。

它的重点不在于“有多少个条目”，而在于每个主推 skill 都尽量回答四个问题：

- 这个任务在真实科研流程中到底卡在哪里？
- 用户需要准备哪些材料，AI 才不会凭空发挥？
- 结果应该交付成什么形态，才真的能继续用于写论文、做汇报或投稿？
- 哪些地方必须保守处理，例如引用真实性、统计结论、版权边界、文件覆盖和外部工具调用？

因此，这里的 skills 不会把成熟软件、数据库或期刊平台说成自己的能力。例如，生信方向可能会调用用户环境中的 `fastp`、`samtools`、`bcftools`、`BLAST`、`KEGG`、`NCBI` 等工具或资源，但 ScholarFlow Skills 的价值在于把这些工具放进可复用的科研流程中：什么时候使用、输入输出如何组织、质控节点怎么看、结果如何解释，以及如何写进论文。

## 适合谁使用

如果你也经常遇到下面这些情况，ScholarFlow Skills 可能会有用：

- 读了很多论文，但真正能写进综述、Introduction 或 Discussion 的信息没有系统沉淀。
- 想让 AI 辅助论文写作，但担心它语气过满、引用不准、逻辑松散或段落功能不清。
- 每次科研作图都要重新强调 panel 结构、统计标注、颜色风格、导出格式和投稿审美。
- 生信分析跑完了，但不知道如何把 QC、参数、结果解释和论文叙述连起来。
- 组会 PPT、PDF、Word、Markdown、引用格式和图表整理总是在最后阶段消耗大量时间。
- 长任务一跨会话就丢上下文，前面已经想清楚的流程，下一轮又要重新铺垫。

我希望这些 skills 能把“重复解释”变成“稳定调用”，让科研工作少一点从头再来，多一点可复用的流程积累。

## 核心工作流

| 工作流 | 解决的真实问题 | 代表 skills |
|---|---|---|
| 文献检索与精读 | 从关键词、PDF 和数据库结果中整理出真正可用的证据 | `nature-academic-search`, `nature-literature-pipeline`, `nature-reader`, `zotero-lit-fetch` |
| 论文脊柱与写作 | 先搭建研究动机、证据链和段落功能，再进入写作和改写 | `paper-spine`, `nature-writing`, `nature-polishing`, `manuscript-writing` |
| 引用与研究诚信 | 投稿前检查引用真实性、过度声称、结果一致性和审稿风险 | `reference-checker`, `nature-citation`, `research-integrity-guardrail`, `paper-self-review` |
| 科研图表与展示 | 让图先服务结论，再处理 panel、统计标注、视觉一致性和导出格式 | `nature-figure`, `sci-figure-composer`, `nature-paper2ppt`, `ppt` |
| 生信与组学分析 | 把 FASTQ、BAM、VCF、宏基因组、系统发育和论文解释串起来 | `bio-*`, `omics-analysis`, `samtools-bam-processing`, `bcftools-variant-manipulation` |
| 交付物整理 | 把 Markdown、PDF、PPT、DOCX、截图和引用格式整理成可交付结果 | `pdf-guide`, `local-md-mermaid-pdf`, `chinese-docx-reference-unifier`, `screenshot-docs` |
| Agent 工作流治理 | 为长任务、文件交接、安全审计和 skill 写作建立可复用纪律 | `planning-with-files`, `session-handoff`, `securityauditor`, `skill-writing-guide` |

完整 skill 列表见 [SKILL_INDEX.md](SKILL_INDEX.md)。第一次使用可以先看 [GETTING_STARTED.md](GETTING_STARTED.md)。发布标准见 [QUALITY_STANDARD.md](QUALITY_STANDARD.md)。

## 使用示例

### 读一篇论文

```text
请用 nature-reader 的方式读这篇论文，输出中英文对照精读，保留图表逻辑、核心贡献、方法路线和可引用要点。
```

### 投稿前检查

```text
请对这篇稿子做投稿前质量检查，重点看引用真实性、过度声称、结果一致性、AI 写作痕迹和审稿风险。
```

### 从结果写论文

```text
请把这些结果和图表整理成论文 Results 和 Discussion。先搭建论证结构，再写正文，不要编造引用或夸大结论。
```

### 做生信分析并写进论文

```text
我有一批测序数据，目标是完成变异分析并写进论文。请先给出完整工作流、质控节点、关键参数和结果解释框架。
```

### 做组会汇报

```text
请把这篇论文做成组会汇报 PPT，保留研究问题、方法、关键图表、主要结论和讨论问题。
```

## 安装方式

选择需要的 skill 文件夹，复制到你的 Agent skills 目录即可。

常见目录：

```text
~/.codex/skills/
~/.claude/skills/
```

每个 skill 至少包含：

```text
skill-name/
├── SKILL.md
└── agents/
    └── openai.yaml
```

复杂 skill 还可能包含：

```text
references/   深度规则、模板、检查清单
scripts/      可复用脚本
assets/       图像、模板或静态资源
```

## 仓库结构

```text
scholarflow-skills/
├── README.md             项目介绍
├── GETTING_STARTED.md    上手指南
├── QUALITY_STANDARD.md   发布标准
├── SKILL_INDEX.md        skill 索引
├── LICENSE               开源许可
└── skills/               可安装 skill
```

## 边界与原则

ScholarFlow Skills 的目标是提高科研效率，而不是替代研究判断本身。

- 文献下载只处理用户已授权访问的内容。
- 引用和事实不确定时必须标注，不编造。
- 研究结果、统计结论和实验数据以用户提供的材料为准。
- 文件删除、覆盖和外部写入必须由用户确认。
- 外部软件、联网脚本和高权限操作应先经过 `securityauditor` 审计。
- 对统计结论、机制推断、临床意义和投稿前判断，应保持保守表达，避免过度声称。

## 许可

ScholarFlow Skills 的原创说明、工作流编排和文档以 [MIT License](LICENSE) 发布。底层公开软件、数据库、期刊平台和外部服务按各自许可、服务条款和访问权限使用。


## 一句话

ScholarFlow Skills 是一套从真实科研使用场景中长出来的 Agent Skills：少一点重复铺垫，多一点稳定复用。

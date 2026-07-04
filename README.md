# ScholarFlow Skills

我做这套 skills，是因为自己在科研工作里反复遇到同一类卡点：不是完全不会做，而是每次都要重新告诉 AI 背景、流程、标准和边界。

查文献时，要重新说检索源、筛选标准和引用格式。读论文时，要反复提醒它别只总结摘要，要保留图表逻辑和证据链。写论文时，又要一遍遍防止编引用、过度声称、段落散掉。到了作图、生信、PPT、PDF 和投稿前检查，真正拖慢人的往往不是某个单点任务，而是这些细碎流程总要从头解释。

ScholarFlow Skills 就是把这些反复解释过很多次的科研工作流，沉淀成可以复用的 Agent Skills。它不是一堆提示词，而是一组可安装的小工具：每个 skill 都说明它适合什么场景、需要什么输入、怎么执行、交付什么结果，以及哪些边界不能越过。

本仓库由 Zhoy 发布和维护，只发布 ScholarFlow Skills 的自有工作流和自研封装。底层公开软件、数据库、期刊平台和外部服务只作为用户环境中的可调用工具，不随本包分发，也不归属本产品。

## 为什么不是又一个 skill 列表

现在已经有很多通用 skill 仓库、跨平台 skill 格式、自动生成器和配置校验器。它们很有价值：让 skill 更容易创建、安装、迁移和检查。ScholarFlow Skills 不重复这类基础设施，而是专注在一个更具体、更容易痛的场景：科研用户怎样把 AI 稳定地带进文献、写作、作图、生信分析和交付物生产。

它的区别不在于“有更多条目”，而在于每个主推 skill 都要尽量回答四个问题：

- 这个任务在真实科研流程里卡在哪里？
- 用户需要准备什么材料，AI 才不会凭空发挥？
- 结果应该交付成什么形态，才真的能继续写论文、做汇报或投稿？
- 哪些地方必须保守处理，比如引用、统计结论、版权、文件覆盖和外部工具调用？

所以这里的 skill 不把成熟软件、数据库或期刊平台说成自己的能力。比如生信方向会调用 `fastp`、`samtools`、`bcftools`、`BLAST`、`KEGG`、`NCBI` 等用户环境里的工具，但 ScholarFlow Skills 的价值在于把这些工具放进可复用的科研工作流：什么时候用、输入输出怎么组织、质量节点怎么看、结果如何写进论文。

## 适合谁

如果你也经常遇到下面这些情况，这套工具会比较有用：

- 读了很多论文，但真正能写进综述、Introduction 或 Discussion 的信息没有沉淀下来。
- 想让 AI 帮忙写论文，却总担心它把语气写得很满、引用写得不准、逻辑写得松。
- 每次做图都要重新强调 panel 结构、统计标注、颜色、导出格式和投稿审美。
- 生信分析跑完了，但不知道怎么把 QC、参数、结果解释和论文叙述连起来。
- 组会 PPT、PDF、Word 引用、Markdown 图表这些交付物，总在最后阶段消耗大量时间。
- 长任务一跨会话就丢上下文，明明前面已经想清楚了，下一轮又要重新铺垫。

我希望这些 skill 能把“重复解释”变成“稳定调用”，让科研工作少一点从头再来。

## 核心工作流

| 工作流 | 解决的真实问题 | 代表 skills |
|---|---|---|
| 文献检索与精读 | 从一堆关键词、PDF 和数据库结果里，整理出真正能用的证据 | `nature-academic-search`, `nature-literature-pipeline`, `nature-reader`, `zotero-lit-fetch` |
| 论文脊柱与写作 | 先把研究动机、证据链和段落功能搭起来，再进入写作和改写 | `paper-spine`, `nature-writing`, `nature-polishing`, `manuscript-writing` |
| 引用与研究诚信 | 投稿前检查引用真实性、过度声称、AI 痕迹和结果一致性 | `reference-checker`, `nature-citation`, `research-integrity-guardrail`, `paper-self-review` |
| 科研图表与展示 | 让图先服务结论，再处理 panel、统计标注、视觉一致性和导出格式 | `nature-figure`, `sci-figure-composer`, `nature-paper2ppt`, `ppt` |
| 生信与组学分析 | 把 FASTQ、BAM、VCF、宏基因组、系统发育和论文解释串起来 | `bio-*`, `omics-analysis`, `samtools-bam-processing`, `bcftools-variant-manipulation` |
| 交付物整理 | 把 Markdown、PDF、PPT、DOCX、截图和引用格式做成可交付结果 | `pdf-guide`, `local-md-mermaid-pdf`, `chinese-docx-reference-unifier`, `screenshot-docs` |
| Agent 工作流治理 | 让长任务、文件交接、安全审计和 skill 写作有一套可复用纪律 | `planning-with-files`, `session-handoff`, `securityauditor`, `skill-writing-guide` |

完整 skill 列表见 [SKILL_INDEX.md](SKILL_INDEX.md)。第一次使用可以先看 [GETTING_STARTED.md](GETTING_STARTED.md)。发布标准见 [QUALITY_STANDARD.md](QUALITY_STANDARD.md)。

## 我通常会这样用

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

复杂 skill 还会包含：

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

## 边界

这套工具的目标是提高科研效率，不替代研究判断本身。

- 文献下载只处理用户已授权访问的内容。
- 引用和事实不确定时必须标注，不编造。
- 研究结果、统计结论和实验数据以用户材料为准。
- 文件删除、覆盖和外部写入必须由用户确认。
- 外部软件、联网脚本和高权限操作应先用 `securityauditor` 审计。

## 许可

ScholarFlow Skills 的原创说明、工作流编排和文档以 [MIT License](LICENSE) 发布。底层公开软件、数据库、期刊平台和外部服务按各自许可、服务条款和访问权限使用。

## 关于非科研工具

Zhoy 的工作流里也有一些内容、商业判断和个人决策类 skill。它们可以有用，但不属于这个仓库的科研核心叙事。这个 GitHub 仓库会优先围绕科研、学术写作、文献、图表、生信分析和交付物来组织；其他方向更适合以后单独发布。

## 一句话

ScholarFlow Skills 是一套由 Zhoy 从真实科研使用场景里长出来的 Agent Skills：少一点重复铺垫，多一点稳定复用。

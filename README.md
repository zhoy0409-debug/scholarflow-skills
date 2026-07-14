# ScholarFlow Skills

科研工作流的 Agent Skills 集合 —— 文献、写作、配图、审稿、投稿、生信。中英双语。

**和大多数 skill 集不一样的地方：它带门禁。**
不是「建议你检查一下对齐」，是「panel 标号偏离网格 → BLOCK，不许出稿」。

```
/plugin marketplace add zhoy0409-debug/scholarflow-skills
/plugin install scholarflow
```

或手动：把 `skills/` 下需要的目录拷到 `~/.claude/skills/` 或 `~/.codex/skills/`。

---

## 按你的条件选

每个人的条件和能力不一样。这套 skill 分三层，**不必全装**：

| 你是 | 用什么 | 前提 |
|---|---|---|
| **想随手让 AI 帮个忙** —— 改段话、画张图、查个文献、看看这稿子有没有问题 | `nature-*`（15 个，各自可直接触发） | 无。纯 markdown，哪儿都能跑 |
| **要认真投一篇稿** —— 愿意花十分钟配置，换一条从材料到成稿的完整链路 | `paper-spine`（1 个入口） | 终端向导 + 配置文件 |
| **跑生信** | `bio-*`（130 个参考库） | 各工具自己的环境 |

> **`paper-spine-*` 的 10 个子技能不要直接调用。** 它们是被 `paper-spine` 编排的内部模块，
> 假定配置文件和 `source_map.md` 已存在 —— 脱离那套上下文跑，结果是错的。

---

## 我该用哪个（轻量层路由表）

按**你手上有什么、想要什么**找，而不是按技能名字猜：

| 你手上有 | 你想要 | 用 |
|---|---|---|
| 笔记 / 结果 / 中文草稿 | 一段还不存在的正文 | `nature-writing` |
| 写完的英文段落 | 更地道的英文（不动结构） | `nature-polishing` |
| 一段文字 | 判断它像不像 AI 写的 / 降 AI 率 | `humanize` |
| 一个问题 | 一批论文 | `nature-academic-search` |
| 一段没引用的文字 | 同一段文字 + 引用 | `nature-citation` |
| 已找到的检索结果 | 连 PDF 进文献库 | `zotero-lit-fetch` |
| 一条引用 | 它是真的吗 / 真支持这句话吗 | `reference-checker` |
| 一份草稿 | **科学判断**：创新性够吗、证据链站得住吗 | `nature-reviewer` |
| 终稿 + 原始数据 | **机械核查**：数字对得上吗、引了没列吗 | `research-integrity-guardrail` |
| 审稿意见 | 逐条回复信 | `nature-response` |
| 数据 | 投稿级的图 | `nature-figure` |
| 一篇论文 / 一份已有的 PPT | 幻灯片，或幻灯片的叙事审计 | `nature-paper2ppt` |
| 别人的论文 PDF | 深读笔记 | `nature-reader` |
| 一篇稿子 | 数据可用性声明 | `nature-data` |
| 一篇稿子 | 该投哪个期刊 / 按期刊要求规范格式 | `journal-selection-advisor` / `journal-submission-normalizer` |

**「科学判断」和「机械核查」是两件事。**
「这篇创新性够发子刊吗」和「摘要里的数字和表 2 对得上吗」需要完全不同的能力 —— 别混用。

裸 prompt（「帮我写论文」「画个图」）信息量为零，skill 会**反问一句**。这是设计，不是 bug。

---

## 门禁

`gates/` 是可执行的，会 `exit 2`：

```bash
python3 gates/gate_checks.py claims    --claims claims.csv --evidence evidence.csv --manuscript draft.md
python3 gates/gate_checks.py data      --file raw.xlsx
python3 gates/gate_checks.py narrative --matrix slides.csv
```

| 门禁 | 拦什么 | 来自哪次真实翻车 |
|---|---|---|
| `claims_have_sources` | 无出处的断言进正文 | — |
| `certainty_in_enum` | `candidate_supported_moderate_to_strong` 这种自由文本值让所有自动检查失效 | 综述引擎 |
| `no_orphan_citation` / `no_unused_claim` | 引了没列 / 列了没引 | 投稿前核查 |
| `filename_not_mock` | 文件名带 `Mock` 的数据被当真实数据分析 | 一次差点酿成学术不端 |
| `missingness_plausible` | 320×191 **零缺失** —— 生成数据的指纹 | 同上 |
| `no_duplicate_advance` | 两页幻灯抢同一个断言 | 四次汇报翻车 |

每条门禁来自哪次事故，写在 [docs/INSIGHTS.md](docs/INSIGHTS.md)。

---

## 为什么要有门禁

skill 的正文是「一段很长的 prompt」：它告诉模型该怎么做，
**但没有任何东西检查模型到底做没做**。

```
指导：「出图后请检查对齐」          → 模型会说「已检查」然后交一张歪的
门禁：「BLOCK: panel 标号偏离网格」  → 不过就是不过
```

同一条原则也用在这个仓库自己身上。CI 会 fail，如果：

- 有 SKILL.md 变成了不加载任何资产的**空壳**（`tools/check_health.py`）
- manifest 指向**不存在的文件**（同上）
- `shared/` 和 `skills/_shared/` **漂移**（`tools/sync_shared.py check`）
- 有文档在推荐**不存在的 skill**（`tools/check_docs.py`）
- 门禁测试挂了（`pytest gates/tests`）

这四条**全是静态可查的**。它们本该被拦住，而不是发布之后才发现。

---

## 边界

- 文献下载只用你有权访问的内容。
- 无法核实的引用和事实，**标注不确定**，不假装确定。
- 结果、统计结论、实验数据以**你提供的材料**为准，不编造。
- 删除、覆盖、对外发布文件，**需要你确认**。
- 统计结论、机制推断、临床意义、期刊匹配 —— **保守表述**。

## 文档

- [SKILL_INDEX.md](SKILL_INDEX.md) —— 全部 skill（自动生成，不会过期）
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) —— 三层分流的设计
- [docs/INSIGHTS.md](docs/INSIGHTS.md) —— 每条门禁来自哪次翻车
- [docs/EVAL.md](docs/EVAL.md) —— 路由 eval，以及为什么设计集上的 100% 什么都不说明

## 开发

```bash
python3 tools/check_health.py --root .       # skill 不是空壳、manifest 无断链
python3 tools/check_docs.py   --root .       # 文档没有悬空引用
python3 tools/sync_shared.py  check --root . # shared/ 与 skills/_shared/ 一致
python3 tools/gen_index.py    --root .       # 重新生成 SKILL_INDEX.md
python3 -m pytest gates/tests -q             # 门禁测试
```

`shared/` 是共享内容的**唯一真源**。`skills/_shared/` 由 sync 生成，不要手改。

## License

MIT。外部软件、数据库、期刊平台和服务各自遵循它们自己的许可与访问条款。

<div align="right"><a href="README.md">English</a></div>

# ScholarFlow

**别的 skill 集给模型一段 prompt。ScholarFlow 给它一道门禁。**

prompt 说：*「出图后请检查对齐。」*
模型说「已检查」，然后交给你一张歪的。

门禁说：`BLOCK: panel 标号偏离共享网格` —— 然后 `exit 2`。

这个仓库里的每一条门禁，都来自一次**真实发生过**的翻车。没有一条是假想的。

```bash
/plugin marketplace add zhoy0409-debug/scholarflow-skills
/plugin install scholarflow
```

---

## 门禁

```bash
python3 gates/gate_checks.py data      --file raw.xlsx
python3 gates/gate_checks.py claims    --claims c.csv --evidence e.csv --manuscript draft.md
python3 gates/gate_checks.py narrative --matrix slides.csv
```

退出码 2 = 有门禁被触发。14 个测试，每个都钉在它来自的那次事故上。

### `data` —— 最要命的那一个

```
BLOCK filename_not_mock       PCa_Mock_Data_320_Final.csv
BLOCK missingness_plausible   320 × 191，零缺失
```

一份数据差一点就被当作**真实的 320 例患者队列**分析、写稿、投出去 —— 还挂着伦理批件号和基金号。
文件名里写着 `Mock`。矩阵是 **320×191 零缺失** —— 真实的问卷研究不可能全满。

这两点是靠**有人碰巧读得仔细**才发现的。那不是控制，那是运气。

现在它是一道门禁。

### `claims` —— 无台账，不出句

```
BLOCK claims_have_sources   C002 没有 source
BLOCK certainty_in_enum     'candidate_supported_moderate_to_strong' 不在受控词表里
BLOCK no_orphan_citation    正文引用了 [C777]，台账里没有 C777
BLOCK no_unused_claim       C005 在台账里，正文里一次都没出现
```

**先立台账，再由台账生成句子。** 不是反过来。

先写句子、再回头找引用，**天然产生无源之句** —— 而且会不动声色地把你推向「那条同意你已经写下的话的文献」。
这是选择性引用，是学术不端的温和版本。

`certainty_in_enum` 之所以存在，是因为一个自由文本值（`candidate_supported_moderate_to_strong`）
曾经**悄无声息地让下游所有自动检查失效**。受控枚举 **加上** 一个自由文本备注列。
永远不要让一个字段干两件事。

### `narrative` —— 一页只准推进一步

```
BLOCK no_duplicate_advance   「CRAB 定义」在 P5 和 P6 都被第一次引入
```

四次组会汇报栽在同一个地方：**每一页都把整个故事从头讲一遍。**

修法很反直觉。那页*看起来*冗余的，通常不是错的那一页 ——
**一个断言归属于第一次能把它讲透的那一页，前面所有页都必须让出来。**

---

## 附带的

**`shared/core/`** —— 同样那些翻车，写成可加载的规范：

| | |
|---|---|
| `figure-qa.md` | *代码跑通 ≠ 图做好了。* matplotlib 不会因为标签被裁掉而报错。**打开 PNG，用眼睛看。** 按最终插入尺寸看。然后把它嵌进真实文档，再看一遍。 |
| `integrity-gates.md` | 一份 qPCR 报告声称「上调 2 倍」。原始 Ct 根本没动，而 GAPDH 内参在过表达组整体晚了 1.5 个 Ct。**那 2 倍是内参漂移校正出来的。** |
| `visual-honesty.md` | 一张 AI 生成的幻灯配图把 *A. baumannii* 画成土壤里的「natural decomposer」—— 学界有争议，答辩现场会被问死。**如果你答不上「有文献支持吗」，这张图就不该在。** |
| `claim-ledger.md` · `narrative-advance.md` · `preflight.md` | |

**`skills/nature-*`** —— 起草、润色、配图、汇报、模拟审稿、回复审稿。
声明式 manifest：每个 skill **只加载这次请求需要的片段**，不是整个库。

**`skills/bio-*`**（130 个）和工具参考手册（samtools、bcftools、Prokka、Bakta…）—— 附赠的生信参考库。
有用。但**不是这个仓库的差异所在**。

---

## 仓库会自己防守

六道 CI。**每一道都对应一个真的发布出去过的 bug。**

| 检查 | 它为哪个 bug 而存在 |
|---|---|
| `check_health` | 15 个 skill 的 SKILL.md 被模板重生成。manifest 还在，400KB 的 references 还在，**但没有一行指令让模型去读它们。** skill 变成了空壳，而**没有任何东西发现**。后来第二轮又扫出 14 个 —— 因为这个检查的第一版**只查了我记得去看的地方**。<br>**一个只检查你想到要看的地方的 CI，比没有 CI 更危险：它给你假的安全感。** |
| `check_xrefs` | skill 的正文里也在互相点名。删一个 skill，那些点名就悬空 —— **而模型会照着它去调一个不存在的 skill。** 这个检查一上来就抓到 `journal-selection-advisor` 在点名一个前一个 commit 刚删掉的 skill。 |
| `check_docs` | 删掉 11 个 skill 之后，README 仍然在让人用它们。 |
| `sync_shared` | `shared/` 和 `skills/_shared/` 曾经是 9 份逐字节相同的复制品。改一次要改九处。 |
| `gen_index` | 手写的索引必然过期。生成的不会。 |
| `pytest gates/tests` | 门禁本身也会坏。 |

这六条**全是静态可查的**。它们本该被机器拦住，而不是几个月后被人翻出来。

---

## 边界

只下载你有权访问的内容。无法核实的引用**标注为无法核实**，不藏着。
结果、统计结论、实验数据以**你提供的材料**为准，绝不编造。
删除、覆盖、对外发布文件，需要你确认。
统计结论、机制推断、临床意义、期刊匹配 —— 保守表述。

## 文档

[SKILL_INDEX](SKILL_INDEX.md)（自动生成）· [架构](docs/ARCHITECTURE.md) ·
[每条门禁来自哪次翻车](docs/INSIGHTS.md) · [路由 eval](docs/EVAL.md)

MIT。

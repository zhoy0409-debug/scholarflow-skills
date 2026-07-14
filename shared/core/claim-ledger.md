# Claim Ledger —— 任何进入正文的句子都必须有一行台账

> 来源：你在「Literature review synthesis workflow」线程里搭的 evidence-gate 引擎。
> 那套东西比现在 ScholarFlow 里任何一个 skill 都严格，但它只活在那一个线程里。
> 这里把它提炼成所有写作类 skill 共用的最小内核。

## 为什么

现在的 nature-writing / nature-citation 是**先写句子，再找引用**。
这个顺序天然会产生「无源之句」——写得很顺、但没人能说清它凭什么。
审稿人和查重系统盯的正是这些句子。

反过来：**先立台账，再由台账生成句子**。没有台账行的断言，写不出来。

## 台账格式

每条断言一行，落到 `claims.csv`：

| 字段 | 说明 |
|---|---|
| `claim_id` | C001, C002 … 正文里用 `[C001]` 占位 |
| `claim` | 一句话，可证伪 |
| `evidence_id` | 指向证据表的外键（**必须能 join**，不能是自由文本） |
| `source` | DOI / PMID / 本研究的图表号 |
| `certainty` | 受控枚举：`established` / `supported` / `suggested` / `contested` / `own-data` |
| `certainty_note` | 自由文本，解释为什么是这个等级 |

**`certainty` 必须是枚举，不能是自由文本。**
（原线程里踩过这个坑：`candidate_supported_moderate_to_strong` 这种值一出现，
就没法做任何自动检查了。枚举 + note 两列拆开。）

## 门禁（BLOCK，不是 WARN）

生成正文之前，跑这几条。**任何一条不过，不许出稿**：

```
BLOCK claims_have_sources     每条 claim 的 source 非空
BLOCK evidence_joinable       每个 evidence_id 都能在证据表里找到
BLOCK certainty_in_enum       certainty 落在受控词表内
BLOCK no_orphan_citation      正文里的每个 [Cxxx] 都在台账里
BLOCK no_unused_claim         台账里的每条 claim 都在正文里用了（或显式标 dropped）
WARN  contested_unflagged     certainty=contested 的句子，正文里必须有让步语气
```

## 产物要带指纹

出稿时把 `claims.csv` 的 sha256 写进产物头部。改了台账没重新出稿 → 指纹对不上 → 立刻看得见。

## 谁用

- **nature-writing** — 起草前先建台账；`Assumptions or missing inputs:` 里列出没有 source 的 claim，而不是编一个。
- **nature-citation** — 输入文本 → 先拆成 claim 台账 → 再逐条配文献。这正是它现在做的事，只是没落成表。
- **cite-verify-amr** — 校验的是台账的 `source` 列，而不是散落在正文里的引用。
- **manuscript-integrity-check** — 「引了没列 / 列了没引」这两条检查，本质就是 `no_orphan_citation` + `no_unused_claim`。

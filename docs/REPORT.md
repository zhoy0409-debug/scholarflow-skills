# ScholarFlow — 路由优化报告 (P0)

## 结果

| 指标 | 改前 | 改后 | |
|---|---|---|---|
| **top1_accuracy** 期望 skill 排第一 | 45.2 % | **78.6 %** | +33.4 |
| **contamination** 明确不该命中的 skill 混进候选集 | 41.3 % | **10.9 %** | −30.4 |
| **ambiguity** 每条 prompt 的候选 skill 数 | 1.67 | **1.41** | −0.26 |
| **none_leak** 非学术 prompt 被误抢 | 75.0 % | **50.0 %** | −25.0 |

46 条用例（22 easy / 17 hard / 7 trap），中英各半，覆盖 17 个 skill + 4 条负例。

只改了 description，**没动任何 skill 的正文、manifest 或 references**。

---

## 改前到底错在哪

不是「description 写得不够详细」，恰恰相反 —— **是写得太全了**。

你在每个 nature-* 的 description 里都补了一句
`Also trigger ... even without the word "Nature"`。
这显然是在修「不触发」的问题。它修好了召回，同时把精确率打穿了：

- `学术写作` 被 5 个 skill 同时声明
- `figure` 被 8 个
- `paper` 被 13 个

当 13 个 skill 都说自己管 "paper"，这个词的区分度就是 0。用户说「帮我写论文」，
模型面对 5 个候选，只能猜。

三个具体的、可复现的翻车：

**1. 关键词直接对撞**
`nature-polishing` 的描述里写了 `Float too large`。于是：
```
prompt: 我的 .tex 编译报错 Float too large
→ nature-polishing (4.50)   ← 赢了
  latex-writer-micro (1.00)
```
LaTeX 报错被路由到润色技能。根因是 polishing 和 latex-writer-micro 的排版功能**本来就是重复的**。

**2. 口语整句当触发词**
`nature-reader` 的触发词里塞了 `帮我读这篇文章`。这不是关键词，这是一个句子。
结果任何含「这篇文章」的 prompt 都命中它：
```
prompt: 这篇文章下周组会要讲，帮我做个 PPT
→ nature-reader (4.83)   ← 赢了
  nature-paper2ppt (1.50)
```

**3. 过度触发**
```
prompt: 给我写一封请假邮件   → nature-writing
prompt: 帮我做个季度营收的PPT → nature-paper2ppt / sci-figure-ppt-amr
```
75% 的非学术 prompt 会被这套 skill 抢走。

---

## 改后遵循的三条规则

**规则 1 — description 不是广告位，删掉共享词。**
被 5 个 skill 抢的词对路由零贡献，只制造候选集。每个 skill 只保留自己独占的动词+宾语。
`学术写作` 现在在**零个** description 里出现 —— 它是领域名，不是技能名。

**规则 2 — 写明「输入是什么、输出是什么」。**
四个「文献」skill 之所以互抢，是因为它们都说自己管「文献」。按 I/O 划界就不抢了：

| skill | 输入 | 输出 |
|---|---|---|
| nature-academic-search | 一个问题 | 一批论文 |
| nature-citation | 一段没引用的文字 | 同一段文字 + 引用 |
| zotero-lit-fetch | 已找到的结果页 | 本地文献库条目 |
| cite-verify-amr | 一条引用 | 真伪判定 |

**规则 3 — 每个 description 必须有显式移交。**
```
Not for: improving the English of prose you already finished → nature-polishing.
Not for: attaching references to existing text → nature-citation.
```
这是把「消歧」从模型的猜测变成描述里的事实。这一条贡献了 contamination 下降的绝大部分。

---

## 顺带做出的两个架构决定

**LaTeX 排版全部归 latex-writer-micro。** `nature-polishing` 的 `references/latex-layout.md`
和 latex-writer-micro 完全重复。polishing 从此只管散文语言，一个字都不碰排版。
（测试集里 E5 的期望答案因此改成 latex-writer-micro —— 测试集编码的是**目标架构**，不是现状。）

**`sci-figure-ppt-amr` 标记为 DEPRECATED。** 它的能力 = nature-figure + nature-paper2ppt，
且它裸声明了 `PPT` / `slides` / `presentation`，是 none_leak 的主要来源。
AMR 的绘图内容已经并进 nature-figure 的描述里。

---

## 还没解决的：eval 有个天花板

剩下的失败大多不是 description 的错，是**这个 eval 方法的下限**：

```
prompt: 帮我写论文    → 无候选
prompt: 画个图        → 无候选
```

「论文」「图」被我当作领域通用词过滤掉之后，这两条 prompt 就没有任何可用信号了。

这不是 bug，是**真相**：这类 prompt 本身信息量为零，任何关键词方案都路由不了它。
正确的产品行为不是继续调 description，而是**反问一句**：

> 「你是想从零起草，还是改已有的稿子？」

建议在 README 里给一张路由表，并明确：裸 prompt → 反问，不要猜。

另外这个 eval 是**确定性关键词打分**，测的是 description 之间的碰撞（也就是坏掉的那个东西），
不是端到端的真实路由。它的天花板在 80% 左右。如果要继续往上推，需要换成 LLM 判分的 eval
（skill-creator 有现成的 eval 工具链）。但在此之前，先把 45% → 79% 这一段吃掉。

---

## 怎么落地

```bash
# 1. 先看 diff，不写盘
python3 apply_descriptions.py --skills path/to/scholarflow-skills/skills --dry-run

# 2. 写回（自动备份 .md.bak）
python3 apply_descriptions.py --skills path/to/scholarflow-skills/skills

# 3. 复跑验证
python3 evals/routing/run_eval.py \
  --skills path/to/scholarflow-skills/skills \
  --desc new_descriptions.yaml --compare
```

以后每次改任何 description，都跑第 3 步。这是把「我觉得它有问题」变成一个数字的唯一办法。

---

## 下一步（按收益排序）

1. **砍 nature-figure 的 30MB PNG** —— 仓库 99% 的体积，运行时价值为零
2. **AMR 降级为 domain 轴** —— 5 个重复 skill 折进 nature-* 的 manifest（`domain: amr`）
3. **`_shared/` 建单一源** —— 现在是 9 份 md5 完全相同的复制品，改一次要同步九处
4. **换 LLM 判分 eval** —— 突破当前 80% 的方法天花板

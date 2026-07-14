---
name: humanize
description: >-
  Judge whether a text reads as AI-written, and — only if asked — rewrite it to lower an
  AI-detection or text-similarity score without changing facts, numbers, or citations. Two modes:
  **verdict** (name the specific tells; say "send it as is" when the text is already fine) and
  **rewrite**. Works on any text, not just manuscripts. Not for: general English quality with no
  detector involved → nature-polishing. 触发：AI率、查AI、AIGC检测、降重、去AI味、一股ChatGPT味、改得像人写的、知网查重。
  Triggers: AI detection score, similarity score, humanize, sounds like ChatGPT, is this
  AI-written.
---

# Humanize — 判定 or 改写

**先分模式。这一步不能跳。**

真实用法里，一半的请求是要一个**判断**，不是要一份改写稿：

> 「这样说有 ai 味道吗？」
> 「你觉得这段行吗？」

对这类请求**直接改写是错的** —— 用户要的是判断和具体的 tell。

## 模式一：判定（默认）

触发：用户在**问**（有没有 AI 味 / 像不像 AI 写的 / 这样行吗 / AI 率多少）。

1. 给一个明确判断。
2. **逐条指出具体的 tell**：哪一句、为什么。不要泛泛说「有点机械」。
3. **如果原文其实没问题，就说「直接发没问题」。**
   这是有价值的答案，不是失职。
4. 最后再问一句要不要改。**不要自动动手。**

## 模式二：改写

触发：用户**明确要求**降 AI 率 / 降重 / 改写。

1. 读 `references/humanize-tiers-zh.md`（或 `-en.md`）确定改写强度分级。
2. 目标平台不同，特征不同 —— 按需读 `references/platform-cnki.md` /
   `platform-weipu.md` / `platform-general.md`。
3. 改写，然后跑 `scripts/humanize_check.py` 复核。
4. 输出一张**改动矩阵**：改了哪句、为什么、改动前后。

## 绝对不许动的

事实、数字、基因名、统计量、引用、专业术语、单位。
改写只处理**机械句式**：

- 「对……进行……」这类翻译腔
- 全篇等长句、节奏均匀
- 「第一…第二…」式的程式化罗列
- 段落开头千篇一律的连接词

## 不要过度改写人写的东西

一段带着**具体细节**的专业文字，本身就是最强的「非 AI」信号：

> 「GAPDH 内参在过表达组整体晚约 1.5 个 Ct」
> 「这对引物没落在鼠 Cx3cl1 的构建插入序列上」

**别把它抹成通用书面语。** AI 写不出这种细节 —— 抹掉它反而更像 AI。

## 边界

- **不是**润色。要提升英文质量、改中式英语 → `nature-polishing`。
- 检测工具的分数是**参考**，不是真理。不要为了压分数而损害可读性或准确性。
- 改写完必须让用户知道**改了什么**，不能悄悄替换他的措辞。

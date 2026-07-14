---
name: chinese-docx-reference-unifier
description: Normalize references and in-text citations in Chinese-language DOCX manuscripts, including numbering, bibliography order, punctuation, duplicates, and consistency checks. Use when a user needs a Chinese manuscript reference list cleaned before review or submission.
---

# 中文 DOCX 参考文献统一

中文期刊的参考文献格式（GB/T 7714）和英文的差别很大，而且 Word 里的域代码、
手打编号、EndNote 残留经常混在一起。这个 skill 处理的就是这一团。

## 先诊断，再动手

打开 DOCX，先搞清楚**引用是怎么插进去的**：

1. **EndNote / Zotero 域代码**（`{ ADDIN EN.CITE ... }`）→ 最好办，但**不要直接改域**，
   要么在文献管理软件里改样式，要么先「转换为纯文本」再统一。
   **转换是不可逆的** —— 先备份。
2. **手打的编号**（`[1]`、`[1-3]`、上标）→ 最麻烦。删一条文献，后面全要重编号，
   而且正文里的引用不会跟着动。
3. **两者混用** → 最常见，也最容易出错。**必须先统一到一种。**

## 必查的几件事

- **引了没列 / 列了没引** —— 正文里的每个 `[n]` 在文献表里都要有；文献表里的每一条都要被引。
  这是审稿人第一眼会看的。
- **编号连续** —— 按正文首次出现顺序，1、2、3… 不许跳号、不许重号。
- **上标 vs 方括号** —— 全文统一。混用是低级错误。
- **中英文混排** —— 中文文献用「[1] 张三, 李四. 题名[J]. 刊名, 2020, 1(2): 3-4.」，
  英文文献用对应的 GB/T 7714 英文格式。**标点是中文全角还是英文半角，要按目标期刊要求统一。**
- **文献类型标识码** —— `[J]` 期刊 / `[M]` 专著 / `[D]` 学位论文 / `[C]` 会议 / `[EB/OL]` 电子文献。
  **漏了会被退修。**
- **et al. vs 等** —— 中文文献用「等」，英文文献用「et al.」。作者超过 3 位才用。

## 用脚本，不要手动数

正文引用和文献表的比对**必须用脚本做**。人肉数到第 40 条就会出错，
而这正是审稿人会挑的地方。

跑仓库的门禁：

```bash
python3 gates/gate_checks.py claims --claims claims.csv --manuscript draft.md
```

`no_orphan_citation`（引了没列）和 `no_unused_claim`（列了没引）就是这两条检查。

## 交付

- 改好的 DOCX
- 一份**改动清单**：哪条改了什么、为什么
- 一份**遗留问题清单**：无法自动判断的（比如某条文献的期刊名有两种写法，需要作者确认）

**不要静默替换。** 作者需要知道你动了什么。

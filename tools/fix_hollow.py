#!/usr/bin/env python3
"""
修 14 个空壳 skill —— 上一轮只修了 nature-*，漏掉了这些。

分三类处理：

  A. 8 个「有资产被埋」—— 自动生成 router，列出它自己的 references/scripts，强制加载。
     ppt 58KB、paper-harbor 44KB、storage-analyzer 27KB、zotero-lit-fetch 13KB…
     这些资产一直躺在磁盘上，但 SKILL.md 是空模板，从不提它们。没人会读。

  B. 4 个「彻底空」—— 零资产，只有模板 + 一句 description。删掉，能力交给已有的。

  C. 2 个「彻底空但真需求」—— 写实。

  D. humanize —— frontmatter 没闭合（616 字节，截断在半句话），文件根本加载不了。修。
"""
import argparse, re, shutil, sys
from pathlib import Path

HOLLOW = "Use this skill to execute the workflow described in the frontmatter description"

# ── B：删（零资产，能力已有别处） ─────────────────────────
MERGE = {
    "literature-review":  "零资产的空壳。「问题 → 一批论文」已由 nature-academic-search 承担",
    "writing-medical":    "零资产的空壳。医学写作是 nature-writing 的一个 domain，不是独立技能",
    "format-basic-norms": "零资产的空壳。「按期刊要求规范格式」已由 journal-submission-normalizer 承担",
    "markitdown":         "零资产的空壳。markitdown 是个 CLI 工具，不需要一个 skill 来包装它",
    # 不是空壳，是**逐字相同的重复**：
    "pdf-guide":          "和 `pdf` 正文逐字相同（diff 只有 name 和标题两行），是个纯拷贝",
}

# ── C：写实（零资产，但确实是真需求） ────────────────────
BODIES = {
"reference-checker": """
# Reference Checker —— 这条引用是真的吗

**核验，不是检索。** 输入是一条已经存在的引用，输出是一个判定。

（要找新论文 → `nature-academic-search`。要给一段文字配引用 → `nature-citation`。）

## 三个层次，从便宜到贵

### 1. 它存在吗（必查）

- 有 DOI → 查 `https://doi.org/<DOI>`，看是否解析到真实条目。
- 有 PMID → 查 PubMed。
- 都没有 → 用标题在 CrossRef / PubMed 精确匹配。**标题对不上就是红旗。**

**编造的引用长什么样**：作者是真的、期刊是真的、年份是真的，但这三者的**组合**不存在。
所以不能只看"这些名字我听说过"，必须**真的去查这个组合**。

### 2. 元数据对得上吗

作者、年份、卷期页、期刊名 —— 逐项和权威源比对。
**只错一项也要报**：年份差一年、卷号错一位，都是引用被"记忆生成"出来的痕迹。

### 3. 它真的支持这句话吗（最贵，也最重要）

这一步不能跳过，而且**只有它能抓到最危险的错误**：引用是真的，但它根本没说那句话。

- 取出正文里那句断言。
- 打开被引文献，找到对应的段落/图表。
- 判定：**直接支持 / 部分支持 / 不支持 / 说的是相反的事**。
- 「部分支持」要说清差在哪：样本不同？条件不同？作者的原话更保守？

## 还要查

- **撤稿**：查 Retraction Watch / PubMed 的 retraction 标记。引用一篇被撤稿的文献是硬伤。
- **预印本 vs 正式发表**：预印本被引用时必须标明，且要查它后来有没有正式发表（结论可能变了）。
- **二手引用**：A 引 B 说的话，但 B 其实是引的 C。**要引 C。**

## 输出

一张表，一条引用一行：

| # | 引用 | 存在 | 元数据 | 支持断言 | 备注 |
|---|---|---|---|---|---|
| 12 | Smith 2021 | ✓ | ✗ 年份应为 2022 | 部分支持 | 原文是小鼠，正文写成了人 |

**判定不确定时，说不确定。** 不要为了让表格好看而猜。
""",

"chinese-docx-reference-unifier": """
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
""",

"humanize": """
# Humanize —— 判定 or 改写

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
   `references/platform-weipu.md` / `references/platform-general.md`。
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
""",
}

# ── D：humanize 的 description 也被截断了（"…similarity" 后面没了）。整条重写。──
HUMANIZE_DESC = (
    "Judge whether a text reads as AI-written, and — only if asked — rewrite it to lower an "
    "AI-detection or text-similarity score without changing facts, numbers, or citations. "
    "Two modes: verdict (name the specific tells; say \"send it as is\" when the text is already "
    "fine) and rewrite. Works on any text, not just manuscripts. "
    "Not for: general English quality with no detector involved → nature-polishing. "
    "触发：AI率、查AI、AIGC检测、降重、去AI味、一股ChatGPT味、改得像人写的、知网查重。 "
    "Triggers: AI detection score, similarity score, humanize, sounds like ChatGPT, is this AI-written."
)


def _wrap(s, w=96):
    out, cur = [], ""
    for word in s.split(" "):
        if len(cur) + len(word) + 1 > w and cur:
            out.append(cur); cur = word
        else:
            cur = f"{cur} {word}".strip()
    if cur: out.append(cur)
    return out


# ── A：8 个有资产的，router 里写一句「这个 skill 是干嘛的」 ──
PURPOSE = {
    "ppt": "从大纲到可导出的 PPTX —— 一个基于文件系统的 deck 工作流",
    "paper-harbor": "从授权的数据库把文献元数据抓成 Zotero 可导入的格式",
    "storage-analyzer": "只读地分析磁盘占用，产出一份可操作的清理报告",
    "zotero-lit-fetch": "把检索结果连同 PDF 抓进 Zotero",
    "support-to-repro-pack": "把支持材料整理成一个可复现的交付包",
    "neat-freak": "会话结束时收尾：对齐文档、内存、待办、文件改动",
    "hv-analysis": "横纵向分析：对一个产品/公司/技术做有据可查的深度研究",
    "chinese-review-docx-finalizer": "中文综述 DOCX 的定稿检查",
}


def gen_router(d: Path) -> str:
    """按 skill 自己的资产生成 router —— 不是又一份模板。"""
    name = d.name
    refs = sorted(p.relative_to(d).as_posix()
                  for p in list(d.glob("references/*.md")) + list(d.glob("reference/*.md")))
    scripts = sorted(p.relative_to(d).as_posix()
                     for p in d.glob("scripts/*") if p.is_file() and p.suffix in
                     (".py", ".mjs", ".js", ".sh", ".ps1"))
    other = sorted(p.relative_to(d).as_posix()
                   for p in list(d.glob("assets/*")) + list(d.glob("templates/*")) if p.is_file())

    title = name.replace("-", " ").title()
    L = [f"# {title} — Router", ""]
    if name in PURPOSE:
        L += [PURPOSE[name], ""]
    L += ["**Do not answer from memory, and do not answer from this file.**",
          "The actual logic lives in the files below. This router only decides which to load.",
          "Loading them is not optional.", "", "## 1. Load what this request needs", ""]

    if refs:
        L += ["**References** —— 按需读，不要一次全读：", ""]
        for r in refs:
            L.append(f"- `{r}`")
        L.append("")
    if scripts:
        L += ["**Scripts** —— 这些是真的要跑的，不是拿来读的：", ""]
        for s in scripts:
            L.append(f"- `{s}`")
        L.append("")
    if other:
        L += ["**Assets / templates**：", ""]
        for o in other[:8]:
            L.append(f"- `{o}`")
        L.append("")

    L += ["## 2. Do the work", "",
          "先说清你**选了哪条路**、**用了哪些文件** —— 一行就够，让用户能便宜地纠正你。",
          "",
          "缺必要输入时，写占位符并列在 `Assumptions or missing inputs:` 下面 —— **不要编。**",
          "",
          "## 3. Check before delivering", "",
          "说清你假设了什么、什么没能核实、什么还开着。",
          ""]
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    R = Path(a.root) / "skills"
    dry = a.dry_run

    def write(d: Path, body: str):
        md = d / "SKILL.md"
        raw = md.read_text(encoding="utf-8")
        m = re.match(r"(---\r?\n.*?\r?\n---\r?\n)", raw, re.S)
        if not m:
            # humanize 就是这种：frontmatter 没闭合。手工补回来。
            fmm = re.match(r"---\r?\n(.*)", raw, re.S)
            if not fmm:
                print(f"      ! {d.name}: 无法解析 frontmatter，跳过"); return
            fm = "---\n" + fmm.group(1).rstrip() + "\n---\n"
            print(f"      ⚠ {d.name}: frontmatter 没闭合 —— 补上 `---`")
        else:
            fm = m.group(1)
        if not dry:
            md.write_text(fm + "\n" + body.lstrip("\n"), encoding="utf-8")

    print("\n[1/3] 8 个「有资产被埋」的 —— 生成 router，解封资产")
    for name in PURPOSE:
        d = R / name
        if not d.exists():
            print(f"      ! {name} 不存在"); continue
        raw = (d / "SKILL.md").read_text(encoding="utf-8", errors="replace")
        if HOLLOW not in raw:
            print(f"      · {name}：不是空壳，跳过"); continue
        kb = sum(f.stat().st_size for f in d.rglob("*") if f.is_file()) // 1024
        print(f"      ✓ {name:<32} 解封 {kb}KB")
        write(d, gen_router(d))

    print("\n[2/3] 3 个写实（reference-checker / chinese-docx-reference-unifier / humanize）")
    for name, body in BODIES.items():
        d = R / name
        if not d.exists():
            print(f"      ! {name} 不存在"); continue
        print(f"      ✓ {name}")
        write(d, body)

    # humanize 的 description 也被截断了 —— 整条重写，不只是补 frontmatter
    hz = R / "humanize" / "SKILL.md"
    if hz.exists() and not dry:
        raw = hz.read_text(encoding="utf-8")
        wrapped = "\n".join("  " + l for l in _wrap(" ".join(HUMANIZE_DESC.split())))
        raw = re.sub(r"description:\s*(?:[>|]-?\s*)?.*?(?=\n[a-z_-]+:\s|\n---)",
                     f"description: >-\n{wrapped}", raw, count=1, flags=re.S)
        hz.write_text(raw, encoding="utf-8")
        print("      ✓ humanize：description 也被截断了（…similarity），整条重写")

    print("\n[3/3] 4 个「彻底空」的 —— 删")
    for name, why in MERGE.items():
        d = R / name
        if not d.exists():
            print(f"      · {name}（已不在）"); continue
        print(f"      ✗ {name:<24} {why}")
        if not dry:
            shutil.rmtree(d)

    if dry:
        print("\n  (dry-run，没动文件)")


if __name__ == "__main__":
    main()

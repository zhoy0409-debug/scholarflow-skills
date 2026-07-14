#!/usr/bin/env python3
"""
第二轮去重 —— 这次是「伪装」和「逐字副本」，不是空壳。

盲判（Sonnet，只看 description）暴露的剩余碰撞：

    「实验结果写成 Results/Discussion」 → nature-writing
    「ML 论文，section 结构乱」        → research-paper-writing     ← 同一件事
    「写 Introduction，论点要有文献支撑」 → evidence-driven-writing   ← 同一件事

## 三类处理

A. 逐字副本 —— research-paper-writing 的 8 份 references，
   有 6 份 md5 和 nature-writing **完全相同**。而 nature-writing 的 manifest
   已经有 `paper_type: algorithmic` 轴 —— ML 论文本来就该走那条轴。
   删。差异的 2 份先并进去。

B. 伪装 —— content-research-writer 538 行，讲的是
   "blog posts, newsletters, thought leadership"。**根本不是学术写作**，
   却在抢「帮我写论文」。和 impeccable 一个性质。删。

C. 有真价值但不该独立 —— evidence-driven-writing 的硬门禁：
   "Do not write the section until an evidence map and paragraph blueprint exist."
   这正是 claim-ledger 的思想。**吸收成 nature-writing 的门禁**，然后删掉独立 skill。

D. 合并 —— review-response 的 5 份 references（rebuttal-templates /
   review-classification / tone-guidelines）比 nature-response 的更实用。并过去。

## 不动的（不是碰撞，是设计正确）

    ppt              非学术 PPT      ← 盲判正确地把「产品发布会 PPT」路由给了它
    sci-figure-composer  散落 panel → 拼成一张图   ← 和 nature-figure（数据→出图）I/O 不同
    paper-harbor     CNKI/ScienceDirect 浏览器自动化 ← 和 zotero-lit-fetch（Connector）实现不同
    user-workflow-orchestrator  「我不知道该用哪个」 ← 盲判正确地路由给了它
"""
import argparse, re, shutil, sys
from pathlib import Path

DELETE = {
    "research-paper-writing":
        "8 份 references 有 6 份 md5 和 nature-writing 逐字相同。"
        "而 nature-writing 的 manifest 已有 paper_type: algorithmic 轴 —— ML 论文走那条轴",
    "content-research-writer":
        "538 行，讲的是 blog posts / newsletters / thought leadership —— 不是学术写作，"
        "却在抢「帮我写论文」。和 impeccable 一个性质",
    "evidence-driven-writing":
        "→ 硬门禁吸收进 nature-writing（见 static/core/evidence-gate.md）",
    "review-response":
        "→ 5 份 references 并入 nature-response",
}

# 迁移：源 skill 的哪些文件搬到哪个目标
MIGRATE = [
    ("research-paper-writing", "nature-writing", "references", "rpw-"),
    ("evidence-driven-writing", "nature-writing", "references", "evidence-"),
    ("review-response",         "nature-response", "references", "rr-"),
]

# evidence-driven-writing 的硬门禁 —— 提炼成 nature-writing 的 static 片段
EVIDENCE_GATE = """# 证据门禁 —— 没有证据地图，不许开写

> 来源：`evidence-driven-writing`（已并入本 skill）。
> 它和 `_shared/core/claim-ledger.md` 是同一个思想：**先立台账，再生成句子。**

## 适用

Introduction、Related Work、背景、文献综述 —— 任何**每一句都需要文献支撑**的章节。

## 硬门禁（BLOCK）

**证据地图和段落蓝图不存在之前，一个字都不许写。**

必须先有：

1. **证据地图** —— 一张表，每行一条文献：它说了什么、支持哪个论点、强度如何。
2. **段落蓝图** —— 每一段：这段要推进哪一步？用哪几条证据？

## 为什么

反过来的顺序（先写句子，再回头找引用）**天然产生无源之句**：
写得很顺、读着很像那么回事，但没人能说清它凭什么。

审稿人和查重系统盯的正是这些句子。

而且这个顺序还会产生一种更隐蔽的错误：**先有了想说的话，再去找支持它的文献** ——
这是选择性引用，是学术不端的温和版本。

## 检查

```bash
python3 gates/gate_checks.py claims --claims claims.csv --evidence evidence.csv --manuscript draft.md
```

`claims_have_sources`（无出处的断言）和 `evidence_joinable`（证据外键悬空）会 BLOCK。
"""

# 收窄 description —— 这三个不是碰撞，但描述写得太宽，会误抢
NARROW = {
    "sci-figure-composer":
        "Turn scattered panels that already exist into one submission-grade composite figure: "
        "layout grid, panel labels on a shared axis, consistent fonts and colors, and export. "
        "Input is existing panels (from any tool); output is one assembled figure. "
        "Not for: generating a plot from raw data → nature-figure. "
        "Not for: slides → nature-paper2ppt. "
        "触发：拼版、组图、多面板图、把这几张图拼成一张、panel 标号对不齐、图注排版。 "
        "Triggers: compose these panels, assemble a multi-panel figure, align panel labels.",
    "paper-harbor":
        "Batch-scrape literature metadata from CNKI / ScienceDirect via browser automation "
        "(DrissionPage), then bridge it into Zotero-ready form. For bulk runs against databases "
        "you are logged into. "
        "Not for: saving a page you already have open via the Zotero Connector → zotero-lit-fetch. "
        "Not for: running a topic search → nature-academic-search. "
        "触发：批量抓知网、批量抓ScienceDirect、爬文献题录、把检索结果整批导出。 "
        "Triggers: batch scrape CNKI, bulk-export search results, scrape reference metadata.",
    "user-workflow-orchestrator":
        "Use ONLY when the user explicitly does not know which skill or workflow they need, or "
        "the request spans several domains and needs triage first. It picks the lane and hands "
        "off — it does not do the work itself. "
        "Do not trigger on a request that already names its own task clearly. "
        "触发：我不知道该用哪个、你帮我决定、这事该怎么做、帮我看看该走哪条流程。 "
        "Triggers: which skill should I use, help me decide, I don't know where to start.",
}


def set_desc(md: Path, desc: str, dry):
    txt = md.read_text(encoding="utf-8")
    m = re.match(r"(---\r?\n)(.*?)(\r?\n---)", txt, re.S)
    if not m:
        print(f"      ! {md.parent.name}: frontmatter 异常"); return
    body = " ".join(desc.split())
    wrapped = "\n".join("  " + l for l in _wrap(body, 96))
    fm = re.sub(r"description:\s*(?:[>|]-?\s*)?.*?(?=\n[a-z_-]+:\s|\Z)",
                f"description: >-\n{wrapped}", m.group(2), flags=re.S)
    if not dry:
        md.write_text(txt[:m.start(2)] + fm + txt[m.end(2):], encoding="utf-8")


def _wrap(s, w):
    out, cur = [], ""
    for x in s.split(" "):
        if len(cur) + len(x) + 1 > w and cur:
            out.append(cur); cur = x
        else:
            cur = f"{cur} {x}".strip()
    if cur: out.append(cur)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    R, dry = Path(a.root) / "skills", a.dry_run

    print("\n[1/4] 迁移资产（删之前先保住）")
    for src, dst, sub, prefix in MIGRATE:
        s, d = R / src, R / dst
        if not s.exists() or not d.exists():
            print(f"      · {src} → {dst}：跳过（不存在）"); continue
        for f in sorted((s / sub).glob("*")):
            if not f.is_file():
                continue
            # 逐字相同的不搬 —— 那是副本，不是新东西
            target_same = (d / sub / f.name)
            if target_same.exists() and target_same.read_bytes() == f.read_bytes():
                print(f"      · {src}/{sub}/{f.name}  逐字相同，不搬")
                continue
            out = d / sub / f"{prefix}{f.name}"
            print(f"      ✓ {src}/{sub}/{f.name}  →  {dst}/{sub}/{out.name}")
            if not dry:
                out.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, out)

    print("\n[2/4] evidence-driven-writing 的硬门禁 → nature-writing 的 static 层")
    nw = R / "nature-writing"
    if nw.exists():
        p = nw / "static" / "core" / "evidence-gate.md"
        print(f"      ✓ {p.relative_to(R)}")
        if not dry:
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(EVIDENCE_GATE, encoding="utf-8")
        mf = nw / "manifest.yaml"
        if mf.exists() and not dry:
            t = mf.read_text(encoding="utf-8")
            if "evidence-gate.md" not in t:
                t = t.replace("  - static/core/stance.md",
                              "  - static/core/stance.md\n  - static/core/evidence-gate.md", 1)
                mf.write_text(t, encoding="utf-8")
                print("      ✓ manifest.always_load += static/core/evidence-gate.md")

    print("\n[3/4] 收窄 description（不是碰撞，但描述太宽会误抢）")
    for name, desc in NARROW.items():
        d = R / name
        if not d.exists():
            print(f"      ! {name} 不存在"); continue
        print(f"      ✓ {name}")
        set_desc(d / "SKILL.md", desc, dry)

    # ── 删 skill 会让别的 skill 正文里的点名悬空。修掉。 ──
    print("\n[3.5/4] 修交叉引用（删 skill 会让别处的点名悬空）")
    XREF_FIX = {
        # 上一轮删了 paper-self-review（资产并入 nature-reviewer）
        "journal-selection-advisor": [("`paper-self-review`", "`nature-reviewer`")],
    }
    for name, fixes in XREF_FIX.items():
        d = R / name
        if not d.exists():
            continue
        md = d / "SKILL.md"
        t = md.read_text(encoding="utf-8")
        n = 0
        for old, new in fixes:
            if old in t:
                t = t.replace(old, new); n += 1
                print(f"      ✓ {name}: {old} → {new}")
        if n and not dry:
            md.write_text(t, encoding="utf-8")
        if not n:
            print(f"      · {name}: 已修过")

    print("\n[4/4] 删除")
    for name, why in DELETE.items():
        d = R / name
        if not d.exists():
            print(f"      · {name}（已不在）"); continue
        print(f"      ✗ {name:<26} {why}")
        if not dry:
            shutil.rmtree(d)

    if dry:
        print("\n  (dry-run，没动文件)")


if __name__ == "__main__":
    main()

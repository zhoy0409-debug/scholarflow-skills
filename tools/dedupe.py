#!/usr/bin/env python3
"""
消除触发词碰撞 —— 靠架构，不靠改词。

「帮我写论文」现在有 9 个 skill 在抢。但其中大部分**根本不干活**：

    academic-paper        16 行  零 references  ← 纯转发壳
    manuscript-writing    16 行  零 references  ← 纯转发壳
    deep-research         16 行  零 references  ← 纯转发壳
    ...

模型本身就是路由器。再写一个 "Route xxx" 的 skill，
等于在路由器前面又放一个路由器 —— 而且这个路由器还要和它的下游抢词。

三步：
  1. 删 9 个零内容转发壳 + impeccable（伪装成学术工具的网页 UI 审查器）
  2. paper-spine 的 10 个子技能标 Internal（它们是被 orchestrator 调的，不该被用户触发）
  3. 审稿簇按「科学判断 vs 机械核查」分两条线，资产合并不丢

  python3 dedupe.py --root <repo> --dry-run
  python3 dedupe.py --root <repo>
"""
import argparse, re, shutil, sys
from pathlib import Path

# ── 1. 删除 ───────────────────────────────────────────────
DELETE = {
    # 零内容转发壳：15-17 行，零 references，只说「去 load 别的 skill」
    "academic-paper":      "纯转发壳（16 行，零 references）→ 模型自己会路由",
    "academic-pipeline":   "纯转发壳（16 行，零 references）",
    "manuscript-writing":  "纯转发壳（16 行，零 references）→ nature-writing 有 180KB 真资产",
    "deep-research":       "纯转发壳（16 行，零 references）",
    "deep-research-review":"纯转发壳（16 行，零 references）",
    "omics-analysis":      "纯转发壳（16 行，零 references）→ bio-* 有真内容",
    "ai-check":            "纯转发壳（17 行，零 references）",
    "aigc-down-skill":     "纯转发壳（15 行，零 references）",
    # 不是学术工具
    "impeccable":          "网页 UI 审查工具（1.8MB JS：detect-antipatterns-browser / "
                           "screenshot-contrast / live-browser），description 写得泛，"
                           "会来抢「帮我最后检查一遍稿子」",
    # 审稿簇合并（资产先迁移，再删）
    "peer-review":         "→ 资产并入 nature-reviewer（科学判断线）",
    "paper-self-review":   "→ 资产并入 nature-reviewer",
}

# ── 2. paper-spine 子技能标 Internal ──────────────────────
# 它们假定 paper_spine_config.json / source_map.md / 已确认的 motivation 存在。
# 脱离那套上下文直接跑，结果是错的 —— 所以不该被用户触发。
INTERNAL = {
    "paper-spine-intake":    ("collects workflow config", None),
    "paper-spine-ui":        ("launches the terminal config wizard", None),
    "paper-spine-research":  ("researches target requirements and motivation options",
                              "finding papers on a topic → nature-academic-search"),
    "paper-spine-citation":  ("builds the citation support bank",
                              "adding citations to a paragraph → nature-citation"),
    "paper-spine-build":     ("drafts the paper from confirmed motivation",
                              "drafting a section from notes → nature-writing"),
    "paper-spine-rewrite":   ("rewrites an existing manuscript from confirmed motivation",
                              "improving the English of finished prose → nature-polishing"),
    "paper-spine-humanize":  ("runs the tiered AI-detection rewrite",
                              "lowering an AI-detection score outside PaperSpine → humanize"),
    "paper-spine-latex":     ("assembles the LaTeX project", None),
    "paper-spine-translate": ("produces the translation_zh/ package", None),
    "paper-spine-audit":     ("audits PaperSpine's own outputs for missing artifacts",
                              "auditing any manuscript for consistency → research-integrity-guardrail"),
}

INTERNAL_TMPL = (
    "Internal module of the PaperSpine pipeline — it {job}. "
    "Invoked by `paper-spine`, never by the user. It assumes PaperSpine's config "
    "(`paper_spine_config.json`), `source_map.md`, and a confirmed motivation already exist; "
    "run outside that context it produces wrong results. "
    "**Do not trigger this on a user request.**{alt}"
)

# ── 3. 审稿两条线 ────────────────────────────────────────
LANES = {
    "nature-reviewer": (
        "Act as a referee and judge the science: novelty, significance, evidence chain, "
        "technical soundness, and whether the claims are actually supported. Returns reviewer "
        "reports and an accept / revise / reject verdict. "
        "Not for: mechanical errors — numbers that disagree between abstract and tables, broken "
        "figure cross-references, references cited but not listed → research-integrity-guardrail. "
        "Not for: writing a reply to reviewers who already reviewed you → nature-response. "
        "触发：模拟审稿、审稿人视角、预审、投稿前看看有什么问题、创新性够吗、能发子刊吗、证据链站得住吗。 "
        "Triggers: mock peer review, referee report, review my manuscript, novelty assessment, "
        "is this defensible."
    ),
    "research-integrity-guardrail": (
        "Mechanical pre-submission audit. Finds and locates errors; never rewrites. Checks that "
        "numbers in the abstract agree with the tables, that figure and reference cross-references "
        "survived renumbering, that every reference is both cited and listed, that percentages add "
        "up, that P-values carry the right test label. Runs the executable gates in `gates/`. "
        "Not for: judgment on novelty or scientific merit → nature-reviewer. "
        "触发：一致性核查、核对数字、对不对得上、引了没列、列了没引、编号错位、交叉引用、终稿核对。 "
        "Triggers: do the numbers match, are all figures cited, consistency check, cross-reference audit."
    ),
    "humanize": (
        "Judge whether a text reads as AI-written, and — only if asked — rewrite it to lower an "
        "AI-detection or text-similarity score without changing facts, numbers, or citations. "
        "Two modes: **verdict** (name the specific tells; say \"send it as is\" when the text is "
        "already fine) and **rewrite**. Works on any text, not just manuscripts. "
        "Not for: general English quality with no detector involved → nature-polishing. "
        "触发：AI率、查AI、AIGC检测、降重、去AI味、一股ChatGPT味、改得像人写的、知网查重。 "
        "Triggers: AI detection score, similarity score, humanize, sounds like ChatGPT, is this AI-written."
    ),
}


HUMANIZE_BODY = """
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
"""


def set_desc(md: Path, desc: str, dry):
    txt = md.read_text(encoding="utf-8")
    m = re.match(r"(---\n)(.*?)(\n---)", txt, re.S)
    if not m:
        print(f"      ! {md.parent.name}: 没有 frontmatter"); return
    body = " ".join(desc.split())
    wrapped = "\n".join("  " + l for l in _wrap(body, 96))
    fm = re.sub(r"description:\s*(?:[>|]-?\s*)?.*?(?=\n[a-z_-]+:\s|\Z)",
                f"description: >-\n{wrapped}", m.group(2), flags=re.S)
    if not dry:
        md.write_text(txt[:m.start(2)] + fm + txt[m.end(2):], encoding="utf-8")


def _wrap(s, w):
    out, cur = [], ""
    for word in s.split(" "):
        if len(cur) + len(word) + 1 > w and cur:
            out.append(cur); cur = word
        else:
            cur = f"{cur} {word}".strip()
    if cur: out.append(cur)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    R = Path(a.root) / "skills"
    dry = a.dry_run

    # ── 审稿簇：先迁资产，再删 ──
    print("\n[1/4] 审稿簇合并 —— 科学判断线：nature-reviewer 吸收 peer-review + paper-self-review")
    nr = R / "nature-reviewer" / "references"
    for src, tag in (("peer-review", "peer-review"), ("paper-self-review", "self-review")):
        s = R / src
        if not s.exists(): continue
        for f in list((s / "references").glob("*")) + list((s / "scripts").glob("*")):
            if not f.is_file(): continue
            sub = "scripts" if f.parent.name == "scripts" else "references"
            dst = (R / "nature-reviewer" / sub) / f"{tag}-{f.name}"
            print(f"      {src}/{sub}/{f.name}  →  nature-reviewer/{sub}/{dst.name}")
            if not dry:
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, dst)
        # 570 行的正文也留着，作为参考
        body = (s / "SKILL.md").read_text(encoding="utf-8")
        if len(body.splitlines()) > 100:
            dst = nr / f"{tag}-workflow.md"
            print(f"      {src}/SKILL.md（{len(body.splitlines())} 行正文）  →  nature-reviewer/references/{dst.name}")
            if not dry:
                nr.mkdir(parents=True, exist_ok=True)
                dst.write_text(re.sub(r"^---\n.*?\n---\n", "", body, flags=re.S), encoding="utf-8")

    # ── 两条线的 description ──
    print("\n[2/4] 两条线 + humanize 的 description")
    for name, desc in LANES.items():
        d = R / name
        if not d.exists():
            print(f"      ! {name} 不存在"); continue
        print(f"      ✓ {name}")
        set_desc(d / "SKILL.md", desc, dry)

    # ── paper-spine 标 Internal ──
    print("\n[3/4] paper-spine 子技能标 Internal（不可直接触发）")
    for name, (job, alt) in INTERNAL.items():
        d = R / name
        if not d.exists():
            print(f"      ! {name} 不存在"); continue
        alt_s = f" Standalone alternative: {alt}." if alt else ""
        print(f"      ✓ {name}")
        set_desc(d / "SKILL.md", INTERNAL_TMPL.format(job=job, alt=alt_s), dry)

    # ── humanize 填实：它的 description 声明了判定+改写，正文却还是转发壳 ──
    # 资产的真源在 paper-spine-humanize/references（分级策略 + 知网/维普平台特性）。
    # 两边共用：humanize 是用户入口，paper-spine-humanize 是流水线内部调用。
    print("\n[3.5/4] humanize 填实（此前是 15 行转发壳，说一套做一套）")
    hz, psh = R / "humanize", R / "paper-spine-humanize"
    if psh.exists():
        for f in (psh / "references").glob("*.md"):
            dst = hz / "references" / f.name
            print(f"      共用资产: {f.name}")
            if not dry:
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, dst)
        sc = psh / "scripts" / "humanize_check.py"
        if sc.exists():
            print(f"      共用脚本: humanize_check.py")
            if not dry:
                (hz / "scripts").mkdir(parents=True, exist_ok=True)
                shutil.copy2(sc, hz / "scripts" / "humanize_check.py")
    if not dry and hz.exists():
        md = hz / "SKILL.md"
        txt = md.read_text(encoding="utf-8")
        fm = re.match(r"(---\n.*?\n---\n)", txt, re.S)
        (hz / "SKILL.md").write_text(fm.group(1) + HUMANIZE_BODY, encoding="utf-8")
        print("      ✓ SKILL.md 从 15 行转发壳 → 真正的两模式流程")

    # ── 删除 ──
    print("\n[4/4] 删除")
    freed = 0
    for name, why in DELETE.items():
        d = R / name
        if not d.exists():
            print(f"      · {name}（已不在）"); continue
        sz = sum(f.stat().st_size for f in d.rglob("*") if f.is_file())
        freed += sz
        print(f"      ✗ {name:<26} {sz/1e6:5.2f}MB   {why}")
        if not dry:
            shutil.rmtree(d)
    print(f"\n      释放 {freed/1e6:.1f} MB，删除 {len([n for n in DELETE if (R/n).exists() or dry])} 个 skill")

    if dry:
        print("\n  (dry-run，没动任何文件)")


if __name__ == "__main__":
    main()

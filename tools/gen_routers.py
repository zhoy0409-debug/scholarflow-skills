#!/usr/bin/env python3
"""
救活 nature-* —— 从 manifest 生成真正的 router SKILL.md。

现状：15 个 nature-* 的 SKILL.md 正文**逐字相同**，是一份通用模板：
    "Use this skill to execute the workflow described in the frontmatter description."
它从不提 manifest、从不提 static/、从不提 references/。

后果：manifest.yaml 声明着 always_load，static/ 和 references/ 里躺着 400KB
真材实料 —— 但没有任何一行指令让模型去读它们。**skill 是空壳。**

这个脚本按每个 skill 的**真实 axes** 生成 router。不是又一份模板 ——
nature-writing 的 router 会明确写出它的 4 个轴和每个轴的取值，
nature-figure 的 router 会写 backend: python|r。

  python3 gen_routers.py --skills <dir> --dry-run
  python3 gen_routers.py --skills <dir>
"""
import argparse, re, sys
from pathlib import Path
import yaml

# 门禁片段 —— 今天做的那批，挂到每个 skill 上
GATES = {
    "nature-writing":   ["claim-ledger", "integrity-gates", "narrative-advance"],
    "nature-polishing": ["claim-ledger"],
    "nature-citation":  ["claim-ledger"],
    "nature-figure":    ["figure-qa", "visual-honesty"],
    "nature-paper2ppt": ["narrative-advance", "visual-honesty", "figure-qa"],
    "nature-reviewer":  ["integrity-gates", "narrative-advance"],
    "nature-data":      ["integrity-gates"],
    "nature-academic-search": ["preflight"],
    "nature-downloader":      ["preflight"],
    "nature-reader":    [],
    "nature-response":  [],
}
GATE_DESC = {
    "claim-ledger":      "无出处的断言不许进正文；certainty 必须是受控枚举",
    "integrity-gates":   "数据来源红旗（mock 文件名、零缺失）+ 原始实验数据自洽红旗",
    "narrative-advance": "冗余矩阵：每一页/每一段只准推进一步",
    "figure-qa":         "「代码跑通 ≠ 图做好了」：必须真的打开 PNG 看，必须按最终插入尺寸看",
    "visual-honesty":    "AI 配图的科学正确性门禁",
    "preflight":         "外部依赖一次性验完，别做到一半才发现没连上",
}

TITLE = {
    "nature-writing": "Manuscript Drafting", "nature-polishing": "Language Polishing",
    "nature-figure": "Manuscript Figures", "nature-citation": "Citation Attachment",
    "nature-academic-search": "Literature Search", "nature-reader": "Bilingual Deep Reading",
    "nature-reviewer": "Referee Simulation", "nature-response": "Reviewer Response",
    "nature-data": "Data Availability", "nature-paper2ppt": "Academic Slide Decks",
    "nature-downloader": "Literature Retrieval", "nature-paper-to-patent": "Paper → Patent",
    "nature-experiment-log": "Experiment Log", "nature-proposal-writer": "Research Proposal",
    "nature-literature-pipeline": "Literature Pipeline",
}


def gate_block(name):
    gs = GATES.get(name) or []
    if not gs:
        return ""
    lines = ["", "## Gates — BLOCK, not advice", "",
             "These are not suggestions. If a gate fails, **fix it and re-run; do not deliver.**",
             ""]
    for g in gs:
        lines.append(f"- Read `../_shared/core/{g}.md` — {GATE_DESC[g]}")
    lines += ["",
              "The repo ships an executable version of these checks:",
              "",
              "```bash",
              "python3 gates/gate_checks.py claims    --claims c.csv --evidence e.csv --manuscript draft.md",
              "python3 gates/gate_checks.py data      --file raw.xlsx",
              "python3 gates/gate_checks.py narrative --matrix slides.csv",
              "```",
              "",
              "Exit code 2 means a BLOCK fired. Run them when the artefacts exist.", ""]
    return "\n".join(lines)


def router_with_manifest(name, m):
    t = TITLE.get(name, name)
    axes = m.get("axes") or {}
    always = m.get("always_load") or []
    od = (m.get("references") or {}).get("on_demand")

    L = [f"# {t} — Router", "",
         "**Do not answer from memory, and do not answer from this file.**",
         f"The actual logic lives in `static/` and `references/`. This file only decides",
         "which fragments to load for the request in front of you. Loading them is not optional.", "",
         "## Routing protocol", "",
         "### 1. Load the core layer", "",
         "Read [manifest.yaml](manifest.yaml). Then Read **every** file it lists under `always_load`:", ""]
    for a in always:
        L.append(f"- `{a}`")
    L += ["", "These carry the default stance, workflow, and output format for every job in this skill.", ""]

    if axes:
        L += ["### 2. Detect the axes", "",
              "The manifest declares these axes. Decide a value for each from the user's input:", ""]
        for ax, cfg in axes.items():
            vals = list((cfg.get("values") or {}).keys())
            dflt = cfg.get("default")
            d = f" · default `{dflt}`" if dflt else ""
            L.append(f"- **`{ax}`** — {' / '.join(f'`{v}`' for v in vals)}{d}")
        L += ["",
              "State the detected values in one short line before you start, so the user can",
              "correct you cheaply instead of after you have produced the wrong thing.",
              "If an axis is genuinely ambiguous **and it changes the output**, ask. Otherwise pick the default.", "",
              "### 3. Load only the matching fragments", "",
              "For each axis value, Read the file the manifest maps it to.",
              "**Do not read every file in `static/`** — load only what step 2 selected.", "",
              "### 4. Do the work", "",
              "Apply the loaded fragments. The `always_load` core wins on stance; the axis",
              "fragments win on specifics. If required input is missing, write a placeholder and",
              "list it under `Assumptions or missing inputs:` — **do not invent it.**", ""]
    else:
        L += ["### 2. Do the work", "",
              "This skill has no axes. Apply the core layer directly.",
              "If required input is missing, write a placeholder and list it under",
              "`Assumptions or missing inputs:` — **do not invent it.**", ""]

    step = "5" if axes else "3"
    L += [f"### {step}. Open `references/` only on demand", "",
          "`references/` is a deep library, not a default. Opening all of it wastes the context",
          "you need for the actual work."]
    if od:
        L += ["", "The manifest's `references.on_demand` table says which file answers which question.",
              "Consult it, then Read only that file."]
    L.append("")
    return "\n".join(L) + gate_block(name)


def router_no_manifest(name, d):
    t = TITLE.get(name, name)
    refs = sorted(p.relative_to(d).as_posix() for p in (d / "references").rglob("*.md")) \
        if (d / "references").exists() else []
    L = [f"# {t} — Router", "",
         "**Do not answer from memory, and do not answer from this file.**",
         "The actual logic lives in `references/`. Load what the request needs before you start.", "",
         "## Routing protocol", "",
         "### 1. Pick the references this request needs", ""]
    if refs:
        for r in refs:
            L.append(f"- `{r}`")
        L += ["", "Read the ones that apply. Read all of them only if the request is genuinely broad.", ""]
    else:
        L += ["_(no reference library yet)_", ""]
    L += ["### 2. Do the work", "",
          "Ask only the questions that would otherwise send you down the wrong route.",
          "If required input is missing, write a placeholder and list it under",
          "`Assumptions or missing inputs:` — **do not invent it.**", "",
          "### 3. Check before delivering", "",
          "Say what you assumed, what you could not verify, and what is still open.", ""]
    return "\n".join(L) + gate_block(name)


# 只重写「空壳」—— 那份逐字相同的通用模板。
# 有真内容的 SKILL.md（比如 nature-literature-pipeline 的 113 行）绝不能覆盖。
HOLLOW = "Use this skill to execute the workflow described in the frontmatter description"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--skills", required=True)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force", action="store_true", help="连有真内容的也重写（危险）")
    a = ap.parse_args()
    R = Path(a.skills)

    for d in sorted(R.glob("nature-*")):
        md = d / "SKILL.md"
        txt = md.read_text(encoding="utf-8")
        fm = re.match(r"(---\n.*?\n---\n)", txt, re.S)
        if not fm:
            print(f"  ! {d.name}: 没有 frontmatter，跳过"); continue

        if HOLLOW not in txt and not a.force:
            print(f"  · {d.name:<28} 有真内容（{len(txt.splitlines())} 行），跳过 —— 不覆盖")
            continue

        mf = d / "manifest.yaml"
        if mf.exists():
            m = yaml.safe_load(mf.read_text(encoding="utf-8"))
            body = router_with_manifest(d.name, m)
            kind = f"manifest · {len(m.get('axes') or {})} 轴"
        else:
            body = router_no_manifest(d.name, d)
            kind = "no manifest"

        new = fm.group(1) + "\n" + body
        old_lines = len(txt.splitlines())
        print(f"  {'[dry] ' if a.dry_run else '✓ '}{d.name:<28} {kind:<18} {old_lines} → {len(new.splitlines())} 行"
              f"{'  +gates' if GATES.get(d.name) else ''}")
        if not a.dry_run:
            md.write_text(new, encoding="utf-8")

    if a.dry_run:
        print("\n  (dry-run，没写文件)")


if __name__ == "__main__":
    main()

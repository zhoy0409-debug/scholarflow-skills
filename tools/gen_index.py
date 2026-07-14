#!/usr/bin/env python3
"""
SKILL_INDEX.md 从文件系统生成 —— 它永远不可能过期。

手写的索引必然过期：删了 11 个 skill，索引里 11 个全在。
生成的索引不会。

  python3 gen_index.py --root <repo>
"""
import argparse, re, sys
from pathlib import Path
from collections import defaultdict

# Windows 控制台默认 GBK —— 打一个 ✓ 就 UnicodeEncodeError 崩掉。Linux CI 撞不到。
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# skill 归属哪一族。顺序即输出顺序。
FAMILY = [
    ("写作与投稿 · 轻量（打开就用）", lambda n: n.startswith("nature-")),
    ("PaperSpine · 深度工作流（要配置）", lambda n: n.startswith("paper-spine")),
    ("生信 · bio-*", lambda n: n.startswith("bio-")),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    a = ap.parse_args()
    R = Path(a.root)

    rows = []
    for d in sorted((R / "skills").iterdir()):
        md = d / "SKILL.md"
        if not d.is_dir() or not md.exists():
            continue
        t = md.read_text(encoding="utf-8", errors="replace")
        m = re.match(r"---\n(.*?)\n---", t, re.S)
        desc = ""
        if m:
            dm = re.search(r"description:\s*(.*?)(?=\n[a-z_-]+:\s|\Z)", m.group(1), re.S)
            if dm:
                desc = " ".join(re.sub(r"^\s*[>|]-?\s*", "", dm.group(1)).split())
        rows.append((d.name, desc))

    groups = defaultdict(list)
    for name, desc in rows:
        for label, pred in FAMILY:
            if pred(name):
                groups[label].append((name, desc)); break
        else:
            groups["其他"].append((name, desc))

    out = ["# Skill 索引", "",
           "> **这份文件是生成的。** 不要手改 —— 改动会在下次 `python3 tools/gen_index.py` 时被覆盖。",
           "> 手写的索引必然过期（曾经删了 11 个 skill，索引里 11 个全在）。生成的不会。", "",
           f"共 **{len(rows)}** 个 skill。", ""]

    for label, _ in FAMILY + [("其他", None)]:
        items = groups.get(label)
        if not items:
            continue
        out += [f"## {label}（{len(items)}）", "", "| skill | 做什么 |", "|---|---|"]
        for name, desc in items:
            internal = "**[Internal]** " if desc.startswith("Internal module") else ""
            short = desc if len(desc) <= 170 else desc[:167].rsplit(" ", 1)[0] + "…"
            short = short.replace("|", "\\|")   # 表格里的竖线要转义（f-string 里不能放反斜杠）
            out.append(f"| `{name}` | {internal}{short} |")
        out.append("")

    (R / "SKILL_INDEX.md").write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"  ✓ SKILL_INDEX.md：{len(rows)} 个 skill，{len([g for g in groups if groups[g]])} 组")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
文档悬空引用检查 —— 让「README 推荐一个不存在的 skill」变成 CI fail。

这个检查存在的理由：
删掉 11 个 skill 之后，README / SKILL_INDEX / GETTING_STARTED 里仍然在推荐它们。
README 的 Core workflows 表还在让人用 `manuscript-writing` —— 一个已经不存在的空壳。

**用户会真的照着做。** 而这个错误的根因和之前所有的一样：没有任何东西在检查它。

静态可查的东西，不该靠人肉发现。

  python3 check_docs.py --root <repo>      # exit 1 表示有悬空引用
"""
import argparse, re, sys
from pathlib import Path

# Windows 控制台默认 GBK —— 打一个 ✓ 就 UnicodeEncodeError 崩掉。Linux CI 撞不到。
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

DOCS = ["README.md", "README.zh-CN.md", "SKILL_INDEX.md",
        "GETTING_STARTED.md", "QUALITY_STANDARD.md"]

# 反引号里出现、且长得像 skill 名的东西
TOKEN = re.compile(r"`([a-z][a-z0-9]+(?:-[a-z0-9]+)+)`")

# 不是 skill，别误报
NOT_SKILLS = {
    "author-instructions", "e-g", "double-column", "single-column",
    "read-only", "open-source", "up-to-date", "end-to-end", "point-by-point",
    "state-of-the-art", "pull-request", "check-health", "gate-checks",
    "sync-shared", "gen-routers",
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    a = ap.parse_args()
    R = Path(a.root)

    live = {d.name for d in (R / "skills").iterdir() if d.is_dir() and (d / "SKILL.md").exists()}
    print(f"\n仓库里有 {len(live)} 个 skill\n")

    bad = 0
    for doc in DOCS:
        p = R / doc
        if not p.exists():
            continue
        dangling = {}
        for i, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
            for tok in TOKEN.findall(line):
                if tok in NOT_SKILLS or tok in live:
                    continue
                # bio-* 通配、以及明显的文件名/路径，跳过
                if tok.endswith(("-md", "-py", "-sh", "-yml", "-json")) or "/" in tok:
                    continue
                # 只报那些「看起来就是 skill 名」的（含常见 skill 词根）
                if not re.search(r"(paper|nature|bio|skill|review|research|write|writing|"
                                 r"citation|figure|check|humanize|academic|literature|"
                                 r"spine|omics|zotero|journal|ppt|pdf)", tok):
                    continue
                dangling.setdefault(tok, []).append(i)
        if dangling:
            bad += 1
            print(f"  ✗ {doc}")
            for tok, lines in sorted(dangling.items()):
                print(f"        `{tok}`  —— 这个 skill 不存在（行 {', '.join(map(str, lines[:4]))}）")
        else:
            print(f"  ✓ {doc}")

    print()
    if bad:
        print(f"  {bad} 份文档在推荐不存在的 skill。用户会照着做。\n")
        sys.exit(1)
    print("  没有悬空引用。")


if __name__ == "__main__":
    main()

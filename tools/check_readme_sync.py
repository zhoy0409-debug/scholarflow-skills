#!/usr/bin/env python3
"""
双语 README 不同步检查。

两份 README 会漂移 —— 改了英文忘了中文，是开源项目的常态。
让它变成一个 CI fail。

判据（结构，不是逐字翻译）：
  · 两边的一级/二级标题数量要一致
  · 两边的代码块数量要一致（门禁命令、BLOCK 输出）
  · 两边的表格行数要一致
  · 互相的语言切换链接要在

  python3 check_readme_sync.py --root <repo>
"""
import argparse, re, sys
from pathlib import Path


def shape(p: Path):
    t = p.read_text(encoding="utf-8")
    return {
        "h2": len(re.findall(r"^## ", t, re.M)),
        "h3": len(re.findall(r"^### ", t, re.M)),
        "code": t.count("```") // 2,
        "table_rows": len(re.findall(r"^\|", t, re.M)),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    a = ap.parse_args()
    R = Path(a.root)
    en, zh = R / "README.md", R / "README.zh-CN.md"

    if not zh.exists():
        print("  ✗ 缺 README.zh-CN.md"); sys.exit(1)
    if "README.zh-CN.md" not in en.read_text(encoding="utf-8"):
        print("  ✗ README.md 里没有切换到中文的链接"); sys.exit(1)
    if "README.md" not in zh.read_text(encoding="utf-8"):
        print("  ✗ README.zh-CN.md 里没有切换到英文的链接"); sys.exit(1)

    se, sz = shape(en), shape(zh)
    bad = [k for k in se if se[k] != sz[k]]
    print(f"\n  {'':14}{'EN':>5}{'ZH':>5}")
    for k in se:
        mark = "✗" if k in bad else "✓"
        print(f"  {mark} {k:<12}{se[k]:>5}{sz[k]:>5}")
    print()
    if bad:
        print("  两份 README 结构不同步 —— 大概率是改了一边忘了另一边。\n")
        sys.exit(1)
    print("  双语 README 同步。\n")


if __name__ == "__main__":
    main()

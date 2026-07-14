#!/usr/bin/env python3
"""GETTING_STARTED.md 里两处悬空引用 —— 指向已删除的 skill。"""
import argparse, sys
from pathlib import Path

FIXES = [
    # 「投稿前检查」那行：paper-self-review 已删（资产并入 nature-reviewer）。
    # 而且原来那行把「科学判断」和「机械核查」混在一起了 —— 这是两件事。
    ("| Select journals or run pre-submission checks | `journal-selection-advisor`, "
     "`journal-submission-normalizer`, `research-integrity-guardrail`, `paper-self-review` |",
     "| Select a journal or normalize submission formatting | `journal-selection-advisor`, "
     "`journal-submission-normalizer` |\n"
     "| Pre-submission: **is the science defensible?** | `nature-reviewer` |\n"
     "| Pre-submission: **do the numbers and cross-references hold up?** | "
     "`research-integrity-guardrail` + `gates/` |"),
    # omics-analysis 是纯转发壳，已删。bio-* 才有真内容。
    ("| Run bioinformatics or omics workflows | `omics-analysis`, `bio-*`, "
     "`samtools-bam-processing`, `bcftools-variant-manipulation` |",
     "| Run bioinformatics or omics workflows | `bio-*` (130 skills), "
     "`samtools-bam-processing`, `bcftools-variant-manipulation` |"),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    a = ap.parse_args()
    p = Path(a.root) / "GETTING_STARTED.md"
    if not p.exists():
        sys.exit("✗ 找不到 GETTING_STARTED.md")
    s = p.read_text(encoding="utf-8")
    n = 0
    for old, new in FIXES:
        if old in s:
            s = s.replace(old, new); n += 1
            print(f"  ✓ 修好：{old[:56]}…")
        else:
            print(f"  · 已修过或格式不同：{old[:56]}…")
    p.write_text(s, encoding="utf-8")
    print(f"\n  {n} 处")


if __name__ == "__main__":
    main()

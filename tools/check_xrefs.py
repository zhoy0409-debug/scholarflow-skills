#!/usr/bin/env python3
"""
skill 之间的悬空引用 —— check_docs 的盲区。

check_docs 只扫 README / SKILL_INDEX / GETTING_STARTED。
但 **skill 的正文里也在互相点名**：

    user-workflow-orchestrator:
      "Prefer `nature-*`, `paper-spine-*`, `reference-checker`, and
       `research-integrity-guardrail`."

    humanize:
      "Not for: general English quality → `nature-polishing`."

删一个 skill，这些引用就悬空了。**而模型会照着它去调一个不存在的 skill。**

同样的病：静态可查，但没人查。

  python3 check_xrefs.py --root <repo>     # exit 1 表示有悬空
"""
import argparse, re, sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

TOKEN = re.compile(r"`([a-z][a-z0-9]*(?:-[a-z0-9]+)+)`")

# 通配和明显不是 skill 名的
IGNORE = re.compile(
    r"^(bio-\*|nature-\*|paper-spine-\*|samtools-\*|bcftools-\*|biopython-\*|"
    r".*\.(md|py|sh|mjs|js|json|yaml|yml|txt|csv|html|png|tex|docx|pptx|xlsx|bib|nbib|ris)|"
    r"[a-z-]+/.*|"                       # 路径
    r"(?:read|write|edit|bash|glob|grep|task)$)"
)
# 常见的非 skill 连字符词
STOP = {
    "end-to-end", "point-by-point", "state-of-the-art", "read-only", "open-source",
    "up-to-date", "double-column", "single-column", "e-g", "et-al", "pre-submission",
    "paired-end", "single-end", "long-read", "short-read", "real-time", "high-throughput",
    "gene-level", "transcript-level", "well-known", "so-called", "self-contained",
    "cross-reference", "cross-references", "follow-up", "in-text", "sub-figure",
    "multi-panel", "multi-source", "one-sentence", "line-by-line", "row-by-row",
    "gb-t", "et-cetera", "de-novo", "pull-request", "left-align", "top-level",
}

# 外部工具 / Python 包 / npm 包 —— 它们出现在反引号里是正常的，不是 skill 引用。
# 判据：如果一个名字在**任何 skill 的目录名里都不存在**，而且它出现的那行在讲
# 「装什么、跑什么」，那它多半是个外部工具。这里用白名单，宁可漏报不要误报。
EXTERNAL = {
    "scikit-bio", "md-to-pdf", "local-md-mermaid-pdf-sandbox", "old-python-code-review",
    "scikit-learn", "python-docx", "python-pptx", "ncbi-datasets", "sra-tools",
    "bwa-mem2", "iq-tree", "raxml-ng", "trim-galore", "cd-hit", "orthofinder3",
}
STOP |= EXTERNAL


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    a = ap.parse_args()
    R = Path(a.root) / "skills"

    live = {d.name for d in R.iterdir() if d.is_dir() and (d / "SKILL.md").exists()}
    print(f"\n仓库里有 {len(live)} 个 skill。检查 skill 正文里的互相点名…\n")

    bad = 0
    for d in sorted(R.iterdir()):
        md = d / "SKILL.md"
        if not md.exists():
            continue

        # router 里会列出 manifest 的**轴取值**（`pdf-text` / `scanned-pdf` / …）。
        # 那些是取值，不是 skill 名 —— 不能当悬空引用报。
        axis_values = set()
        mf = d / "manifest.yaml"
        if mf.exists() and yaml:
            try:
                man = yaml.safe_load(mf.read_text(encoding="utf-8")) or {}
                for ax in (man.get("axes") or {}).values():
                    axis_values |= set((ax or {}).get("values") or {})
            except Exception:
                pass

        in_code = False
        dangling = {}
        for i, line in enumerate(md.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if line.lstrip().startswith("```"):
                in_code = not in_code
                continue
            if in_code:          # 代码块和示例里的名字不算引用
                continue
            for tok in TOKEN.findall(line):
                if (tok in live or tok in STOP or IGNORE.match(tok) or tok == d.name
                        or tok in axis_values):
                    continue
                # 只报「长得就像 skill 名」的
                if not re.search(r"(nature|paper|bio|spine|humanize|review|research|"
                                 r"citation|figure|writing|zotero|journal|reference|"
                                 r"literature|academic|integrity|check|ppt|pdf)", tok):
                    continue
                dangling.setdefault(tok, []).append(i)
        if dangling:
            bad += 1
            print(f"  ✗ {d.name}/SKILL.md")
            for tok, lines in sorted(dangling.items()):
                print(f"        `{tok}` 不存在 —— 模型会照着它去调一个没有的 skill（行 "
                      f"{', '.join(map(str, lines[:4]))}）")

    print()
    if bad:
        print(f"  {bad} 个 skill 在点名不存在的 skill。\n")
        sys.exit(1)
    print("  没有悬空的交叉引用。\n")


if __name__ == "__main__":
    main()

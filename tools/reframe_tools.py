#!/usr/bin/env python3
"""
11 个工具 skill → 参考手册。不删，不争抢任务。

盲判（Sonnet，只看 description）：11 条生信任务，**10 条输给了 bio-***。

    「把 BAM 按坐标排序」→ bio-alignment-sorting   （不是 samtools-bam-processing）
    「FASTQ 去接头质控」→ bio-read-qc-fastp-workflow（不是 fastp-fastq-preprocessing）
    「注释一个细菌基因组」→ bio-genome-annotation-… （不是 prokka / bakta）

原因不是它们写得差 —— 每个 300~570 行，质量很好。原因是**组织方式**：

    bio-*      任务导向：「把 BAM 排序」          ← 用户说的是任务
    工具 skill  工具导向：「samtools 能干的所有事」  ← 用户不这么说话

所以它们永远拿不到路由，成了死重。但里面有 ~4000 行真内容，删了可惜。

**改成参考手册。** description 明说：任务先走 bio-*；需要一个它们没覆盖的
flag 或子命令时，才查这里。碰撞消失，内容一行不丢。
"""
import argparse, re, sys
from pathlib import Path

TOOLS = {
    "samtools-bam-processing": (
        "samtools", "bio-alignment-sorting / bio-alignment-indexing / bio-alignment-filtering / "
        "bio-bam-statistics / bio-sam-bam-basics"),
    "bcftools-variant-manipulation": (
        "bcftools", "bio-vcf-basics / bio-vcf-manipulation / bio-variant-calling / "
        "bio-variant-normalization"),
    "pysam-genomic-files": (
        "pysam", "bio-sam-bam-basics / bio-pileup-generation"),
    "bwa-mem2-dna-aligner": (
        "bwa-mem2", "bio-read-alignment-bwa-alignment"),
    "fastp-fastq-preprocessing": (
        "fastp", "bio-read-qc-fastp-workflow / bio-read-qc-adapter-trimming"),
    "multiqc-qc-reports": (
        "MultiQC", "bio-reporting-automated-qc-reports / bio-read-qc-quality-reports"),
    "snpeff-variant-annotation": (
        "SnpEff / SnpSift", "bio-variant-annotation"),
    "vcf-variant-filtering": (
        "VCF 质控过滤", "bio-variant-calling-filtering-best-practices"),
    "prokka-genome-annotation": (
        "Prokka", "bio-genome-annotation-prokaryotic-annotation"),
    "bakta-genome-annotation": (
        "Bakta", "bio-genome-annotation-prokaryotic-annotation"),
    "roary-pangenome": (
        "Roary", "bio-comparative-genomics-pangenome-analysis"),
}

TMPL = (
    "**Reference manual for {tool}, not a task skill.** "
    "The task-oriented skills route first — {tasks}. "
    "Come here only when you need a flag, subcommand, or edge case those do not cover, "
    "or when you want the full tool surface in one place. "
    "**Do not trigger this on a plain task request** like \"sort my BAM\" or "
    "\"annotate this genome\" — that belongs to the task skill."
)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    R = Path(a.root) / "skills"

    print(f"\n{len(TOOLS)} 个工具 skill → 参考手册（内容一行不删）\n")
    for name, (tool, tasks) in TOOLS.items():
        d = R / name
        if not d.exists():
            print(f"  ! {name} 不存在"); continue
        md = d / "SKILL.md"
        txt = md.read_text(encoding="utf-8")
        m = re.match(r"(---\r?\n)(.*?)(\r?\n---)", txt, re.S)
        if not m:
            print(f"  ! {name}: frontmatter 异常"); continue

        # 保留原描述的第一句（它讲清了这个工具是干嘛的），前面加上「参考手册」的定位
        old = re.search(r"description:\s*(.*?)(?=\n[a-z_-]+:\s|\Z)", m.group(2), re.S)
        first = ""
        if old:
            o = " ".join(re.sub(r'^\s*[>|]-?\s*', "", old.group(1)).split()).strip('"')
            first = o.split(". ")[0].rstrip(".") + ". "

        desc = first + TMPL.format(tool=tool, tasks=tasks)
        wrapped = "\n".join("  " + l for l in _wrap(" ".join(desc.split()), 96))
        fm = re.sub(r"description:\s*(?:[>|]-?\s*)?.*?(?=\n[a-z_-]+:\s|\Z)",
                    f"description: >-\n{wrapped}", m.group(2), flags=re.S)
        lines = len(txt.splitlines())
        print(f"  ✓ {name:<32} {lines:>4} 行内容保留，description → 参考手册")
        if not a.dry_run:
            md.write_text(txt[:m.start(2)] + fm + txt[m.end(2):], encoding="utf-8")

    if a.dry_run:
        print("\n  (dry-run)")


def _wrap(s, w):
    out, cur = [], ""
    for x in s.split(" "):
        if len(cur) + len(x) + 1 > w and cur:
            out.append(cur); cur = x
        else:
            cur = f"{cur} {x}".strip()
    if cur: out.append(cur)
    return out


if __name__ == "__main__":
    main()

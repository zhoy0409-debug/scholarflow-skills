#!/usr/bin/env python3
"""
skill 健康检查 —— 把「空壳 skill」变成一个会 fail 的 CI。

今天发现的两个断裂，都是静态可查的，本该被 CI 拦住：
  1. SKILL.md 是通用模板，从不提 manifest / static / references  → skill 是空壳
  2. manifest 声明的 always_load 指向不存在的文件               → 加载必然失败

  python3 check_health.py --root <repo>        # exit 1 表示有问题
"""
import argparse, re, sys
from pathlib import Path
import yaml

HOLLOW = "Use this skill to execute the workflow described in the frontmatter description"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--prefix", default="nature-", help="只查这一族")
    a = ap.parse_args()

    R = Path(a.root) / "skills"
    bad = 0
    print(f"\n检查 {a.prefix}* …\n")

    for d in sorted(R.glob(f"{a.prefix}*")):
        md = d / "SKILL.md"
        if not md.exists():
            print(f"  ✗ {d.name}: 没有 SKILL.md"); bad += 1; continue
        txt = md.read_text(encoding="utf-8")
        issues = []

        # 1. 空壳检测
        if HOLLOW in txt:
            issues.append("SKILL.md 是通用模板 —— 不加载任何 static/references，等于空壳")

        # 2. 有资产但 SKILL.md 从不引用它们
        has_assets = (d / "static").exists() or (d / "references").exists()
        mentions = re.search(r"manifest|static/|references/", txt)
        if has_assets and not mentions:
            kb = sum(f.stat().st_size for f in d.rglob("*.md")) // 1024
            issues.append(f"有 {kb}KB 的 static/references，但 SKILL.md 一个字都没提 → 没人会读")

        # 3. manifest 断链
        mf = d / "manifest.yaml"
        if mf.exists():
            m = yaml.safe_load(mf.read_text(encoding="utf-8")) or {}
            missing = []

            def chk(p):
                if isinstance(p, str) and p.endswith(".md") and not (d / p).exists():
                    missing.append(p)

            for x in (m.get("always_load") or []):
                chk(x)
            for ax in (m.get("axes") or {}).values():
                for v in (ax.get("values") or {}).values():
                    chk(v)
            if missing:
                issues.append(f"manifest 指向 {len(missing)} 个不存在的文件: {missing[:3]}")

        if issues:
            bad += 1
            print(f"  ✗ {d.name}")
            for i in issues:
                print(f"        {i}")
        else:
            print(f"  ✓ {d.name}")

    print()
    if bad:
        print(f"  {bad} 个 skill 不健康。")
        sys.exit(1)
    print("  全部健康。")


if __name__ == "__main__":
    main()

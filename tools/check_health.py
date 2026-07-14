#!/usr/bin/env python3
"""
skill 健康检查 —— 检查**每一个** skill，不只是我记得去看的那些。

## 上一版为什么是危险的

上一版只 glob 了 `nature-*`。它报「全部健康」的时候：

  - 另有 **14 个** skill 是同一份空壳模板，其中 8 个有资产但没有任何指令去读
    （`ppt` 108KB、`paper-harbor` 76KB、`storage-analyzer` 44KB、`zotero-lit-fetch` 32KB…）
  - `humanize/SKILL.md` 的 frontmatter **没有闭合的 `---`** —— 这种文件根本加载不了

**一个只检查你记得去看的地方的 CI，比没有 CI 更危险 —— 它给你假的安全感。**

## 现在查什么

  frontmatter_valid   ---  开了要闭；必须有 name 和 description
  name_matches_dir    frontmatter 的 name 要和目录名一致
  not_hollow          正文不是那份「Use this skill to execute the workflow…」通用模板
  assets_are_loaded   有 static/ references/ 就必须在正文里被引用，否则等于没有
  manifest_resolves   manifest 声明的每个路径都要存在
  description_sane    description 不能为空、不能截断在半截

  python3 check_health.py --root <repo>            # 全部
  python3 check_health.py --root <repo> --fix-list # 只列出需要修的
"""
import argparse, re, sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

HOLLOW = "Use this skill to execute the workflow described in the frontmatter description"

# 这些是真正的「单文件即全部」skill —— 没有资产，正文自己就是全部内容。
# 它们不需要 router，但仍然要通过 frontmatter 和 not_hollow 检查。
ASSET_DIRS = ("static", "references", "reference", "scripts", "assets")


def check(d: Path):
    """返回 (issues, is_hollow)。"""
    issues = []
    md = d / "SKILL.md"
    if not md.exists():
        return ["没有 SKILL.md"], False

    raw = md.read_text(encoding="utf-8", errors="replace")

    # ── frontmatter 合法性 ──────────────────────────────
    m = re.match(r"---\r?\n(.*?)\r?\n---\r?\n?", raw, re.S)
    if not m:
        if raw.lstrip().startswith("---"):
            issues.append("frontmatter 开了但**没有闭合的 `---`** → 这个文件根本加载不了")
        else:
            issues.append("没有 frontmatter")
        return issues, False

    fm, body = m.group(1), raw[m.end():]

    name = re.search(r"^name:\s*(\S+)", fm, re.M)
    if not name:
        issues.append("frontmatter 缺 name")
    elif name.group(1).strip("\"'") != d.name:
        issues.append(f"name (`{name.group(1)}`) 和目录名 (`{d.name}`) 不一致")

    dm = re.search(r"description:\s*(.*?)(?=\n[a-z_-]+:\s|\Z)", fm, re.S)
    if not dm:
        issues.append("frontmatter 缺 description")
    else:
        desc = " ".join(re.sub(r"^\s*[>|]-?\s*", "", dm.group(1)).split())
        # YAML 的 description 可能被引号包起来 —— 去掉引号再判断结尾
        probe = desc.strip().strip('"\'').rstrip().rstrip("*")   # 去掉引号和 markdown 粗体标记再判断结尾
        if len(desc) < 20:
            issues.append(f"description 过短或为空（{len(desc)} 字符）")
        elif len(probe) > 200 and not re.search(r"[.。!?！？…)\]*]$", probe.rstrip("*")):
            issues.append(f"description 疑似被截断（结尾：…{probe[-40:]}）")

    # ── 空壳 ───────────────────────────────────────────
    hollow = HOLLOW in body
    if hollow:
        issues.append("正文是那份通用空壳模板 —— 不加载任何东西，等于什么都不做")

    # ── 有资产但没人读 ─────────────────────────────────
    # 只算「模型真的要读/要跑」的东西。图标、LICENSE、封面图不算资产。
    LOADABLE = (".md", ".py", ".mjs", ".js", ".sh", ".ps1", ".json", ".yaml", ".yml",
                ".txt", ".csv", ".html", ".ipynb")
    assets = {}
    for p in d.iterdir():
        if not (p.is_dir() and p.name in ASSET_DIRS):
            continue
        sz = sum(f.stat().st_size for f in p.rglob("*")
                 if f.is_file() and f.suffix.lower() in LOADABLE)
        if sz:
            assets[p.name] = sz
    if assets:
        mentions = re.search(r"manifest|static/|references?/|scripts/|assets/", body)
        if not mentions:
            kb = sum(assets.values()) // 1024
            issues.append(f"有 {kb}KB 的 {'/'.join(assets)}，但正文一个字都没提 → 没人会读")

    # ── manifest 断链 ──────────────────────────────────
    mf = d / "manifest.yaml"
    if mf.exists() and yaml:
        try:
            man = yaml.safe_load(mf.read_text(encoding="utf-8")) or {}
        except Exception as e:
            issues.append(f"manifest.yaml 解析失败: {e}")
            man = {}
        missing = []

        def chk(p):
            if isinstance(p, str) and p.endswith(".md") and not (d / p).exists():
                missing.append(p)

        for x in (man.get("always_load") or []):
            chk(x)
        for ax in (man.get("axes") or {}).values():
            for v in ((ax or {}).get("values") or {}).values():
                chk(v)
        if missing:
            issues.append(f"manifest 指向 {len(missing)} 个不存在的文件: {missing[:3]}")

    return issues, hollow


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--fix-list", action="store_true", help="只输出需要修的 skill 名，一行一个")
    a = ap.parse_args()

    R = Path(a.root) / "skills"
    skills = sorted(d for d in R.iterdir() if d.is_dir() and not d.name.startswith("_"))

    bad, hollow_names = {}, []
    for d in skills:
        issues, hollow = check(d)
        if issues:
            bad[d.name] = issues
        if hollow:
            hollow_names.append(d.name)

    if a.fix_list:
        print("\n".join(hollow_names))
        return

    print(f"\n检查全部 {len(skills)} 个 skill（不是只查我记得去看的那些）\n")
    for name in sorted(bad):
        print(f"  ✗ {name}")
        for i in bad[name]:
            print(f"        {i}")

    ok = len(skills) - len(bad)
    print(f"\n  ✓ {ok} 个健康")
    if bad:
        print(f"  ✗ {len(bad)} 个有问题（其中 {len(hollow_names)} 个是空壳）\n")
        sys.exit(1)
    print()


if __name__ == "__main__":
    main()

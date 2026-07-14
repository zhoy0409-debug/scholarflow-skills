#!/usr/bin/env python3
"""
shared/  →  skills/_shared/   单一真源 + 生成副本 + 漂移检查

为什么需要两份：
  - manifest.yaml 里写的是 `../_shared/core/ethics.md`（相对 skill 目录）。
    这个路径在 skill 被单独拷到 ~/.claude/skills/ 时也成立 —— 前提是
    skills/_shared/ 跟着一起走。
  - 但 gates/ 和 docs/ 引用的是仓库根的 shared/。

所以：shared/ 是**唯一真源，人只改这里**；skills/_shared/ 由本脚本生成并提交。
CI 跑 check，两边不一致就 exit 1 —— 防止有人手改了副本然后忘了同步。

  python3 sync_shared.py sync  --root <repo>
  python3 sync_shared.py check --root <repo>      # CI
"""
import argparse, hashlib, shutil, sys
from pathlib import Path


def digest(p: Path):
    return {f.relative_to(p).as_posix(): hashlib.md5(f.read_bytes()).hexdigest()
            for f in sorted(p.rglob("*")) if f.is_file()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["sync", "check"])
    ap.add_argument("--root", required=True)
    a = ap.parse_args()

    root = Path(a.root)
    src, dst = root / "shared", root / "skills" / "_shared"
    if not src.exists():
        sys.exit(f"✗ 缺少真源: {src}")

    if a.cmd == "sync":
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
        (dst / "DO-NOT-EDIT.md").write_text(
            "# 不要改这个目录\n\n"
            "本目录由 `tools/sync_shared.py` 从仓库根的 `shared/` 生成。\n"
            "改动请改 `shared/`，然后跑：\n\n"
            "```bash\npython3 tools/sync_shared.py sync --root .\n```\n\n"
            "CI 会检查两边是否一致，不一致直接 fail。\n", encoding="utf-8")
        n = len(list(dst.rglob("*")))
        print(f"  ✓ shared/ → skills/_shared/  ({n} 项)")
        return

    if not dst.exists():
        print("  ✗ skills/_shared/ 不存在 → 跑 sync"); sys.exit(1)
    want, got = digest(src), digest(dst)
    got.pop("DO-NOT-EDIT.md", None)
    if want != got:
        for k in sorted(set(want) - set(got)):        print(f"  ✗ 副本缺失: {k}")
        for k in sorted(set(got) - set(want)):        print(f"  ✗ 副本多余: {k}")
        for k in sorted(set(want) & set(got)):
            if want[k] != got[k]:                     print(f"  ✗ 内容漂移: {k}")
        print("\n  跑: python3 tools/sync_shared.py sync --root .")
        sys.exit(1)
    print(f"  ✓ shared/ 与 skills/_shared/ 一致（{len(want)} 个文件）")


if __name__ == "__main__":
    main()

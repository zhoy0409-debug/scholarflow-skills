#!/usr/bin/env python3
"""把 figure 门禁接到 nature-figure 和 sci-figure-composer 的 router 上。

门禁写完没人调用，等于没写 —— 这正是这个仓库之前的病。
"""
import argparse, re, sys
from pathlib import Path

# Windows 控制台默认 GBK —— 打一个 ✓ 就 UnicodeEncodeError 崩掉。Linux CI 撞不到。
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

GATE_BLOCK = """
## Gates — BLOCK, not advice

**代码跑通 ≠ 图做好了。** matplotlib 不会因为
标签被裁掉、panel 标号错位、字小到印不出、你把位图当「可编辑产物」交付
而报错。**代码零报错，图是废的。**

出图之后、交付之前，必须跑：

```bash
# 位图：DPI 够不够（按最终插入宽度算）、内容有没有被画布裁掉
python3 gates/gate_checks.py figure --file fig1.png --width-mm 180

# 线条图门槛更高（600 dpi）
python3 gates/gate_checks.py figure --file fig1.png --width-mm 180 --line-art

# 矢量：最终尺寸下最小字号够不够；若声称「可编辑」，必须有真的 <text>
python3 gates/gate_checks.py figure --file fig1.svg --width-mm 180 --claim-editable

# 多面板：同一行的标号必须同一个 y，同一列必须同一个 x
python3 gates/gate_checks.py figure --panels panels.csv
```

`--width-mm` 是**最终插进版面的宽度**，不是画布宽度。
单栏常见 85–90 mm，双栏 170–180 mm。**这个数填错，DPI 检查就没意义。**

退出码 2 = 有 BLOCK。**修完重跑，不许交付。**

深层规范见 `../_shared/core/figure-qa.md`（QA 环、release blockers、按结论选图形形式）
和 `../_shared/core/visual-honesty.md`（AI 配图的科学正确性）。
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    R = Path(a.root) / "skills"

    for name in ("nature-figure", "sci-figure-composer"):
        d = R / name
        if not d.exists():
            print(f"  ! {name} 不存在"); continue
        md = d / "SKILL.md"
        t = md.read_text(encoding="utf-8")
        if "gate_checks.py figure" in t:
            print(f"  · {name}：已接过"); continue
        # 接在已有的 Gates 段之后；没有就追加到末尾
        if re.search(r"^## Gates", t, re.M):
            t = re.sub(r"(^## Gates.*?)(?=^## |\Z)", r"\1" + GATE_BLOCK.lstrip("\n") + "\n",
                       t, count=1, flags=re.S | re.M)
        else:
            t = t.rstrip() + "\n" + GATE_BLOCK
        print(f"  ✓ {name}：接上 figure 门禁")
        if not a.dry_run:
            md.write_text(t, encoding="utf-8")

    if a.dry_run:
        print("\n  (dry-run)")


if __name__ == "__main__":
    main()

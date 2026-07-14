#!/usr/bin/env python3
"""
ScholarFlow 门禁引擎 —— 把 SHOULD 变成 BLOCK。

现在的 skill 是「一段很长的 prompt」：它告诉模型该怎么做，
但没有任何东西检查模型到底做没做。模型会说「已检查对齐」然后交一张歪的图。

这个文件把 _shared/core/ 里的三份规范变成**会 exit 2 的可执行检查**。

  gates claims    --claims c.csv --evidence e.csv --manuscript draft.md
  gates data      --file raw.xlsx
  gates narrative --matrix slides.csv
  gates all       --config gates.yaml

退出码：0 = 全过（并写指纹）  2 = 有 BLOCK  （WARN 不阻塞）
"""
from __future__ import annotations

import argparse, hashlib, json, re, sys
from dataclasses import dataclass, field
from pathlib import Path

# ── 受控词表 ──────────────────────────────────────────────
# 教训（来自你的综述引擎线程）：certainty 一旦允许自由文本
# （'candidate_supported_moderate_to_strong'），所有自动检查立刻失效。
# 枚举 + note 两列拆开，这是硬性的。
CERTAINTY = {"established", "supported", "suggested", "contested", "own-data"}

MOCK_TOKENS = ("mock", "sim", "simulated", "fake", "dummy", "test", "demo",
               "example", "synthetic", "placeholder")

HEDGES = ("may", "might", "could", "suggest", "appear", "possibl", "likely",
          "remains unclear", "debated", "contested", "有争议", "可能", "提示", "尚不明确")


@dataclass
class Result:
    blocks: list = field(default_factory=list)
    warns: list = field(default_factory=list)
    passes: list = field(default_factory=list)

    def block(self, gate, msg): self.blocks.append((gate, msg))
    def warn(self, gate, msg):  self.warns.append((gate, msg))
    def ok(self, gate):         self.passes.append(gate)

    def merge(self, o: "Result"):
        self.blocks += o.blocks; self.warns += o.warns; self.passes += o.passes
        return self

    @property
    def failed(self): return bool(self.blocks)

    def report(self):
        for g in self.passes:       print(f"  PASS  {g}")
        for g, m in self.warns:     print(f"  WARN  {g}: {m}")
        for g, m in self.blocks:    print(f"  BLOCK {g}: {m}")
        print()
        if self.failed:
            print(f"  ✗ {len(self.blocks)} 条 BLOCK —— 不许出稿。")
        else:
            print(f"  ✓ 全部通过（{len(self.warns)} 条 WARN）")


def _rows(path: Path):
    """读 CSV/XLSX 成 list[dict]，不依赖 pandas。"""
    if path.suffix.lower() in (".xlsx", ".xls"):
        import openpyxl
        wb = openpyxl.load_workbook(path, data_only=True)
        ws = wb.active
        it = ws.iter_rows(values_only=True)
        hdr = [str(h).strip() if h is not None else "" for h in next(it)]
        return [{h: ("" if v is None else v) for h, v in zip(hdr, r)} for r in it]
    import csv
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


# ══════════════════════════════════════════════════════════
# 1. CLAIM LEDGER —— 无台账不出句
# ══════════════════════════════════════════════════════════
def check_claims(claims_p: Path, evidence_p: Path | None,
                 manuscript_p: Path | None) -> Result:
    r = Result()
    claims = _rows(claims_p)
    if not claims:
        r.block("claims_nonempty", "台账为空")
        return r

    # claims_have_sources —— 每条断言必须有出处
    missing = [c["claim_id"] for c in claims if not str(c.get("source", "")).strip()]
    r.block("claims_have_sources", f"{len(missing)} 条断言没有 source: {missing[:5]}") \
        if missing else r.ok("claims_have_sources")

    # certainty_in_enum —— 受控词表，不许自由文本
    bad = [(c["claim_id"], c.get("certainty")) for c in claims
           if str(c.get("certainty", "")).strip() not in CERTAINTY]
    r.block("certainty_in_enum",
            f"{len(bad)} 条 certainty 不在词表 {sorted(CERTAINTY)}: {bad[:3]}") \
        if bad else r.ok("certainty_in_enum")

    # evidence_joinable —— 外键必须能 join，不能是自由文本
    if evidence_p and evidence_p.exists():
        ev_ids = {str(e.get("evidence_id", "")).strip() for e in _rows(evidence_p)}
        orphan = [(c["claim_id"], c.get("evidence_id")) for c in claims
                  if str(c.get("evidence_id", "")).strip() not in ev_ids]
        r.block("evidence_joinable",
                f"{len(orphan)} 条 evidence_id 在证据表里不存在: {orphan[:3]}") \
            if orphan else r.ok("evidence_joinable")

    # 正文交叉检查
    if manuscript_p and manuscript_p.exists():
        text = manuscript_p.read_text(encoding="utf-8")
        cited = set(re.findall(r"\[(C\d{3,})\]", text))
        ledger = {c["claim_id"] for c in claims}

        orphan_cit = sorted(cited - ledger)
        r.block("no_orphan_citation",
                f"正文引用了台账里没有的 claim: {orphan_cit[:5]}") \
            if orphan_cit else r.ok("no_orphan_citation")

        unused = sorted(cid for cid in ledger - cited
                        if str(next(c for c in claims if c["claim_id"] == cid)
                               .get("status", "")).strip().lower() != "dropped")
        r.block("no_unused_claim",
                f"台账里有断言没被正文使用，也没标 dropped: {unused[:5]}") \
            if unused else r.ok("no_unused_claim")

        # contested 的句子必须有让步语气（WARN —— 判断题，不硬拦）
        for c in claims:
            if str(c.get("certainty", "")).strip() != "contested":
                continue
            cid = c["claim_id"]
            for sent in re.split(r"(?<=[.。!?！？])\s*", text):
                if f"[{cid}]" in sent and not any(h in sent.lower() for h in HEDGES):
                    r.warn("contested_unflagged",
                           f"{cid} 是 contested，但正文句子没有让步语气: {sent.strip()[:60]}…")
                    break
    return r


# ══════════════════════════════════════════════════════════
# 2. DATA INTEGRITY —— 拿到数据先扫红旗，别靠模型碰巧发现
# ══════════════════════════════════════════════════════════
def check_data(path: Path) -> Result:
    """来源：Prostate cancer 线程。文件名里的 Mock + 320×191 零缺失。"""
    r = Result()

    # 文件名红旗
    stem = path.stem.lower()
    hits = [t for t in MOCK_TOKENS if re.search(rf"(?:^|[_\-. ]){t}", stem)]
    if hits:
        r.block("filename_not_mock",
                f"文件名含 {hits} —— 先确认这是真实采集数据还是模拟数据，再动手分析")
    else:
        r.ok("filename_not_mock")

    rows = _rows(path)
    if not rows:
        r.block("data_nonempty", "空文件")
        return r
    n, cols = len(rows), list(rows[0])

    # 零缺失红旗 —— 真实问卷/病历几乎不可能 0 缺失
    blanks = sum(1 for row in rows for c in cols
                 if str(row.get(c, "")).strip() in ("", "NA", "NaN", "None", "."))
    total = n * len(cols)
    rate = blanks / total if total else 0
    if rate == 0 and n >= 30 and len(cols) >= 10:
        r.block("missingness_plausible",
                f"{n}×{len(cols)} 零缺失。真实采集几乎不可能全满 —— "
                f"这是生成数据的典型指纹，先确认数据性质")
    else:
        r.ok("missingness_plausible")
        if 0 < rate < 0.001 and n >= 100:
            r.warn("missingness_plausible", f"缺失率仅 {rate:.4%}，偏低，留意")

    # 组间过度平衡 —— 真实随机化会有噪声
    grp_col = next((c for c in cols
                    if c.lower() in ("group", "arm", "组别", "分组", "treatment")), None)
    if grp_col:
        from collections import Counter
        cnt = Counter(str(row[grp_col]) for row in rows)
        if len(cnt) > 1 and len(set(cnt.values())) == 1 and n >= 60:
            r.warn("group_balance_plausible",
                   f"各组样本量完全相等 {dict(cnt)} —— 若非按设计强制等分，可疑")
    return r


# ══════════════════════════════════════════════════════════
# 3. NARRATIVE ADVANCE —— 每页只准推进一步
# ══════════════════════════════════════════════════════════
def check_narrative(matrix_p: Path) -> Result:
    """来源：你 4 条 PPT 线程。'slide 5 把 slide 6 的活提前干完了。'"""
    r = Result()
    rows = _rows(matrix_p)
    if not rows:
        r.block("matrix_nonempty", "冗余矩阵为空")
        return r

    def claims_of(row):
        return [c.strip().lower() for c in
                re.split(r"[;；|]", str(row.get("new_claims", ""))) if c.strip()]

    # 每页必须引入至少一条新断言
    empty = [row["slide"] for row in rows if not claims_of(row)]
    r.block("every_slide_advances",
            f"这些页引入不了任何新断言，不该存在: {empty}") \
        if empty else r.ok("every_slide_advances")

    # 同一断言不许在两页的「新断言」列出现
    seen, dup = {}, []
    for row in rows:
        for c in claims_of(row):
            if c in seen:
                dup.append((c, seen[c], row["slide"]))
            else:
                seen[c] = row["slide"]
    if dup:
        lines = "; ".join(
            f"「{c}」同时出现在 {a} 和 {b} —— 归属于第一次能讲透它的那一页，"
            f"另一页必须让出来" for c, a, b in dup[:3])
        r.block("no_duplicate_advance", lines)
    else:
        r.ok("no_duplicate_advance")
    return r


# ══════════════════════════════════════════════════════════
# 指纹 —— 改了台账没重新出稿，立刻看得见
# ══════════════════════════════════════════════════════════
def stamp(paths: list[Path], out: Path):
    prov = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()[:16]
            for p in paths if p and p.exists()}
    out.write_text(json.dumps(prov, indent=2, ensure_ascii=False), encoding="utf-8")
    return prov


def main():
    ap = argparse.ArgumentParser(prog="gates")
    sub = ap.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("claims");    c.add_argument("--claims", required=True)
    c.add_argument("--evidence");    c.add_argument("--manuscript")
    d = sub.add_parser("data");      d.add_argument("--file", required=True)
    n = sub.add_parser("narrative"); n.add_argument("--matrix", required=True)
    for p in (c, d, n):
        p.add_argument("--provenance", help="通过时把 sha256 指纹写到这里")

    a = ap.parse_args()
    P = lambda x: Path(x) if x else None

    print(f"\n═══ gate: {a.cmd} ═══")
    if a.cmd == "claims":
        res = check_claims(P(a.claims), P(a.evidence), P(a.manuscript))
        srcs = [P(a.claims), P(a.evidence), P(a.manuscript)]
    elif a.cmd == "data":
        res = check_data(P(a.file));      srcs = [P(a.file)]
    else:
        res = check_narrative(P(a.matrix)); srcs = [P(a.matrix)]

    res.report()
    if not res.failed and getattr(a, "provenance", None):
        pv = stamp(srcs, P(a.provenance))
        print(f"  指纹: {pv}")
    sys.exit(2 if res.failed else 0)


if __name__ == "__main__":
    main()

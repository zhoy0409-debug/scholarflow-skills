"""门禁的测试。重点不是「代码能跑」，是「坏内容真的会被拦下」。

每个 test 都对应一次真实翻车（见 ../../INSIGHTS.md）。
"""
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from gate_checks import check_claims, check_data, check_narrative, CERTAINTY, stamp

F = Path(__file__).resolve().parents[1] / "fixtures"


# ── claim ledger ────────────────────────────────────────
def test_clean_ledger_passes():
    r = check_claims(F / "claims_clean.csv", F / "evidence.csv", F / "draft_clean.md")
    assert not r.failed, r.blocks


def test_missing_source_blocks():
    r = check_claims(F / "claims_dirty.csv", F / "evidence.csv", F / "draft_dirty.md")
    assert "claims_have_sources" in [g for g, _ in r.blocks]


def test_free_text_certainty_blocks():
    """原线程的真实 bug：'candidate_supported_moderate_to_strong'。
    一旦允许自由文本，所有自动检查失效。"""
    r = check_claims(F / "claims_dirty.csv", F / "evidence.csv", F / "draft_dirty.md")
    assert "certainty_in_enum" in [g for g, _ in r.blocks]
    assert "candidate_supported_moderate_to_strong" not in CERTAINTY


def test_dangling_evidence_fk_blocks():
    r = check_claims(F / "claims_dirty.csv", F / "evidence.csv", F / "draft_dirty.md")
    assert "evidence_joinable" in [g for g, _ in r.blocks]


def test_orphan_citation_in_text_blocks():
    """正文写了 [C777]，台账里没有 —— 这就是「引了没列」。"""
    r = check_claims(F / "claims_dirty.csv", F / "evidence.csv", F / "draft_dirty.md")
    assert "no_orphan_citation" in [g for g, _ in r.blocks]


def test_unused_claim_blocks():
    """台账有 C005，正文没用，也没标 dropped —— 这就是「列了没引」。"""
    r = check_claims(F / "claims_dirty.csv", F / "evidence.csv", F / "draft_dirty.md")
    assert "no_unused_claim" in [g for g, _ in r.blocks]


def test_contested_without_hedge_warns_not_blocks():
    """判断题只 WARN，不硬拦 —— 门禁不该替作者做措辞决定。"""
    r = check_claims(F / "claims_dirty.csv", F / "evidence.csv", F / "draft_dirty.md")
    assert "contested_unflagged" in [g for g, _ in r.warns]
    assert "contested_unflagged" not in [g for g, _ in r.blocks]


# ── data integrity ──────────────────────────────────────
def test_mock_filename_blocks():
    """Prostate cancer 线程：PCa_Mock_Data_320_Final.csv"""
    r = check_data(F / "PCa_Mock_Data_320_Final.csv")
    assert "filename_not_mock" in [g for g, _ in r.blocks]


def test_zero_missingness_blocks():
    """320×191 零缺失 = 生成数据指纹。真实问卷不可能全满。"""
    r = check_data(F / "PCa_Mock_Data_320_Final.csv")
    assert "missingness_plausible" in [g for g, _ in r.blocks]


def test_real_cohort_passes():
    r = check_data(F / "cohort_real.csv")
    assert not r.failed, r.blocks


# ── narrative advance ───────────────────────────────────
def test_duplicate_advance_blocks():
    """PPT 线程：slide 5 把 slide 6 的活提前干完了。"""
    r = check_narrative(F / "slides_dirty.csv")
    msgs = dict(r.blocks)
    assert "no_duplicate_advance" in msgs
    assert "crab 定义" in msgs["no_duplicate_advance"]


def test_empty_slide_blocks():
    """一页引入不了任何新断言 → 它不该存在。"""
    r = check_narrative(F / "slides_dirty.csv")
    assert "every_slide_advances" in [g for g, _ in r.blocks]


def test_clean_deck_passes():
    r = check_narrative(F / "slides_clean.csv")
    assert not r.failed, r.blocks


# ── provenance ──────────────────────────────────────────
def test_provenance_changes_when_ledger_changes(tmp_path):
    """改了台账没重新出稿 → 指纹对不上 → 立刻看得见。"""
    out = tmp_path / "prov.json"
    a = stamp([F / "claims_clean.csv"], out)
    tweak = tmp_path / "claims.csv"
    tweak.write_text((F / "claims_clean.csv").read_text(encoding="utf-8") + "\n# edited",
                     encoding="utf-8")
    b = stamp([tweak], tmp_path / "prov2.json")
    assert list(a.values())[0] != list(b.values())[0]

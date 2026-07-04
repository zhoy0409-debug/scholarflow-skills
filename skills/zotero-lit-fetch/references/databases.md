# 各数据库抓取要点

针对某个库开工前先读它这一小节。每小节说明：怎么确认在这个库、条目怎么定位、Connector 翻译器抓什么、PDF 在哪、有没有标识符可用于 OA 补漏。

> 通用原则：**先让 Connector 翻译器干活**（元数据 + 受限 PDF），DOM 解析只用于枚举条目数量、核对、以及在翻译器失灵时抽取标识符做兜底。DOM 选择器会随站点改版变化，下面给的是方向性锚点，运行时以 `read_page` 实际看到的为准。

## 目录
- [知网 CNKI](#知网-cnki)
- [万方 Wanfang](#万方-wanfang)
- [维普 VIP](#维普-vip)
- [PubMed](#pubmed)
- [Web of Science](#web-of-science)
- [Google Scholar](#google-scholar)
- [Scopus](#scopus)
- [CrossRef / 出版商页面](#crossref--出版商页面)
- [bioRxiv / medRxiv / arXiv](#biorxiv--medrxiv--arxiv)

---

## 知网 CNKI
- **识别**：URL 含 `cnki.net`（如 `kns.cnki.net`）。
- **前提**：用户必须已登录（个人或机构 IP 授权），否则 PDF/CAJ 下不了。
- **条目定位**：结果列表在表格里，每行一条，标题链接、作者、来源、年份分列。
- **翻译器**：Zotero 有 CNKI translator，能识别列表页并弹出多条目选择浮层，抓题录 + 下载 **PDF（若该文有 PDF 版）**。部分老文献只有 CAJ 格式——CAJ 非 PDF，Connector 通常抓不到可读 PDF，这类要标 `needs-PDF`。
- **PDF 位置**：详情页有"PDF下载"和"CAJ下载"两个按钮；优先 PDF。
- **标识符**：多数无 DOI（尤其中文核心以外），OA 补漏基本无效——CNKI 内容不在 Unpaywall。所以 CNKI 的 PDF 几乎**只能**靠登录会话 + Connector 拿。
- **要点**：优先在"结果列表页"触发 Connector 批量抓；抓不到 PDF 的（仅 CAJ / 无全文）标 `needs-PDF`，不做 OA 补漏（无意义）。

## 万方 Wanfang
- **识别**：URL 含 `wanfangdata.com.cn`。
- **前提**：同 CNKI，需登录/授权。
- **条目定位**：结果为卡片/列表，每条含标题、作者、期刊、年。
- **翻译器**：有 Wanfang translator，支持列表页多选，抓题录 +（有授权时）PDF。
- **PDF 位置**：详情页"在线阅读/下载 PDF"。
- **标识符**：部分有 DOI；无 DOI 的走会话抓取，PDF 拿不到就标 `needs-PDF`。

## 维普 VIP
- **识别**：URL 含 `cqvip.com`。
- **翻译器**：覆盖不如知网/万方稳定。若翻译器抓不动：DOM 枚举条目 + 抽取题名/作者/刊/年，用 `zotero_save.py` 兜底建元数据；PDF 靠详情页登录下载，拿不到标 `needs-PDF`。

## PubMed
- **识别**：URL 含 `pubmed.ncbi.nlm.nih.gov`。
- **条目定位**：结果列表每条有 PMID、标题、作者、期刊；可勾选。
- **翻译器**：PubMed translator 非常成熟，列表页多选抓题录很稳。
- **PDF**：PubMed 本身不托管 PDF。**OA 补漏在这里最有效**：抽 PMID/DOI → `oa_pdf.py`（会查 PMC、Unpaywall）。很多生物医学文献在 PMC 有免费全文。
- **可选增强**：装了 bio-research 插件时，用 `mcp__plugin_bio-research_pubmed__get_full_text_article` / `convert_article_ids` 取 PMC 全文与 ID 互转。
- **流程建议**：Connector 抓题录 → 对每条用 PMID 走 OA 补 PDF。

## Web of Science
- **识别**：URL 含 `webofscience.com`。
- **前提**：机构订阅登录。
- **条目定位**：结果列表可勾选，每条有标题、作者、来源、被引。
- **翻译器**：有 WoS translator，支持列表多选抓题录。WoS 本身不放全文 PDF——PDF 在出版商。
- **PDF**：抽 DOI → 若机构对该出版商有订阅，最稳的是 Connector 在**出版商页面**再抓一次 PDF；否则走 `oa_pdf.py` 找 OA 版。拿不到标 `needs-PDF`。

## Google Scholar
- **识别**：URL 含 `scholar.google`。
- **条目定位**：每条结果有标题、右侧可能有 `[PDF]` 直链。
- **翻译器**：Scholar translator 支持列表多选抓题录（元数据质量一般，建议后续核对）。
- **PDF**：右侧 `[PDF]` 常指向 OA 直链，Connector 通常能一并抓；抓不到就抽 DOI 走 `oa_pdf.py`。

## Scopus
- **识别**：URL 含 `scopus.com`。需订阅登录。
- **翻译器**：有 Scopus translator，列表多选抓题录。PDF 同 WoS——在出版商，抽 DOI 后 Connector 出版商页再抓或 OA 补漏。

## CrossRef / 出版商页面
- 单篇文章的出版商页（ScienceDirect、Springer、Wiley、Nature、ACS、Frontiers、PLOS 等）：**这是拿受限 PDF 最直接的地方**。在文章页触发 Connector，翻译器会抓题录并在会话内下载 PDF（有订阅/OA 时）。
- 抽 DOI 后可用 CrossRef 补全/校验元数据；OA 判断交给 `oa_pdf.py`。

## bioRxiv / medRxiv / arXiv
- **识别**：`biorxiv.org` / `medrxiv.org` / `arxiv.org`。
- 全部开放获取，PDF 直链公开。Connector 抓题录 + PDF 都很稳；即便失败，`oa_pdf.py` 也能按 DOI/arXiv ID 直接拿 PDF。
- 装了 bio-research 插件时，可用 `mcp__plugin_bio-research_biorxiv__*` 增强检索/取元数据。

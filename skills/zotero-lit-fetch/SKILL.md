---
name: zotero-lit-fetch
description: >-
  全自动抓取中英文文献到 Zotero，优先获取 PDF，跨 Windows / macOS。当用户想把
  知网(CNKI)、万方(Wanfang)、维普(VIP)、PubMed、Web of Science、Google Scholar、
  Scopus、CrossRef、bioRxiv、Semantic Scholar 等数据库的检索结果或单篇文章导入 Zotero、
  批量抓取文献、抓取文献 PDF、把参考文献存进文献管理软件时使用。触发词包括：抓取文献、
  导入 Zotero、文献入库、批量抓文献、抓 PDF、把这些论文存到 Zotero、fetch literature、
  save to Zotero、grab papers with PDF、import search results to Zotero、
  scrape references。只要用户已在浏览器登录好有授权的数据库网页并希望把文献连同 PDF 存入
  Zotero，就应主动使用本技能，即使用户没有明确说"Zotero"或"skill"字样。
---

# Zotero 文献自动抓取 (zotero-lit-fetch)

把用户已登录的中英文数据库页面上的文献，连同 PDF，自动导入 Zotero。核心目标是**尽量拿到 PDF**，方便用户后续精读。

## 最重要的一条原理（先读这个）

**受限 PDF 只能在用户自己已登录的浏览器会话里拿到。** 知网、万方、维普这些中文库，以及很多被机构订阅的英文出版商，PDF 都在登录/授权后才可下载。Zotero 本机进程**没有**浏览器的登录 cookie，所以任何"把 URL 交给 Zotero 让它自己下载"的做法都会对受限 PDF 失败。

因此本技能的主引擎是**用户浏览器里已安装的 Zotero Connector 扩展**——它在页面上下文里跑翻译器(translator)，能带着登录 cookie 抓元数据 + 受限 PDF，这正是它被设计来做的事。开放获取(OA)的补漏才走 Unpaywall / PMC 这类无需 cookie 的通道。

不要试图用 `curl`/`requests`/Python 去抓这些数据库的 PDF——会因缺少会话而失败，且违反抓取规范。始终经由用户已登录的浏览器会话。

## 前置检查（每次开工先做，别跳过）

依次确认，任何一项缺失就先帮用户补齐再继续：

1. **Zotero 桌面端正在运行。** 用 `scripts/zotero_check.py` ping 本机连接器服务 `http://127.0.0.1:23119/connector/ping`。返回正常即在运行。没运行就请用户打开 Zotero 桌面端。
2. **浏览器装了 Zotero Connector 扩展。** 用户已确认装了；若抓取时看不到扩展图标/保存无反应，指引见 `references/setup.md`。
3. **用户已在目标数据库登录并停在检索结果页。** 例如知网的检索结果列表、PubMed 的 results 页。让用户把要抓的结果筛好、停在那一页。
4. **Claude in Chrome 已连接。** 本技能靠浏览器工具(`mcp__claude-in-chrome__*`)读取页面并操作。用 `tabs_context_mcp` 确认能看到用户当前标签页；看不到就请用户确认 Chrome 扩展已连接、当前标签页已授权。

## 跨平台差异（Windows / macOS）

功能一致，只有三处不同，操作时按当前系统取值：

- **修饰键**：Windows 用 `Ctrl`，macOS 用 `Cmd`。先用 bash `uname` 或看环境判断系统。
- **Zotero 存储/下载路径**：Windows `%USERPROFILE%\Zotero`，macOS `~/Zotero`。一般不用直接碰，PDF 由 Connector 存入 Zotero 存储；仅在需要落地临时文件时用得上。
- **连接器端口一致**：两平台都是 `127.0.0.1:23119`，脚本无需区分。

## 主流程

按下面顺序做。把整个任务建成 TaskList 跟踪进度。

### 1. 识别数据库与页面类型
读取当前页 URL 和结构，判断是哪个库、是"结果列表页"还是"单篇详情页"。每个库的 DOM 结构、条目定位、翻译器名称、PDF 位置见 `references/databases.md`——**开工前先读对应小节**。

### 2. 用 Zotero Connector 批量保存（主引擎，拿元数据 + 受限 PDF）
这是拿到受限 PDF 的关键步骤。

1. 触发 Connector 保存。两种方式，优先 a：
   - **(a) 点扩展工具栏按钮**：用浏览器的视觉/截图工具(`computer` / `screenshot`)定位并点击地址栏右侧的 Zotero Connector 图标。在**结果列表页**点它，Connector 会注入一个**页面内的多条目选择浮层(Select Items 对话框)**——这个浮层是嵌在页面 DOM 里的，可以用 `read_page`/`find` 读取、用 `computer`/`form_input` 勾选。
   - **(b) 若工具栏按钮点击不稳定**：直接请用户点一下 Zotero Connector 图标，然后你接手后续（选择浮层、校验、OA 补漏）。这种"人点一下、其余全自动"的降级是完全可以接受的，别硬卡在点按钮上。
2. 在选择浮层里**全选**要抓的条目（或按用户指定筛选），确认保存。
3. 等待保存完成。Connector 会把元数据写入 Zotero，并**在浏览器会话里下载受限 PDF** 作为附件——这是 `curl`/连接器 POST 都做不到的。
4. 若某个库没有可用翻译器、Connector 抓不动（少见），退到第 3 步的兜底：抽取标识符走连接器服务 POST + OA 补 PDF。

详细的连接器交互、`saveItems` 载荷格式、必需请求头（重要：`zotero-allowed-request: 1`）见 `references/zotero-connector.md`。

### 3. 兜底入库（仅当 Connector 抓不动某些条目时）
当翻译器缺失或个别条目没进 Zotero 时，用 `scripts/zotero_save.py` 把抽取到的元数据 POST 到 `http://127.0.0.1:23119/connector/saveItems` 直接建条目。注意这条路**只可靠地建元数据**，受限 PDF 仍需第 2 步的浏览器会话。

### 4. PDF 校验与开放获取补漏（尽力再找 OA 版）
用户要求：抓不到 PDF 时，先尽力找开放获取版，再存元数据并打标记。

1. **校验**：确认第 2 步后哪些条目已带 PDF 附件。可用 `scripts/zotero_check.py` 查最近条目，或直接在 Zotero 里看。
2. **补漏**：对没有 PDF 的条目，抽取 DOI / PMID，用 `scripts/oa_pdf.py`（Unpaywall + PMC + arXiv/bioRxiv）解析开放 PDF：
   - 有 OA PDF：这类 URL **无需 cookie**，可让 Zotero 自己下载——把 `url_for_pdf` 作为 attachment 一并 POST（用法见 `references/zotero-connector.md`），或先落地再手动附加。
   - 若装了 bio-research 插件，PubMed 条目也可用 `mcp__plugin_bio-research_pubmed__get_full_text_article` 取 PMC 全文作为补充。
3. **标记**：仍然没有任何 PDF 的条目，给它打标签 `needs-PDF`，方便用户后续人工补。绝不因为没 PDF 就丢掉条目。

### 5. 汇总报告
简洁报告：共处理 N 条 → 成功入库 N 条 → 带 PDF N 条（其中受限库 PDF X、OA 补漏 Y）→ 标 `needs-PDF` N 条。列出没拿到 PDF 的条目标题，供用户决定是否手动跟进。

## 稳健性与礼节

- **分批**：结果页很多条时分批保存（如每批 20 条），避免 Connector 超时或触发数据库限流。
- **限流**：批次之间稍等；OA 查询用 `scripts/oa_pdf.py` 内置的节流，别猛发。
- **登录态**：中途若发现掉登录（页面跳登录框），停下来请用户重新登录，别继续空抓。
- **只在授权范围内**：只抓用户自己已登录、有权访问的内容；这是用户手动登录授权页面这一前提的意义所在。不要绕过付费墙或规避访问控制。
- **去重**：Zotero 自带重复检测；大批量后可提示用户在 Zotero 里查重合并。

## 参考文件

- `references/databases.md` — 各库(知网/万方/维普/PubMed/WoS/Scholar/Scopus/CrossRef/bioRxiv)的页面结构、条目定位、翻译器与 PDF 位置。**每次针对某个库开工前先读对应小节。**
- `references/zotero-connector.md` — 连接器 HTTP 服务端点、`saveItems` 载荷与附件字段、必需请求头、错误排查。
- `references/setup.md` — Windows / macOS 上 Zotero 桌面端 + Connector 扩展的安装与一次性配置、常见故障。

## 脚本

- `scripts/zotero_check.py` — ping 连接器服务、查 Zotero 是否运行、列出最近条目用于校验。
- `scripts/zotero_save.py` — 把元数据(可含 OA PDF 附件)POST 到 `saveItems` 建条目（兜底/补漏用）。
- `scripts/oa_pdf.py` — 按 DOI/PMID 走 Unpaywall + PMC + arXiv 解析开放获取 PDF 链接。

脚本用法：先 `--help`。运行环境需要 Python 3；`oa_pdf.py` 用标准库即可（`urllib`），无需额外安装。

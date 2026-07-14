# 前置检查 —— 依赖外部环境的 skill，第一步就验，别做到一半才发现

> 来源：「Cross-platform literature scraping skill」线程。
> zotero-lit-fetch 假定 Claude in Chrome 扩展已连接，一路做下去，
> 到真正要抓 PDF 时才发现扩展没连——整个会话的规划全部作废。

## 规则

任何依赖**外部状态**的 skill，SKILL.md 的第一步必须是 preflight，且：

1. **一次性检完所有依赖**，不要一个一个试
2. 失败时给**可执行的修复清单**，不是「请检查你的配置」
3. 给**降级路径**：外部依赖不可用时，能做什么？

（`nature-academic-search` 已经有 `scripts/preflight.py` —— 这是对的，其余 skill 照抄。）

## 各 skill 的依赖清单

| skill | 必须先验 | 降级路径 |
|---|---|---|
| zotero-lit-fetch | Claude in Chrome 扩展**已连接**（≠ Zotero Connector 已装）；Zotero 桌面端在跑；目标集合已选中；数据库已登录/VPN 通 | 给用户一份逐篇手动捕获清单 |
| nature-academic-search | PubMed/CrossRef/arXiv MCP 可达；API key（若需） | 降级到 WebSearch |
| nature-figure | Python 还是 R（**必须先问，不能猜**）；matplotlib/ggplot2 可用；字体可用 | 换后端 |
| nature-paper2ppt | python-pptx；源论文的图能不能取到（PDF 里抠图 vs 只有文字） | 只有文字时明确告诉用户「图我拿不到」 |
| latex-writer-micro | tex 发行版可用；期刊 cls 文件在不在 | 输出 .tex 让用户本地编译 |

## zotero-lit-fetch 的额外坑（已踩过，写死在 skill 里）

中文数据库（CNKI/万方/维普）的 PDF 走的是 Connector 抓取，
**它会新建一条带 PDF 的条目，无法直接挂到你已有的纯题录条目上**。
所以正确顺序是：

1. 先在 Zotero 里选好目标集合
2. 抓取（会产生重复条目）
3. Zotero → 重复条目 → 合并（合并会保留 PDF 和原有标签）

这一段必须写进 SKILL.md，否则每个用户都要自己撞一次。

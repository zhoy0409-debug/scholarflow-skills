# 一次性安装与配置（Windows / macOS）

用户若已装好 Zotero 桌面端 + 浏览器 Connector 扩展，可跳过本页，只在排障时回看。

## 1. Zotero 桌面端
- 下载：<https://www.zotero.org/download/>。Windows 和 macOS 各有安装包，装法与普通软件一致。
- 装好后**保持打开**——本机连接器服务(端口 23119)只在 Zotero 运行时可用。
- 登录 Zotero 账号可选（用于云同步），不影响本机抓取。

## 2. 浏览器 Zotero Connector 扩展
- 下载：<https://www.zotero.org/download/connectors>。支持 Chrome / Edge / Firefox / Safari。
- 本技能配合 **Claude in Chrome** 使用，建议装在 Chrome/Edge。
- 装好后地址栏右侧会出现 Zotero 图标（会随当前页面类型变成文章/文件夹/网页图标）。把它固定(pin)到工具栏，方便定位点击。

## 3. 关键设置
- Zotero → 设置(Preferences) → 高级(Advanced)：如需其它程序访问本机 API，可勾选 "Allow other applications on this computer to communicate with Zotero"。**批量抓取的核心连接器功能默认即可用，通常无需改这项。**
- Connector 设置里可设"保存后自动附加 PDF/快照"，保持默认(抓 PDF)即可。
- 想让条目直接进某个分类：抓取前在 Zotero 里点选目标分类(collection)。

## 4. Claude in Chrome
- 确保 Claude 的 Chrome 扩展已连接、当前标签页已授权，本技能才能读取页面、操作页面内的 Zotero 选择浮层。

## 常见故障
- **点了 Connector 没反应 / "Is Zotero running?"**：Zotero 桌面端没开，或刚开还没就绪。打开并等几秒。参考 <https://www.zotero.org/support/kb/connector_zotero_unavailable>。
- **图标不出现**：扩展被禁用或没 pin。到浏览器扩展管理里启用并固定。
- **中文库抓不到 PDF**：多半没登录/无授权，或该文只有 CAJ 无 PDF。先确认登录态；只有 CAJ 的标 `needs-PDF`。
- **列表页不弹多选浮层**：可能停在了详情页而非结果列表页，或该库翻译器不支持列表多选。回到检索结果列表页重试，或逐篇在详情页抓。
- **端口 23119 无响应**：防火墙拦截或端口被改。确认 Zotero 在运行；企业环境可能需放行本地回环端口。

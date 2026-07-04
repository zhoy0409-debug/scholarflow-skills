# Zotero 连接器 HTTP 服务

Zotero 桌面端运行时会在本机开一个 HTTP 服务，端口 **23119**，供浏览器里的 Zotero Connector 扩展通信。我们可以用它 (1) 判断 Zotero 是否在运行，(2) 在翻译器抓不动时兜底直接建条目。

> 关键理解：这个本机服务由 **Zotero 进程**处理请求。它**没有**浏览器的登录 cookie。所以经它下载的附件 URL 必须是**公开可访问**的（如 OA PDF）；受限库(知网/万方/订阅出版商)的 PDF 必须由**浏览器里的 Connector 扩展**在会话内下载，走不了这条 POST。

## 必需请求头（否则 403）

本机服务对 `User-Agent` 以 `Mozilla/` 开头的请求有防护（防 DNS rebinding）。程序化请求必须带下面任一头，否则返回 403：

```
zotero-allowed-request: 1
```

建议同时带上：

```
Content-Type: application/json
X-Zotero-Connector-API-Version: 3
```

脚本 `scripts/zotero_save.py` / `zotero_check.py` 已内置这些头。

## 端点

- `GET /connector/ping` — 探活。Zotero 在运行则返回 200。用来做前置检查。
- `POST /connector/saveItems` — 直接建条目（兜底/OA 补漏用）。
- `POST /connector/getSelectedCollection` — 查当前选中的分类(collection)，可用于把条目存到用户当前分类。
- 翻译器相关端点由扩展内部使用，我们不直接调。

## `saveItems` 载荷

Body 为 JSON，核心是 `items` 数组，每个 item 用 Zotero item 格式（不是 CSL-JSON）。最小可用例子：

```json
{
  "items": [
    {
      "itemType": "journalArticle",
      "title": "文章标题",
      "creators": [
        {"creatorType": "author", "firstName": "San", "lastName": "Zhang"}
      ],
      "publicationTitle": "期刊名",
      "date": "2024",
      "DOI": "10.xxxx/xxxxx",
      "tags": [{"tag": "needs-PDF"}],
      "attachments": []
    }
  ]
}
```

常用 `itemType`：`journalArticle`、`conferencePaper`、`preprint`、`thesis`、`book`、`bookSection`。

### 附加 OA PDF（无需 cookie 的公开 PDF）

在该 item 的 `attachments` 里加一条，Zotero 会自己下载：

```json
"attachments": [
  {
    "title": "Full Text PDF",
    "mimeType": "application/pdf",
    "url": "https://example.org/oa/paper.pdf"
  }
]
```

只对**公开可下载**的 URL 有效（Unpaywall `url_for_pdf`、PMC、arXiv 等）。受限库 PDF 别放这里——会因缺 cookie 失败。

### 存到用户当前分类
默认存到 Zotero 的 "My Library" 根。若想进当前选中分类，先 `getSelectedCollection` 拿到 collection，再在请求里带上会话/分类信息；多数情况下让用户在 Zotero 里选好目标分类，条目建好后拖动即可，不必强求。

## 响应与去重
- 成功返回 200 及所建条目信息。
- Zotero 有内置重复检测，重复条目不会自动合并，但会在"重复条目"里列出，提醒用户批量后查重。

## 错误排查
- **403**：缺 `zotero-allowed-request: 1` 头。加上重试。
- **连接被拒 / ping 失败**：Zotero 桌面端没开，或被防火墙拦。请用户打开 Zotero。
- **端口占用/改端口**：极少数用户改过端口；若 23119 无响应，请用户在 Zotero 设置→高级里确认。
- **附件没下下来**：多半是该 URL 非公开（受限）。改用浏览器 Connector 会话抓，或标 `needs-PDF`。

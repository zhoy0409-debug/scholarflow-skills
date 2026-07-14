# 从 65 个历史线程里挖出来的东西

你让我看看过往对话里有什么值得吸收的。结论比我预期的重：

**你在别的线程里临时搭出来的东西，比 ScholarFlow 里任何一个 skill 都严格。**
但它们只活在那一个线程里，会话一结束就没了。ScholarFlow 的真正问题不是「description 写得不好」——
那只是表层。真正的问题是：**它是一堆 prompt 包装，而不是一套带门禁的工具。**

下面七条，每一条都来自一个真实翻车/真实救场，不是我想出来的。

---

## 1. Evidence gate：内容级门禁 ★ 最有价值

**来源**：`Literature review synthesis workflow`

你在那条线程里搭了个综述引擎，有这些东西：

- stage gate，`advance` 会因为**内容**不合格而退出码 2（`BLOCK: claims_have_sources`）
- evidence matrix 有 `evidence_id` 外键，**能 join**
- `certainty` 是**受控枚举**，不是自由文本
- 产物带 sha256 指纹

引擎当时还抓到一个自己身上的 bug：`claim_register.status` 里出现了
`candidate_supported_moderate_to_strong` 这种自由文本值——**一旦允许自由文本，
任何自动检查都失效**。所以拆成 enum + note 两列。

**ScholarFlow 现在一条这样的门禁都没有。** nature-writing 是「先写句子，再找引用」——
这个顺序天然产生无源之句。反过来才对：**先立台账，再由台账生成句子。没有台账行的断言，写不出来。**

→ 已落成 `shared/core/claim-ledger.md`

---

## 2. 学术诚信门禁：不能靠模型碰巧发现

**来源**：`Prostate cancer manuscript rejection`

那次是靠模型**碰巧**注意到：文件名叫 `PCa_Mock_Data_320_Final_Ready.csv`，
而且 320 人 × 191 变量**零缺失**——真实问卷不可能零缺失。于是停下来问你数据性质。

**「碰巧」不是门禁。** 换个模型、换个上下文长度，就漏了。

→ 已落成 `shared/core/integrity-gates.md`：拿到任何数据文件先扫红旗清单
（文件名含 mock/sim/test、零缺失、样本量恰好命中 power 下限、组间过度平衡……）

---

## 3. 原始实验数据 QC：检验选对了，输入是假的，毫无意义

**来源**：`Q-PCR results evaluation`

外包公司报「约 2 倍上调」。但原始 Ct 里：**目的基因根本没前移**，
而 GAPDH 内参在过表达组整体**晚了 1.5 个 Ct**。
那 2 倍完全是内参漂移校正出来的——**是假的**。

外加靶标搞错了：`Fkn for mouse.gb` 实际是 `Cx3cr1`（受体），项目要的是 `Cx3cl1`（配体）。

`stats-sanity-amr` 现在是从「选哪个检验」开始的。**这个起点太晚了。**

→ 已落成 `integrity-gates.md` 的「结果自洽红旗」；`stats-sanity` 加 Step 0

---

## 4. 叙事推进审计：四条 PPT 线程反复栽在同一个坑

**来源**：`Thesis progress presentation optimization` ×3、`补骨脂甲素进展汇报优化`、
`CRAB thesis progress presentation`

痛点从来不是「PPT 不好看」，是**每一页都把整个故事从头讲一遍**。

原话：
> "slide 5 把 slide 6 的活提前干完了，所以 slide 6 看着像重复。
>  错的不是 slide 6，是 slide 5 越界。"

这个判断很反直觉但它是对的：**冲突时，断言归属于第一次能把它讲透的那一页，
前面的页必须让出来。**

`nature-paper2ppt` 会查文字溢出、查图片质量、查模板感——**唯独不查这个**，
而这才是真正会让汇报垮掉的东西。

→ 已落成 `shared/core/narrative-advance.md`：出稿后强制填冗余矩阵，BLOCK 级

---

## 5. AI 配图会在答辩现场炸掉

**来源**：同上 PPT 线程

slide 上有张 AI 图，把 *A. baumannii* 画成 soil·water 里的 "NATURAL DECOMPOSER"。
这个说法在学界**有争议**——答辩现场会被问死。另一张是「怪兽细菌砸盾牌」，
专业读者会觉得 kitsch。

判据很好用：**如果有人指着这张图问「有文献支持吗」，你答不上来 → 这张图不该在。**

还有个现实分工要写清，省得每次重新讨论：
写实插画（ICU/电镜/器官）模型生成不了，走 CC0 图源或用户自备；
**矢量图标、机制示意图、数据图模型自己画**——无版权/AI 争议，这是主力。

→ 已落成 `shared/core/visual-honesty.md`

---

## 6. Preflight：做到一半才发现依赖没连，整个规划作废

**来源**：`Cross-platform literature scraping skill`

`zotero-lit-fetch` 假定 Claude in Chrome 扩展已连接，一路规划下去，
到真要抓 PDF 时才发现**扩展没连**（用户装的是 Zotero Connector，两回事）。

还踩出一个必须写死的坑：中文数据库的 PDF 走 Connector 抓取时，
**会新建一条带 PDF 的条目，无法挂到你已有的纯题录条目上**。
正确顺序是：先选好集合 → 抓取（产生重复）→ Zotero 合并重复项（合并保留 PDF 和标签）。

→ 已落成 `shared/core/preflight.md`

---

## 7. 出图 QA 环：「代码跑通」≠「图做好了」

**来源**：你上传的 Codex 版 `polish-sci-figures` + `Figure formatting adjustments` 线程

那个 Codex skill **整体不该采用**——它的 description 是 700+ 字符的关键词堆砌
（`论文配图/科研作图/结果可视化/组图/图件优化/重绘/拼版/统一配色`），
正是我们刚治好的那个病，照搬会和 nature-figure、paper2ppt 直接对撞；
而且是 192 行单体，无渐进披露、无 manifest。

**但它有四样东西是被真实踩坑打磨出来的**，值得整段吸收：

1. **「Do not equate successful code execution with a finished figure.」**
   matplotlib 不会因为标签被裁掉而报错。**必须真的把 PNG 打开看一眼**，
   必须按最终插入尺寸看，必须把图嵌进真实 DOCX/PPT 再渲染一遍。
2. **Release blockers 清单** —— panel 标号偏离网格、文字被裁、纯位图被说成「可编辑」……
3. **可编辑性诚信** —— "Never claim that wrapping a PNG inside SVG makes the underlying
   image elements editable." 这种规则只有被烧过才写得出来。
4. **反「满屏柱状图」** —— 按结论类型选图形形式的对照表。

一处**不采纳**：它把 biomedical figure 的默认字体定为 Times New Roman。这是错的——
绝大多数期刊要求图内文字**无衬线**。你自己在 `Figure formatting adjustments` 那条线程里，
最后也是统一成 Arial 的。

→ 已落成 `shared/core/figure-qa.md`

---

## 一条元观察

你的这些 skill 目前的形态是：**一段很长的 prompt + 一堆 reference**。
它们告诉模型「应该怎么做」，但**没有任何东西在检查模型到底做没做**。

上面七条的共同点：全都是**门禁**，不是**指导**。

```
指导：「出图后请检查对齐」          → 模型会说「已检查」然后交一张歪的
门禁：「BLOCK: panel 标号偏离网格」  → 不过就是不过
```

ScholarFlow 从「能用」到「真正好用」，差的就是这一步：
**把 SHOULD 变成 BLOCK。**

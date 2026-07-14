# 架构：三层分流

## 问题

230 个 skill 里，学术写作那 100 个是**三套互相不知道对方存在的并行系统**：

- `nature-*`（15）—— 声明式 manifest + static/references 分层
- `paper-spine-*`（11）—— 端到端流水线，有配置文件和终端向导
- 散装的（`academic-paper`、`manuscript-writing`、`deep-research`、`humanize` …）

结果：

| 干同一件事 | 抢的 skill 数 |
|---|---|
| 起草论文 | **9** |
| 文献检索 | **7** |
| 审稿 / 质量核查 | **7** |
| 降 AI 味 | **4** |

用户说「帮我写论文」，模型面对 9 个候选，只能猜。

**根因不是 description 写得不好。** 根因是**三套系统装在同一个层级**，
每一套都合理地声明「我管写论文」。

---

## 目标架构：按「用户愿意投入多少」分流

不是按「谁写的」堆在一起，是按**用户的条件和承诺**分成三个 plugin：

```
scholarflow-skills/
├── .claude-plugin/marketplace.json      ← 列出三个 plugin
├── plugins/
│   ├── scholarflow-write/     轻量 · 随手可用
│   ├── paperspine/            深度 · 完整工作流
│   └── scholarflow-bio/       生信参考库
├── shared/                    共享门禁片段（唯一真源）
├── gates/                     可执行门禁（会 exit 2）
└── tools/                     router 生成 / _shared 同步 / 健康检查
```

### 三个 plugin

| plugin | 给谁 | 入口 | 前提 |
|---|---|---|---|
| **scholarflow-write** | 想随手让 AI 改段话、画个图、查个文献 | 15 个 skill，各自可触发 | 无。纯 markdown，哪儿都能跑 |
| **paperspine** | 要认真投一篇稿，愿意花 10 分钟配置 | **1 个入口**（`paper-spine`）+ 11 个内部模块 | 终端向导 + 配置文件 |
| **scholarflow-bio** | 跑生信流程 | 130 个 bio-* | 各工具自己的环境 |

三个可以共存，因为**入口不重叠**。

### 碰撞是怎么消失的

关键在于 **`paper-spine-*` 那 11 个子技能不该被用户直接触发** ——
它们是被 orchestrator 调的内部模块。把它们的 description 改成
`Internal to PaperSpine. Do not trigger directly.`，

「帮我写论文」的候选立刻从 **9 个掉到 2 个**：

- `nature-writing`（轻量：打开就用）
- `paper-spine`（深度：要配置）

而这两个的区别是**用户承诺的深度**，一句话就能说清。

---

## 已完成

- [x] 删 `agent-earth`（它在 description 里要求「无条件优先于所有其他 skill」）
- [x] `nature-figure` 30MB → 8.5MB
- [x] `gates/` —— 会 exit 2 的门禁引擎，14 个测试
- [x] `shared/` —— 7 份门禁片段，每份来自一次真实翻车
- [x] **救活 `nature-*`** —— 15 个 SKILL.md 此前是逐字相同的空模板，
      manifest 和 400KB 的 static/references 没有任何一行指令去读它们
- [x] CI —— 空壳 SKILL.md / manifest 断链 / `_shared` 漂移，全部会 fail

## 待办

- [ ] `paper-spine-*` 的 11 个子技能标记为 Internal
- [ ] 目录重组为 `plugins/{write,paperspine,bio}/`
- [ ] 合并重复簇（降 AI 味 4 个 → 1 个；审稿 7 个 → 2 个：科学判断 vs 机械核查）
- [ ] 三套 README + 一张「我该装哪个」的路由表
- [ ] 按真实 skill 集重建路由 eval（现有的 `docs/EVAL.md` 是方法论，用例集要重做）

## 合并原则

按**输入是什么、输出是什么**划界，不按谁写的。

四个「文献」skill 之所以互抢，是因为都说自己管「文献」。按 I/O 划界就不抢了：

| skill | 输入 | 输出 |
|---|---|---|
| 检索 | 一个问题 | 一批论文 |
| 补引用 | 一段没引用的文字 | 同一段文字 + 引用 |
| 入库 | 已找到的结果 | 本地文献库条目 |
| 核验 | 一条引用 | 真伪判定 |

**科学判断 ≠ 机械核查。** 这两类必须分开：
- 「这篇创新性够吗」→ 审稿模拟
- 「摘要里的数字和表 2 对得上吗」→ 一致性核查

## 一条元原则

skill 的正文是「一段很长的 prompt」：它告诉模型该怎么做，
但**没有任何东西检查模型到底做没做**。

```
指导：「出图后请检查对齐」          → 模型会说「已检查」然后交一张歪的
门禁：「BLOCK: panel 标号偏离网格」  → 不过就是不过
```

从「能用」到「真正好用」，差的就是 **把 SHOULD 变成 BLOCK**。

# 两层 eval —— 以及一个诚实的结果

## 为什么要两层

| | 关键词 eval | LLM eval |
|---|---|---|
| 测什么 | description 之间**有没有抢词** | 真实路由器**会不会选对** |
| 确定性 | 是（可进 CI，每次 push 跑） | 否（有方差，贵） |
| 天花板 | ~80%（裸 prompt 无信号） | 无 |
| 何时跑 | 每次改 description | 改大版本时 |

**两个都要。** 关键词 eval 当护栏，LLM eval 当验收。

---

## 结果

### 关键词 eval（46 例，确定性）

| | 改前 | 改后 |
|---|---|---|
| top1_accuracy | 45.2 % | **83.3 %** |
| contamination（抢到明确禁止的 skill） | 41.3 % | **10.9 %** |
| none_leak（非学术 prompt 被误抢） | 75.0 % | **50.0 %** |

### LLM 判分（46 例，独立 subagent 盲判）

| | 改前 | 改后 |
|---|---|---|
| accuracy | 87.0 % | **100 %** |
| hard_fail | 13.0 % | **0 %** |
| hard 档（骑在两个 skill 边界上） | 12/17 | **17/17** |

---

## 第一个诚实的发现：关键词 eval 夸大了问题

LLM 判分下，**旧版 description 就已经有 87%**。
一个真实的路由器会**读懂**一段写得啰嗦的描述，不像关键词打分那样被共享词淹死。

所以「45%」不是真实的路由质量，它是**描述碰撞的严重程度**。

那真正修好的是什么？

- **hard 档 12/17 → 17/17**。骑在边界上的那些请求（写 vs 润色、查 vs 补引用、审 vs 回审）
  才是旧描述真正会翻车的地方，而这些恰恰是高频请求。
- **hard_fail 13% → 0%**。「抢到明确禁止的 skill」清零。

---

## 第二个诚实的发现：100% 是个红旗

设计集上 100%——但**测试集和 description 是同一个人在同一个会话里写的**。
这是标准的出题人偏差。

所以又做了一个**留出集**：20 条 prompt **全部取自 zhoy 的真实历史线程**
（会话标题和原话，比如「这是 chatgpt 做的 slide6，你觉得对吗」、
「这样说有 ai 味道吗」、「补骨脂甲素的进展汇报帮我优化一下」）。
写 description 的时候我没看过这些。

**留出集第一次跑：85%（17/20）。不是 100%。那 15 分的差距就是过拟合。**

而且三条失败全是真问题，不是噪声：

| 真实 prompt | 期望 | 判成 | 根因 |
|---|---|---|---|
| 「这是 chatgpt 做的 slide6，你觉得做得对吗」 | nature-paper2ppt | `__none__` | description 只写了「论文→deck」，**没声明「审已有的 deck」** |
| 「补骨脂甲素的进展汇报帮我优化一下」 | nature-paper2ppt | `__none__` | 同上 |
| 「qPCR 报告说上调 2 倍，但原始 Ct 不对劲」 | stats-sanity | manuscript-integrity-check | manifest 里加了 Step 0 原始数据 QC，**但 description 一个字没提** |

前两条尤其打脸：**「审已有的 PPT」是 zhoy 历史上最高频的用法（5 条线程），
而 skill 从来没声明过自己会做这件事。** 一个只测「我想象中的用法」的测试集，
永远发现不了这个。

修完这两处 → **留出集 100%（20/20）**。

---

## 结论

- 留出集必须来自**真实用户语料**，不能来自作者的想象。
- 设计集上的 100% 什么也不说明；留出集上的 85% → 100% 才说明修对了。
- 每次给 skill 加能力（比如 stats 的 Step 0），**必须同步改 description**。
  能力和广告不一致 = 这个能力等于不存在。

## 复现

```bash
# 关键词（CI 每次跑）
python3 evals/routing/run_eval.py --skills $REPO/skills --desc new_descriptions.yaml --compare

# LLM 判分（改大版本时跑；判官必须盲判）
python3 evals/llm/score_llm.py --generate
claude -p "$(cat evals/llm/prompt_holdout_v2.txt)" > evals/llm/result_holdout_v2.json
python3 evals/llm/score_llm.py
```

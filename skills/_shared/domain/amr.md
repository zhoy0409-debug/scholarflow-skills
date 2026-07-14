# Domain 轴：AMR / 微生物基因组学

> 这个文件的存在，是为了让 `cite-verify-amr`、`stats-sanity-amr`、
> `sci-figure-ppt-amr`、`grant-survey-amr`、`latex-writer-micro` 这些
> **按领域切分**的 skill 消失。
>
> 领域不是技能。「给 AMR 论文画图」和「给论文画图」是同一个技能，
> 只是加载的领域片段不同。按领域复制一整套 skill，只会制造触发词碰撞。

manifest 里加一个轴：

```yaml
axes:
  domain:
    detect: 从用户文本里检出病原体名/耐药基因/MIC/WGS 等词
    values:
      generic: null                    # 默认，不加载
      amr:     _shared/domain/amr.md
```

## 术语与写法

- 菌名首次全称 + 斜体（*Acinetobacter baumannii*），此后 *A. baumannii*
- CRAB / CRE / CRPA / MRSA：首次给出定义（CRAB = carbapenem-resistant *A. baumannii*）
- 耐药基因斜体小写（*bla*<sub>OXA-23</sub>、*mcr-1*），蛋白正体大写（OXA-23）
- 折点必须写清标准和版本：CLSI M100-Ed34 / EUCAST v14.0。**不写版本的折点等于没写**
- MIC 单位 mg/L（EUCAST）或 µg/mL（CLSI），全文统一，别混

## 统计上的领域特异陷阱

- **MIC 是序数、离散、右删失的**（">64" 不是 65）。
  → 不能算均值。用 MIC50/MIC90、几何均数需谨慎、比较用非参数或区间删失模型
- **耐药率比较**：分母是「做了药敏的分离株数」还是「所有分离株数」？必须写清
- **同一病人多株分离株不独立**。要么去重（每人保留首株），要么用混合效应模型
- **WGS 的系统发育不独立**：克隆传播会把关联做出来。基因型-表型关联必须做群体结构校正
- 小样本耐药率比较（各组 < 5）→ Fisher，不是卡方
- 多重比较：药物 × 菌种的两两比较很容易做出假阳性，必须校正

## 图表

- 耐药率趋势：折线 + 95%CI，标注每年的分母 n
- 基因存在/缺失：二值热图，行=分离株、列=基因，配 core-genome 树左对齐
- MIC 分布：堆叠柱（按 MIC 折点分色），标注 S/I/R 折点线和标准版本
- 系统发育树：标注 bootstrap/aLRT，注明建树方法和模型
- 质粒图：标注 replicon type、耐药基因、IS 元件

## 报告规范

- 分离株来源、时间跨度、医院/科室、去重规则 —— 缺一不可
- 测序：平台、深度、组装工具+版本、分型工具+数据库版本（**数据库版本尤其容易漏**）
- 上传 NCBI：BioProject + BioSample + SRA 三个号都要给

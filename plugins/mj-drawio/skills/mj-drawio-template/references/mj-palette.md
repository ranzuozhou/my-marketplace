# mj-system 配色规范

> 单独抽出的配色速查。完整 XML 生成规范见 `../../mj-drawio-create/references/xml-reference.md`。

## DDD 六层架构配色

| 层级 | fillColor | strokeColor | 语义 |
|---|---|---|---|
| Interface | `#D4E1F5` | `#6C8EBF` | 接入层:Controller / API / CLI 入口 |
| Application | `#D5E8D4` | `#82B366` | 应用服务:编排用例,不含业务规则 |
| Domain | `#FFE6CC` | `#D79B00` | **领域模型**:聚合 / 实体 / 值对象 / 领域服务(核心) |
| Infrastructure | `#F8CECC` | `#B85450` | 基础设施:Repository 实现 / 外部集成 / 消息 |
| Shared | `#E1D5E7` | `#9673A6` | 共享内核:DTO / Utils / 跨层类型 |
| Config | `#DAE8FC` | `#6C8EBF` | 配置 / 依赖注入 / 启动装配 |

**惯例**:
- 每层用 **圆角矩形** `rounded=1;whiteSpace=wrap;html=1;` + 上述配色
- 层名加粗显示在上方(`fontStyle=1`)
- 模块名列在层内下方

## 数仓分层配色(ODS / DWD / DWS)

| 层 | fillColor | strokeColor | 语义 |
|---|---|---|---|
| ODS | `#CCE5FF` | `#6C8EBF` | 贴源层 — 原始数据,仅做类型规整 |
| DWD | `#D5E8D4` | `#82B366` | 明细层 — 清洗后的最细粒度事实表 |
| DWS | `#FFE6CC` | `#D79B00` | 汇总层 — 按业务主题聚合的宽表 |

**惯例**:
- 表节点用 **圆柱** `shape=cylinder3;...` + 对应层颜色
- 层划分用竖条分隔(无色背景矩形 + 深色左边界)

## ETL 流程图元

| 图元 | 样式关键字 | 用途 |
|---|---|---|
| 源表 / 目标表 | `shape=cylinder3;fillColor=<ODS/DWD/DWS 色>` | 数据库表 |
| PL/pgSQL 函数 | `shape=process;fillColor=#FFF2CC;strokeColor=#D6B656` | ETL 函数节点(浅黄) |
| dblink 调用 | edge `strokeDasharray=3 3;strokeColor=#999999` | 虚线表示跨库 |
| Advisory Lock | 小矩形 `fillColor=#F5F5F5` + value 含 `🔒 advisory_lock(xxx)` | 锁标记 |
| Priority Queue | `shape=mxgraph.flowchart.sequential_data;fillColor=#E1D5E7` | LPT 队列 |
| 触发源(如 Kafka / cron) | `shape=mxgraph.flowchart.manual_input;fillColor=#F5F5F5` | 上游触发 |

## ER 图图元

| 图元 | 样式 | 用途 |
|---|---|---|
| 表实体 | `shape=mxgraph.er.entity;fillColor=#FFFFFF;strokeColor=#333333` | 矩形表头 + 列列表 |
| 主键列 | 列文字前加 **PK** | 主键标识 |
| 外键列 | 列文字前加 **FK** | 外键标识 |
| 1:N 关系 | edge `startArrow=ERone;endArrow=ERmany` | 一对多 |
| N:M 关系 | edge `startArrow=ERmany;endArrow=ERmany` | 多对多 |

## 通用排版

| 元素 | 取值 |
|---|---|
| 标题字号 | `fontSize=16;fontStyle=1`(加粗) |
| 正文字号 | `fontSize=12` |
| 层间距 | 水平 80,垂直 60 |
| 节点最小宽度 | 160 |
| 节点最小高度 | 60 |
| 画布尺寸 | `pageWidth="1169" pageHeight="826"`(A4 横版) |

## 扩展建议

新增模板时,**优先复用上述配色**,不要自创新色(除非领域明确有区分需求)。扩展指引:

1. 需要新层/新角色 → 先检查是否能映射到现有 DDD 或数仓层,映射到则复用配色
2. 确需新色 → 从 drawio 默认调色盘选,避免与现有六色碰撞,记录到本文件
3. **绿色优先给"正向/成功"语义,红色优先给"错误/风险"语义**

# drawio XML 生成参考

> **来源**: 基于 [jgraph/drawio-mcp](https://github.com/jgraph/drawio-mcp) 的 shared/xml-reference 本地化,追加 mj-system 专用样式扩展。
>
> **同步策略**: 每季度检查一次上游变更,或在 validate-xml 频繁失败时重新校对。

## 最小合法文档结构

```xml
<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net">
  <diagram name="Page-1" id="page1">
    <mxGraphModel dx="1422" dy="798" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="826" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <!-- 图元 cells 从这里开始,parent 引用 "1" -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

**硬性规则**:
1. `id="0"` 和 `id="1"` 两个根 cell 必须存在
2. 所有业务图元的 `parent` 属性指向 `"1"`
3. 属性里的 `&`、`<`、`>` 必须转义为 `&amp;`、`&lt;`、`&gt;`
4. XML 注释不能含 `--`

## 节点 cell(vertex)

```xml
<mxCell id="node-1" value="Node Label" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#D4E1F5;strokeColor=#6C8EBF;"
        vertex="1" parent="1">
  <mxGeometry x="40" y="40" width="160" height="80" as="geometry" />
</mxCell>
```

| 属性 | 说明 |
|---|---|
| `id` | 唯一标识 |
| `value` | 显示文字(可含 HTML,需转义) |
| `style` | 分号分隔的 `key=value` 样式串 |
| `vertex="1"` | 标记为节点 |
| `parent="1"` | 固定为 `1`(根图层) |
| `mxGeometry x/y/width/height` | 坐标和尺寸(像素) |
| `mxGeometry as="geometry"` | 必填 |

## 连线 cell(edge)

```xml
<mxCell id="edge-1" value="" style="endArrow=classic;html=1;rounded=0;"
        edge="1" parent="1" source="node-1" target="node-2">
  <mxGeometry relative="1" as="geometry" />
</mxCell>
```

| 属性 | 说明 |
|---|---|
| `edge="1"` | 标记为连线 |
| `source` / `target` | 引用节点 id |
| `mxGeometry relative="1" as="geometry"` | **必填**,否则导出空白 |

**常见 edge 样式**:

| 样式片段 | 效果 |
|---|---|
| `endArrow=classic` | 经典箭头 |
| `endArrow=none` | 无箭头(双向) |
| `dashed=1` | 虚线 |
| `strokeDasharray=3 3` | 自定义虚线 |
| `curved=1` | 曲线 |

## 常用 vertex 样式

| 形状 | style 关键字 |
|---|---|
| 圆角矩形 | `rounded=1;whiteSpace=wrap;html=1;` |
| 椭圆 | `ellipse;whiteSpace=wrap;html=1;` |
| 菱形(决策) | `rhombus;whiteSpace=wrap;html=1;` |
| 六边形 | `shape=hexagon;whiteSpace=wrap;html=1;` |
| 圆柱(数据库) | `shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;` |
| 人形(actor) | `shape=umlActor;whiteSpace=wrap;html=1;` |
| 进程(ETL 函数) | `shape=process;whiteSpace=wrap;html=1;` |
| 顺序数据 | `shape=mxgraph.flowchart.sequential_data;whiteSpace=wrap;html=1;` |

## 颜色属性

| key | 说明 | 示例 |
|---|---|---|
| `fillColor` | 填充色 | `#D4E1F5` |
| `strokeColor` | 边框色 | `#6C8EBF` |
| `fontColor` | 文字色 | `#000000` |
| `fontSize` | 文字大小 | `14` |
| `fontStyle` | 1=加粗 2=斜体 4=下划线 | `1` |

---

## mj-system 专用样式扩展

### DDD 六层配色

| 层级 | fillColor | strokeColor | 语义 |
|---|---|---|---|
| Interface | `#D4E1F5` | `#6C8EBF` | 接入层(Controller / API) |
| Application | `#D5E8D4` | `#82B366` | 应用服务 |
| Domain | `#FFE6CC` | `#D79B00` | 领域模型(核心) |
| Infrastructure | `#F8CECC` | `#B85450` | 基础设施(Repo / 外部集成) |
| Shared | `#E1D5E7` | `#9673A6` | 共享内核 |
| Config | `#DAE8FC` | `#6C8EBF` | 配置 / 依赖注入 |

### 数仓分层配色

| 层 | fillColor | strokeColor | 语义 |
|---|---|---|---|
| ODS | `#CCE5FF` | `#6C8EBF` | 贴源层(浅蓝) |
| DWD | `#D5E8D4` | `#82B366` | 明细层(浅绿) |
| DWS | `#FFE6CC` | `#D79B00` | 汇总层(浅橙) |

统一用 `shape=rectangle;rounded=1;` + 上述配色。层名用加粗标题,表名列在下方。

### ETL 节点约定

| 图元 | 样式片段 | 用途 |
|---|---|---|
| 源表 / 目标表 | `shape=cylinder3;fillColor=<ODS/DWD/DWS 色>` | 数据库表 |
| 函数节点 | `shape=process;fillColor=#FFF2CC;strokeColor=#D6B656` | PL/pgSQL 函数(浅黄) |
| dblink 调用 | edge + `strokeDasharray=3 3` | 虚线表示跨库 |
| Advisory Lock | `value="🔒 advisory_lock"` + 小矩形,浅灰 `#F5F5F5` | 锁标记 |
| Priority Queue | `shape=mxgraph.flowchart.sequential_data` | LPT 队列 |

### 图元命名惯例

- 表节点 value:`<schema>.<table>`(如 `ods.orders`)
- 函数节点 value:`<schema>.<function>()`(如 `dwd.clean_orders()`)
- edge value:数据流动作(`insert` / `upsert` / `merge`)

---

## 坐标布局建议

- 画布标准尺寸: `pageWidth="1169" pageHeight="826"`(A4 横版)
- 节点最小宽度: 160
- 节点最小高度: 60
- 水平间距: 80
- 垂直间距: 60
- 从 `(40, 40)` 开始,逐行堆叠

## 转义速查

| 原字符 | 在 XML 属性里写 |
|---|---|
| `&` | `&amp;` |
| `<` | `&lt;` |
| `>` | `&gt;` |
| `"` | `&quot;` |
| `'` | `&apos;` |

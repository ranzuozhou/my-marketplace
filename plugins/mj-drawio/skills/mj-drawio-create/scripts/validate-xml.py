#!/usr/bin/env python3
"""drawio XML 预校验脚本。

检查项:
1. XML well-formedness(ET.parse 通过)
2. 根 cell 完整: 必须有 id="0" 和 id="1"
3. 每条 edge 必须有 <mxGeometry>,且属性 relative="1" as="geometry"

用法:
    python validate-xml.py <path-to-.drawio>

退出码:
    0 = OK
    1 = FAIL(stdout 打印诊断)
"""
from __future__ import annotations

import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def validate(path: Path) -> int:
    try:
        tree = ET.parse(path)
    except ET.ParseError as e:
        print(f"FAIL: XML parse error: {e}")
        return 1
    except FileNotFoundError:
        print(f"FAIL: file not found: {path}")
        return 1

    root = tree.getroot()
    cells = list(root.iter("mxCell"))
    cell_ids = {c.get("id") for c in cells}

    if "0" not in cell_ids or "1" not in cell_ids:
        print("FAIL: 缺少根 cell (id=0 或 id=1)")
        return 1

    edges = [c for c in cells if c.get("edge") == "1"]
    for edge in edges:
        geom = edge.find("mxGeometry")
        eid = edge.get("id")
        if geom is None:
            print(f"FAIL: edge id={eid} 缺少 <mxGeometry>")
            return 1
        if geom.get("relative") != "1" or geom.get("as") != "geometry":
            print(f"FAIL: edge id={eid} 的 mxGeometry 属性不全 (需 relative='1' as='geometry')")
            return 1

    print(f"OK: {len(cells)} cells, {len(edges)} edges, 全部 geometry 完整")
    return 0


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python validate-xml.py <path-to-.drawio>")
        return 1
    return validate(Path(sys.argv[1]))


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 读取文件
with open('wangzhe_report/index_with_tabs.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 打印 411-416 行的精确内容（包括缩进）
print("=== 411-416 行的精确内容 ===")
for i in range(410, min(416, len(lines))):
    line = lines[i]
    # 显示原始字符串和长度
    print(f"行{i+1} (len={len(line)}): {repr(line)}")

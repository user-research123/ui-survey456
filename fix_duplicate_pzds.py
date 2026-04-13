#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复HTML文件中重复的盼之卡片
"""

html_file = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/index_with_tabs.html'

with open(html_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 找到并删除第479-484行的旧盼之卡片（"暂无新动态"部分）
# 行号从1开始，所以索引是478-483
print(f"总行数: {len(lines)}")
print(f"第479行内容: {lines[478].strip()}")
print(f"第480行内容: {lines[479].strip()}")
print(f"第481行内容: {lines[480].strip()}")
print(f"第482行内容: {lines[481].strip()}")
print(f"第483行内容: {lines[482].strip()}")
print(f"第484行内容: {lines[483].strip()}")

# 删除第479-484行（索引478-483，共6行）
# 这包括：空行、div开始、竞品二标题、h3标题、p暂无新动态、div结束、空行
del lines[478:485]  # 删除索引478到484（不包括485），共7行

with open(html_file, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("已删除重复的旧盼之卡片")
print(f"剩余行数: {len(lines)}")

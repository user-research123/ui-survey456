#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修复竞品动态追踪板块的 4 月 7 日按钮文本"""

file_path = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/index_with_tabs.html'

# 读取文件行
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 查找并修复第 439 行（索引 438）
fixed = False
for i, line in enumerate(lines):
    if "showCompetitorDate('04-07')" in line and "4 月 8 日" in line:
        print(f"✓ 在第 {i+1} 行找到需要修复的按钮")
        print(f"  原内容：{line.strip()}")
        # 替换文本
        lines[i] = line.replace("4 月 8 日", "4 月 7 日")
        print(f"  新内容：{lines[i].strip()}")
        fixed = True
        break

if fixed:
    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print("\n✓ 成功修复按钮文本")
else:
    print("✗ 未找到需要修复的按钮")
    # 显示第 438-440 行的内容
    print("\n第 438-440 行内容:")
    for i in range(437, min(441, len(lines))):
        print(f"  {i+1}: {lines[i][:100]}")

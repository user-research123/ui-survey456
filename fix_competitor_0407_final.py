#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修复竞品动态追踪板块的 4 月 7 日按钮文本"""

file_path = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/index_with_tabs.html'

# 读取所有行
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 找到第 439 行（索引 438）并修改
target_line_idx = 438  # 第 439 行（0-based）
if target_line_idx < len(lines):
    line = lines[target_line_idx]
    if "showCompetitorDate('04-07')" in line:
        print(f"✓ 确认第 {target_line_idx + 1} 行是 4 月 7 日按钮")
        print(f"  修改前：{line.strip()}")
        
        # 直接替换
        lines[target_line_idx] = line.replace("4 月 8 日", "4 月 7 日")
        print(f"  修改后：{lines[target_line_idx].strip()}")
        
        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        
        print("\n✓ 成功修复！")
    else:
        print(f"✗ 第 {target_line_idx + 1} 行不是预期的按钮")
        print(f"  内容：{line[:100]}")
else:
    print(f"✗ 文件行数不足，总行数：{len(lines)}")

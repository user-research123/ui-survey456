#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修复竞品动态追踪板块的 4 月 7 日按钮文本"""

file_path = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/index_with_tabs.html'

# 读取文件行
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 查找并修复包含 showCompetitorDate('04-07') 的行
fixed = False
for i, line in enumerate(lines):
    if "showCompetitorDate('04-07')" in line:
        print(f"✓ 在第 {i+1} 行找到 4 月 7 日按钮")
        print(f"  原始内容（repr）: {repr(line[:150])}")
        
        # 使用正则表达式替换日期文本
        import re
        # 匹配">4 月 X 日</button>"其中 X=8 但应该是 7
        old_line = line
        new_line = re.sub(r'(showCompetitorDate\(\'04-07\'\)">)4 月 [0-9] 日 (</button>)', r'\g<1>4 月 7 日\g<2>', line)
        
        if old_line != new_line:
            lines[i] = new_line
            print(f"  修改后内容：{new_line.strip()}")
            fixed = True
        else:
            print(f"  未修改，当前文本：{line.strip()}")
        break

if fixed:
    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print("\n✓ 成功修复按钮文本")
else:
    print("\n✗ 未能修复按钮文本")

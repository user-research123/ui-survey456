#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
精确修复第 1379 行
"""

file_path = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/index_with_tabs.html'

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 修复第 1379 行（索引 1378）
if '                                <!-- 4 月 8 日内容 --> class="user-feedback-date-content">' in lines[1378]:
    lines[1378] = '                <!-- 4 月 8 日内容 -->\n'
    lines.insert(1379, '                <div id="user-feedback-04-08" class="user-feedback-date-content">\n')
    print("✅ 已修复第 1379 行")
else:
    print(f"❌ 第 1379 行内容不匹配：{lines[1378]}")

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("✅ 修复完成！")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复用户需求追踪板块的日期切换问题 - v3
使用精确的字符串替换
"""

file_path = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/index_with_tabs.html'

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 找到并修复第 1379 行（索引 1378）
for i in range(len(lines)):
    if '                                <!-- 4 月 8 日内容 --> class="user-feedback-date-content">' in lines[i]:
        # 替换为正确的 HTML 标签
        lines[i] = '                <!-- 4 月 8 日内容 -->\n                <div id="user-feedback-04-08" class="user-feedback-date-content">\n'
        print(f"✅ 已修复第 {i+1} 行")
        break

# 确保 4 月 9 日有 active 类，其他没有
for i in range(len(lines)):
    if 'id="user-feedback-04-09"' in lines[i] and 'class="user-feedback-date-content"' in lines[i]:
        if ' active>' not in lines[i]:
            lines[i] = lines[i].replace('class="user-feedback-date-content">', 'class="user-feedback-date-content active">')
            print(f"✅ 已为 4 月 9 日添加 active 类（第 {i+1} 行）")
    
    # 移除其他日期的 active 类
    if 'user-feedback-04-' in lines[i] and 'class="user-feedback-date-content active"' in lines[i] and 'user-feedback-04-09' not in lines[i]:
        lines[i] = lines[i].replace('class="user-feedback-date-content active"', 'class="user-feedback-date-content"')
        print(f"✅ 已移除第 {i+1} 行的 active 类")

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("\n✅ 用户需求追踪板块修复完成 (v3)！")

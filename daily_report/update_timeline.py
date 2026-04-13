#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将游戏官方事件部分改为时间线布局
"""

# 读取文件
with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 找到要替换的行（251-258行，索引250-257）
# 新的时间线布局内容
new_lines = [
    '<!-- 游戏官方事件/活动 -->\n',
    '           <div class="section">\n',
    '<h2 class="section-title">1、游戏官方事件/活动</h2>\n',
    '                \n',
    '<div class="timeline">\n',
    '<div class="timeline-item">\n',
    '                      <div class="timeline-date">3月30日</div>\n',
    '<div class="timeline-content">\n',
    '<p style="margin: 0; color: #4a5568;">10:00正式开放昵称抢注；云游戏版本开放限时体验</p>\n',
    '                        </div>\n',
    '                   </div>\n',
    '                </div>\n',
    '            </div>\n',
]

# 替换第251-258行（索引250-257）
new_content = lines[:250] + new_lines + lines[258:]

# 写回文件
with open('index.html', 'w', encoding='utf-8') as f:
    f.writelines(new_content)

print("✓ 成功将游戏官方事件部分改为时间线布局")
print(f"原文件行数: {len(lines)}")
print(f"新文件行数: {len(new_content)}")

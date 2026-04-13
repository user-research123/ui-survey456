#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复用户需求追踪板块的日期切换问题
"""

import re

file_path = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/index_with_tabs.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 修复 4 月 8 日的损坏标签并移除 active 类
content = re.sub(
    r'<!-- 4 月 8 日内容 -->\s*class="user-feedback-date-content active">',
    '<!-- 4 月 8 日内容 -->\n                <div id="user-feedback-04-08" class="user-feedback-date-content">',
    content
)

# 2. 确保 4 月 9 日是唯一有 active 类的区块
# 先移除所有 user-feedback-date-content 的 active 类
content = re.sub(
    r'class="user-feedback-date-content active"',
    'class="user-feedback-date-content"',
    content
)

# 然后给 4 月 9 日添加 active 类（如果它存在）
content = re.sub(
    r'(<div id="user-feedback-04-09" class="user-feedback-date-content")>',
    r'\1 active>',
    content
)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ 用户需求追踪板块修复完成！")
print("- 已修复 4 月 8 日的 HTML 标签")
print("- 已移除所有区块的 active 类")
print("- 已为 4 月 9 日添加 active 类")

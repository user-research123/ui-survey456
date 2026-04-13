#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复用户需求追踪板块的日期切换问题 - v2
"""

file_path = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/index_with_tabs.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 修复 4 月 8 日的损坏标签
old_text = '                                <!-- 4 月 8 日内容 --> class="user-feedback-date-content">'
new_text = '                <!-- 4 月 8 日内容 -->\n                <div id="user-feedback-04-08" class="user-feedback-date-content">'

content = content.replace(old_text, new_text)

# 确保 4 月 9 日有正确的 active 类
old_0409 = '<div id="user-feedback-04-09" class="user-feedback-date-content" active>'
new_0409 = '<div id="user-feedback-04-09" class="user-feedback-date-content active">'

content = content.replace(old_0409, new_0409)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ 用户需求追踪板块修复完成 (v2)！")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
精确修复第 1379 行 - v2
"""

file_path = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/index_with_tabs.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 使用精确的字符串替换
old_text = '                                <!-- 4 月 8 日内容 --> class="user-feedback-date-content">'
new_text = '                <!-- 4 月 8 日内容 -->\n                <div id="user-feedback-04-08" class="user-feedback-date-content">'

if old_text in content:
    content = content.replace(old_text, new_text)
    print("✅ 已修复 4 月 8 日的 HTML 标签")
else:
    print("❌ 未找到匹配的文本")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ 修复完成！")

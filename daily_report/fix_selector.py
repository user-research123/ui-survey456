#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复用户需求追踪板块的JavaScript选择器问题
问题: .section:nth-of-type(3) 选择的是"竞品动态追踪"(第3个section),而不是"用户需求追踪"(第4个section)
解决方案: 
1. 给"用户需求追踪"的section添加唯一ID
2. 修改JavaScript函数使用ID选择器
"""

import re

file_path = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/daily_report/index_with_tabs.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 步骤1: 给"用户需求追踪"的section添加唯一ID
# 查找: <!-- 用户需求追踪（带日期切换） -->\n            <div class="section">
# 替换为: <!-- 用户需求追踪（带日期切换） -->\n            <div class="section" id="user-feedback-section">

old_section_start = '<!-- 用户需求追踪（带日期切换） -->\n            <div class="section">'
new_section_start = '<!-- 用户需求追踪（带日期切换） -->\n            <div class="section" id="user-feedback-section">'

if old_section_start in content:
    content = content.replace(old_section_start, new_section_start)
    print("✓ 已为用户需求追踪section添加ID: user-feedback-section")
else:
    print("✗ 未找到目标section标签")
    exit(1)

# 步骤2: 修改JavaScript函数中的选择器
# 将 document.querySelectorAll('.section:nth-of-type(3) .date-content')
# 改为 document.querySelectorAll('#user-feedback-section .date-content')

old_js_contents = "document.querySelectorAll('.section:nth-of-type(3) .date-content')"
new_js_contents = "document.querySelectorAll('#user-feedback-section .date-content')"

if old_js_contents in content:
    content = content.replace(old_js_contents, new_js_contents)
    print("✓ 已更新contents选择器")
else:
    print("⚠ 未找到旧的contents选择器")

old_js_tabs = "document.querySelectorAll('.section:nth-of-type(3) .date-tab')"
new_js_tabs = "document.querySelectorAll('#user-feedback-section .date-tab')"

if old_js_tabs in content:
    content = content.replace(old_js_tabs, new_js_tabs)
    print("✓ 已更新tabs选择器")
else:
    print("⚠ 未找到旧的tabs选择器")

# 写回文件
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("\n✓ 修复完成!")
print(f"文件路径: {file_path}")

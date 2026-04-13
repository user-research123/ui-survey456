#!/usr/bin/env python3
"""
调整紫色背景为更浅的色调，并优化标题颜色对比度
"""

import re

file_path = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/index_premium_apple.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 修改背景渐变为更浅的紫色调
old_bg = "background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);"
new_bg = "background: linear-gradient(135deg, #c3cfe2 0%, #d4a5ff 50%, #e8d5f5 100%);"
content = content.replace(old_bg, new_bg)

# 2. 修改头部渐变背景为更浅的紫色
old_header = "background: linear-gradient(135deg, rgba(102, 126, 234, 0.7) 0%, rgba(118, 75, 162, 0.7) 100%);"
new_header = "background: linear-gradient(135deg, rgba(195, 207, 226, 0.8) 0%, rgba(212, 165, 255, 0.8) 100%);"
content = content.replace(old_header, new_header)

# 3. 修改标题颜色为深色（提高对比度）
old_title_gradient = """        .section-title {
            font-size: 28px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;"""

new_title_gradient = """        .section-title {
            font-size: 28px;
            color: #2d3748;
            background: none;
            -webkit-text-fill-color: initial;"""

content = content.replace(old_title_gradient, new_title_gradient)

# 4. 修改副标题和竞品名称颜色为深色
content = content.replace(
    "color: #667eea;",
    "color: #4a5568;"
).replace(
    "background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);",
    "color: #2d3748;"
)

# 5. 修改日期标签背景为更浅的紫色
content = content.replace(
    "background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);",
    "background: linear-gradient(135deg, #f3e8ff 0%, #e9d5ff 100%);"
)

# 6. 修改边框颜色为更柔和的紫色
content = content.replace(
    "border-left: 5px solid #667eea;",
    "border-left: 5px solid #c3cfe2;"
).replace(
    "border-bottom: 3px solid #667eea;",
    "border-bottom: 3px solid #c3cfe2;"
)

# 7. 修改按钮激活态背景
content = content.replace(
    "background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);",
    "background: linear-gradient(135deg, #c3cfe2 0%, #d4a5ff 100%);"
)

# 8. 修改图表相关颜色
content = content.replace(
    "'#667eea'",
    "'#a78bfa'"
).replace(
    "'#764ba2'",
    "'#c4b5fd'"
)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ 背景已调整为浅紫色调，标题颜色已优化为深色以提高对比度")
print("   - 背景：淡紫渐变 (#c3cfe2 → #d4a5ff → #e8d5f5)")
print("   - 标题：深灰蓝色 (#2d3748)，清晰可读")
print("   - 所有紫色元素均已调浅，保持整体协调")

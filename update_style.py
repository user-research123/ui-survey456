#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将 index_duotone.html 的 CSS 样式应用到 index_with_tabs.html
保持所有 HTML 结构和内容不变,只替换 <style>...</style> 部分
"""

import os

# 文件路径
duotone_file = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/index_duotone.html'
target_file = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report_repo/index_with_tabs.html'

# 读取参考文件
with open(duotone_file, 'r', encoding='utf-8') as f:
    duotone_content = f.read()

# 提取 reference 文件的 style 部分 (从 <style> 到 </style>)
style_start = duotone_content.find('<style>')
style_end = duotone_content.find('</style>') + len('</style>')
new_style = duotone_content[style_start:style_end]

print(f"提取到新样式长度: {len(new_style)} 字符")

# 读取目标文件
with open(target_file, 'r', encoding='utf-8') as f:
    target_content = f.read()

# 找到目标文件的 style 部分
old_style_start = target_content.find('<style>')
old_style_end = target_content.find('</style>') + len('</style>')

if old_style_start == -1 or old_style_end == -1:
    print("错误: 未找到 style 标签")
    exit(1)

print(f"旧样式范围: {old_style_start} - {old_style_end}")
print(f"旧样式长度: {old_style_end - old_style_start} 字符")

# 替换样式
new_content = target_content[:old_style_start] + new_style + target_content[old_style_end:]

# 写回文件
with open(target_file, 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"✓ 样式替换完成!")
print(f"  原文件大小: {len(target_content)} 字符")
print(f"  新文件大小: {len(new_content)} 字符")
print(f"  差异: {len(new_content) - len(target_content)} 字符")

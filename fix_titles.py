#!/usr/bin/env python3
import re

file_path = 'index_with_tabs.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 替换所有竞品标题
replacements = [
    ('竞品一：螃蟹', '竞品：螃蟹'),
    ('竞品二：盼之', '竞品：盼之'),
    ('竞品三：闲鱼', '竞品：闲鱼'),
]

for old, new in replacements:
    content = content.replace(old, new)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ 标题修改完成")

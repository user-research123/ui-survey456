#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复 index_with_tabs.html 中的 rawData 数组格式问题
"""

import re

target_file = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/index_with_tabs.html'

with open(target_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 使用正则表达式修复
# 查找 const rawData = [\n[ 并替换为 const rawData = [\npattern = r'(const rawData = \[)\n\[(\s+\{"time": "2026-04-03 00 点 00 分")'
replacement = r'\1\2'

new_content, count = re.subn(pattern, replacement, content)

if count > 0:
    print(f"✓ 已修复 {count} 处多余的左方括号")
    
    # 写入修复后的内容
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("✓ 文件已更新")
else:
    print("✗ 未找到匹配的模式")

print("\n修复完成！")

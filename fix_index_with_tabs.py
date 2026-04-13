#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复index_with_tabs.html文件中4月1日闲鱼部分的HTML结构
"""

# 读取文件
file_path = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report_temp/index_with_tabs.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 修复多余的div标签
# 将 "<div class=\"competitor-card\">\n                                                                    <div class=\"competitor-card\">" 
# 替换为 "<div class=\"competitor-card\">"
content = content.replace(
    '<div class="competitor-card">\n                                                                    <div class="competitor-card">',
    '<div class="competitor-card">'
)

# 修复末尾多余的</div>标签
# 找到闲鱼部分,移除多余的</div>
import re

# 匹配闲鱼部分的完整结构
pattern = r'(<div class="competitor-card">.*?<div class="competitor-name">竞品三：闲鱼</div>.*?</ul>\s*</div>)\s*</div>'

def fix_extra_div(match):
    return match.group(1)

# 只修复第一次出现(即4月1日的部分)
new_content = re.sub(pattern, fix_extra_div, content, count=1, flags=re.DOTALL)

# 写入文件
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("成功修复index_with_tabs.html文件中4月1日闲鱼部分的HTML结构")

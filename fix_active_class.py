#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复用户需求追踪板块的active类问题
确保只有一个日期内容区块带有active类
"""

import re

html_file = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/index_with_tabs.html'

with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 查找所有user-feedback-date-content的区块
pattern = r'<div id="user-feedback-(\d{2}-\d{2})" class="user-feedback-date-content active">'
matches = list(re.finditer(pattern, content))

print(f"找到 {len(matches)} 个带有active类的user-feedback-date-content区块:")
for match in matches:
    date_id = match.group(1)
    print(f"  - user-feedback-{date_id} (位置: {match.start()})")

if len(matches) > 1:
    # 保留第一个（最新的日期），移除其他的active类
    for i, match in enumerate(matches):
        if i == 0:
            print(f"\n保留第一个区块 (user-feedback-{matches[0].group(1)}) 的active类")
        else:
            date_id = match.group(1)
            old_text = match.group(0)
            new_text = f'<div id="user-feedback-{date_id}" class="user-feedback-date-content">'
            content = content.replace(old_text, new_text, 1)
            print(f"移除 user-feedback-{date_id} 的active类")
    
    # 写回文件
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("\n修复完成！")
else:
    print("\n只有一个active类，无需修复")

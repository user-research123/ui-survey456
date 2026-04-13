#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复HTML文件中重复的user-feedback-04-03区块
"""

import re

html_path = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/index_with_tabs.html'

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 查找所有user-feedback-04-03区块
pattern = r'(<div id="user-feedback-04-03" class="user-feedback-date-content active">.*?</div>\s*</div>\s*</div>\s*</div>)'
matches = list(re.finditer(pattern, content, re.DOTALL))

print(f"找到 {len(matches)} 个 user-feedback-04-03 区块")

if len(matches) > 1:
    # 删除第二个及之后的重复区块
    # 从后往前删除，避免索引偏移
    for i in range(len(matches) - 1, 0, -1):
        start = matches[i].start()
        end = matches[i].end()
        print(f"删除第 {i+1} 个区块 (位置: {start}-{end})")
        content = content[:start] + content[end:]
    
    # 写入修复后的内容
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("修复完成！已删除重复区块。")
else:
    print("未找到重复区块，无需修复。")

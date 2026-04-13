#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清理HTML文件中多余的注释和标签
"""

html_path = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/index_with_tabs.html'

with open(html_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 找到并删除多余的行（第901-905行，索引从0开始是900-904）
# 但需要先确认这些行的内容
for i in range(895, 910):
    if i < len(lines):
        print(f"行 {i+1}: {lines[i].rstrip()}")

# 删除第901-905行（索引900-904）
# 这些行是：
# 901: <!-- 4月3日内容 -->
# 902: 空行
# 903: <!-- 4月3日内容 -->
# 904: 空行  
# 905: </div>

del lines[900:905]

# 写入清理后的内容
with open(html_path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("清理完成！")

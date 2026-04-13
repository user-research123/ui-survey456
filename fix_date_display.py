#!/usr/bin/env python3
# -*- coding: utf-8 -*-

html_file = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/index_with_tabs.html'

# 读取 HTML 文件
with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 替换错误的日期显示
content = content.replace('D 月 08 日总结', '04 月 08 日总结')

# 保存修改后的 HTML 文件
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("日期显示已修复！")

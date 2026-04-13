#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修复竞品动态追踪板块的 4 月 7 日按钮文本"""

import re

file_path = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/index_with_tabs.html'

# 读取文件
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 查找并替换错误的按钮文本
# 匹配：onclick="showCompetitorDate('04-07')">4 月 8 日</button>
# 替换为：onclick="showCompetitorDate('04-07')">4 月 7 日</button>
old_pattern = r'''(onclick="showCompetitorDate\('04-07'\)">)4 月 8 日 (</button>)'''
new_text = r'\g<1>4 月 7 日\g<2>'

# 执行替换
new_content, count = re.subn(old_pattern, new_text, content)

if count > 0:
    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"✓ 成功修复 {count} 处错误")
    print("  将 '04-07' 按钮的文本从 '4 月 8 日' 改为 '4 月 7 日'")
else:
    print("✗ 未找到需要修复的按钮")
    # 显示找到的相关内容以便调试
    matches = re.findall(r'onclick="showCompetitorDate\(\'04-07\'\)"[^>]*>[^<]*</button>', content)
    if matches:
        print(f"找到以下匹配的按钮：{matches}")

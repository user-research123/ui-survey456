#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修复竞品动态追踪板块的 4 月 7 日按钮文本"""

file_path = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/index_with_tabs.html'

# 读取文件
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 直接字符串替换
old_text = '''onclick="showCompetitorDate('04-07')">4 月 8 日</button>'''
new_text = '''onclick="showCompetitorDate('04-07')">4 月 7 日</button>'''

if old_text in content:
    new_content = content.replace(old_text, new_text)
    
    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("✓ 成功修复按钮文本")
    print(f"  原内容：{old_text}")
    print(f"  新内容：{new_text}")
else:
    print("✗ 未找到需要修复的按钮文本")
    # 尝试查找相关内容
    import re
    matches = re.findall(r'showCompetitorDate\([^)]*\)[^>]*>[^<]*月 [^<]*日</button>', content)
    print(f"找到的相关按钮：{matches[:5]}")

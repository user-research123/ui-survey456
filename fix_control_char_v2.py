#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复控制字符问题
"""

target_file = 'wangzhe_report/index_with_tabs.html'

with open(target_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 查找并替换包含控制字符的部分
old_text = ']\n        \x03 - 只保留有数据的点'
new_text = '];\n\n            // 处理数据 - 只保留有数据的点'

if old_text in content:
    content = content.replace(old_text, new_text)
    print('✓ 已修复控制字符问题')
    
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print('✓ 文件已保存')
else:
    print('✗ 未找到目标文本')
    # 调试输出
    import re
    match = re.search(r'\]\n[ ]{5,10}\x03', content)
    if match:
        print(f'找到类似模式：{repr(match.group(0))}')

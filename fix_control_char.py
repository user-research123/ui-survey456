#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复控制字符问题
"""

target_file = 'wangzhe_report/index_with_tabs.html'

with open(target_file, 'rb') as f:
    content = f.read()

# 查找并替换控制字符区域
old_bytes = b']\n        \x03 - 只保留有数据的点'
new_bytes = b'];\n\n            // 处理数据 - 只保留有数据的点'

if old_bytes in content:
    content = content.replace(old_bytes, new_bytes)
    print('✓ 已修复控制字符问题')
    
    with open(target_file, 'wb') as f:
        f.write(content)
    print('✓ 文件已保存')
else:
    print('✗ 未找到目标字节序列')
    # 调试输出
    import re
    match = re.search(b'\\]\\n[ ]{5,10}\\x03', content)
    if match:
        print(f'找到类似模式：{match.group(0)}')

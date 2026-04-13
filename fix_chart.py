#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复 index_with_tabs.html 中的 rawData 数组格式问题
"""

target_file = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/index_with_tabs.html'

with open(target_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 修复多余的左方括号
old_pattern = 'const rawData = [\n[\n            {"time": "2026-04-03 00 点 00 分"'
new_pattern = 'const rawData = [\n            {"time": "2026-04-03 00 点 00 分"'

if old_pattern in content:
    content = content.replace(old_pattern, new_pattern)
    print("✓ 已修复多余的左方括号")
else:
    print("✗ 未找到需要修复的模式")
    # 尝试另一种格式
    old_pattern2 = 'const rawData = [\n[\n            {\\\"time\\\": \\\"2026-04-03 00 点 00 分\\\"'
    if old_pattern2 in content:
        content = content.replace(old_pattern2, 'const rawData = [\n            {\\"time\\": \\"2026-04-03 00 点 00 分\\"')
        print("✓ 已修复（转义格式）")
    else:
        print("正在查找实际内容...")
        import re
        match = re.search(r'const rawData = \[(.{0,100})', content, re.DOTALL)
        if match:
            print(f"找到内容：{repr(match.group(0)[:200])}")

# 写入修复后的内容
with open(target_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("\n修复完成！")

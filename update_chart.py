#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新 index_with_tabs.html 中的曲线图数据
"""

import re

# 读取新的曲线图数据
with open('/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/云·王者荣耀世界_游戏免费榜排行曲线图.html', 'r', encoding='utf-8') as f:
    new_chart_content = f.read()

# 提取新数据中的 rawData 数组
raw_data_match = re.search(r'const rawData = (\[.*?\]);', new_chart_content, re.DOTALL)
if not raw_data_match:
    print("错误：无法在新文件中找到 rawData 数组")
    exit(1)

new_raw_data = raw_data_match.group(1)

# 读取目标文件
target_file = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/index_with_tabs.html'
with open(target_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 更新副标题的日期范围
old_subtitle = '数据统计周期：2026-04-01 至 2026-04-07'
new_subtitle = '数据统计周期：2026-04-03 至 2026-04-09'
content = content.replace(old_subtitle, new_subtitle)
print(f"✓ 已更新副标题：{old_subtitle} → {new_subtitle}")

# 2. 替换 rawData 数组
# 查找旧的 rawData 数组（从 const rawData = [ 到最后一个 ];）
old_raw_data_pattern = r'(const rawData = \[)(.*?)(\];\n\n\s+// 处理数据)'
old_match = re.search(old_raw_data_pattern, content, re.DOTALL)

if not old_match:
    print("错误：无法在目标文件中找到旧的 rawData 数组")
    exit(1)

# 替换为新的数据
new_content = re.sub(
    old_raw_data_pattern,
    r'\1\n' + new_raw_data.strip() + '\n        \3',
    content,
    flags=re.DOTALL
)

# 写入更新后的内容
with open(target_file, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("✓ 已成功替换 rawData 数组")
print(f"✓ 新数据包含 {len(new_raw_data.strip().split('},'))} 个数据点")
print("\n更新完成！")

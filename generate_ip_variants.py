#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成王者荣耀 IP 主题风的绿色和紫色变体版本
"""

import os

# 读取原始 IP 主题风文件
base_path = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/index_ip_style.html'

with open(base_path, 'r', encoding='utf-8') as f:
    base_content = f.read()

# ========== 翡翠绿版本配色方案 ==========
green_color_map = {
    '#1e3c72': '#0d2818',   # 深蓝 → 深绿（主文字/标题）
    '#2a5298': '#1a4d2e',   # 中蓝 → 中绿（次要文字）
    '#d4af37': '#50c878',   # 金色 → 翡翠绿（边框/强调色）
    '#ffd700': '#98fb98',   # 亮金 → 淡绿（高亮/悬停）
    '#fff9e6': '#f0fff0',   # 淡金背景 → 蜜露绿背景
    '#fff3cc': '#e0ffe0',   # 深金背景 → 浅绿背景
}

# ========== 紫晶色版本配色方案 ==========
purple_color_map = {
    '#1e3c72': '#2d1b4e',   # 深蓝 → 深紫（主文字/标题）
    '#2a5298': '#4b2c6e',   # 中蓝 → 中紫（次要文字）
    '#d4af37': '#9966cc',   # 金色 → 紫水晶（边框/强调色）
    '#ffd700': '#dda0dd',   # 亮金 → 梅红（高亮/悬停）
    '#fff9e6': '#f8f0ff',   # 淡金背景 → 淡紫背景
    '#fff3cc': '#f0e0ff',   # 深金背景 → 中紫背景
}

def replace_colors(content, color_map):
    """替换 CSS 中的颜色"""
    result = content
    for old_color, new_color in color_map.items():
        result = result.replace(old_color, new_color)
    return result

# 生成绿色版本
green_content = replace_colors(base_content, green_color_map)
# 修改标题
green_content = green_content.replace('（IP 主题风）', '（翡翠绿 IP 风）')
green_output_path = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/index_ip_green_style.html'

with open(green_output_path, 'w', encoding='utf-8') as f:
    f.write(green_content)

print(f"✅ 翡翠绿版本已生成：{green_output_path}")

# 生成紫色版本
purple_content = replace_colors(base_content, purple_color_map)
# 修改标题
purple_content = purple_content.replace('（IP 主题风）', '（紫晶色 IP 风）')
purple_output_path = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/index_ip_purple_style.html'

with open(purple_output_path, 'w', encoding='utf-8') as f:
    f.write(purple_content)

print(f"✅ 紫晶色版本已生成：{purple_output_path}")

print("\n🎨 两个新配色方案已完成！")

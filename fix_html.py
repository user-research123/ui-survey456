#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修复 HTML 文件的问题"""

with open('wangzhe_report/index_with_tabs.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 找到 4 月 7 日内容的行号范围
start_line = None
end_line = None
for i, line in enumerate(lines):
    if '<!-- 4 月 7 日内容 -->' in line:
        start_line = i
    if start_line and '<!-- 4 月 6 日内容 -->' in line:
        end_line = i
        break

print(f"4 月 7 日内容范围：{start_line+1} - {end_line}")

# 读取这部分内容
block = ''.join(lines[start_line:end_line])

# 问题 1：闲鱼卡片在 timeline-content 外面，需要移进去
# 问题 2：顺序是盼之→螃蟹→闲鱼，需要改为螃蟹→盼之→闲鱼

# 提取三个卡片
import re

# 找到盼之卡片
panzhi_match = re.search(r'<div class="competitor-card".*?<div class="competitor-name">竞品二：盼之</div>.*?</div>\s*</div>\s*<div class="competitor-card".*?<div class="competitor-name">竞品一：螃蟹</div>', block, re.DOTALL)
if panzhi_match:
    print("找到盼之卡片")

# 找到螃蟹卡片  
pangxie_match = re.search(r'<div class="competitor-card".*?<div class="competitor-name">竞品一：螃蟹</div>.*?</div>\s*</div>\s*</div>\s*</div>\s*</div>\s*<div class="competitor-card".*?<div class="competitor-name">竞品三：闲鱼</div>', block, re.DOTALL)
if pangxie_match:
    print("找到螃蟹卡片")

# 找到闲鱼卡片
xianyu_match = re.search(r'<div class="competitor-card".*?<div class="competitor-name">竞品三：闲鱼</div>.*?</div>\s*</div>\s*</div>\s*</div>\s*</div>\s*</div>', block, re.DOTALL)
if xianyu_match:
    print("找到闲鱼卡片")

# 更简单的方法：直接替换文本
# 1. 将"竞品二：盼之"改为"竞品一：螃蟹"（第一个卡片）
# 2. 将"竞品一：螃蟹"改为"竞品二：盼之"（第二个卡片）
# 3. 将闲鱼卡片移到 timeline-content 内

# 由于结构复杂，我们采用逐行处理的方式
new_lines = []
in_competitor_0407 = False
timeline_content_closed = False
found_panzhi = False
found_pangxie = False

for i, line in enumerate(lines):
    # 检测是否进入 4 月 7 日内容
    if '<!-- 4 月 7 日内容 -->' in line:
        in_competitor_0407 = True
        new_lines.append(line)
        continue
    
    # 检测是否离开 4 月 7 日内容
    if in_competitor_0407 and '<!-- 4 月 6 日内容 -->' in line:
        in_competitor_0407 = False
        timeline_content_closed = False
    
    if not in_competitor_0407:
        new_lines.append(line)
        continue
    
    # 在 4 月 7 日内容块内处理
    # 找到第一个 competitor-card（盼之），改为螃蟹
    if not found_panzhi and '<div class="competitor-name">竞品二：盼之</div>' in line:
        # 需要交换盼之和螃蟹的内容
        # 暂时跳过，稍后统一处理
        pass
    
    new_lines.append(line)

print("处理完成，但此方法太复杂，需要更好的策略")

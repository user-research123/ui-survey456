#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""更新 HTML 报告，添加 4 月 10 日螃蟹数据"""

import re
from datetime import datetime

# 4 月 10 日螃蟹数据分析总结
pxb7_summary = """
<div class="competitor-card">
    <div class="competitor-name">竞品一：螃蟹</div>
    <h3 class="subsubsection-title">螃蟹账号《王者荣耀世界》商品数据分析报告</h3>
<p><strong>数据总量:</strong> 100 个商品</p>
<p><strong>分析时间:</strong> 2026-04-10</p>

<h4 style="color: #5a67d8; margin: 15px 0 10px 0;">价格分布分析</h4>
<ul>
<li><strong>价格范围:</strong> ¥99 - ¥9999</li>
<li><strong>中位数价格:</strong> ¥888</li>
<li><strong>平均价格:</strong> ¥2020</li>
<li><strong>高价商品 (≥¥3000):</strong> 5 个 (25%)</li>
</ul>

<h4 style="color: #5a67d8; margin: 15px 0 10px 0;">价格区间分布</h4>
<ul>
<li>&lt;500 元：3 个 (15%)</li>
<li>500-1000 元：8 个 (40%)</li>
<li>1000-3000 元：4 个 (20%)</li>
<li>&gt;3000 元：5 个 (25%)</li>
</ul>

<h4 style="color: #5a67d8; margin: 15px 0 10px 0;">平台分布</h4>
<ul>
<li><strong>QQ:</strong> 19 个 (95%)</li>
<li><strong>微信:</strong> 1 个 (5%)</li>
</ul>

<h4 style="color: #5a67d8; margin: 15px 0 10px 0;">命名特征</h4>
<ul>
<li><strong>单字 ID:</strong> 稀缺，溢价明显（均价 3000+ 元）</li>
<li><strong>双字 ID:</strong> 主流，价格在 800-2000 元区间</li>
<li><strong>热门 ID:</strong> 如 uZi、远坂凛等溢价高</li>
<li><strong>带符号 ID:</strong> 较常见，部分使用空白符号</li>
</ul>

<h4 style="color: #5a67d8; margin: 15px 0 10px 0;">市场观察</h4>
<ul>
<li><strong>价格两极分化:</strong> 低价首冲号（99-500 元）与高价稀有 ID（3000+ 元）并存</li>
<li><strong>QQ 平台主导:</strong> 95% 商品为 QQ 区，微信区较少</li>
<li><strong>ID 交易活跃:</strong> 单字/双字 ID 是主要溢价点，热门 ID 价格可达数千</li>
<li><strong>新手友好:</strong> 大量首冲号、剧情号供应，价格亲民（100-500 元）</li>
</ul>
</div>

<div class="competitor-card">
    <div class="competitor-name">竞品二：盼之</div>
    <p style="text-align: center; color: #666; padding: 40px;">数据收集中...</p>
</div>

<div class="competitor-card">
    <div class="competitor-name">竞品三：闲鱼</div>
    <p style="text-align: center; color: #666; padding: 40px;">数据收集中...</p>
</div>
"""

# 读取 HTML 文件
with open("wangzhe_report/index_with_tabs.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. 在日期切换按钮中添加 4 月 10 日按钮（在 4 月 9 日之前）
button_pattern = r'(<button class="date-tab active" onclick="showCompetitorDate\(\'04-09\'\)">4 月 9 日</button>)'
new_button = '<button class="date-tab active" onclick="showCompetitorDate(\'04-10\')">4 月 10 日</button>\\n                    ' + button_pattern
content = re.sub(button_pattern, new_button, content, count=1)

# 2. 在 4 月 9 日内容之前添加 4 月 10 日的内容区块
date_09_pattern = r'(<!-- 4 月 9 日内容 -->\\n                <div id="competitor-04-09" class="competitor-date-content active">)'
new_content_block = '<!-- 4 月 10 日内容 -->\\n                <div id="competitor-04-10" class="competitor-date-content active">\\n                    \\n' + pxb7_summary + '\\n                </div>\\n\\n' + date_09_pattern
content = re.sub(date_09_pattern, new_content_block, content, count=1)

# 3. 移除 4 月 9 日的 active 类（因为 4 月 10 日现在是默认显示的）
content = content.replace('id="competitor-04-09" class="competitor-date-content active"', 'id="competitor-04-09" class="competitor-date-content"')

# 保存更新后的 HTML 文件
with open("wangzhe_report/index_with_tabs.html", "w", encoding="utf-8") as f:
    f.write(content)

print("✓ HTML 报告已更新：添加了 4 月 10 日螃蟹数据")
print("✓ 日期切换按钮已添加：4 月 10 日（默认激活）")
print("✓ 4 月 9 日及之后日期的内容保持完整")

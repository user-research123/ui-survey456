#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新index_with_tabs.html文件，添加4月2日盼之数据分析内容
"""

import re

# 读取文件
file_path = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report_temp/index_with_tabs.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 在日期切换按钮中添加"4月2日"（放在最前面）
date_tabs_pattern = r'(<div class="date-tabs">)'
new_date_tabs = '''<div class="date-tabs">
                    <button class="date-tab active" onclick="showDate('04-02')">4月2日</button>'''

content = re.sub(date_tabs_pattern, new_date_tabs, content)

# 将原来的第一个按钮改为非active状态
content = content.replace('<button class="date-tab active" onclick="showDate(\'04-01\')">4月1日</button>', 
                          '<button class="date-tab" onclick="showDate(\'04-01\')">4月1日</button>')

# 2. 添加4月2日的内容区块（在4月1日之前）
pzds_content_0402 = '''                <!-- 4月2日内容 -->
                <div id="date-04-02" class="date-content active">
                    <div class="timeline">
                        <div class="timeline-item">
                            <div class="timeline-date">4月2日</div>
                            <div class="timeline-content">
                                <div class="competitor-card" style="margin-bottom: 20px;">
                                    <div class="competitor-name">竞品一：盼之</div>
                                    <h3 class="subsubsection-title">盼之网站前100个商品分析报告</h3>
                                    
                                    <h4 style="color: #5a67d8; margin: 15px 0 10px 0;">商品类型分析</h4>
                                    <p>商品类型多样化，主要包括以下类型商品：</p>
                                    <ul>
                                        <li>双字ID: 22 个 (22.0%) - 如"玉佩"、"推辞"、"好宅"等</li>
                                        <li>特殊含义ID: 21 个 (21.0%) - 包含"极品"、"绝版"、"正版"等特殊标签的ID</li>
                                        <li>单字ID: 20 个 (20.0%) - 如"胆"、"衿"、"瞻"等稀有单字</li>
                                        <li>普通ID: 19 个 (19.0%) - 常规游戏账号和ID</li>
                                        <li>明星名人ID: 8 个 (8.0%) - 如"杨颖baby"、"吴彦祖"、"刘亦菲"、"张艺兴"等</li>
                                        <li>三字及以上ID: 5 个 (5.0%) - 如"自习室"、"听细雨绵绵"等</li>
                                        <li>情侣/闺蜜ID: 3 个 (3.0%) - 可搭配使用的情侣或闺蜜ID组合</li>
                                        <li>招商/返利账号: 2 个 (2.0%) - 高价值的招商和返利专用账号</li>
                                    </ul>

                                    <h4 style="color: #5a67d8; margin: 15px 0 10px 0;">价格分布分析</h4>
                                    <ul>
                                        <li>价格范围: ¥69 - ¥9,999,999</li>
                                        <li>平均价格: ¥121,260</li>
                                        <li>中位数价格: ¥888</li>
                                        <li>高价商品(≥¥10,000): 16 个 (16.0%)</li>
                                    </ul>

                                    <h4 style="color: #5a67d8; margin: 15px 0 10px 0;">价格区间分布</h4>
                                    <ul>
                                        <li>0-500: 36 个 (36.0%)</li>
                                        <li>500-1000: 29 个 (29.0%)</li>
                                        <li>1000-5000: 17 个 (17.0%)</li>
                                        <li>5000-10000: 2 个 (2.0%)</li>
                                        <li>10000-50000: 9 个 (9.0%)</li>
                                        <li>50000+: 7 个 (7.0%)</li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

'''

# 在4月1日内容之前插入4月2日内容
content = content.replace('                <!-- 4月1日内容 -->', pzds_content_0402 + '                <!-- 4月1日内容 -->')

# 写入文件
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ 成功更新index_with_tabs.html文件，已添加4月2日盼之数据分析内容")

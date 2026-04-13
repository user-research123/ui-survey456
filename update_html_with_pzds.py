#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新HTML文件，添加4月7日盼之平台商品分析内容
"""

import re

# 读取HTML文件
html_path = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/index_with_tabs.html'

with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

# 1. 在日期切换按钮中添加"4月7日"按钮（放在最前面）
date_tabs_pattern = r'(<div class="date-tabs" id="competitor-date-tabs">)'
new_date_button = '''<button class="date-tab active" onclick="showCompetitorDate('04-07')">4月7日</button>
                    <button class="date-tab" onclick="showCompetitorDate('04-06')">4月6日</button>'''

# 替换第一个按钮为active，其他为非active
old_tabs = '''                <div class="date-tabs" id="competitor-date-tabs">
                    <button class="date-tab active" onclick="showCompetitorDate('04-06')">4月6日</button>
                    <button class="date-tab" onclick="showCompetitorDate('04-05')">4月5日</button>'''

new_tabs = '''                <div class="date-tabs" id="competitor-date-tabs">
                    <button class="date-tab active" onclick="showCompetitorDate('04-07')">4月7日</button>
                    <button class="date-tab" onclick="showCompetitorDate('04-06')">4月6日</button>
                    <button class="date-tab" onclick="showCompetitorDate('04-05')">4月5日</button>'''

html_content = html_content.replace(old_tabs, new_tabs)

# 2. 准备4月7日盼之内容
pzds_content = '''                <!-- 4月7日内容 -->
                <div id="competitor-04-07" class="competitor-date-content active">
                    <div class="timeline">
                        <div class="timeline-item">
                            <div class="timeline-date">4月7日</div>
                            <div class="timeline-content">
                                <div class="competitor-card" style="margin-bottom: 20px;">
                                    <div class="competitor-name">竞品二：盼之</div>
                                    <h3 class="subsubsection-title">盼之平台《王者荣耀世界》商品数据分析报告</h3>
                                    <p><strong>数据分析数量:</strong> 100 个商品</p>
                                    <p><strong>分析时间:</strong> 04-07</p>
                                    
                                    <h4 style="color: #5a67d8; margin: 15px 0 10px 0;">一、商品品类有：成品号、昵称 (hot)、代肝 (hot)</h4>
                                    
                                    <h4 style="color: #5a67d8; margin: 15px 0 10px 0;">二、账号的详细信息</h4>
                                    
                                    <h4 style="color: #5a67d8; margin: 15px 0 10px 0;">1）价格分布分析</h4>
                                    <ul>
                                        <li>价格范围: ¥60 - ¥66,666</li>
                                        <li>中位数价格: ¥829</li>
                                        <li>高价商品(≥¥10,000): 6 个 (6.0%)</li>
                                    </ul>

                                    <h4 style="color: #5a67d8; margin: 15px 0 10px 0;">2）价格区间分布</h4>
                                    <ul>
                                        <li>0-500: 28 个 (28.0%)</li>
                                        <li>500-1000: 39 个 (39.0%)</li>
                                        <li>1000-5000: 17 个 (17.0%)</li>
                                        <li>5000-10000: 10 个 (10.0%)</li>
                                        <li>10000以上: 6 个 (6.0%)</li>
                                    </ul>

                                    <h4 style="color: #5a67d8; margin: 15px 0 10px 0;">3）平台分布</h4>
                                    <ul>
                                        <li>安卓QQ: 72 个 (72.0%)</li>
                                        <li>苹果QQ: 21 个 (21.0%)</li>
                                        <li>安卓微信: 4 个 (4.0%)</li>
                                        <li>苹果微信: 3 个 (3.0%)</li>
                                    </ul>

                                    <h4 style="color: #5a67d8; margin: 15px 0 10px 0;">4）命名特征</h4>
                                    <ul>
                                        <li>双字ID: 41 个 (41.0%)</li>
                                        <li>其他: 30 个 (30.0%)</li>
                                        <li>单字ID: 19 个 (19.0%)</li>
                                        <li>四字及以上ID: 5 个 (5.0%)</li>
                                        <li>三字ID: 5 个 (5.0%)</li>
                                    </ul>
                                    <p><strong>主要风格:</strong> 其他 (70%)、诗意/文学类 (15%)、霸气/中二类 (10%)</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

'''

# 3. 在4月6日内容之前插入4月7日内容
marker = '<!-- 4月6日内容 -->'
if marker in html_content:
    html_content = html_content.replace(marker, pzds_content + marker)
    
    # 移除4月6日的active类
    html_content = html_content.replace('<div id="competitor-04-06" class="competitor-date-content active">', 
                                         '<div id="competitor-04-06" class="competitor-date-content">')

# 4. 写入更新后的HTML文件
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print("HTML文件已成功更新，添加了4月7日盼之平台商品分析内容")
print(f"文件路径: {html_path}")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新GitHub Pages报告，添加4月3日的竞品动态追踪数据
"""

import re

# 读取HTML文件
html_file = "/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/index_with_tabs.html"

with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 在日期切换按钮区域添加"4月3日"按钮（在最前面）
date_tabs_pattern = r'(<div class="date-tabs" id="competitor-date-tabs">)'
new_date_button = '''<button class="date-tab active" onclick="showCompetitorDate('04-03')">4月3日</button>'''

# 替换第一个按钮的active类，并添加新的4月3日按钮
content = re.sub(
    r'<button class="date-tab active" onclick="showCompetitorDate\(\'04-02\'\)">4月2日</button>',
    '<button class="date-tab" onclick="showCompetitorDate(\'04-02\')">4月2日</button>',
    content
)
content = re.sub(
    date_tabs_pattern,
    r'\1\n                    ' + new_date_button,
    content
)

# 2. 添加4月3日的内容区块（在4月2日之前）
competitor_0403_content = '''
                <!-- 4月3日内容 -->
                <div id="competitor-04-03" class="competitor-date-content active">
                    <div class="timeline">
                        <div class="timeline-item">
                            <div class="timeline-date">4月3日</div>
                            <div class="timeline-content">
                                <div class="competitor-card" style="margin-bottom: 20px;">
                                    <div class="competitor-name">竞品一：螃蟹</div>
                                    <h3 class="subsubsection-title">螃蟹账号《王者荣耀世界》商品数据分析报告</h3>
                                    <p><strong>数据分析数量:</strong> 112 个商品</p>
                                    <p><strong>分析时间:</strong> 04-03</p>
                                    
                                    <h4 style="color: #5a67d8; margin: 15px 0 10px 0;">一、商品品类有：双字ID, 单字ID, 热门ID, 英文ID, 情侣ID</h4>
                                    
                                    <h4 style="color: #5a67d8; margin: 15px 0 10px 0;">二、账号的详细信息</h4>
                                    
                                    <h4 style="color: #5a67d8; margin: 15px 0 10px 0;">1）价格分布分析</h4>
                                    <ul>
                                        <li>价格范围: ¥60 - ¥250,000</li>
                                        <li>中位数价格: ¥888</li>
                                        <li>高价商品(≥¥10,000): 11 个 (9.8%)</li>
                                    </ul>

                                    <h4 style="color: #5a67d8; margin: 15px 0 10px 0;">2）价格区间分布</h4>
                                    <ul>
                                        <li>0-500: 36 个 (32.1%)</li>
                                        <li>500-1000: 28 个 (25.0%)</li>
                                        <li>1000-5000: 32 个 (28.6%)</li>
                                        <li>5000-10000: 5 个 (4.5%)</li>
                                        <li>10000以上: 11 个 (9.8%)</li>
                                    </ul>

                                    <h4 style="color: #5a67d8; margin: 15px 0 10px 0;">3）平台分布</h4>
                                    <ul>
                                        <li>QQ: 93 个 (83.0%)</li>
                                        <li>微信: 19 个 (17.0%)</li>
                                    </ul>

                                    <h4 style="color: #5a67d8; margin: 15px 0 10px 0;">4）命名特征</h4>
                                    <ul>
                                        <li>单字ID: 27 个 (24.1%)</li>
                                        <li>双字ID: 54 个 (48.2%)</li>
                                        <li>热门ID: 25 个 (22.3%)</li>
                                        <li>情侣ID: 4 个 (3.6%)</li>
                                        <li>英文ID: 2 个 (1.8%)</li>
                                    </ul>
                                </div>

                                <div class="competitor-card" style="margin-bottom: 20px;">
                                    <div class="competitor-name">竞品二：盼之</div>
                                    <h3 class="subsubsection-title">盼之网站商品分析报告</h3>
                                    <p>暂无新动态</p>
                                </div>

                                <div class="competitor-card" style="margin-bottom: 20px;">
                                    <div class="competitor-name">竞品三：闲鱼</div>
                                    <h3 class="subsubsection-title">闲鱼市场分析报告</h3>
                                    <p>暂无新动态</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
'''

# 在4月2日内容之前插入4月3日内容
content = content.replace(
    '                <!-- 4月2日内容 -->',
    competitor_0403_content + '\n                <!-- 4月2日内容 -->'
)

# 3. 移除4月2日的active类
content = re.sub(
    r'<div id="competitor-04-02" class="competitor-date-content active">',
    '<div id="competitor-04-02" class="competitor-date-content">',
    content
)

# 保存修改后的HTML文件
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("报告已更新，添加了4月3日的竞品动态追踪数据")
print(f"文件路径: {html_file}")

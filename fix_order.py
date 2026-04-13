#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复 4 月 7 日竞品动态追踪板块的产品卡片顺序
目标顺序：螃蟹 → 盼之 → 闲鱼
"""

import re

file_path = 'wangzhe_report/index_with_tabs.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 定义 4 月 7 日的三个产品卡片内容
pangxie_card = '''                                <div class="competitor-card" style="margin-bottom: 20px;">
                                    <div class="competitor-name">竞品一：螃蟹</div>
                                    <h3 class="subsubsection-title">螃蟹账号《王者荣耀世界》商品数据分析报告</h3>
                                    <p><strong>数据总量:</strong> 98 个商品</p>
                                    <p><strong>分析时间:</strong> 04-07</p>
                                    
                                    <h4 style="color: #5a67d8; margin: 15px 0 10px 0;">一、商品类型有：账号、代练、充值</h4>
                                    
                                    <h4 style="color: #5a67d8; margin: 15px 0 10px 0;">二、账号的详细信息</h4>
                                    
                                    <h4 style="color: #5a67d8; margin: 15px 0 10px 0;">1）价格分布分析</h4>
                                    <ul>
                                        <li>价格范围：¥150 - ¥1,888,888</li>
                                        <li>中位数价格：¥7,502</li>
                                        <li>高价商品 (≥¥10,000): 39 个 (39.8%)</li>
                                    </ul>

                                    <h4 style="color: #5a67d8; margin: 15px 0 10px 0;">2）价格区间分布</h4>
                                    <ul>
                                        <li>0-500: 6 个 (6.1%)</li>
                                        <li>500-1000: 9 个 (9.2%)</li>
                                        <li>1000-5000: 26 个 (26.5%)</li>
                                        <li>5000-10000: 18 个 (18.4%)</li>
                                        <li>10000-50000: 15 个 (15.3%)</li>
                                        <li>50000+: 24 个 (24.5%)</li>
                                    </ul>

                                    <h4 style="color: #5a67d8; margin: 15px 0 10px 0;">3）平台分布</h4>
                                    <ul>
                                        <li>QQ: 85 个 (86.7%)</li>
                                        <li>微信：13 个 (13.3%)</li>
                                    </ul>

                                    <h4 style="color: #5a67d8; margin: 15px 0 10px 0;">4）命名特征</h4>
                                    <ul>
                                        <li>单字 ID: 13 个 (13.3%)</li>
                                        <li>双字 ID: 42 个 (42.9%)</li>
                                        <li>主要风格：双字 ID</li>
                                    </ul>
                                </div>'''

panzhi_card = '''                                <div class="competitor-card" style="margin-bottom: 20px;">
                                    <div class="competitor-name">竞品二：盼之</div>
                                    <h3 class="subsubsection-title">盼之平台《王者荣耀世界》商品数据分析报告</h3>
                                    <p><strong>数据分析数量:</strong> 100 个商品</p>
                                    <p><strong>分析时间:</strong> 04-07</p>
                                    
                                    <h4 style="color: #5a67d8; margin: 15px 0 10px 0;">一、商品品类有：成品号、昵称 (hot)、代肝 (hot)</h4>
                                    
                                    <h4 style="color: #5a67d8; margin: 15px 0 10px 0;">二、账号的详细信息</h4>
                                    
                                    <h4 style="color: #5a67d8; margin: 15px 0 10px 0;">1）价格分布分析</h4>
                                    <ul>
                                        <li>价格范围：¥60 - ¥66,666</li>
                                        <li>中位数价格：¥829</li>
                                        <li>高价商品 (≥¥10,000): 6 个 (6.0%)</li>
                                    </ul>

                                    <h4 style="color: #5a67d8; margin: 15px 0 10px 0;">2）价格区间分布</h4>
                                    <ul>
                                        <li>0-500: 28 个 (28.0%)</li>
                                        <li>500-1000: 39 个 (39.0%)</li>
                                        <li>1000-5000: 17 个 (17.0%)</li>
                                        <li>5000-10000: 10 个 (10.0%)</li>
                                        <li>10000 以上：6 个 (6.0%)</li>
                                    </ul>

                                    <h4 style="color: #5a67d8; margin: 15px 0 10px 0;">3）平台分布</h4>
                                    <ul>
                                        <li>安卓 QQ: 72 个 (72.0%)</li>
                                        <li>苹果 QQ: 21 个 (21.0%)</li>
                                        <li>安卓微信：4 个 (4.0%)</li>
                                        <li>苹果微信：3 个 (3.0%)</li>
                                    </ul>

                                    <h4 style="color: #5a67d8; margin: 15px 0 10px 0;">4）命名特征</h4>
                                    <ul>
                                        <li>双字 ID: 41 个 (41.0%)</li>
                                        <li>其他：30 个 (30.0%)</li>
                                        <li>单字 ID: 19 个 (19.0%)</li>
                                        <li>四字及以上 ID: 5 个 (5.0%)</li>
                                        <li>三字 ID: 5 个 (5.0%)</li>
                                    </ul>
                                    <p><strong>主要风格:</strong> 其他 (70%)、诗意/文学类 (15%)、霸气/中二类 (10%)</p>
                                </div>'''

xianyu_card = '''                                <div class="competitor-card" style="margin-bottom: 20px;">
                                    <div class="competitor-name">竞品三：闲鱼</div>
                                    <h3 class="subsubsection-title">闲鱼平台商品分析 (2026 年 04 月 07 日)</h3>
<p><strong>数据概况:</strong> 采集前 100 个商品信息</p>
<h4 style="color: #5a67d8; margin: 15px 0 10px 0;">一、价格区间分布</h4>
<ul>
    <li><strong>0-10 元:</strong> 3 个 (3%)</li>
    <li><strong>11-50 元:</strong> 0 个 (0%)</li>
    <li><strong>51-100 元:</strong> 9 个 (9%)</li>
    <li><strong>101-500 元:</strong> 9 个 (9%)</li>
    <li><strong>501-1000 元:</strong> 0 个 (0%)</li>
    <li><strong>1000 元以上:</strong> 79 个 (79%)</li>
</ul>
<p><strong>价格中位数:</strong> ¥6999</p>
<h4 style="color: #5a67d8; margin: 15px 0 10px 0;">二、商品品类分布</h4>
<ul>
    <li><strong>普通 ID:</strong> 62 个 (62%)</li>
    <li><strong>极品 ID:</strong> 24 个 (24%)</li>
    <li><strong>账号:</strong> 7 个 (7%)</li>
    <li><strong>其他:</strong> 7 个 (7%)</li>
</ul>
<h4 style="color: #5a67d8; margin: 15px 0 10px 0;">三、平台占比</h4>
<ul>
    <li><strong>QQ 平台:</strong> 23 个 (23%)</li>
    <li><strong>微信平台:</strong> 4 个 (4%)</li>
    <li><strong>未明确:</strong> 73 个 (73%)</li>
</ul>
<h4 style="color: #5a67d8; margin: 15px 0 10px 0;">四、ID 命名特征</h4>
<ul>
    <li><strong>单字 ID:</strong> 22 个</li>
    <li><strong>双字 ID:</strong> 6 个</li>
    <li><strong>情侣/CP ID:</strong> 3 个</li>
</ul>
<h4 style="color: #5a67d8; margin: 15px 0 10px 0;">五、市场观察</h4>
<ul>
    <li><strong>低价商品为主:</strong> 3 个商品价格在 50 元以下，占比 3%，显示闲鱼以低单价虚拟物品交易为主</li>
    <li><strong>ID 交易活跃:</strong> 极品 ID 和普通 ID 合计 86 个，占 86%，是主要交易品类</li>
    <li><strong>QQ 平台主导:</strong> QQ 平台商品 23 个，占比 23%，远超微信平台</li>
    <li><strong>高价 ID 稀缺:</strong> 1000 元以上商品 79 个，多为极品单字/双字 ID 或名人同名 ID</li>
</ul>

                                </div>'''

# 构建正确的 4 月 7 日内容块
correct_content = '''                <!-- 4 月 7 日内容 -->
                <div id="competitor-04-07" class="competitor-date-content active">
                    <div class="timeline">
                        <div class="timeline-item">
                            <div class="timeline-date">4 月 7 日</div>
                            <div class="timeline-content">
''' + pangxie_card + '\n\n' + panzhi_card + '\n\n' + xianyu_card + '''                            </div>
                        </div>
                    </div>
                </div>

<!-- 4 月 6 日内容 -->'''

# 定义旧的 4 月 7 日内容块（从文件第 443 行到 586 行）
old_pattern = r'                \n                                <!-- 4 月 7 日内容 -->\n                <div id="competitor-04-07" class="competitor-date-content active">\n                    <div class="timeline">\n                        <div class="timeline-item">\n                            <div class="timeline-date">4 月 7 日</div>\n                            <div class="timeline-content">.*?</div>\n                </div>\n                </div>\n\n<!-- 4 月 6 日内容 -->'

# 使用 DOTALL 模式让。匹配换行符
new_content = re.sub(old_pattern, correct_content, content, flags=re.DOTALL, count=1)

if new_content == content:
    print("✗ 未找到匹配的内容块")
else:
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("✓ 4 月 7 日竞品排序修复完成（螃蟹→盼之→闲鱼）")

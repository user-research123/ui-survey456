#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复index_with_tabs.html文件，在4月2日添加完整的三个竞品数据
"""

import re

# 读取文件
file_path = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/index_with_tabs.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 定义4月2日的完整内容（包含螃蟹、盼之、闲鱼）
full_content_0402 = '''                <!-- 4月2日内容 -->
                <div id="date-04-02" class="date-content active">
                    <div class="timeline">
                        <div class="timeline-item">
                            <div class="timeline-date">4月2日</div>
                            <div class="timeline-content">
                                <div class="competitor-card" style="margin-bottom: 20px;">
                                    <div class="competitor-name">竞品一：螃蟹</div>
                                    <h3 class="subsubsection-title">螃蟹账号《王者荣耀世界》商品数据分析报告</h3>
                                    <p><strong>数据总量:</strong> 112 个商品</p>
                                    <p><strong>分析时间:</strong> 04-02</p>
                                    
                                    <h4 style="color: #5a67d8; margin: 15px 0 10px 0;">价格分布分析</h4>
                                    <ul>
                                        <li>价格范围: ¥80 - ¥999,999</li>
                                        <li>平均价格: ¥21,779</li>
                                        <li>中位数价格: ¥1,500</li>
                                        <li>高价商品(≥¥10,000): 16 个 (14.3%)</li>
                                    </ul>

                                    <h4 style="color: #5a67d8; margin: 15px 0 10px 0;">价格区间分布</h4>
                                    <ul>
                                        <li>0-500: 30 个 (26.8%)</li>
                                        <li>500-1000: 22 个 (19.6%)</li>
                                        <li>1000-5000: 32 个 (28.6%)</li>
                                        <li>5000-10000: 10 个 (8.9%)</li>
                                        <li>10000-50000: 5 个 (4.5%)</li>
                                        <li>50000+: 13 个 (11.6%)</li>
                                    </ul>

                                    <h4 style="color: #5a67d8; margin: 15px 0 10px 0;">平台分布</h4>
                                    <ul>
                                        <li>QQ: 96 个 (85.7%)</li>
                                        <li>微信: 16 个 (14.3%)</li>
                                    </ul>

                                    <h4 style="color: #5a67d8; margin: 15px 0 10px 0;">命名特征</h4>
                                    <ul>
                                        <li>单字ID: 19 个 (17.0%)</li>
                                        <li>双字ID: 31 个 (27.7%)</li>
                                        <li>主要风格: 诗意/文学类 (12%)、霸气/中二类 (8%)、可爱/萌系 (7%)</li>
                                    </ul>
                                </div>

                                <div class="competitor-card" style="margin-bottom: 20px;">
                                    <div class="competitor-name">竞品二：盼之</div>
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

                                <div class="competitor-card">
                                    <div class="competitor-name">竞品三：闲鱼</div>
                                    <h3 class="subsubsection-title">核心发现</h3>
                                    <ul>
                                        <li><strong>低价小额交易主导：</strong>商品价格普遍较低，以游戏资源、充值服务、虚拟道具为主，体现与垂直交易平台的市场差异化。</li>
                                        <li><strong>游戏资源/安装包活跃：</strong>包括王者荣耀世界iOS安装包、MOD、材质包、角色卡等虚拟资源。</li>
                                        <li><strong>充值/代充服务普遍：</strong>涵盖多款游戏的代充业务，满足玩家快速充值需求。</li>
                                        <li><strong>虚拟道具/资源交易集中：</strong>包括激活码、CDK、游戏内宠物、称号等。</li>
                                        <li><strong>代练/代打服务存在：</strong>主要为王者荣耀世界红buff称号代打、狂暴模式通关等服务。</li>
                                        <li><strong>长尾品类多样：</strong>包括PC单机游戏、账号/ID交易、捞人/组队服务等。</li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

'''

# 查找并替换现有的4月2日内容（只包含盼之的部分）
# 匹配从 <!-- 4月2日内容 --> 到下一个 <!-- 4月1日内容 --> 之间的所有内容
pattern = r'(<!-- 4月2日内容 -->.*?)(<!-- 4月1日内容 -->)'
replacement = full_content_0402 + r'\2'

content = re.sub(pattern, replacement, content, flags=re.DOTALL)

# 写入文件
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ 成功修复index_with_tabs.html文件，已添加4月2日完整的三个竞品数据")

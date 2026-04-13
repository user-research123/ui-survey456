#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新GitHub Pages报告中的螃蟹账号数据
"""

import re

# 读取HTML文件
with open('/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/index_with_tabs.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# 新的螃蟹数据分析结果
new_pxb7_data = """                                <div class="competitor-card" style="margin-bottom: 20px;">
                                    <div class="competitor-name">竞品一：螃蟹</div>
                                    <h3 class="subsubsection-title">螃蟹账号《王者荣耀世界》商品数据分析报告</h3>
                                    <p><strong>数据总量:</strong> 112 个商品</p>
                                    <p><strong>分析时间:</strong> 04-03</p>
                                    
                                    <h4 style="color: #5a67d8; margin: 15px 0 10px 0;">一、商品类型有：账号、代练</h4>
                                    
                                    <h4 style="color: #5a67d8; margin: 15px 0 10px 0;">二、账号的详细信息</h4>
                                    
                                    <h4 style="color: #5a67d8; margin: 15px 0 10px 0;">1）价格分布分析</h4>
                                    <ul>
                                        <li>价格范围: ¥60 - ¥250,000</li>
                                        <li>中位数价格: ¥999</li>
                                        <li>高价商品(≥¥10,000): 13 个 (11.7%)</li>
                                    </ul>

                                    <h4 style="color: #5a67d8; margin: 15px 0 10px 0;">2）价格区间分布</h4>
                                    <ul>
                                        <li>0-500: 32 个 (28.8%)</li>
                                        <li>500-1000: 28 个 (25.2%)</li>
                                        <li>1000-5000: 30 个 (27.0%)</li>
                                        <li>5000-10000: 8 个 (7.2%)</li>
                                        <li>10000-50000: 8 个 (7.2%)</li>
                                        <li>50000+: 5 个 (4.5%)</li>
                                    </ul>

                                    <h4 style="color: #5a67d8; margin: 15px 0 10px 0;">3）平台分布</h4>
                                    <ul>
                                        <li>QQ: 87 个 (78.4%)</li>
                                        <li>微信: 15 个 (13.5%)</li>
                                    </ul>

                                    <h4 style="color: #5a67d8; margin: 15px 0 10px 0;">4）命名特征</h4>
                                    <ul>
                                        <li>单字ID: 28 个 (25.2%)</li>
                                        <li>双字ID: 52 个 (46.8%)</li>
                                        <li>主要风格: 以双字ID和单字ID为主，热门ID也占一定比例</li>
                                    </ul>
                                </div>"""

# 找到4月3日内容中的螃蟹部分并替换
# 使用正则表达式匹配从"竞品一：螃蟹"到下一个"竞品二：盼之"之间的内容
pattern = r'(<div class="competitor-card" style="margin-bottom: 20px;">\s*<div class="competitor-name">竞品一：螃蟹</div>.*?)(<div class="competitor-card" style="margin-bottom: 20px;">\s*<div class="competitor-name">竞品二：盼之</div>)'

# 在4月3日的内容块中进行替换
def replace_pxb7(match):
    return new_pxb7_data + '\n\n' + match.group(2)

# 只替换4月3日部分（在id="competitor-04-03"和id="competitor-04-02"之间）
# 首先找到4月3日的开始和结束位置
start_marker = '<div id="competitor-04-03" class="competitor-date-content active">'
end_marker = '<!-- 4月2日内容 -->'

start_idx = html_content.find(start_marker)
end_idx = html_content.find(end_marker)

if start_idx != -1 and end_idx != -1:
    # 提取4月3日的内容
    before_section = html_content[:start_idx]
    section_0403 = html_content[start_idx:end_idx]
    after_section = html_content[end_idx:]
    
    # 在4月3日部分中替换螃蟹数据
    updated_section = re.sub(pattern, replace_pxb7, section_0403, flags=re.DOTALL)
    
    # 重新组合HTML
    html_content = before_section + updated_section + after_section
    
    # 写回文件
    with open('/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/index_with_tabs.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("成功更新4月3日螃蟹账号数据")
else:
    print("未找到4月3日内容区块")

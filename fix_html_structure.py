#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复 HTML 报告总结部分的结构问题
"""

import re

html_file = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/index_with_tabs.html'

# 读取 HTML 文件
with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 定义旧内容（错误的结构）
old_pattern = r'(        <div class="content">\n            )04 月 08 日总结<br>.*?反映玩家对省时省力和资源获取的明显需求</div>\n            </div>'

# 定义新内容（正确的结构）
new_content = r'''\1<!-- 总结部分 -->
            <div class="section">
                <h2 class="section-title">总结</h2>
                <div class="section-content">
                    04 月 08 日总结<br>官方活动：无<br>竞品动态：<br>螃蟹：迅速跟进热门、单双字及角色 ID 的账号交易服务，并提供代练业务。其中账号价格区间：大部分集中在 50000+元（占 31%）<br>盼之：跟进账号和代练业务，价格分布：以 500-1000 元为主（占 0%）<br>闲鱼：提供代练、账号、抢注等服务，个人卖家居多，交易活跃<br>用户需求：微博舆情分析<br>核心关注点：社交互动 (15%)、游戏内容 (15%)；服务类需求：代练代肝 (9%) + 道具交易 (9%) = 19%，反映玩家对省时省力和资源获取的明显需求
                </div>
            </div>'''

# 执行替换
new_html = re.sub(old_pattern, new_content, content, flags=re.DOTALL)

# 保存修改后的 HTML 文件
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(new_html)

print("HTML 报告结构已修复！")
print(f"文件路径：{html_file}")

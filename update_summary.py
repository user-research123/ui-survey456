#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""更新HTML报告中的总结部分，添加4月10日内容"""

import re

html_path = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/index_with_tabs.html'

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 查找并替换总结部分
old_summary_pattern = r'(                <div class="section-content">\n                    )4 月 9 日总结<br>'
new_summary = r'\g<1>4 月 10 日总结<br>官方活动：王者荣耀 x 王者荣耀世界 联动版本正式上线；农友同行，奔赴世界丨王者荣耀世界 PC 端公测正式开启<br>竞品动态：<br>- 闲鱼：商品数量较少（仅8条），但高价商品占比显著（62.5% ≥¥10,000），中位数价格达 ¥30,000，主要交易品类为成品号与极品昵称/ID<br>用户需求：微博舆情分析显示，核心关注点为组队社交 (15.5%)、道具交易 (15.5%)；服务类需求合计 25.9%（代练代肝 10.3% + 道具交易 15.5%），反映玩家对省时省力和资源获取的明显需求<br><br>4 月 9 日总结<br>'

content = re.sub(old_summary_pattern, new_summary, content)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("总结部分更新成功！")

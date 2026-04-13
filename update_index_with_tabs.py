#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新index_with_tabs.html文件中4月1日闲鱼部分的内容
"""

import re

# 读取文件
file_path = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report_temp/index_with_tabs.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 定义新的闲鱼内容
xianyu_content = """                                <div class=\"competitor-card\">
                                    <div class=\"competitor-name\">竞品三：闲鱼</div>
                                    <h3 class=\"subsubsection-title\">核心发现</h3>
                                    <ul>
                                        <li><strong>低价小额交易主导：</strong>所有101个商品价格均在¥500以下，价格范围¥1.00-¥280.00，平均价格¥11.91，中位数价格¥5.00，无高价账号交易，体现与垂直交易平台的市场差异化。</li>
                                        <li><strong>游戏资源/安装包占比最高：</strong>18个(17.8%)，包括王者荣耀世界iOS安装包、MOD、材质包、角色卡等虚拟资源。</li>
                                        <li><strong>充值/代充服务活跃：</strong>16个(15.8%)，涵盖PJSK大小月卡、网易我的世界代充、暗区突围代充等多款游戏。</li>
                                        <li><strong>虚拟道具/资源交易普遍：</strong>15个(14.9%)，包括WRC激活码、雨世界CDK、游戏内宠物、称号等。</li>
                                        <li><strong>攻略/辅助工具需求明显：</strong>11个(10.9%)，如王者荣耀世界红buff挑战攻略、羊了个羊科技辅助等。</li>
                                        <li><strong>代练/代打服务集中：</strong>9个(8.9%)，主要为王者荣耀世界红buff称号代打、狂暴模式通关等服务。</li>
                                        <li><strong>长尾品类多样：</strong>包括PC单机游戏(7个)、账号/ID交易(6个)、捞人/组队服务(3个)、小说/文学(3个)、花园类物品(3个)等。</li>
                                    </ul>
                                </div>"""

# 使用正则表达式替换4月1日的闲鱼部分
# 匹配模式: 找到第一个"竞品三：闲鱼"后面的"暂无新动态"部分
pattern = r'(<div class=\"competitor-name\">竞品三：闲鱼</div>)\s*<p style=\"color: #718096; font-style: italic;\">暂无新动态</p>'

# 只替换第一次出现(即4月1日的部分)
new_content = re.sub(pattern, xianyu_content.replace('\\n', '\n').replace('                                    <div class=\"competitor-name\">竞品三：闲鱼</div>', '\\1'), content, count=1)

# 写入文件
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("成功更新index_with_tabs.html文件中4月1日闲鱼部分的内容")

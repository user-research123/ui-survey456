#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新 4 月 7 日日报总结到 HTML 报告
"""

import re

# 新的总结内容
new_summary = """4 月 7 日总结<br>官方活动：《王者荣耀世界》PC 端预下载将于 4 月 7 日上午 10:00 开启<br>竞品动态：<br>- 螃蟹：迅速跟进热门、单双字及角色 ID 的账号交易服务，并提供代练业务。其中账号价格区间：大部分集中在 1000-5000 元（占 26%）<br>- 盼之：跟进账号和代练业务，价格分布：以 500-1000 元为主（占 39%）<br>- 闲鱼：提供代练、账号、抢注等服务，大部分集中在 1000 元以上（占 79%），个人卖家居多，交易活跃<br>用户需求：微博舆情分析<br>核心关注点：游戏攻略 (18%)、同人创作 (16%)；服务类需求：代练代肝 (10%) + 道具交易 (13%) = 23%，反映玩家对省时省力和资源获取的明显需求</p>"""

# 读取 HTML 文件
html_path = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/index_with_tabs.html'

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 使用正则表达式匹配并替换总结内容
# 匹配从"D 月 07 日总结"或"4 月 7 日总结"开始到</p>结束的内容
pattern = r'(D 月 07 日总结|4 月 7 日总结)<br>.*?</p>\n                </div>'

# 检查是否找到匹配
if re.search(pattern, content, re.DOTALL):
    # 替换总结内容
    new_content = re.sub(pattern, new_summary + '\n                </div>', content, flags=re.DOTALL)
    
    # 写回文件
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("✅ 总结已成功更新到 HTML 报告")
else:
    print("❌ 未找到总结模块，请检查文件格式")
    # 输出查找提示
    if "总结" in content:
        print("💡 文件中包含'总结'关键词，但格式不匹配")

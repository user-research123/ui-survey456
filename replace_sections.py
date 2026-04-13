#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
替换总结和曲线图部分为正确的结构
"""
import re

html_path = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/index_with_tabs.html'

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 新的正确结构
new_summary_section = '''            <!-- 总结部分 -->
            <div class="section">
                <h2 class="section-title">总结</h2>
                <div class="section-content">
                    4 月 7 日总结<br>官方活动：《王者荣耀世界》PC 端预下载将于 4 月 7 日上午 10:00 开启<br>竞品动态：<br>- 螃蟹：迅速跟进热门、单双字及角色 ID 的账号交易服务，并提供代练业务。其中账号价格区间：大部分集中在 1000-5000 元（占 26%）<br>- 盼之：跟进账号和代练业务，价格分布：以 500-1000 元为主（占 39%）<br>- 闲鱼：提供代练、账号、抢注等服务，大部分集中在 1000 元以上（占 79%），个人卖家居多，交易活跃<br>用户需求：微博舆情分析<br>核心关注点：游戏攻略 (18%)、同人创作 (16%)；服务类需求：代练代肝 (10%) + 道具交易 (13%) = 23%，反映玩家对省时省力和资源获取的明显需求
                </div>
            </div>
            
            <!-- 榜单曲线图 -->
            <div class="section">
                <h2 class="section-title">云·王者荣耀世界 - 游戏 (免费) 榜单曲线图</h2>
                <p style="text-align: center; color: #666; font-size: 14px; margin-bottom: 20px;">数据统计周期：2026-04-01 至 2026-04-07</p>
                
                <div class="chart-legend">
                    <div class="chart-legend-item">
                        <div class="chart-legend-color" style="background-color: #91CC75;"></div>
                        <span>游戏 (免费)</span>
                    </div>
                </div>
                
                <div id="rank-chart-container">
                    <div class="chart-tooltip" id="chart-tooltip"></div>
                </div>
                
                <p class="chart-data-source">数据来源：七麦数据</p>
            </div>

            <!-- 游戏官方事件/活动 -->'''

# 使用正则表达式匹配旧的总结 + 曲线图部分
# 从"<!-- 总结部分 -->"匹配到"<!-- 游戏官方事件/活动 -->"之前
pattern = r'            <!-- 总结部分 -->.*?            <!-- 游戏官方事件/活动 -->'

# 查找匹配
match = re.search(pattern, content, re.DOTALL)
if match:
    print("✅ 找到需要替换的部分")
    print(f"   原始长度：{len(match.group(0))} 字符")
    print(f"   新长度：{len(new_summary_section)} 字符")
    
    # 替换
    content = content[:match.start()] + new_summary_section + content[match.end():]
    
    # 写回文件
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ 替换成功！")
else:
    print("❌ 未找到匹配的部分")

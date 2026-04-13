#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
精确修复 HTML 结构
目标：将总结和曲线图分离为两个独立的 .section 板块
"""

html_path = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/index_with_tabs.html'

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 定义旧结构（从总结开始到游戏官方事件之前）
old_structure = '''            <!-- 总结部分 -->
            <div class="section">
                <h2 class="section-title">总结</h2>
                4 月 7 日总结<br>官方活动：《王者荣耀世界》PC 端预下载将于 4 月 7 日上午 10:00 开启<br>竞品动态：<br>- 螃蟹：迅速跟进热门、单双字及角色 ID 的账号交易服务，并提供代练业务。其中账号价格区间：大部分集中在 1000-5000 元（占 26%）<br>- 盼之：跟进账号和代练业务，价格分布：以 500-1000 元为主（占 39%）<br>- 闲鱼：提供代练、账号、抢注等服务，大部分集中在 1000 元以上（占 79%），个人卖家居多，交易活跃<br>用户需求：微博舆情分析<br>核心关注点：游戏攻略 (18%)、同人创作 (16%)；服务类需求：代练代肝 (10%) + 道具交易 (13%) = 23%，反映玩家对省时省力和资源获取的明显需求</p>
                </div>
                
                <!-- 榜单曲线图 -->
                <div style="margin-top: 30px;">
                    <h3 style="text-align: center; color: #333; margin-bottom: 10px;">云·王者荣耀世界 - 游戏 (免费) 榜单曲线图</h3>
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
            </div>

            <!-- 游戏官方事件/活动 -->'''

# 定义新结构
new_structure = '''            <!-- 总结部分 -->
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

if old_structure in content:
    content = content.replace(old_structure, new_structure)
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ HTML 结构修复成功！")
    print("\n📋 修改内容：")
    print("   1. ✅ 总结内容包裹在 <div class='section-content'> 中")
    print("   2. ✅ 移除了错误的 </p> 标签")
    print("   3. ✅ 总结板块正确闭合")
    print("   4. ✅ 榜单曲线图现在是独立的 .section 板块")
    print("   5. ✅ 曲线图标题使用 h2.section-title 保持一致性")
    print("   6. ✅ 移除了多余的嵌套 div")
else:
    print("❌ 未找到完全匹配的结构")
    print("💡 可能原因：空格或换行符不匹配")

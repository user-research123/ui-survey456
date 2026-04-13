#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清理曲线图板块重复的标题
"""

html_path = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/index_with_tabs.html'

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 移除多余的 div 包装和 h3 标题
old_pattern = '''            <!-- 榜单曲线图 -->
            <div class="section">
                <h2 class="section-title">云·王者荣耀世界 - 游戏 (免费) 榜单曲线图</h2>
                <div style="margin-top: 30px;">
                    <h3 style="text-align: center; color: #333; margin-bottom: 10px;">云·王者荣耀世界 - 游戏 (免费) 榜单曲线图</h3>
                    <p style="text-align: center; color: #666; font-size: 14px; margin-bottom: 20px;">数据统计周期：2026-04-01 至 2026-04-07</p>'''

new_pattern = '''            <!-- 榜单曲线图 -->
            <div class="section">
                <h2 class="section-title">云·王者荣耀世界 - 游戏 (免费) 榜单曲线图</h2>
                <p style="text-align: center; color: #666; font-size: 14px; margin-bottom: 20px;">数据统计周期：2026-04-01 至 2026-04-07</p>'''

if old_pattern in content:
    content = content.replace(old_pattern, new_pattern)
    
    # 同时移除图表容器结束后的多余 </div>
    # 找到图表数据源行之后的结构
    old_end = '''                    <p class="chart-data-source">数据来源：七麦数据</p>
                </div>
            </div>'''
    
    new_end = '''                <p class="chart-data-source">数据来源：七麦数据</p>
            </div>'''
    
    if old_end in content:
        content = content.replace(old_end, new_end)
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ 清理完成！")
    print("📋 已移除：")
    print("   1. 多余的 <div style='margin-top: 30px;'> 包装")
    print("   2. 重复的 h3 标题")
    print("   3. 多余的嵌套层级")
else:
    print("❌ 未找到匹配的模式")

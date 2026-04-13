#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用正则表达式修复 HTML 结构
"""
import re

html_path = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/index_with_tabs.html'

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 匹配从"<!-- 总结部分 -->"到"</div>\n\n            <!-- 游戏官方事件/活动 -->"
# 使用非贪婪匹配
pattern = r'(            <!-- 总结部分 -->\n            <div class="section">\n                <h2 class="section-title">总结</h2>\n)(.*?)(</p>\n                </div>\n                \n                <!-- 榜单曲线图 -->\n                <div style="margin-top: 30px;">\n                    <h3 style="text-align: center; color: #333; margin-bottom: 10px;">云·王者荣耀世界 - 游戏\(免费\) 榜单曲线图</h3>\n                    <p style="text-align: center; color: #666; font-size: 14px; margin-bottom: 20px;">数据统计周期：2026-04-01 至 2026-04-07</p>\n                    \n                    <div class="chart-legend">\n                        <div class="chart-legend-item">\n                            <div class="chart-legend-color" style="background-color: #91CC75;"></div>\n                            <span>游戏\(免费\)</span>\n                        </div>\n                    </div>\n                    \n                    <div id="rank-chart-container">\n                        <div class="chart-tooltip" id="chart-tooltip"></div>\n                    </div>\n                    \n                    <p class="chart-data-source">数据来源：七麦数据</p>\n                </div>\n            </div>\n\n            )(<!-- 游戏官方事件/活动 -->)'

def replace_func(match):
    summary_content = match.group(2).strip()
    return f'''{match.group(1)}                <div class="section-content">
                    {summary_content}
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

{match.group(4)}'''

new_content = re.sub(pattern, replace_func, content, flags=re.DOTALL)

if new_content != content:
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("✅ HTML 结构修复成功！")
    print("\n📋 修改内容：")
    print("   1. ✅ 总结内容包裹在 <div class='section-content'> 中")
    print("   2. ✅ 移除了错误的 </p> 标签")
    print("   3. ✅ 总结板块正确闭合")
    print("   4. ✅ 榜单曲线图现在是独立的 .section 板块")
    print("   5. ✅ 曲线图标题使用 h2.section-title 保持一致性")
else:
    print("❌ 正则表达式未匹配到内容")
    # 调试：检查是否包含关键字符串
    checks = [
        ("<!-- 总结部分 -->", "<!-- 总结部分 -->" in content),
        ("<!-- 游戏官方事件/活动 -->", "<!-- 游戏官方事件/活动 -->" in content),
        ("</p>", "</p>" in content),
    ]
    for name, result in checks:
        print(f"   {name}: {'✓' if result else '✗'}")

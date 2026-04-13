#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单直接的修复方案
"""
import re

html_path = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/index_with_tabs.html'

with open(html_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 找到关键行
summary_h2_idx = None
chart_comment_idx = None

for i, line in enumerate(lines):
    if '<h2 class="section-title">总结</h2>' in line:
        summary_h2_idx = i
    if '<!-- 榜单曲线图 -->' in line and summary_h2_idx and i > summary_h2_idx:
        chart_comment_idx = i
        break

if summary_h2_idx and chart_comment_idx:
    print(f"✅ 找到关键位置:")
    print(f"   总结标题：第 {summary_h2_idx + 1} 行")
    print(f"   曲线图注释：第 {chart_comment_idx + 1} 行")
    
    # 修改策略：
    # 1. 在总结内容前添加 <div class="section-content">
    # 2. 将 </p> 改为 </div>（关闭 section-content）
    # 3. 在曲线图注释前添加 </div>（关闭总结 section）和新的 <div class="section">
    # 4. 将曲线图的 h3 改为 h2 class="section-title"
    # 5. 移除曲线图 div 外的包装
    
    # 步骤 1: 在总结内容行（h2 的下一行）前添加 section-content 开始标签
    content_line_idx = summary_h2_idx + 1
    original_content = lines[content_line_idx]
    lines[content_line_idx] = '                <div class="section-content">\n' + original_content
    
    # 步骤 2: 找到</p>并替换为</div>
    for i in range(content_line_idx, chart_comment_idx):
        if '</p>' in lines[i]:
            lines[i] = lines[i].replace('</p>', '')
            # 在这行后面添加 section-content 的闭合标签
            if not lines[i].strip():  # 如果这行变为空
                lines[i] = '                </div>\n'
            else:
                # 在下一行插入闭合标签
                lines.insert(i + 1, '                </div>\n')
            break
    
    # 步骤 3: 在曲线图注释前添加额外的换行和 section 开始标签
    # 先找到曲线图注释的索引（可能因为插入而改变）
    for i, line in enumerate(lines):
        if '<!-- 榜单曲线图 -->' in line:
            chart_comment_idx = i
            break
    
    # 在曲线图注释前插入空行和新的 section 开始标签
    lines.insert(chart_comment_idx, '\n')
    lines.insert(chart_comment_idx + 1, '            <div class="section">\n')
    
    # 步骤 4: 找到曲线图的 h3 并改为 h2
    for i in range(chart_comment_idx, min(chart_comment_idx + 10, len(lines))):
        if '<h3 style="text-align: center; color: #333; margin-bottom: 10px;">云·王者荣耀世界 - 游戏 (免费) 榜单曲线图</h3>' in lines[i]:
            lines[i] = '                <h2 class="section-title">云·王者荣耀世界 - 游戏 (免费) 榜单曲线图</h2>\n'
            break
    
    # 步骤 5: 找到图表数据源行后的结构，调整闭合标签
    for i in range(chart_comment_idx, min(chart_comment_idx + 30, len(lines))):
        if '<p class="chart-data-source">数据来源：七麦数据</p>' in lines[i]:
            # 接下来的几行应该是：</div>\n            </div>\n
            # 我们需要移除一个</div>（多余的包装层）
            if i + 1 < len(lines) and '</div>' in lines[i + 1]:
                # 这是关闭图表容器的</div>，保留
                # 检查下一行
                if i + 2 < len(lines) and '</div>' in lines[i + 2]:
                    # 这是关闭旧包装 div 的，移除
                    lines.pop(i + 2)
            break
    
    # 写回文件
    with open(html_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print("✅ 修复完成！")
else:
    print("❌ 无法定位关键位置")

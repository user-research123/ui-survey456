#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复 HTML 结构：将总结和曲线图分离为独立板块
使用逐行读取的方式精确定位
"""

html_path = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/index_with_tabs.html'

with open(html_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 找到关键行的索引
summary_start_idx = None
chart_start_idx = None
section_close_idx = None
official_events_idx = None

for i, line in enumerate(lines):
    if '<!-- 总结部分 -->' in line:
        summary_start_idx = i
    if '<!-- 榜单曲线图 -->' in line and i > summary_start_idx:
        chart_start_idx = i
    if '<!-- 游戏官方事件/活动 -->' in line:
        official_events_idx = i

print(f"📍 找到关键位置:")
print(f"   总结部分开始：第 {summary_start_idx + 1} 行")
print(f"   榜单曲线图开始：第 {chart_start_idx + 1} 行")
print(f"   游戏官方事件开始：第 {official_events_idx + 1} 行")

# 检查第 chart_start_idx - 1 行（曲线图前一行）是否包含 </div>
if chart_start_idx and chart_start_idx > 0:
    prev_line = lines[chart_start_idx - 1]
    print(f"\n🔍 曲线图前一行内容：{repr(prev_line)}")
    
    # 如果前一行是 </div>\n，说明这是错误的 section 闭合
    if prev_line.strip() == '</div>':
        print("✅ 确认问题：曲线图前有错误的 </div> 标签")
        
        # 现在我们需要：
        # 1. 在总结内容后添加 </div> 来关闭 section-content
        # 2. 删除曲线图前的 </div>
        # 3. 在曲线图前添加新的 <div class="section">
        # 4. 将曲线图的 h3 改为 h2 class="section-title"
        
        # 找到总结内容的行（h2 之后的那行）
        summary_content_idx = None
        for i in range(summary_start_idx, chart_start_idx):
            if '<h2 class="section-title">总结</h2>' in lines[i]:
                summary_content_idx = i + 1
                break
        
        if summary_content_idx:
            print(f"\n✏️  修改总结内容行：第 {summary_content_idx + 1} 行")
            # 在总结内容前后添加 <div class="section-content"> 和 </div>
            original_content = lines[summary_content_idx]
            lines[summary_content_idx] = original_content.replace(
                '                4 月 7 日总结',
                '                <div class="section-content">\n                    4 月 7 日总结'
            )
            
            # 找到总结内容的结束行（曲线图前两行）
            summary_end_idx = chart_start_idx - 2  # 跳过空行和</div>
            if '</div>' in lines[summary_end_idx]:
                lines[summary_end_idx] = lines[summary_end_idx].replace(
                    '</div>',
                    '</div>\n                </div>'  # 关闭 section-content
                )
            
            # 删除曲线图前的 </div>（它错误地关闭了 section）
            del lines[chart_start_idx - 1]
            
            # 在曲线图前添加新的 section 开始标签
            lines.insert(chart_start_idx - 1, '            <div class="section">\n')
            
            # 将曲线图的 h3 改为 h2 class="section-title"
            for i in range(chart_start_idx, min(chart_start_idx + 5, len(lines))):
                if '<h3 style="text-align: center; color: #333; margin-bottom: 10px;">云·王者荣耀世界 - 游戏 (免费) 榜单曲线图</h3>' in lines[i]:
                    lines[i] = lines[i].replace(
                        '<h3 style="text-align: center; color: #333; margin-bottom: 10px;">云·王者荣耀世界 - 游戏 (免费) 榜单曲线图</h3>',
                        '<h2 class="section-title">云·王者荣耀世界 - 游戏 (免费) 榜单曲线图</h2>'
                    )
                    break
            
            # 在曲线图结束后添加 </div> 来关闭 section
            # 找到曲线图的结束位置（数据来源之后）
            for i in range(chart_start_idx, min(chart_start_idx + 30, len(lines))):
                if '<p class="chart-data-source">数据来源：七麦数据</p>' in lines[i]:
                    # 在这行之后添加 </div>
                    lines.insert(i + 1, '            </div>\n\n')
                    break
            
            print("✅ 结构修改完成")
            
            # 写回文件
            with open(html_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            
            print("💾 文件已保存")
        else:
            print("❌ 未找到总结内容行")
    else:
        print("⚠️ 前一行不是 </div>，结构可能已经正确")
else:
    print("❌ 无法定位关键位置")

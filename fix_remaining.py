#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复剩余问题
"""

html_path = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/index_with_tabs.html'

with open(html_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    
    # 移除多余的 </div>（第 389 行位置）
    if line.strip() == '</div>' and i > 0 and '</div>' in lines[i-1]:
        # 这是连续的第二个</div>，跳过
        i += 1
        continue
    
    # 将曲线图的 h3 改为 h2
    if '<h3 style="text-align: center; color: #333; margin-bottom: 10px;">云·王者荣耀世界 - 游戏 (免费) 榜单曲线图</h3>' in line:
        line = '                <h2 class="section-title">云·王者荣耀世界 - 游戏 (免费) 榜单曲线图</h2>\n'
    
    # 在曲线图数据源后添加缺失的</div>
    if '<p class="chart-data-source">数据来源：七麦数据</p>' in line:
        new_lines.append(line)
        i += 1
        # 下一行应该是</div>（关闭图表容器），再下一行需要添加</div>（关闭 section）
        if i < len(lines):
            new_lines.append(lines[i])  # 保留关闭图表容器的</div>
            i += 1
            # 添加关闭 section 的</div>
            new_lines.append('            </div>\n\n')
        continue
    
    new_lines.append(line)
    i += 1

# 写回文件
with open(html_path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("✅ 剩余问题已修复！")

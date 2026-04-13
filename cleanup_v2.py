#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清理曲线图板块重复的标题 - v2 逐行处理
"""

html_path = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/index_with_tabs.html'

with open(html_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip_until_div_close = False

for i, line in enumerate(lines):
    # 跳过多余的 div style="margin-top: 30px;"
    if '<div style="margin-top: 30px;">' in line:
        skip_until_div_close = True
        continue
    
    # 跳过重复的 h3 标题
    if '<h3 style="text-align: center; color: #333; margin-bottom: 10px;">云·王者荣耀世界 - 游戏 (免费) 榜单曲线图</h3>' in line:
        continue
    
    # 找到对应的 </div> 关闭标签
    if skip_until_div_close and line.strip() == '</div>':
        skip_until_div_close = False
        # 检查下一行是否是 section 的关闭标签
        if i + 1 < len(lines) and lines[i + 1].strip() == '</div>':
            # 保留这个 </div> 作为 section 的关闭
            new_lines.append('            </div>\n\n')
            continue
        continue
    
    # 其他行保持不变
    new_lines.append(line)

# 写回文件
with open(html_path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("✅ 清理完成！")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
手动精确修复 HTML 结构
基于已知的行号进行修改
"""

html_path = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/index_with_tabs.html'

with open(html_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 输出关键行以便确认
print("📋 原始关键行内容:")
for i in [381, 382, 383, 384, 385, 386]:
    if i <= len(lines):
        print(f"第{i+1}行：{repr(lines[i])}")

# 修改第 383 行（索引 382）：在总结内容前添加 section-content
if '<h2 class="section-title">总结</h2>' in lines[382]:
    # 在第 384 行（索引 383）前插入 section-content 开始标签
    original_content = lines[383]
    lines[383] = '                <div class="section-content">\n' + original_content
    print("\n✅ 已添加 section-content 开始标签")

# 找到</p>并替换
for i in range(384, 390):
    if i < len(lines) and '</p>' in lines[i]:
        lines[i] = lines[i].replace('</p>', '\n                </div>')
        print(f"✅ 已将第{i+1}行的</p>改为</div>")
        break

# 找到曲线图注释，在它前面添加闭合标签和新的 section
for i in range(385, 395):
    if i < len(lines) and '<!-- 榜单曲线图 -->' in lines[i]:
        # 在曲线图注释前插入：空行 + </div>（关闭总结 section）+ 空行 + <div class="section">
        lines[i] = '\n            </div>\n\n            <!-- 榜单曲线图 -->\n            <div class="section">\n'
        print(f"✅ 已在第{i+1}行位置添加 section 分隔")
        break

# 找到曲线图的 h3 并改为 h2
for i in range(385, min(400, len(lines))):
    if '<h3 style="text-align: center; color: #333; margin-bottom: 10px;">云·王者荣耀世界 - 游戏 (免费) 榜单曲线图</h3>' in lines[i]:
        lines[i] = '                <h2 class="section-title">云·王者荣耀世界 - 游戏 (免费) 榜单曲线图</h2>\n'
        print(f"✅ 已将第{i+1}行的 h3 改为 h2")
        break

# 写回文件
with open(html_path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("\n💾 文件已保存")

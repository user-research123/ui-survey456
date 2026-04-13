#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 读取文件
with open('wangzhe_report/index_with_tabs.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 找到包含"4 月 1 日"的行号
target_line_idx = None
for i, line in enumerate(lines):
    if '4 月 1 日</div>' in line and 'timeline-date' in line:
        # 确认这是在官方事件板块（在竞品动态之前）
        # 检查前面几行是否有"游戏官方事件/活动"
        context = ''.join(lines[max(0, i-10):i])
        if '游戏官方事件/活动' in context and '竞品动态追踪' not in context:
            target_line_idx = i
            break

if target_line_idx is None:
    print("❌ 未找到目标位置")
    exit(1)

# 构建新的事件 HTML（带缩进）
new_lines = [
    '                    <div class="timeline-item">\n',
    '                        <div class="timeline-date">4 月 7 日</div>\n',
    '                        <div class="timeline-content">\n',
    '                            <p style="margin: 0; color: #4a5568;">《王者荣耀世界》PC 端预下载将于 4 月 7 日上午 10:00 开启</p>\n',
    '                        </div>\n',
    '                    </div>\n'
]

# 在目标行之前插入新内容
lines[target_line_idx:target_line_idx] = new_lines

# 写回文件
with open('wangzhe_report/index_with_tabs.html', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print(f"✅ 已成功添加 PC 端预下载信息到 4 月 7 日（在第{target_line_idx+1}行前插入）")

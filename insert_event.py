#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 读取文件
with open('wangzhe_report/index_with_tabs.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 在第 411 行之前插入新的 4 月 7 日事件（即在 4 月 1 日之前）
# 新事件的格式与现有格式完全一致
new_event_lines = [
    '                    <div class="timeline-item">\n',
    '                        <div class="timeline-date">4 月 7 日</div>\n',
    '                        <div class="timeline-content">\n',
    '                            <p style="margin: 0; color: #4a5568;">《王者荣耀世界》PC 端预下载将于 4 月 7 日上午 10:00 开启</p>\n',
    '                        </div>\n',
    '                    </div>\n'
]

# 在索引 410（第 411 行）之前插入
lines[410:410] = new_event_lines

# 写回文件
with open('wangzhe_report/index_with_tabs.html', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("✅ 已成功添加 PC 端预下载信息到 4 月 7 日")
print(f"   文件现在共有 {len(lines)} 行")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

# 读取文件
with open('wangzhe_report/index_with_tabs.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 要插入的新事件 HTML
new_event = '''                    <div class="timeline-item">
                        <div class="timeline-date">4 月 7 日</div>
                        <div class="timeline-content">
                            <p style="margin: 0; color: #4a5568;">《王者荣耀世界》PC 端预下载将于 4 月 7 日上午 10:00 开启</p>
                        </div>
                    </div>
'''

# 查找 4 月 1 日的事件，在其前面插入新事件
pattern = r'(<div class="timeline">\n                    <div class="timeline-item">\n                        <div class="timeline-date">4 月 1 日</div>)'
replacement = new_event + r'\1'

# 替换
new_content = re.sub(pattern, replacement, content)

# 写回文件
with open('wangzhe_report/index_with_tabs.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("✅ 已成功添加 PC 端预下载信息到 4 月 7 日")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 读取文件
with open('wangzhe_report/index_with_tabs.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 目标字符串（4 月 1 日的完整 timeline-item）
old_string = '''                    <div class="timeline-item">
                        <div class="timeline-date">4 月 1 日</div>
                        <div class="timeline-content">
                            <p style="margin: 0; color: #4a5568;">【王者荣耀世界】峡谷外相遇组队活动公告</p>
                        </div>
                    </div>'''

# 新字符串（添加 4 月 7 日的内容）
new_string = '''                    <div class="timeline-item">
                        <div class="timeline-date">4 月 7 日</div>
                        <div class="timeline-content">
                            <p style="margin: 0; color: #4a5568;">《王者荣耀世界》PC 端预下载将于 4 月 7 日上午 10:00 开启</p>
                        </div>
                    </div>
                    <div class="timeline-item">
                        <div class="timeline-date">4 月 1 日</div>
                        <div class="timeline-content">
                            <p style="margin: 0; color: #4a5568;">【王者荣耀世界】峡谷外相遇组队活动公告</p>
                        </div>
                    </div>'''

# 替换
if old_string in content:
    new_content = content.replace(old_string, new_string, 1)
    
    # 写回文件
    with open('wangzhe_report/index_with_tabs.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("✅ 已成功添加 PC 端预下载信息到 4 月 7 日")
else:
    print("❌ 未找到目标字符串")
    print("正在查找原因...")
    if '4 月 1 日' in content:
        print("- 文件中包含'4 月 1 日'")
    if '峡谷外相遇' in content:
        print("- 文件中包含'峡谷外相遇'")

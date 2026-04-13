#!/usr/bin/env python3
# 在用户需求追踪板块添加 4 月 7 日按钮

file_path = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/index_with_tabs.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 替换：在 4 月 8 日和 4 月 6 日之间插入 4 月 7 日按钮
old_line = '''                    <button class="date-tab active" onclick="showUserFeedbackDate('04-08')">4 月 8 日</button>
                    <button class="date-tab " onclick="showUserFeedbackDate('04-06')">4 月 6 日</button>'''

new_line = '''                    <button class="date-tab active" onclick="showUserFeedbackDate('04-08')">4 月 8 日</button>
                    <button class="date-tab " onclick="showUserFeedbackDate('04-07')">4 月 7 日</button>
                    <button class="date-tab " onclick="showUserFeedbackDate('04-06')">4 月 6 日</button>'''

if old_line in content:
    content = content.replace(old_line, new_line)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("✓ 成功添加 4 月 7 日按钮")
else:
    print("✗ 未找到匹配的行")

# 修复 4 月 7 日内容块中的日期标签
old_date_label = '<div class="timeline-date">4 月 8 日</div>'
new_date_label = '<div class="timeline-date">4 月 7 日</div>'

# 查找所有 user-feedback-04-07 后面的日期标签
import re
pattern = r'(<div id="user-feedback-04-07"[^>]*>.*?<div class="timeline">.*?<div class="timeline-item">.*?<div class="timeline-date">)4 月 8 日 (</div>)'
matches = list(re.finditer(pattern, content, flags=re.DOTALL))

if matches:
    # 只替换第一个匹配项（4 月 7 日内容块中的）
    match = matches[0]
    start = match.start()
    end = match.end()
    replacement = match.group(1) + '4 月 7 日' + match.group(2)
    content = content[:start] + replacement + content[end:]
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("✓ 成功修复 4 月 7 日内容块的日期标签")
else:
    print("✗ 未找到需要修复的日期标签")

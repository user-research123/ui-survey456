#!/usr/bin/env python3
"""修复竞品动态追踪板块 4 月 7 日内容块的日期标签"""

file_path = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/index_with_tabs.html'

# 读取所有字节
with open(file_path, 'rb') as f:
    content = f.read()

# 在 competitor-04-07 的上下文中查找并替换日期标签
# 注意：只替换 4 月 7 日内容块中的错误日期，不影响 4 月 8 日的内容
target_context = b'<div id="competitor-04-07" class="competitor-date-content active">\n                    <div class="timeline">\n                        <div class="timeline-item">\n                            <div class="timeline-date">4\xe6\x9c\x888\xe6\x97\xa5</div>'
replacement = b'<div id="competitor-04-07" class="competitor-date-content active">\n                    <div class="timeline">\n                        <div class="timeline-item">\n                            <div class="timeline-date">4\xe6\x9c\x887\xe6\x97\xa5</div>'

if target_context in content:
    print("✓ 找到 4 月 7 日内容块的错误日期标签")
    new_content = content.replace(target_context, replacement)
    
    # 写回文件
    with open(file_path, 'wb') as f:
        f.write(new_content)
    
    print("✓ 成功将日期标签从'4 月 8 日'改为'4 月 7 日'")
else:
    print("✗ 未找到目标上下文")

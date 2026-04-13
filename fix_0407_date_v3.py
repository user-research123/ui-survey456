#!/usr/bin/env python3
# 修复 4 月 7 日内容块中的日期标签（字节级精确）

file_path = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/index_with_tabs.html'

with open(file_path, 'rb') as f:
    content = f.read()

# 查找并替换 4 月 7 日内容块中的日期标签
# 先找到 user-feedback-04-07 的位置
pos_0407 = content.find(b'user-feedback-04-07')
if pos_0407 == -1:
    print("✗ 未找到 user-feedback-04-07")
    exit(1)

# 在这个位置之后查找 timeline-date
pos_timeline = content.find(b'<div class="timeline-date">', pos_0407)
if pos_timeline == -1:
    print("✗ 未找到 timeline-date")
    exit(1)

# 检查后面的日期
pos_date = pos_timeline + len(b'<div class="timeline-date">')
date_end = content.find(b'</div>', pos_date)
current_date = content[pos_date:date_end]
print(f"当前日期：{current_date.decode('utf-8')}")

# 如果是 4 月 8 日，则替换为 4 月 7 日
if current_date == b'4\xe6\x9c\x888\xe6\x97\xa5':  # UTF-8 encoding of "4 月 8 日"
    new_content = content[:pos_date] + b'4\xe6\x9c\x887\xe6\x97\xa5' + content[date_end:]  # "4 月 7 日"
    with open(file_path, 'wb') as f:
        f.write(new_content)
    print("✓ 成功将 4 月 8 日改为 4 月 7 日")
else:
    print(f"日期已经是：{current_date.decode('utf-8')}")

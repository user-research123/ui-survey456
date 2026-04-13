#!/usr/bin/env python3
file_path = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/index_with_tabs.html'
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 检查第 1304 行
line_1304 = lines[1303]
print("Line 1304:", line_1304.strip())

# 查找所有用户反馈按钮
for i, line in enumerate(lines, 1):
    if "user-feedback-date-tabs" in line.lower() or (i >= 1303 and i <= 1315):
        print(f"Line {i}: {line.rstrip()}")

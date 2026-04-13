#!/usr/bin/env python3
file_path = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/index_with_tabs.html'
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines, 1):
    if "showUserFeedbackDate('04-08')" in line:
        print(f"Line {i}: {line.strip()}")

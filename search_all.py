#!/usr/bin/env python3
file_path = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/index_with_tabs.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 搜索所有包含 04-08 的模式
import re
pattern = r"04-08[^\n]*button"
matches = re.findall(pattern, content)
print("All patterns with 04-08:")
for i, match in enumerate(matches):
    print(f"{i}: {repr(match)}")

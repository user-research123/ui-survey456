#!/usr/bin/env python3
file_path = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/index_with_tabs.html'

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

line_1304 = lines[1303]
print("Original line:")
print(repr(line_1304))
print()

# 尝试不同的替换
test1 = line_1304.replace("4 月 7 日", "4 月 8 日")
print(f"After replace('4 月 7 日', '4 月 8 日'): {repr(test1)}")

test2 = line_1304.replace("7 日", "8 日")
print(f"After replace('7 日', '8 日'): {repr(test2)}")

# 检查是否包含这些字符串
print(f"\nContains '4 月 7 日': {'4 月 7 日' in line_1304}")
print(f"Contains '7 日': {'7 日' in line_1304}")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 读取文件
with open('wangzhe_report/index_with_tabs.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 打印所有包含"4 月 1 日"的行
print("=== 包含'4 月 1 日'的行 ===")
for i, line in enumerate(lines):
    if '4 月 1 日' in line:
        print(f"行 {i+1}: {repr(line)}")

print("\n=== 官方事件板块附近的内容（405-430 行）===")
for i in range(404, min(430, len(lines))):
    print(f"{i+1}: {repr(lines[i])}")

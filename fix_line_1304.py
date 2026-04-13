#!/usr/bin/env python3
file_path = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/index_with_tabs.html'

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 修改第 1304 行（索引 1303）
old_line = lines[1303]
new_line = old_line.replace("4 月 7 日", "4 月 8 日")

print(f"Old line 1304: {old_line.strip()}")
print(f"New line 1304: {new_line.strip()}")

lines[1303] = new_line

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("\n✅ Fixed line 1304!")

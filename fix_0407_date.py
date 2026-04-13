#!/usr/bin/env python3
# 修复 4 月 7 日内容块中的日期标签

file_path = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/index_with_tabs.html'

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 找到 user-feedback-04-07 后面的 timeline-date 行并修改
for i, line in enumerate(lines):
    if 'user-feedback-04-07' in line:
        # 在接下来的几行中查找 timeline-date
        for j in range(i, min(i+10, len(lines))):
            if '<div class="timeline-date">' in lines[j]:
                print(f"第 {j+1} 行原始内容：{lines[j].strip()}")
                lines[j] = lines[j].replace('4 月 8 日', '4 月 7 日')
                print(f"修改后内容：{lines[j].strip()}")
                break
        break

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("✓ 完成修复")

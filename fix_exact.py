#!/usr/bin/env python3
file_path = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/index_with_tabs.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 使用提取的精确文本
old_text = "showUserFeedbackDate('04-08')\">4 月 7 日</button>"
new_text = "showUserFeedbackDate('04-08')\">4 月 8 日</button>"

count = content.count(old_text)
print(f"Found '{old_text}': {count} times")

if count > 0:
    content = content.replace(old_text, new_text)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ Replaced successfully!")
else:
    print("❌ Not found in file")

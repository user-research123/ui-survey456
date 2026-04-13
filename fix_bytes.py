#!/usr/bin/env python3
"""使用字节级替换修复按钮文本"""

file_path = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/index_with_tabs.html'

# 读取所有字节
with open(file_path, 'rb') as f:
    content = f.read()

# 要查找和替换的字节序列
# 4 月 8 日的 UTF-8: 34 e6 9c 88 38 e6 97 a5
old_bytes = b'4\xe6\x9c\x888\xe6\x97\xa5'  # 4 月 8 日
new_bytes = b'4\xe6\x9c\x887\xe6\x97\xa5'  # 4 月 7 日

print(f"查找字节：{old_bytes.hex()}")
print(f"替换字节：{new_bytes.hex()}")

# 在包含 showCompetitorDate('04-07') 的上下文中查找
target_context = b"showCompetitorDate('04-07')\">4\xe6\x9c\x888\xe6\x97\xa5</button>"
replacement = b"showCompetitorDate('04-07')\">4\xe6\x9c\x887\xe6\x97\xa5</button>"

if target_context in content:
    print("\n✓ 找到目标上下文")
    new_content = content.replace(target_context, replacement)
    
    # 写回文件
    with open(file_path, 'wb') as f:
        f.write(new_content)
    
    print("✓ 成功替换！")
else:
    print("\n✗ 未找到目标上下文")
    # 尝试只查找日期部分
    if old_bytes in content:
        print("  但找到了日期字节序列")
        count = content.count(old_bytes)
        print(f"  出现次数：{count}")

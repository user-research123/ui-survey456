#!/usr/bin/env python3
import re

test_line = '''<button class="date-tab" onclick="showCompetitorDate('04-07')">4 月 8 日</button>\n'''

print(f"测试字符串：{repr(test_line)}")

# 尝试不同的正则模式
patterns = [
    r'(showCompetitorDate\(\'04-07\'\)">)4 月 [0-9] 日 (</button>)',
    r'(\'>)4 月 [0-9] 日 (</button>)',
    r'>4 月 [0-9] 日<',
    r'4 月 8 日',
]

for pattern in patterns:
    match = re.search(pattern, test_line)
    print(f"\n模式：{pattern}")
    print(f"匹配结果：{match}")
    if match:
        print(f"匹配内容：{repr(match.group())}")
        
# 直接替换
new_line = test_line.replace("4 月 8 日", "4 月 7 日")
print(f"\n直接替换结果：{repr(new_line)}")

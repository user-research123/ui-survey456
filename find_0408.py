#!/usr/bin/env python3
file_path = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/index_with_tabs.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 找到 4 月 8 日的位置
idx = content.find("4 月 8 日</button>")
if idx >= 0:
    # 前后各取 100 个字符
    start = max(0, idx - 100)
    end = min(len(content), idx + 50)
    print("Context around '4 月 8 日</button>':")
    print(repr(content[start:end]))
    
    # 计算行号
    line_num = content[:idx].count('\n') + 1
    print(f"\nLine number: {line_num}")
else:
    print("Not found!")

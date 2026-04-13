#!/usr/bin/env python3
file_path = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/index_with_tabs.html'

with open(file_path, 'rb') as f:
    lines = f.readlines()

line_1304 = lines[1303]
print("Bytes:", line_1304)
print()

# 查找 "4 月" 的字节
idx_4yue = line_1304.find(b'4\xe6\x9c\x88')
if idx_4yue >= 0:
    print(f"Found '4 月' at byte {idx_4yue}")
    # 打印后面的字节
    snippet = line_1304[idx_4yue:idx_4yue+20]
    print(f"Snippet bytes: {snippet}")
    print(f"Snippet hex: {snippet.hex()}")
    
    # 尝试解码
    try:
        decoded = snippet.decode('utf-8')
        print(f"Decoded: {repr(decoded)}")
    except Exception as e:
        print(f"Decode error: {e}")

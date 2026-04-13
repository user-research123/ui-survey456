#!/usr/bin/env python3
line_num = 438  # 0-based

with open('/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/index_with_tabs.html', 'rb') as f:
    lines = f.readlines()

if line_num < len(lines):
    line_bytes = lines[line_num]
    print(f"第 {line_num + 1} 行原始字节:")
    print(f"  {line_bytes}")
    print(f"\n十六进制:")
    print(f"  {line_bytes.hex()}")
    
    # 尝试解码
    try:
        line_str = line_bytes.decode('utf-8')
        print(f"\nUTF-8 解码:")
        print(f"  {repr(line_str)}")
        
        # 查找日期部分
        import re
        match = re.search(r'>([^<]+)</button>', line_str)
        if match:
            date_text = match.group(1)
            print(f"\n按钮文本：{repr(date_text)}")
            print(f"字符编码：{[hex(ord(c)) for c in date_text]}")
    except Exception as e:
        print(f"解码失败：{e}")

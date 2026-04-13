#!/usr/bin/env python3
file_path = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/index_with_tabs.html'
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    line_1304 = lines[1303]
    
    # 逐个字符打印
    start = line_1304.find('showUserFeedbackDate')
    end = line_1304.find('</button>') + len('</button>')
    text = line_1304[start:end]
    
    print("Characters:")
    for i, char in enumerate(text):
        print(f"{i:3d}: '{char}' (U+{ord(char):04X})")

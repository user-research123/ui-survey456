#!/usr/bin/env python3
file_path = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/index_with_tabs.html'
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    line_1304 = lines[1303]
    # 提取按钮部分
    start = line_1304.find('showUserFeedbackDate')
    end = line_1304.find('</button>') + len('</button>')
    print("Exact text:", repr(line_1304[start:end]))

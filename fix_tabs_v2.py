#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复用户需求追踪板块的日期按钮问题
"""

file_path = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/index_with_tabs.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 修复 1: 将第一个按钮的文本从 4 月 7 日改为 4 月 8 日
content = content.replace(
    '''onclick="showUserFeedbackDate('04-08')">4 月 7 日</button>''',
    '''onclick="showUserFeedbackDate('04-08')">4 月 8 日</button>'''
)

# 修复 2: 确保 4 月 7 日内容块没有 active 类 (已经处理过，再次确认)
content = content.replace(
    '''id="user-feedback-04-07" class="user-feedback-date-content active">''',
    '''id="user-feedback-04-07" class="user-feedback-date-content ">'''
)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ 修复完成！")

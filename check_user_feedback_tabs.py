#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查用户需求追踪部分的日期按钮是否存在
"""

import re

html_file = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/index_with_tabs.html'

with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

print("=" * 60)
print("用户需求追踪 - 日期按钮检查报告")
print("=" * 60)

# 检查日期按钮容器
if 'id="user-feedback-date-tabs"' in content:
    print("✓ 日期按钮容器ID存在: user-feedback-date-tabs")
else:
    print("✗ 日期按钮容器ID缺失")

# 检查日期按钮
date_buttons = re.findall(r'onclick="showUserFeedbackDate\(\'([^\']+)\'\)"', content)
print(f"\n✓ 找到 {len(date_buttons)} 个日期按钮:")
for btn in date_buttons:
    print(f"  - {btn}")

# 检查内容区块
content_blocks = re.findall(r'id="user-feedback-([^"]+)" class="user-feedback-date-content', content)
print(f"\n✓ 找到 {len(content_blocks)} 个内容区块:")
for block in content_blocks:
    print(f"  - {block}")

# 检查JavaScript函数
if 'function showUserFeedbackDate(dateId)' in content:
    print("\n✓ JavaScript函数 showUserFeedbackDate() 存在")
else:
    print("\n✗ JavaScript函数 showUserFeedbackDate() 缺失")

# 检查CSS样式
if '.user-feedback-date-content {' in content:
    print("✓ CSS样式 .user-feedback-date-content 存在")
else:
    print("✗ CSS样式 .user-feedback-date-content 缺失")

print("\n" + "=" * 60)
print("检查完成")
print("=" * 60)

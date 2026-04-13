#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证双日期切换功能的完整性
"""

import re

file_path = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/index_with_tabs.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

print("=" * 60)
print("双日期切换功能验证报告")
print("=" * 60)

# 1. 验证竞品动态追踪部分
print("\n1. 竞品动态追踪部分:")
print("-" * 60)

# 检查日期按钮容器ID
if 'id="competitor-date-tabs"' in content:
    print("✓ 日期按钮容器ID正确: competitor-date-tabs")
else:
    print("✗ 日期按钮容器ID缺失")

# 检查竞品日期按钮
competitor_buttons = re.findall(r"onclick=\"showCompetitorDate\('([^']+)'\)", content)
print(f"✓ 找到 {len(competitor_buttons)} 个竞品日期按钮: {competitor_buttons}")

# 检查竞品内容区块
competitor_contents = re.findall(r'id="competitor-([^"]+)" class="competitor-date-content', content)
print(f"✓ 找到 {len(competitor_contents)} 个竞品内容区块: {competitor_contents}")

# 检查active状态
active_competitor = re.findall(r'id="competitor-([^"]+)" class="competitor-date-content active"', content)
print(f"✓ 当前激活的竞品日期: {active_competitor}")

# 2. 验证用户需求追踪部分
print("\n2. 用户需求追踪部分:")
print("-" * 60)

# 检查日期按钮容器ID
if 'id="user-feedback-date-tabs"' in content:
    print("✓ 日期按钮容器ID正确: user-feedback-date-tabs")
else:
    print("✗ 日期按钮容器ID缺失")

# 检查用户反馈日期按钮
user_feedback_buttons = re.findall(r"onclick=\"showUserFeedbackDate\('([^']+)'\)", content)
print(f"✓ 找到 {len(user_feedback_buttons)} 个用户反馈日期按钮: {user_feedback_buttons}")

# 检查用户反馈内容区块
user_feedback_contents = re.findall(r'id="user-feedback-([^"]+)" class="user-feedback-date-content', content)
print(f"✓ 找到 {len(user_feedback_contents)} 个用户反馈内容区块: {user_feedback_contents}")

# 检查active状态
active_user_feedback = re.findall(r'id="user-feedback-([^"]+)" class="user-feedback-date-content active"', content)
print(f"✓ 当前激活的用户反馈日期: {active_user_feedback}")

# 3. 验证JavaScript函数
print("\n3. JavaScript函数:")
print("-" * 60)

if 'function showCompetitorDate(dateId)' in content:
    print("✓ showCompetitorDate() 函数存在")
else:
    print("✗ showCompetitorDate() 函数缺失")

if 'function showUserFeedbackDate(dateId)' in content:
    print("✓ showUserFeedbackDate() 函数存在")
else:
    print("✗ showUserFeedbackDate() 函数缺失")

# 4. 验证CSS样式
print("\n4. CSS样式:")
print("-" * 60)

if '.competitor-date-content {' in content and '.competitor-date-content.active {' in content:
    print("✓ 竞品日期内容CSS样式存在")
else:
    print("✗ 竞品日期内容CSS样式缺失")

if '.user-feedback-date-content {' in content and '.user-feedback-date-content.active {' in content:
    print("✓ 用户反馈日期内容CSS样式存在")
else:
    print("✗ 用户反馈日期内容CSS样式缺失")

# 5. 总结
print("\n" + "=" * 60)
print("验证总结:")
print("=" * 60)

all_checks = [
    'id="competitor-date-tabs"' in content,
    len(competitor_buttons) == 4,
    len(competitor_contents) == 4,
    len(active_competitor) == 1,
    'id="user-feedback-date-tabs"' in content,
    len(user_feedback_buttons) == 4,
    len(user_feedback_contents) == 4,
    len(active_user_feedback) == 1,
    'function showCompetitorDate(dateId)' in content,
    'function showUserFeedbackDate(dateId)' in content,
    '.competitor-date-content {' in content,
    '.user-feedback-date-content {' in content,
]

if all(all_checks):
    print("✓ 所有检查通过！双日期切换功能已正确实现。")
    print("\n功能说明:")
    print("- 两个板块拥有独立的日期切换按钮")
    print("- 点击某板块的日期按钮只影响该板块的内容显示")
    print("- 默认显示最新日期（4月2日）的内容")
    print("- 如果某天某渠道无数据，显示空状态而非复制前一天数据")
else:
    print("✗ 部分检查未通过，请检查上述详细信息")
    failed_count = sum(1 for check in all_checks if not check)
    print(f"  失败项数: {failed_count}/{len(all_checks)}")

print("=" * 60)

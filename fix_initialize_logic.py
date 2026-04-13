#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复 initializeActiveTabs 函数的回退逻辑
在激活第一个内容之前,先隐藏所有内容区块
"""

import re

file_path = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/index_with_tabs.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 修复竞品动态追踪的回退逻辑
old_competitor = """            } else {
                console.log(`⚠ 未找到 ${month}月${day}日 的竞品内容，回退到最新日期`);
                // 回退到第一个可用的内容（通常是最新的）
                const firstCompetitorContent = document.querySelector('.competitor-date-content');"""

new_competitor = """            } else {
                console.log(`⚠ 未找到 ${month}月${day}日 的竞品内容，回退到最新日期`);
                // 先隐藏所有竞品内容
                document.querySelectorAll('.competitor-date-content').forEach(c => c.classList.remove('active'));
                // 回退到第一个可用的内容（通常是最新的）
                const firstCompetitorContent = document.querySelector('.competitor-date-content');"""

content = content.replace(old_competitor, new_competitor)

# 修复用户需求追踪的回退逻辑
old_user = """            } else {
                console.log(`⚠ 未找到 ${month}月${day}日 的用户需求内容，回退到最新日期`);
                // 回退到第一个可用的内容（通常是最新的）
                const firstUserFeedbackContent = document.querySelector('.user-feedback-date-content');"""

new_user = """            } else {
                console.log(`⚠ 未找到 ${month}月${day}日 的用户需求内容，回退到最新日期`);
                // 先隐藏所有用户反馈内容
                document.querySelectorAll('.user-feedback-date-content').forEach(c => c.classList.remove('active'));
                // 回退到第一个可用的内容（通常是最新的）
                const firstUserFeedbackContent = document.querySelector('.user-feedback-date-content');"""

content = content.replace(old_user, new_user)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ 修复完成！")
print("已添加隐藏逻辑到两个回退分支")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复竞品动态追踪和用户需求追踪模块的日期切换功能：
1. 确保所有日期内容区块使用正确的 class 名称
2. 移除所有 active 类，只给最新日期（04-09）添加 active
3. 添加 JavaScript 初始化代码
"""

import re

file_path = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/index_with_tabs.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 修复 competitor-04-09 的 class
content = re.sub(
    r'id="competitor-04-09"\s+class="date-content"\s+style="display:\s*block;"',
    'id="competitor-04-09" class="competitor-date-content active"',
    content
)

# 2. 移除 competitor-04-08 的 active 类
content = re.sub(
    r'id="competitor-04-08"\s+class="competitor-date-content\s+active"',
    'id="competitor-04-08" class="competitor-date-content"',
    content
)

# 3. 移除 competitor-04-07 的 active 类
content = re.sub(
    r'id="competitor-04-07"\s+class="competitor-date-content\s+active"',
    'id="competitor-04-07" class="competitor-date-content"',
    content
)

# 4. 检查并修复 user-feedback-04-09 的 class（如果有类似问题）
content = re.sub(
    r'id="user-feedback-04-09"\s+class="date-content"\s+style="display:\s*block;"',
    'id="user-feedback-04-09" class="user-feedback-date-content active"',
    content
)

# 5. 查找 JavaScript 插入位置 - 在 showUserFeedbackDate 函数之后，榜单曲线图之前
js_init_code = '''
        // 页面加载时初始化：只显示最新日期的内容
        function initDateTabs() {
            // 竞品动态追踪：只保留 04-09 的 active 状态
            document.querySelectorAll('.competitor-date-content').forEach(el => {
                el.classList.remove('active');
            });
            const latestCompetitor = document.getElementById('competitor-04-09');
            if (latestCompetitor) {
                latestCompetitor.classList.add('active');
            }
            
            // 重置竞品日期按钮状态
            document.querySelectorAll('#competitor-date-tabs .date-tab').forEach(el => {
                el.classList.remove('active');
            });
            const latestCompetitorBtn = document.querySelector('#competitor-date-tabs .date-tab:first-child');
            if (latestCompetitorBtn) {
                latestCompetitorBtn.classList.add('active');
            }
            
            // 用户需求追踪：只保留 04-09 的 active 状态
            document.querySelectorAll('.user-feedback-date-content').forEach(el => {
                el.classList.remove('active');
            });
            const latestFeedback = document.getElementById('user-feedback-04-09');
            if (latestFeedback) {
                latestFeedback.classList.add('active');
            }
            
            // 重置用户反馈日期按钮状态
            document.querySelectorAll('#user-feedback-date-tabs .date-tab').forEach(el => {
                el.classList.remove('active');
            });
            const latestFeedbackBtn = document.querySelector('#user-feedback-date-tabs .date-tab:first-child');
            if (latestFeedbackBtn) {
                latestFeedbackBtn.classList.add('active');
            }
        }

'''

# 在 showUserFeedbackDate 函数结束后插入 initDateTabs 函数
# 查找 showUserFeedbackDate 函数的结束位置和榜单曲线图代码的开始位置
pattern = r'(function showUserFeedbackDate\(dateId\)\s*\{[^}]*\}\n\n\s*//\s*榜单曲线图绘制代码)'
replacement = r'\1\n\n' + js_init_code

content = re.sub(pattern, replacement, content, flags=re.DOTALL)

# 6. 在 window.onload 或 IIFE 结束时调用 initDateTabs
# 查找 createChart(); 后面的位置，添加 initDateTabs() 调用
content = re.sub(
    r'(createChart\(\);\n\n\s*//\s*响应式调整)',
    'initDateTabs();\n\n        \\1',
    content
)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ 修复完成！")
print("- 已修复 competitor-04-09 的 class 名称")
print("- 已移除 competitor-04-08 和 competitor-04-07 的 active 类")
print("- 已添加 initDateTabs 初始化函数")
print("- 已在页面加载时调用 initDateTabs()")

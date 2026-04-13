#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为竞品动态追踪和用户需求追踪板块添加自动 active 逻辑
1. 移除 HTML 中硬编码的 active 类
2. 添加页面加载时的自动初始化函数
"""

import re
from datetime import datetime

file_path = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/index_with_tabs.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 移除竞品动态追踪按钮的 active 类（但保留第一个按钮作为 fallback）
# 找到所有竞品按钮，只保留第一个按钮的 active 类
competitor_buttons_pattern = r'(<button class="date-tab)(?: active)?( onclick="showCompetitorDate\([^\)]+\)">)'
competitor_button_matches = list(re.finditer(competitor_buttons_pattern, content))

if competitor_button_matches:
    # 第一个按钮保留 active，其他移除
    for i, match in enumerate(competitor_button_matches[1:], 1):
        start = match.start()
        end = match.end()
        old_text = content[start:end]
        new_text = old_text.replace(' active', '')
        content = content[:start] + new_text + content[end:]
    print(f"✓ 已处理竞品按钮：保留第 1 个 active，移除后续 {len(competitor_button_matches)-1} 个 active")

# 2. 移除用户需求追踪按钮的 active 类（但保留第一个按钮作为 fallback）
user_feedback_buttons_pattern = r'(<button class="date-tab)(?: active)?( onclick="showUserFeedbackDate\([^\)]+\)">)'
user_feedback_button_matches = list(re.finditer(user_feedback_buttons_pattern, content))

if user_feedback_button_matches:
    # 第一个按钮保留 active，其他移除
    for i, match in enumerate(user_feedback_button_matches[1:], 1):
        start = match.start()
        end = match.end()
        old_text = content[start:end]
        new_text = old_text.replace(' active', '')
        content = content[:start] + new_text + content[end:]
    print(f"✓ 已处理用户反馈按钮：保留第 1 个 active，移除后续 {len(user_feedback_button_matches)-1} 个 active")

# 3. 移除所有内容块的 active 类
content = re.sub(r'(class="competitor-date-content )active(")', r'\1\2', content)
content = re.sub(r'(class="user-feedback-date-content )active(")', r'\1\2', content)
print("✓ 已移除所有内容块的 active 类")

# 4. 在 showUserFeedbackDate 函数后添加初始化函数
init_function = '''
        // 页面加载时自动设置当天日期为 active
        function initializeActiveTabs() {
            const today = new Date();
            const month = String(today.getMonth() + 1).padStart(2, '0');
            const day = String(today.getDate()).padStart(2, '0');
            const todayId = `${month}-${day}`;
            
            console.log(`初始化日期标签：今天是 ${month}月${day}日 (ID: ${todayId})`);
            
            // 初始化竞品动态追踪
            const competitorContent = document.getElementById('competitor-' + todayId);
            if (competitorContent) {
                // 隐藏所有竞品内容
                document.querySelectorAll('.competitor-date-content').forEach(c => c.classList.remove('active'));
                // 显示今天的内容
                competitorContent.classList.add('active');
                
                // 激活对应的按钮
                document.querySelectorAll('#competitor-date-tabs .date-tab').forEach(tab => {
                    tab.classList.remove('active');
                    if (tab.getAttribute('onclick').includes(todayId)) {
                        tab.classList.add('active');
                    }
                });
                console.log(`✓ 竞品动态追踪已设置为 ${month}月${day}日`);
            } else {
                console.log(`⚠ 未找到 ${month}月${day}日 的竞品内容，使用默认`);
            }
            
            // 初始化用户需求追踪
            const userFeedbackContent = document.getElementById('user-feedback-' + todayId);
            if (userFeedbackContent) {
                // 隐藏所有用户反馈内容
                document.querySelectorAll('.user-feedback-date-content').forEach(c => c.classList.remove('active'));
                // 显示今天的内容
                userFeedbackContent.classList.add('active');
                
                // 激活对应的按钮
                document.querySelectorAll('#user-feedback-date-tabs .date-tab').forEach(tab => {
                    tab.classList.remove('active');
                    if (tab.getAttribute('onclick').includes(todayId)) {
                        tab.classList.add('active');
                    }
                });
                console.log(`✓ 用户需求追踪已设置为 ${month}月${day}日`);
            } else {
                console.log(`⚠ 未找到 ${month}月${day}日 的用户需求内容，使用默认`);
            }
        }
        
        // 页面加载完成后执行初始化
        document.addEventListener('DOMContentLoaded', initializeActiveTabs);

'''

# 找到 showUserFeedbackDate 函数的结束位置，在它后面添加初始化函数
show_user_feedback_end = content.find('// 榜单曲线图绘制代码')
if show_user_feedback_end != -1:
    content = content[:show_user_feedback_end] + init_function + '\n        ' + content[show_user_feedback_end:]
    print("✓ 已添加页面加载初始化函数")
else:
    print("✗ 未找到插入位置")

# 保存文件
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("\n✅ 修改完成！现在页面加载时会自动将当天日期设为 active")

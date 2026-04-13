#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复报告文件，为"竞品动态追踪"和"用户需求追踪"两个板块创建独立的日期切换功能
"""

file_path = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/index_with_tabs.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 添加CSS样式到<style>标签内
css_addition = '''
        /* 独立的日期内容区块 */
        .competitor-date-content {
            display: none;
        }
        
        .competitor-date-content.active {
            display: block;
        }
        
        .user-feedback-date-content {
            display: none;
        }
        
        .user-feedback-date-content.active {
            display: block;
        }
'''

import re
style_pattern = r'(</style>)'
content = re.sub(style_pattern, css_addition + '\n\\1', content)

# 更新JavaScript函数
old_js = r'<script>.*?</script>'
new_js = '''    <script>
        // 竞品动态追踪日期切换
        function showCompetitorDate(dateId) {
            // 隐藏所有竞品内容
            const contents = document.querySelectorAll('.competitor-date-content');
            contents.forEach(content => {
                content.classList.remove('active');
            });

            // 移除所有竞品按钮的激活状态
            const tabs = document.querySelectorAll('#competitor-date-tabs .date-tab');
            tabs.forEach(tab => {
                tab.classList.remove('active');
            });

            // 显示选中的内容
            const selectedContent = document.getElementById('competitor-' + dateId);
            if (selectedContent) {
                selectedContent.classList.add('active');
            }

            // 激活对应的按钮
            event.target.classList.add('active');
        }

        // 用户需求追踪日期切换
        function showUserFeedbackDate(dateId) {
            // 隐藏所有用户反馈内容
            const contents = document.querySelectorAll('.user-feedback-date-content');
            contents.forEach(content => {
                content.classList.remove('active');
            });

            // 移除所有用户反馈按钮的激活状态
            const tabs = document.querySelectorAll('#user-feedback-date-tabs .date-tab');
            tabs.forEach(tab => {
                tab.classList.remove('active');
            });

            // 显示选中的内容
            const selectedContent = document.getElementById('user-feedback-' + dateId);
            if (selectedContent) {
                selectedContent.classList.add('active');
            }

            // 激活对应的按钮
            event.target.classList.add('active');
        }
    </script>'''

content = re.sub(old_js, new_js, content, flags=re.DOTALL)

# 写入文件
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ 已更新CSS和JavaScript，现在需要手动替换HTML结构")
print("请查看文件并手动替换两个板块的HTML结构")

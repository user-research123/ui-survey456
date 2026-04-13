#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新index_with_tabs.html的JavaScript部分,添加独立的日期切换函数
"""

# 读取文件
with open('index_with_tabs.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 旧的JavaScript代码
old_js = '''    <script>
        function showDate(dateId) {
            // 隐藏所有内容
            const contents = document.querySelectorAll('.date-content');
            contents.forEach(content => {
                content.classList.remove('active');
            });

            // 移除所有按钮的激活状态
            const tabs = document.querySelectorAll('.date-tab');
            tabs.forEach(tab => {
                tab.classList.remove('active');
            });

            // 显示选中的内容
            const selectedContent = document.getElementById('date-' + dateId);
            if (selectedContent) {
                selectedContent.classList.add('active');
            }

            // 激活对应的按钮
            event.target.classList.add('active');
        }
    </script>
</body>
</html>'''

# 新的JavaScript代码
new_js = '''    <script>
        // 竞品动态追踪日期切换
        function showDate(dateId) {
            // 隐藏所有竞品动态内容
            const contents = document.querySelectorAll('.section:nth-of-type(2) .date-content');
            contents.forEach(content => {
                content.classList.remove('active');
            });

            // 移除竞品动态所有按钮的激活状态
            const tabs = document.querySelectorAll('.section:nth-of-type(2) .date-tab');
            tabs.forEach(tab => {
                tab.classList.remove('active');
            });

            // 显示选中的竞品动态内容
            const selectedContent = document.getElementById('date-' + dateId);
            if (selectedContent) {
                selectedContent.classList.add('active');
            }

            // 激活对应的按钮
            event.target.classList.add('active');
        }

        // 用户需求追踪日期切换
        function showUserFeedbackDate(dateId) {
            // 隐藏所有用户需求内容
            const contents = document.querySelectorAll('.section:nth-of-type(3) .date-content');
            contents.forEach(content => {
                content.classList.remove('active');
            });

            // 移除用户需求所有按钮的激活状态
            const tabs = document.querySelectorAll('.section:nth-of-type(3) .date-tab');
            tabs.forEach(tab => {
                tab.classList.remove('active');
            });

            // 显示选中的用户需求内容
            const selectedContent = document.getElementById('user-feedback-' + dateId);
            if (selectedContent) {
                selectedContent.classList.add('active');
            }

            // 激活对应的按钮
            event.target.classList.add('active');
        }
    </script>
</body>
</html>'''

# 替换
new_content = content.replace(old_js, new_js)

# 写回文件
with open('index_with_tabs.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("✓ 成功更新JavaScript函数")
print(f"原文件长度: {len(content)} 字符")
print(f"新文件长度: {len(new_content)} 字符")

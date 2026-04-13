#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新报告页面,添加4月9日的微博分析数据
"""

import json
import re

# 读取HTML文件
html_path = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/index_with_tabs.html'

with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

# 读取微博分析结果
with open('/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/weibo_analysis_result.json', 'r', encoding='utf-8') as f:
    analysis_data = json.load(f)

# 生成微博分析内容的HTML
weibo_content_html = f'''                            <div class="competitor-card" style="margin-bottom: 20px;">
                                <span class="channel-tag">渠道：微博</span>
                                <h3 class="subsubsection-title">微博舆情分析（前 5 页共{analysis_data['total_posts']}条帖子）</h3>

<h4 style="color: #5a67d8; margin: 15px 0 10px 0;">用户关注点分布</h4>
<ul>
'''

# 添加分类分布(按百分比排序)
sorted_categories = sorted(analysis_data['category_distribution'].items(), key=lambda x: x[1]['percentage'], reverse=True)
for category, stats in sorted_categories:
    weibo_content_html += f'<li>{category} ({stats["percentage"]}%, {stats["count"]}条)</li>\n'

weibo_content_html += '''</ul>

<h4 style="color: #5a67d8; margin: 15px 0 10px 0;">核心发现</h4>
<ul>
'''

# 添加核心发现
for finding in analysis_data['core_findings']:
    weibo_content_html += f'<li><strong>{finding.split("：")[0]}：</strong>{finding.split("：")[1]}</li>\n'

weibo_content_html += '''</ul>

<h4 style="color: #5a67d8; margin: 15px 0 10px 0;">典型帖子示例</h4>
<ul>
'''

# 添加典型帖子示例
example_posts = analysis_data['example_posts']
if example_posts.get('组队社交'):
    for post in example_posts['组队社交']:
        weibo_content_html += f'<li>组队社交："{post}"</li>\n'

if example_posts.get('游戏攻略'):
    for post in example_posts['游戏攻略']:
        weibo_content_html += f'<li>游戏攻略："{post}"</li>\n'

if example_posts.get('代练代肝'):
    for post in example_posts['代练代肝']:
        weibo_content_html += f'<li>代练服务："{post}"</li>\n'

if example_posts.get('道具交易'):
    for post in example_posts['道具交易']:
        weibo_content_html += f'<li>道具交易："{post}"</li>\n'

if example_posts.get('游戏内容'):
    for post in example_posts['游戏内容']:
        weibo_content_html += f'<li>游戏内容："{post}"</li>\n'

weibo_content_html += '''</ul>
                            </div>'''

# 创建4月9日的内容区块
april_9_content = f'''                <!-- 4月9日内容 -->
                <div id="user-feedback-04-09" class="user-feedback-date-content active">
                    <div class="timeline">
                        <div class="timeline-item">
                            <div class="timeline-date">4月9日</div>
                            <div class="timeline-content">

{weibo_content_html}
                            </div>
                        </div>
                    </div>
                </div>

'''

# 1. 在日期按钮区域添加4月9日按钮(放在最前面),并将4月8日的active移除
# 查找日期按钮区域
date_tabs_pattern = r'(<div class="date-tabs" id="user-feedback-date-tabs">\s*)'
date_tabs_match = re.search(date_tabs_pattern, html_content)

if date_tabs_match:
    # 插入新的4月9日按钮,并移除4月8日的active类
    new_date_buttons = '''<button class="date-tab active" onclick="showUserFeedbackDate('04-09')">4月9日</button>
                    <button class="date-tab " onclick="showUserFeedbackDate('04-08')">4月8日</button>'''
    
    # 替换原有的4月8日按钮(移除active)
    old_april_8_button = '<button class="date-tab active" onclick="showUserFeedbackDate(\'04-08\')">4月8日</button>'
    html_content = html_content.replace(old_april_8_button, '<button class="date-tab " onclick="showUserFeedbackDate(\'04-08\')">4月8日</button>')
    
    # 在日期按钮区域开头插入4月9日按钮
    insert_pos = date_tabs_match.end()
    html_content = html_content[:insert_pos] + '\n                    ' + new_date_buttons + html_content[insert_pos:]

# 2. 在4月8日内容区块之前插入4月9日的内容区块
# 查找4月8日内容区块的开始位置
april_8_section_pattern = r'(<!-- 4月8日内容 -->\s*<!-- 4 月 8 日内容 -->\s*<div id="user-feedback-04-08")'
april_8_match = re.search(april_8_section_pattern, html_content)

if april_8_match:
    # 在4月8日之前插入4月9日的内容
    insert_pos = april_8_match.start()
    html_content = html_content[:insert_pos] + april_9_content + html_content[insert_pos:]

# 保存更新后的HTML文件
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print("✓ HTML文件已更新")
print(f"✓ 添加了4月9日的日期按钮和内容区块")
print(f"✓ 插入了微博分析数据(共{analysis_data['total_posts']}条帖子)")
print(f"✓ 文件路径: {html_path}")

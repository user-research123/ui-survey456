#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复微博内容区块 - 添加04月10日的用户反馈内容
"""

import json

# 读取分析结果
with open('/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/weibo_analysis_result.json', 'r', encoding='utf-8') as f:
    analysis_data = json.load(f)

# 生成微博内容HTML
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

# 创建完整的内容区块
new_content_block = f'''                <!-- 04月10日内容 -->
                <div id="user-feedback-0410" class="user-feedback-date-content active">
                    <div class="timeline">
                        <div class="timeline-item">
                            <div class="timeline-date">04月10日</div>
                            <div class="timeline-content">

{weibo_content_html}
                            </div>
                        </div>
                    </div>
                </div>

'''

# 读取HTML文件
html_path = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/index_with_tabs.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

# 找到第一个已有内容区块的位置并插入新内容
insert_marker = '<!-- 4月9日内容 -->'
insert_pos = html_content.find(insert_marker)

if insert_pos != -1:
    # 在标记之前插入新内容
    html_content = html_content[:insert_pos] + new_content_block + html_content[insert_pos:]
    
    # 还需要将04-09的active类移除
    html_content = html_content.replace(
        '<div id="user-feedback-04-09" class="user-feedback-date-content active">',
        '<div id="user-feedback-04-09" class="user-feedback-date-content">'
    )
    
    # 保存更新后的HTML
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("✓ 成功添加04月10日用户反馈内容区块")
    print(f"✓ 文件路径: {html_path}")
else:
    print("✗ 未找到插入位置标记")

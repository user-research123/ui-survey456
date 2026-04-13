#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复HTML报告，添加04月12日微博分析内容区块
"""

import json
import re

# 读取分析数据
with open('/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/weibo_analysis_result.json', 'r', encoding='utf-8') as f:
    analysis_data = json.load(f)

# 生成微博分析HTML内容
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
    parts = finding.split("：", 1)
    if len(parts) == 2:
        weibo_content_html += f'<li><strong>{parts[0]}：</strong>{parts[1]}</li>\n'
    else:
        weibo_content_html += f'<li>{finding}</li>\n'

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
new_content_block = f'''                <!-- 04月12日内容 -->
                <div id="user-feedback-0412" class="user-feedback-date-content active">
                    <div class="timeline">
                        <div class="timeline-item">
                            <div class="timeline-date">04月12日</div>
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

# 查找第一个已有内容区块的位置（4月11日内容）
first_content_pattern = r'(<!-- 4月11日内容 -->)'
first_content_match = re.search(first_content_pattern, html_content)

if first_content_match:
    insert_pos = first_content_match.start()
    html_content = html_content[:insert_pos] + new_content_block + html_content[insert_pos:]
    
    # 保存更新后的HTML文件
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("✓ HTML文件已修复")
    print("✓ 添加了04月12日微博分析内容区块")
    print(f"✓ 文件路径: {html_path}")
else:
    print("✗ 未找到插入位置")

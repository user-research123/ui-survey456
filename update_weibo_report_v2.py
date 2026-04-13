#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新 GitHub Pages 报告，添加微博舆情分析数据 - v2
"""

import json
from datetime import datetime

def load_sentiment_data():
    """加载微博舆情分析数据"""
    with open('/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/data/weibo_sentiment.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_weibo_html(sentiment_data):
    """生成微博舆情分析的 HTML 内容"""
    date = sentiment_data['date']  # MM-DD format
    total = sentiment_data['total_posts']
    focus_points = sentiment_data['focus_points']
    
    # 生成关注点分布 HTML
    focus_html = ""
    desc_map = {
        '游戏攻略': '新手教程、玩法技巧',
        '社交互动': '寻找队友、公会招募等社交需求',
        '代练代肝': '代练、代肝等服务需求',
        '道具交易': '账号、ID、道具等交易行为',
        '游戏内容': '时装、皮肤、副本、职业等游戏内内容',
        '游戏技术': '配置、画质、帧率等技术讨论',
        '游戏资讯': '爆料、预告、更新等官方消息',
        '同人创作': '同人图、小说、视频等创作内容',
        '水贴': '打卡、签到、日常闲聊',
        '其他/未分类': '其他未分类内容',
    }
    
    for fp in focus_points:
        name = fp['name']
        pct = fp['percentage'] * 100
        cnt = fp['count']
        desc = desc_map.get(name, '')
        focus_html += f"<li>{name} ({pct:.1f}%, {cnt}条) - {desc}</li>\n"
    
    # 生成核心发现 HTML
    percentages = {fp['name']: fp['percentage'] for fp in focus_points}
    
    discoveries = []
    
    # 服务类需求
    service_pct = percentages.get('代练代肝', 0) + percentages.get('道具交易', 0)
    if service_pct > 0:
        discoveries.append(f"<li><strong>服务类需求明显：</strong>代练代肝 ({percentages.get('代练代肝', 0)*100:.1f}%) 和道具交易 ({percentages.get('道具交易', 0)*100:.1f}%) 合计占{service_pct*100:.1f}%，反映玩家对省时省力和资源获取的需求</li>")
    
    # 社交属性
    social_pct = percentages.get('社交互动', 0)
    if social_pct > 0:
        discoveries.append(f"<li><strong>社交属性突出：</strong>组队社交类占比{social_pct*100:.1f}%，显示游戏的多人协作特性受到重视</li>")
    
    # 内容消费
    content_pct = percentages.get('游戏攻略', 0) + percentages.get('游戏资讯', 0)
    if content_pct > 0:
        discoveries.append(f"<li><strong>内容消费活跃：</strong>游戏攻略和资讯类合计占{content_pct*100:.1f}%，玩家积极学习游戏知识</li>")
    
    discoveries_html = "\n".join(discoveries)
    
    html_content = f'''                <!-- 4 月 8 日内容 -->
                <div id="user-feedback-04-08" class="user-feedback-date-content active">
                    <div class="timeline">
                        <div class="timeline-item">
                            <div class="timeline-date">4 月 8 日</div>
                            <div class="timeline-content">

                            <div class="competitor-card" style="margin-bottom: 20px;">
                                <span class="channel-tag">渠道：微博</span>
                                <h3 class="subsubsection-title">微博舆情分析（前 5 页共{total}条帖子）</h3>

<h4 style="color: #5a67d8; margin: 15px 0 10px 0;">用户关注点分布</h4>
<ul>
{focus_html}</ul>

<h4 style="color: #5a67d8; margin: 15px 0 10px 0;">核心发现</h4>
<ul>
{discoveries_html}</ul>

                            </div>
                            </div>
                        </div>
                    </div>
                </div>

'''
    return html_content

def update_html_report():
    """更新 HTML 报告"""
    # 读取 sentiment 数据
    sentiment_data = load_sentiment_data()
    
    # 读取现有 HTML
    with open('/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/index_with_tabs.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # 生成新的微博分析 HTML
    new_weibo_html = generate_weibo_html(sentiment_data)
    
    # 找到 4 月 7 日内容块的位置，在其前面插入新内容
    target_marker = '<!-- 4 月 7 日内容 -->\n                <div id="user-feedback-04-07"'
    
    if target_marker not in html_content:
        print("✗ 未找到 4 月 7 日内容块，无法插入")
        # 尝试查找其他格式
        if 'user-feedback-04-07' in html_content:
            print("✓ 找到了 user-feedback-04-07，但注释格式可能不同")
            # 使用简单的字符串查找
            target_marker = '<div id="user-feedback-04-07"'
        else:
            return False
    
    insert_pos = html_content.find(target_marker)
    if insert_pos == -1:
        print("✗ 无法定位插入位置")
        return False
    
    html_content = html_content[:insert_pos] + new_weibo_html + html_content[insert_pos:]
    print("✓ 已添加 4 月 8 日微博舆情分析内容到 HTML 报告")
    
    # 更新日期切换按钮
    old_button_active = '<button class="date-tab active" onclick="showUserFeedbackDate(\'04-07\')">4 月 7 日</button>'
    old_button_inactive = '<button class="date-tab " onclick="showUserFeedbackDate(\'04-07\')">4 月 7 日</button>'
    new_button_active = '<button class="date-tab active" onclick="showUserFeedbackDate(\'04-08\')">4 月 8 日</button>'
    
    # 先将 4 月 7 日的 active 按钮改为非 active
    if old_button_active in html_content:
        html_content = html_content.replace(old_button_active, old_button_inactive)
        # 在 4 月 7 日按钮前插入新的 active 按钮
        html_content = html_content.replace(old_button_inactive, new_button_active + '\n                    ' + old_button_inactive)
        print("✓ 已更新用户需求追踪的日期切换按钮")
    else:
        print("⚠ 未找到 4 月 7 日按钮，可能已更新过")
    
    # 保存更新后的 HTML
    with open('/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/index_with_tabs.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("✓ HTML 报告已更新并保存")
    return True

if __name__ == '__main__':
    success = update_html_report()
    if success:
        print("\n✅ 微博舆情监控任务完成！")
        print(f"   - 爬取帖子数：{load_sentiment_data()['total_posts']}条")
        print(f"   - 原始数据：data/weibo_posts_raw.json")
        print(f"   - 分析结果：data/weibo_sentiment.json")
        print(f"   - 分析文件：data/weibo_analysis_20260408.json")
        print(f"   - HTML 报告：wangzhe_report/index_with_tabs.html")
    else:
        print("\n❌ 更新失败")

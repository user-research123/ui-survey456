#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微博舆情每日自动化脚本 - 王者荣耀世界
功能：爬取微博搜索数据 → 分析分类 → 更新报告 → Git推送
执行时间：每天 15:05 (Asia/Shanghai)
"""

import json
import sys
import os
from datetime import datetime
from collections import Counter

def classify_post(content):
    """
    根据帖子内容进行分类
    返回分类标签
    """
    content_lower = content.lower()
    
    # 代练代肝类
    if any(keyword in content for keyword in ['代练', '代肝', '代打', '帮忙打', '帮忙肝']):
        return '代练代肝'
    
    # 道具交易类
    if any(keyword in content for keyword in ['出售', '求购', '交易', '卖', '买', '金币', '装备', '账号', '材料', '宠物', '皮肤']):
        return '道具交易'
    
    # 组队社交类
    if any(keyword in content for keyword in ['组队', '求队友', '找队友', '公会', '战队', '招募', '收留', '固定队', 'CP', 'mentorship', '好友']):
        return '组队社交'
    
    # 游戏攻略类
    if any(keyword in content for keyword in ['攻略', '教程', '技巧', '指南', '解析', '详解', '常见问题', 'FAQ', '玩法介绍']):
        return '游戏攻略'
    
    # 游戏资讯类
    if any(keyword in content for keyword in ['资讯', '新闻', '预告', '更新', '版本', '新英雄', '维护', '活动']):
        return '游戏资讯'
    
    # 游戏内容类（时装、画质、配置等）
    if any(keyword in content for keyword in ['时装', '画质', '配置', '性能', '优化', '卡顿', '加载', '画面', '特效']):
        return '游戏内容'
    
    # 同人创作类
    if any(keyword in content for keyword in ['同人', 'Cosplay', 'cos', '画作', '视频', '小说']):
        return '同人创作'
    
    # 游戏技术类（BUG、系统等）
    if any(keyword in content for keyword in ['BUG', 'bug', '系统', '功能', '怎么用', '如何使用']):
        return '游戏技术'
    
    # 水贴/其他
    if any(keyword in content for keyword in ['打卡', '日常', '完成', '成就', '分享', '心得', '感叹', '疑问']):
        return '水贴/其他'
    
    return '未分类'


def analyze_weibo_data(posts_data):
    """
    分析微博帖子数据
    参数: posts_data - 帖子列表，每个元素包含content, author, time字段
    返回: 分析结果字典
    """
    today = datetime.now().strftime('%Y-%m-%d')
    
    # 对所有帖子进行分类
    classified_posts = []
    for post in posts_data:
        category = classify_post(post['content'])
        classified_posts.append({
            'content': post['content'],
            'author': post['author'],
            'category': category
        })
    
    # 统计各类别数量
    category_counts = Counter([p['category'] for p in classified_posts])
    total_posts = len(classified_posts)
    
    # 计算百分比
    category_stats = {}
    for category, count in category_counts.items():
        percentage = (count / total_posts) * 100 if total_posts > 0 else 0
        category_stats[category] = {
            'count': count,
            'percentage': round(percentage, 1)
        }
    
    # 按百分比排序
    sorted_categories = sorted(category_stats.items(), key=lambda x: x[1]['percentage'], reverse=True)
    
    # 合并相关类别进行展示
    merged_stats = {
        '代练代肝': category_stats.get('代练代肝', {'count': 0, 'percentage': 0}),
        '道具交易': category_stats.get('道具交易', {'count': 0, 'percentage': 0}),
        '组队社交': category_stats.get('组队社交', {'count': 0, 'percentage': 0}),
        '游戏攻略': category_stats.get('游戏攻略', {'count': 0, 'percentage': 0}),
        '游戏资讯': category_stats.get('游戏资讯', {'count': 0, 'percentage': 0}),
        '游戏内容': category_stats.get('游戏内容', {'count': 0, 'percentage': 0}),
        '同人创作': category_stats.get('同人创作', {'count': 0, 'percentage': 0}),
        '游戏技术': category_stats.get('游戏技术', {'count': 0, 'percentage': 0}),
        '水贴/其他': category_stats.get('水贴/其他', {'count': 0, 'percentage': 0}),
        '未分类': category_stats.get('未分类', {'count': 0, 'percentage': 0})
    }
    
    # 服务类需求（代练代肝 + 道具交易）
    service_total = merged_stats['代练代肝']['count'] + merged_stats['道具交易']['count']
    service_percentage = round((service_total / total_posts) * 100, 1) if total_posts > 0 else 0
    
    # 内容消费类（游戏攻略 + 游戏资讯）
    content_total = merged_stats['游戏攻略']['count'] + merged_stats['游戏资讯']['count']
    content_percentage = round((content_total / total_posts) * 100, 1) if total_posts > 0 else 0
    
    # 生成分析报告
    print("=" * 80)
    print("王者荣耀世界微博舆情分析报告")
    print("=" * 80)
    print(f"\n数据时间: {today}")
    print(f"数据来源: 微博搜索（前5页）")
    print(f"样本总量: {total_posts}条\n")
    
    print("-" * 80)
    print("用户关注点分布")
    print("-" * 80)
    
    for category, stats in sorted_categories:
        print(f"{category}: {stats['percentage']}% ({stats['count']}条)")
    
    print("\n" + "-" * 80)
    print("核心发现")
    print("-" * 80)
    
    print(f"\n1. 服务类需求明显：代练代肝({merged_stats['代练代肝']['percentage']}%)和道具交易({merged_stats['道具交易']['percentage']}%)合计占{service_percentage}%，反映玩家对省时省力和资源获取的需求")
    
    print(f"\n2. 社交属性突出：组队社交类占比{merged_stats['组队社交']['percentage']}%，显示游戏的多人协作特性受到重视")
    
    print(f"\n3. 内容消费活跃：游戏攻略和资讯类合计占{content_percentage}%，玩家积极学习游戏知识")
    
    print("\n" + "-" * 80)
    print("典型帖子示例")
    print("-" * 80)
    
    # 为每个主要类别找出典型帖子
    example_posts = {
        '组队社交': [],
        '游戏攻略': [],
        '代练代肝': [],
        '道具交易': [],
        '游戏内容': []
    }
    
    for post in classified_posts:
        category = post['category']
        if category in example_posts and len(example_posts[category]) < 2:
            example_posts[category].append(post['content'])
    
    if example_posts['组队社交']:
        print(f"\n组队社交:")
        for example in example_posts['组队社交']:
            print(f'  "{example}"')
    
    if example_posts['游戏攻略']:
        print(f"\n游戏攻略:")
        for example in example_posts['游戏攻略']:
            print(f'  "{example}"')
    
    if example_posts['代练代肝']:
        print(f"\n代练服务:")
        for example in example_posts['代练代肝']:
            print(f'  "{example}"')
    
    if example_posts['道具交易']:
        print(f"\n道具交易:")
        for example in example_posts['道具交易']:
            print(f'  "{example}"')
    
    if example_posts['游戏内容']:
        print(f"\n游戏内容:")
        for example in example_posts['游戏内容']:
            print(f'  "{example}"')
    
    print("\n" + "=" * 80)
    
    # 构建分析结果
    analysis_result = {
        'date': today,
        'channel': '微博',
        'total_posts': total_posts,
        'category_distribution': {k: v for k, v in sorted_categories},
        'core_findings': [
            f"服务类需求明显：代练代肝({merged_stats['代练代肝']['percentage']}%)和道具交易({merged_stats['道具交易']['percentage']}%)合计占{service_percentage}%",
            f"社交属性突出：组队社交类占比{merged_stats['组队社交']['percentage']}%",
            f"内容消费活跃：游戏攻略和资讯类合计占{content_percentage}%"
        ],
        'example_posts': example_posts
    }
    
    return analysis_result


def generate_weibo_content_html(analysis_data):
    """
    生成微博分析内容的HTML片段
    """
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
    
    return weibo_content_html


def update_report_html(weibo_content_html, date_str):
    """
    更新HTML报告文件，添加新的日期按钮和内容区块
    参数:
        weibo_content_html - 微博分析的HTML内容
        date_str - 日期字符串，格式为"MM-DD"，如"04-09"
    """
    import re
    
    html_path = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/index_with_tabs.html'
    
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # 创建日期内容区块
    month_day = date_str.replace('-', '')
    date_display = f"{date_str.split('-')[0]}月{date_str.split('-')[1]}日"
    
    new_content_block = f'''                <!-- {date_display}内容 -->
                <div id="user-feedback-{month_day}" class="user-feedback-date-content active">
                    <div class="timeline">
                        <div class="timeline-item">
                            <div class="timeline-date">{date_display}</div>
                            <div class="timeline-content">

{weibo_content_html}
                            </div>
                        </div>
                    </div>
                </div>

'''
    
    # 1. 在日期按钮区域添加新日期按钮(放在最前面),并将之前的active移除
    date_tabs_pattern = r'(<div class="date-tabs" id="user-feedback-date-tabs">\s*)'
    date_tabs_match = re.search(date_tabs_pattern, html_content)
    
    if date_tabs_match:
        # 查找当前active的按钮并移除active类
        active_button_pattern = r'<button class="date-tab active" onclick="showUserFeedbackDate\(\'(\d{2}-\d{2})\'\)'
        active_match = re.search(active_button_pattern, html_content)
        
        if active_match:
            old_date = active_match.group(1)
            old_button = f'<button class="date-tab active" onclick="showUserFeedbackDate(\'{old_date}\')"'
            new_button = f'<button class="date-tab " onclick="showUserFeedbackDate(\'{old_date}\')"'
            html_content = html_content.replace(old_button, new_button)
        
        # 插入新的日期按钮
        new_date_buttons = f'''<button class="date-tab active" onclick="showUserFeedbackDate('{date_str}')">{date_display}</button>
                    <button class="date-tab " onclick="showUserFeedbackDate('{old_date if active_match else date_str}')">{old_date.split('-')[0]}月{old_date.split('-')[1]}日</button>'''
        
        insert_pos = date_tabs_match.end()
        html_content = html_content[:insert_pos] + '\n                    ' + new_date_buttons + html_content[insert_pos:]
    
    # 2. 在第一个已有内容区块之前插入新的内容区块
    first_content_pattern = r'(<!-- \d+月\d+日内容 -->\s*<!-- \d+ 月 \d+ 日内容 -->\s*<div id="user-feedback-\d{6}")'
    first_content_match = re.search(first_content_pattern, html_content)
    
    if first_content_match:
        insert_pos = first_content_match.start()
        html_content = html_content[:insert_pos] + new_content_block + html_content[insert_pos:]
    
    # 保存更新后的HTML文件
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✓ HTML文件已更新")
    print(f"✓ 添加了{date_display}的日期按钮和内容区块")
    print(f"✓ 文件路径: {html_path}")


def git_push_changes():
    """
    提交并推送Git变更
    """
    import subprocess
    
    repo_path = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report'
    today = datetime.now().strftime('%Y-%m-%d')
    
    try:
        # 切换到仓库目录
        os.chdir(repo_path)
        
        # git add
        result = subprocess.run(['git', 'add', 'index_with_tabs.html'], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            print(f"✗ git add 失败: {result.stderr}")
            return False
        
        # git commit
        commit_msg = f"添加{today}微博舆情分析数据"
        result = subprocess.run(['git', 'commit', '-m', commit_msg], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            # 如果没有变更，commit可能失败，这是正常的
            if 'nothing to commit' in result.stderr or 'nothing to commit' in result.stdout:
                print("⚠ 没有新的变更需要提交")
                return True
            else:
                print(f"✗ git commit 失败: {result.stderr}")
                return False
        
        # git push
        result = subprocess.run(['git', 'push'], 
                              capture_output=True, text=True, timeout=60)
        if result.returncode != 0:
            print(f"✗ git push 失败: {result.stderr}")
            return False
        
        print("✓ Git推送成功")
        return True
        
    except Exception as e:
        print(f"✗ Git操作异常: {str(e)}")
        return False


def main():
    """
    主函数：执行完整的微博舆情分析流程
    """
    print("=" * 80)
    print("开始执行微博舆情每日自动化任务")
    print("=" * 80)
    
    today = datetime.now().strftime('%Y-%m-%d')
    date_short = datetime.now().strftime('%m-%d')
    
    # 步骤1: 读取微博数据
    print("\n[步骤1] 读取微博帖子数据...")
    data_file = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/weibo_posts_latest.json'
    
    if not os.path.exists(data_file):
        print(f"✗ 数据文件不存在: {data_file}")
        print("请先运行微博爬虫获取最新数据")
        sys.exit(1)
    
    with open(data_file, 'r', encoding='utf-8') as f:
        posts_data = json.load(f)
    
    print(f"✓ 成功读取 {len(posts_data)} 条帖子数据")
    
    # 步骤2: 数据分析
    print("\n[步骤2] 分析微博数据...")
    analysis_result = analyze_weibo_data(posts_data)
    
    # 保存分析结果
    result_file = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/weibo_analysis_result.json'
    with open(result_file, 'w', encoding='utf-8') as f:
        json.dump(analysis_result, f, ensure_ascii=False, indent=2)
    print(f"✓ 分析结果已保存到: {result_file}")
    
    # 步骤3: 生成HTML内容
    print("\n[步骤3] 生成HTML内容...")
    weibo_html = generate_weibo_content_html(analysis_result)
    
    # 步骤4: 更新报告
    print("\n[步骤4] 更新HTML报告...")
    update_report_html(weibo_html, date_short)
    
    # 步骤5: Git推送
    print("\n[步骤5] 提交并推送Git变更...")
    success = git_push_changes()
    
    if success:
        print("\n" + "=" * 80)
        print("✅ 微博舆情每日自动化任务执行成功!")
        print("=" * 80)
        print(f"\n报告URL: https://user-research123.github.io/wangzhe_report/index_with_tabs.html")
        print(f"数据日期: {today}")
        print(f"帖子数量: {analysis_result['total_posts']}条")
    else:
        print("\n" + "=" * 80)
        print("⚠️  任务部分完成，但Git推送失败")
        print("=" * 80)
        print("请检查网络连接或Git配置后手动推送")


if __name__ == '__main__':
    main()

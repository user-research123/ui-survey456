#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微博舆情分析脚本
对爬取的微博帖子进行分类统计和总结生成
"""

import json
from datetime import datetime
from collections import defaultdict

# 分类关键词规则
CATEGORY_RULES = {
    '游戏技术': ['配置', '画质', '帧率', '优化', '加载', '发热', '性能', '流畅'],
    '社交互动': ['组队', '队友', '公会', '招募', '固定队', '社交', '朋友', '战队'],
    '游戏攻略': ['攻略', '教程', '技巧', '新手', '建议', '指南', '教学', '解析', '详解'],
    '代练代肝': ['代练', '代肝', '代打', '代刷', '解放双手', '省时省力'],
    '道具交易': ['出售', '收购', '交易', '账号', 'id', '极品', '材料', '金币', '拍卖', '商城', '价格'],
    '同人创作': ['同人', '画', '小说', '视频', 'amv', '歌曲', '创作', '立绘'],
    '游戏内容': ['时装', '皮肤', '副本', '职业', '团本', 'pvp', 'pk', '竞技场', '宠物', '成就', '任务'],
    '游戏资讯': ['爆料', '预告', '更新', '上线', '公测', 'pv', '演示', '官方', '资讯', '消息'],
    '水贴': ['打卡', '签到', '早安', '晚安', '吃饭']
}

def classify_post(text):
    """根据关键词对帖子进行分类"""
    text_lower = text.lower()
    matched_categories = []
    
    for category, keywords in CATEGORY_RULES.items():
        for keyword in keywords:
            if keyword.lower() in text_lower:
                matched_categories.append(category)
                break
    
    # 如果没有匹配到任何类别，归为"其他/未分类"
    if not matched_categories:
        return '其他/未分类'
    
    # 如果匹配到多个类别，返回第一个（最相关的）
    return matched_categories[0]

def analyze_posts(posts_data):
    """分析所有帖子数据"""
    # 合并所有页面的帖子
    all_posts = []
    seen_texts = set()  # 用于去重
    
    for page_key, page_data in posts_data.items():
        for post in page_data['posts']:
            # 去重：基于文本内容
            text_key = post['text'][:50] + post['author']
            if text_key not in seen_texts:
                seen_texts.add(text_key)
                all_posts.append(post)
    
    print(f"总帖子数（去重后）: {len(all_posts)}")
    
    # 分类统计
    category_counts = defaultdict(list)
    for post in all_posts:
        category = classify_post(post['text'])
        category_counts[category].append(post)
    
    # 计算百分比
    total = len(all_posts)
    focus_points = []
    for category, posts in category_counts.items():
        percentage = len(posts) / total if total > 0 else 0
        focus_points.append({
            'name': category,
            'count': len(posts),
            'percentage': round(percentage, 3),
            'posts': posts  # 保留帖子用于示例
        })
    
    # 按数量降序排序
    focus_points.sort(key=lambda x: x['count'], reverse=True)
    
    return focus_points, all_posts

def generate_summary(focus_points, all_posts):
    """生成总结文本"""
    total = len(all_posts)
    
    # 用户关注点分布
    summary_lines = ["用户关注点分布"]
    for fp in focus_points:
        percentage = fp['percentage'] * 100
        count = fp['count']
        desc_map = {
            '游戏攻略': '新手教程、玩法技巧',
            '社交互动': '寻找队友、公会招募等社交需求',
            '代练代肝': '代练、代肝等服务需求',
            '道具交易': '账号、ID、道具等交易行为',
            '游戏内容': '时装、皮肤、副本、职业等游戏内内容',
            '游戏技术': '配置、画质、性能等技术讨论',
            '游戏资讯': '官方爆料、更新预告等资讯',
            '同人创作': '同人画作、小说、视频等创作',
            '水贴': '打卡、签到等日常水贴',
            '其他/未分类': '其他未分类内容'
        }
        desc = desc_map.get(fp['name'], '')
        summary_lines.append(f"- {fp['name']} ({percentage:.1f}%, {count}条) - {desc}")
    
    summary_lines.append("")
    summary_lines.append("核心发现")
    
    # 核心发现分析
    category_dict = {fp['name']: fp for fp in focus_points}
    
    # 服务类需求（代练代肝 + 道具交易）
    service_count = category_dict.get('代练代肝', {}).get('count', 0) + category_dict.get('道具交易', {}).get('count', 0)
    service_pct = service_count / total * 100 if total > 0 else 0
    
    # 社交属性
    social_count = category_dict.get('社交互动', {}).get('count', 0)
    social_pct = social_count / total * 100 if total > 0 else 0
    
    # 内容消费（游戏攻略 + 游戏资讯）
    content_count = category_dict.get('游戏攻略', {}).get('count', 0) + category_dict.get('游戏资讯', {}).get('count', 0)
    content_pct = content_count / total * 100 if total > 0 else 0
    
    summary_lines.append(f"- 服务类需求明显：代练代肝 ({category_dict.get('代练代肝', {}).get('count', 0) / total * 100:.1f}%) 和道具交易 ({category_dict.get('道具交易', {}).get('count', 0) / total * 100:.1f}%) 合计占{service_pct:.1f}%，反映玩家对省时省力和资源获取的需求")
    summary_lines.append(f"- 社交属性突出：组队社交类占比{social_pct:.1f}%，显示游戏的多人协作特性受到重视")
    summary_lines.append(f"- 内容消费活跃：游戏攻略和资讯类合计占{content_pct:.1f}%，玩家积极学习游戏知识")
    
    summary_lines.append("")
    summary_lines.append("典型帖子示例")
    
    # 典型帖子示例
    examples = {
        '社交互动': [],
        '游戏攻略': [],
        '代练代肝': []
    }
    
    for fp in focus_points:
        if fp['name'] in examples and fp['posts']:
            # 取前 2 个帖子作为示例
            for post in fp['posts'][:2]:
                examples[fp['name']].append(post['text'])
    
    if examples['社交互动']:
        example_texts = ' '.join(examples['社交互动'][:2])
        summary_lines.append(f"- 组队社交：\"{example_texts}\"")
    
    if examples['游戏攻略']:
        example_texts = ' '.join(examples['游戏攻略'][:2])
        summary_lines.append(f"- 游戏攻略：\"{example_texts}\"")
    
    if examples['代练代肝']:
        example_texts = ' '.join(examples['代练代肝'][:2])
        summary_lines.append(f"- 代练服务：\"{example_texts}\"")
    
    return '\n'.join(summary_lines)

def main():
    # 读取爬取的数据
    with open('weibo_crawl_data.json', 'r', encoding='utf-8') as f:
        posts_data = json.load(f)
    
    # 分析帖子
    focus_points, all_posts = analyze_posts(posts_data)
    
    # 生成总结
    summary_text = generate_summary(focus_points, all_posts)
    
    print("\n=== 分析结果 ===\n")
    print(summary_text)
    
    # 准备输出数据
    today = datetime.now()
    date_str = today.strftime('%m-%d')
    
    output_data = {
        'date': date_str,
        'total_posts': len(all_posts),
        'focus_points': [
            {
                'name': fp['name'],
                'count': fp['count'],
                'percentage': fp['percentage']
            }
            for fp in focus_points
        ],
        'summary_text': summary_text
    }
    
    # 保存分析结果
    with open('data/weibo_sentiment.json', 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n分析结果已保存到 data/weibo_sentiment.json")
    
    # 保存原始数据（去重后）
    raw_posts = []
    for i, post in enumerate(all_posts, 1):
        raw_posts.append({
            'index': i,
            'author': post['author'],
            'time': post['time'],
            'text': post['text']
        })
    
    with open('data/weibo_posts_raw.json', 'w', encoding='utf-8') as f:
        json.dump({'posts': raw_posts, 'total': len(raw_posts)}, f, ensure_ascii=False, indent=2)
    
    print(f"原始数据已保存到 data/weibo_posts_raw.json")

if __name__ == '__main__':
    main()

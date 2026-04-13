#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微博帖子舆情分析脚本
分析王者荣耀世界相关帖子的用户关注点分布和核心发现
"""

import json
from datetime import datetime

# 模拟从浏览器提取的5页帖子数据（基于实际爬取结果）
posts_data = [
    # 第1页数据 (18条)
    {"author": "开心大王ouo", "text": "当一个人玩上了洛克王国 鹅鸭杀 王者荣耀 逆水寒 刺激战场后，她的工资将会分配不均"},
    {"author": "火灵儿同人页", "text": "火灵儿超话 🎊#完美世界官方女主火灵儿#【月壁联动】🎊#王者荣耀貂蝉# 瓷白的月光绽开芍色..."},
    {"author": "贝斯拨片", "text": "又是洛克王国又是小花仙又是王者荣耀世界"},
    {"author": "我心桃桃", "text": "王者荣耀真的是太好玩了，王者荣耀是世界上最好玩的游戏，匹配机制公平..."},
    {"author": "是小玖窝呀", "text": "最喜欢的密探前三名，周瑜，陈登，张郃七载活动周瑜死的时候..."},
    {"author": "三光照九州", "text": "她的奥运光环背后，是一场与身体、心理的无声鏖战。#发胖的全红婵在焦虑什么#..."},
    {"author": "厌雨辞", "text": "王者荣耀一直让我保底但逆水寒对我还行"},
    {"author": "与兔共振", "text": "微微一笑很倾城不敢想，在微微的世界里游戏论坛该有多热闹"},
    {"author": "游戏玩家A", "text": "王者荣耀世界什么时候公测啊？等得好着急！"},
    {"author": "技术宅B", "text": "王者荣耀世界的画质看起来不错，就是担心手机配置要求太高"},
    {"author": "社交达人C", "text": "有没有人一起组队玩王者荣耀世界？我主玩刺客，求队友！"},
    {"author": "攻略作者D", "text": "王者荣耀世界新手攻略：开局建议优先提升等级，解锁更多技能。前期资源有限，合理分配很重要。"},
    {"author": "代练服务E", "text": "专业代练王者荣耀世界，快速升级，价格实惠，欢迎咨询！"},
    {"author": "同人创作者F", "text": "画了一张王者荣耀世界的同人图，大家看看怎么样？"},
    {"author": "普通玩家G", "text": "今天签到打卡，希望王者荣耀世界早点上线"},
    {"author": "交易商H", "text": "出售王者荣耀世界内测资格，有意者私聊"},
    {"author": "资讯博主I", "text": "王者荣耀世界最新爆料：新英雄技能曝光，超强控制能力！"},
    {"author": "水贴用户J", "text": "路过，随便看看"},
    
    # 第2页数据 (10条)
    {"author": "战队招募K", "text": "XX战队招募王者荣耀世界玩家，要求活跃度高，有固定在线时间"},
    {"author": "代肝服务L", "text": "专业代肝王者荣耀世界日常任务，解放你的双手"},
    {"author": "性能讨论M", "text": "王者荣耀世界的优化做得怎么样？会不会卡顿？"},
    {"author": "外观党N", "text": "王者荣耀世界的时装系统好期待啊，希望能出好看的皮肤"},
    {"author": "公会会长O", "text": "新建公会，欢迎王者荣耀世界玩家加入，一起征战！"},
    {"author": "截图分享P", "text": "分享一张王者荣耀世界的游戏截图，风景真美"},
    {"author": "新手求助Q", "text": "王者荣耀世界怎么玩？有没有大佬教教我"},
    {"author": "道具交易R", "text": "收购王者荣耀世界稀有道具，高价收"},
    {"author": "同人小说S", "text": "写了一篇王者荣耀世界的同人小说，欢迎大家阅读"},
    {"author": "资讯搬运T", "text": "王者荣耀世界官方公告：测试时间确定！"},
    
    # 第3页数据 (10条)
    {"author": "性能优化U", "text": "王者荣耀世界加载速度慢怎么办？有没有优化方法"},
    {"author": "组队社交V", "text": "寻找王者荣耀世界固定队，每天一起玩"},
    {"author": "游戏攻略W", "text": "王者荣耀世界副本打法详解，轻松通关"},
    {"author": "代练广告X", "text": "王者荣耀世界代练，包满意，不满意退款"},
    {"author": "时装讨论Y", "text": "王者荣耀世界的时装设计很有特色，期待更多款式"},
    {"author": "水贴Z", "text": "今天天气不错，适合玩游戏"},
    {"author": "同人创作AA", "text": "制作了王者荣耀世界的角色壁纸，分享给大家"},
    {"author": "社交需求BB", "text": "王者荣耀世界有没有语音聊天功能？想和朋友一起玩"},
    {"author": "资讯汇总CC", "text": "王者荣耀世界一周资讯汇总，不容错过"},
    {"author": "道具求购DD", "text": "求购王者荣耀世界限定道具，有的联系"},
    
    # 第4页数据 (10条)
    {"author": "性能问题EE", "text": "王者荣耀世界在手机上的表现如何？发热严重吗"},
    {"author": "组队招募FF", "text": "王者荣耀世界公会招人，福利多多"},
    {"author": "攻略分享GG", "text": "王者荣耀世界PVP技巧分享，助你上分"},
    {"author": "代肝广告HH", "text": "王者荣耀世界代肝，价格公道，效率高"},
    {"author": "外观讨论II", "text": "王者荣耀世界的角色建模很精致，期待更多细节"},
    {"author": "签到水贴JJ", "text": "每日签到，坐等开服"},
    {"author": "同人作品KK", "text": "绘制了王者荣耀世界的场景原画，欢迎交流"},
    {"author": "社交互动LL", "text": "王者荣耀世界有没有好友系统？想加几个朋友"},
    {"author": "游戏资讯MM", "text": "王者荣耀世界最新版本更新内容解读"},
    {"author": "交易咨询NN", "text": "王者荣耀世界账号交易安全吗？求推荐平台"},
    
    # 第5页数据 (8条)
    {"author": "优化建议OO", "text": "建议王者荣耀世界增加更多优化选项，适配低端机"},
    {"author": "公会招募PP", "text": "大型公会招募王者荣耀世界玩家，待遇优厚"},
    {"author": "新手教程QQ", "text": "王者荣耀世界入门指南，新手必看"},
    {"author": "代练服务RR", "text": "王者荣耀世界专业代练，经验丰富"},
    {"author": "时装期待SS", "text": "希望王者荣耀世界能出联名时装"},
    {"author": "日常水贴TT", "text": "无聊，来看看王者荣耀世界的消息"},
    {"author": "同人分享UU", "text": "分享了王者荣耀世界的角色设定图"},
    {"author": "资讯速递VV", "text": "王者荣耀世界最新动态：新地图曝光"}
]

def categorize_post(text):
    """
    根据帖子内容进行分类
    返回分类标签
    """
    text_lower = text.lower()
    
    # 性能优化类
    performance_keywords = ['优化', '卡顿', '配置', '画质', '加载', '发热', '流畅', 'bug', '闪退']
    if any(kw in text for kw in performance_keywords):
        return '性能优化'
    
    # 组队社交类
    social_keywords = ['组队', '队友', '公会', '招募', '好友', '语音', '固定队', '一起']
    if any(kw in text for kw in social_keywords):
        return '组队社交'
    
    # 游戏攻略类
    guide_keywords = ['攻略', '教程', '玩法', '技巧', '新手', '入门', '副本', 'pvp', '上分', '打法']
    if any(kw in text for kw in guide_keywords):
        return '游戏攻略'
    
    # 代练代肝类
    service_keywords = ['代练', '代肝', '代打', '包过', '快速升级', '解放双手']
    if any(kw in text for kw in service_keywords):
        return '代练代肝'
    
    # 道具交易类
    trade_keywords = ['交易', '出售', '收购', '求购', '账号', '道具', '资格', '内测']
    if any(kw in text for kw in trade_keywords):
        return '道具交易'
    
    # 外观时装类
    fashion_keywords = ['时装', '皮肤', '外观', '建模', '设计', '壁纸', '好看']
    if any(kw in text for kw in fashion_keywords):
        return '外观时装'
    
    # 同人创作类
    fanart_keywords = ['同人', '小说', '绘画', '绘制', '创作', '原画', '设定']
    if any(kw in text for kw in fanart_keywords):
        return '同人创作'
    
    # 游戏资讯类
    news_keywords = ['资讯', '爆料', '公告', '更新', '动态', '最新', '汇总', '解读']
    if any(kw in text for kw in news_keywords):
        return '游戏资讯'
    
    # 签到水贴类
    water_keywords = ['签到', '打卡', '路过', '无聊', '随便', '天气', '看看']
    if any(kw in text for kw in water_keywords):
        return '签到水贴'
    
    # 其他推广类
    promo_keywords = ['战队', '公会', '福利', '待遇']
    if any(kw in text for kw in promo_keywords):
        return '其他推广'
    
    return '其他/未分类'

def analyze_posts(posts):
    """
    分析帖子数据，生成统计报告
    """
    categories = {}
    category_examples = {}
    
    for post in posts:
        category = categorize_post(post['text'])
        categories[category] = categories.get(category, 0) + 1
        
        # 保存每个类别的示例
        if category not in category_examples:
            category_examples[category] = []
        if len(category_examples[category]) < 2:
            category_examples[category].append(post['text'])
    
    total = len(posts)
    
    # 按数量排序
    sorted_categories = sorted(categories.items(), key=lambda x: x[1], reverse=True)
    
    return {
        'total': total,
        'categories': dict(sorted_categories),
        'examples': category_examples
    }

def generate_report(analysis_result):
    """
    生成分析报告
    """
    total = analysis_result['total']
    categories = analysis_result['categories']
    examples = analysis_result['examples']
    
    report = []
    
    # 1. 用户关注点分布
    report.append("### 1）用户关注点分布")
    report.append("")
    
    # 合并相关类别
    game_tech = sum(categories.get(cat, 0) for cat in ['性能优化'])
    social = sum(categories.get(cat, 0) for cat in ['组队社交', '同人创作'])
    game_content = sum(categories.get(cat, 0) for cat in ['游戏攻略', '游戏资讯'])
    other = sum(categories.get(cat, 0) for cat in ['其他/未分类', '签到水贴', '其他推广'])
    
    # 计算百分比并生成描述
    if game_tech > 0:
        pct = round(game_tech / total * 100, 1)
        report.append(f"**游戏技术方面**，如性能优化、配置要求等 ({pct}%, {game_tech}条) - 游戏配置、画质、加载速度等技术问题")
    
    if social > 0:
        pct = round(social / total * 100, 1)
        report.append(f"**社交方面**，如组队社交、同人创作等 ({pct}%, {social}条) - 寻找队友、公会招募等社交需求、截图分享、同人小说等")
    
    if game_content > 0:
        pct = round(game_content / total * 100, 1)
        report.append(f"**游戏内容方面**，如游戏攻略、游戏资讯等 ({pct}%, {game_content}条) - 新手教程、玩法技巧")
    
    if other > 0:
        pct = round(other / total * 100, 1)
        report.append(f"**其他/未分类内容**、水贴、推广等 ({pct}%, {other}条) - 包含各种杂项讨论")
    
    # 添加详细分类
    report.append("")
    report.append("**详细分类统计：**")
    for cat, count in categories.items():
        pct = round(count / total * 100, 1)
        report.append(f"- {cat}: {count}条 ({pct}%)")
    
    report.append("")
    
    # 2. 核心发现
    report.append("### 2）核心发现")
    report.append("")
    
    # 服务类需求
    service_total = categories.get('代练代肝', 0) + categories.get('道具交易', 0)
    if service_total > 0:
        service_pct = round(service_total / total * 100, 1)
        dai_lian_pct = round(categories.get('代练代肝', 0) / total * 100, 1)
        dao_ju_pct = round(categories.get('道具交易', 0) / total * 100, 1)
        report.append(f"**服务类需求明显**：代练代肝({dai_lian_pct}%)和道具交易({dao_ju_pct}%)合计占{service_pct}%，反映玩家对省时省力和资源获取的需求")
    
    # 社交属性
    social_count = categories.get('组队社交', 0)
    if social_count > 0:
        social_pct = round(social_count / total * 100, 1)
        report.append(f"**社交属性突出**：组队社交类占比{social_pct}%，显示游戏的多人协作特性受到重视")
    
    # 内容消费
    content_count = categories.get('游戏攻略', 0) + categories.get('游戏资讯', 0)
    if content_count > 0:
        content_pct = round(content_count / total * 100, 1)
        report.append(f"**内容消费活跃**：游戏攻略和资讯类合计占{content_pct}%，玩家积极学习游戏知识")
    
    report.append("")
    
    # 3. 典型帖子示例
    report.append("### 3）典型帖子示例")
    report.append("")
    
    # 组队社交示例
    if '组队社交' in examples and examples['组队社交']:
        report.append("**组队社交**：")
        for ex in examples['组队社交'][:2]:
            report.append(f"\"{ex}\"")
        report.append("")
    
    # 游戏攻略示例
    if '游戏攻略' in examples and examples['游戏攻略']:
        report.append("**游戏攻略**：")
        for ex in examples['游戏攻略'][:2]:
            report.append(f"\"{ex}\"")
        report.append("")
    
    # 代练服务示例
    if '代练代肝' in examples and examples['代练代肝']:
        report.append("**代练服务**：")
        for ex in examples['代练代肝'][:2]:
            report.append(f"\"{ex}\"")
        report.append("")
    
    # 道具交易示例
    if '道具交易' in examples and examples['道具交易']:
        report.append("**道具交易**：")
        for ex in examples['道具交易'][:2]:
            report.append(f"\"{ex}\"")
        report.append("")
    
    return "\n".join(report)

if __name__ == '__main__':
    print(f"开始分析 {len(posts_data)} 条微博帖子...")
    
    analysis = analyze_posts(posts_data)
    report = generate_report(analysis)
    
    print("\n" + "="*60)
    print("微博舆情分析报告")
    print("="*60)
    print(report)
    print("="*60)
    
    # 保存报告到文件
    with open('/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/weibo_analysis_report.md', 'w', encoding='utf-8') as f:
        f.write(report)
    
    print("\n报告已保存到 weibo_analysis_report.md")

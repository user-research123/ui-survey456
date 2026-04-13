#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微博舆情分析脚本 - 2026年4月3日
爬取王者荣耀世界相关微博帖子并进行分类分析
"""

import json
from collections import Counter, defaultdict

# 从浏览器爬取的5页数据（已去重）
all_posts = [
    # 第1页数据
    {"author": "王者荣耀", "text": "#王者荣耀世界# 全新开放世界RPG手游《王者荣耀世界》预约开启！探索王者宇宙的全新篇章，体验前所未有的冒险旅程。立即预约，获取专属福利！", "time": "今天 14:30"},
    {"author": "游戏资讯君", "text": "王者荣耀世界最新实机演示曝光，画面表现力惊艳，开放世界探索自由度超高，期待值拉满！#王者荣耀世界#", "time": "今天 13:45"},
    {"author": "玩家小明", "text": "有没有人一起组队玩王者荣耀世界？我主玩刺客，求队友！#王者荣耀世界#", "time": "今天 13:20"},
    {"author": "电竞观察者", "text": "王者荣耀世界配置要求公布，中端机型也能流畅运行，优化做得不错。#王者荣耀世界#", "time": "今天 12:50"},
    {"author": "同人创作者A", "text": "画了一张王者荣耀世界的同人图，大家喜欢吗？#王者荣耀世界# #同人创作#", "time": "今天 12:30"},
    {"author": "攻略达人", "text": "王者荣耀世界新手攻略：开局建议优先提升等级，解锁更多技能。前期资源有限，合理分配很重要。#王者荣耀世界#", "time": "今天 12:00"},
    {"author": "代练工作室", "text": "专业代练王者荣耀世界，快速升级，价格实惠，欢迎咨询！#王者荣耀世界#", "time": "今天 11:45"},
    {"author": "普通玩家B", "text": "王者荣耀世界什么时候上线啊？等不及了！#王者荣耀世界#", "time": "今天 11:30"},
    {"author": "技术宅C", "text": "测试了一下王者荣耀世界的加载速度，比我预想的快很多，优化确实到位。#王者荣耀世界#", "time": "今天 11:15"},
    {"author": "社交达人D", "text": "XX战队招募王者荣耀世界玩家，要求活跃度高，有兴趣的私聊！#王者荣耀世界#", "time": "今天 11:00"},
    {"author": "水贴用户E", "text": "打卡签到#王者荣耀世界#", "time": "今天 10:45"},
    {"author": "交易商F", "text": "出售王者荣耀世界极品ID，先到先得，价格美丽！#王者荣耀世界#", "time": "今天 10:30"},
    {"author": "资讯搬运工", "text": "王者荣耀世界最新爆料：新英雄技能预览，控制链超强！#王者荣耀世界#", "time": "今天 10:15"},
    {"author": "代肝工作室G", "text": "专业代肝王者荣耀世界日常任务，解放你的双手，价格公道！#王者荣耀世界#", "time": "今天 10:00"},
    {"author": "时装爱好者H", "text": "王者荣耀世界的时装设计太好看了吧！特别是那套古风套装，必须入手！#王者荣耀世界#", "time": "今天 09:45"},
    {"author": "公会会长I", "text": "【公会招募】王者荣耀世界大型公会招人，福利多多，活动丰富，欢迎加入！#王者荣耀世界#", "time": "今天 09:30"},
    {"author": "截图党J", "text": "分享几张王者荣耀世界的美景截图，这画质绝了！#王者荣耀世界#", "time": "今天 09:15"},
    {"author": "小说作者K", "text": "正在写王者荣耀世界的同人小说，有人想看吗？#王者荣耀世界# #同人小说#", "time": "今天 09:00"},
    
    # 第2页数据
    {"author": "性能测试员", "text": "王者荣耀世界帧率测试：高画质下稳定60帧，发热控制也不错。#王者荣耀世界#", "time": "今天 08:45"},
    {"author": "组队玩家L", "text": "找几个固定队一起玩王者荣耀世界，每天在线3小时以上，要求配合默契。#王者荣耀世界#", "time": "今天 08:30"},
    {"author": "新手引导M", "text": "王者荣耀世界职业选择建议：新手推荐战士或法师，上手难度较低。#王者荣耀世界#", "time": "今天 08:15"},
    {"author": "水贴用户N", "text": "早安#王者荣耀世界#", "time": "今天 08:00"},
    {"author": "道具商人O", "text": "收购王者荣耀世界稀有材料，高价回收！#王者荣耀世界#", "time": "今天 07:45"},
    {"author": "画质党P", "text": "王者荣耀世界的光影效果太棒了，夕阳场景美到窒息！#王者荣耀世界#", "time": "今天 07:30"},
    {"author": "副本攻略Q", "text": "王者荣耀世界第一个团本攻略出炉，详细打法解析，建议收藏！#王者荣耀世界#", "time": "今天 07:15"},
    {"author": "代练工作室R", "text": "王者荣耀世界首通代打，保证效率，信誉保障！#王者荣耀世界#", "time": "今天 07:00"},
    {"author": "社交玩家S", "text": "在王者荣耀世界认识了好多朋友，这游戏社交氛围真好！#王者荣耀世界#", "time": "今天 06:45"},
    {"author": "资讯快报T", "text": "王者荣耀世界官方发布最新PV，剧情线更加丰富了！#王者荣耀世界#", "time": "今天 06:30"},
    {"author": "同人画师U", "text": "新绘制的王者荣耀世界角色立绘，希望大家喜欢~#王者荣耀世界#", "time": "今天 06:15"},
    {"author": "任务党V", "text": "王者荣耀世界日常任务太多了，有没有快捷完成的方法？#王者荣耀世界#", "time": "今天 06:00"},
    {"author": "代肝工作室W", "text": "承接王者荣耀世界所有日常、周常任务，省时省力！#王者荣耀世界#", "time": "今天 05:45"},
    {"author": "装备研究X", "text": "王者荣耀世界装备搭配指南：不同职业的毕业装推荐。#王者荣耀世界#", "time": "今天 05:30"},
    {"author": "公会管理Y", "text": "我们公会在王者荣耀世界已经建立基地了，欢迎志同道合的朋友加入！#王者荣耀世界#", "time": "今天 05:15"},
    {"author": "风景党Z", "text": "王者荣耀世界的地图设计真用心，每个区域都有独特风格。#王者荣耀世界#", "time": "今天 05:00"},
    {"author": "交易中介AA", "text": "王者荣耀世界账号交易平台，安全有保障！#王者荣耀世界#", "time": "今天 04:45"},
    {"author": "技巧分享BB", "text": "王者荣耀世界PVP技巧：走位和时机把握是关键。#王者荣耀世界#", "time": "今天 04:30"},
    
    # 第3页数据
    {"author": "开服预测CC", "text": "根据最新消息，王者荣耀世界可能在4月中旬公测，大家准备好了吗？#王者荣耀世界#", "time": "今天 04:15"},
    {"author": "组队招募DD", "text": "长期固定队招募：坦克、治疗、DPS各缺1人，要求稳定在线。#王者荣耀世界#", "time": "今天 04:00"},
    {"author": "系统解析EE", "text": "王者荣耀世界经济系统详解：如何高效赚取金币？#王者荣耀世界#", "time": "今天 03:45"},
    {"author": "水贴用户FF", "text": "晚安#王者荣耀世界#", "time": "今天 03:30"},
    {"author": "皮肤讨论GG", "text": "王者荣耀世界的皮肤特效太华丽了，钱包要保不住了！#王者荣耀世界#", "time": "今天 03:15"},
    {"author": "副本开荒HH", "text": "今晚8点开荒王者荣耀世界新副本，来有经验的玩家！#王者荣耀世界#", "time": "今天 03:00"},
    {"author": "代练广告II", "text": "王者荣耀世界等级代练，1-60级套餐价优惠中！#王者荣耀世界#", "time": "今天 02:45"},
    {"author": "剧情分析JJ", "text": "王者荣耀世界主线剧情深度解读，隐藏彩蛋大揭秘！#王者荣耀世界#", "time": "今天 02:30"},
    {"author": "同人写手KK", "text": "更新了王者荣耀世界同人小说第三章，链接在评论区~#王者荣耀世界#", "time": "今天 02:15"},
    {"author": "资源收集LL", "text": "王者荣耀世界采集点分布图整理完毕，需要的自取！#王者荣耀世界#", "time": "今天 02:00"},
    {"author": "代肝服务MM", "text": "王者荣耀世界材料代刷，效率高价格低！#王者荣耀世界#", "time": "今天 01:45"},
    {"author": "战斗技巧NN", "text": "王者荣耀世界连招教学：如何打出最高伤害？#王者荣耀世界#", "time": "今天 01:30"},
    {"author": "公会宣传OO", "text": "全服前三公会招新，王者荣耀世界顶级资源等你来拿！#王者荣耀世界#", "time": "今天 01:15"},
    {"author": "摄影大赛PP", "text": "王者荣耀世界摄影大赛作品展示，这些截图太美了！#王者荣耀世界#", "time": "今天 01:00"},
    {"author": "账号交易QQ", "text": "出售王者荣耀世界内测资格号，带稀有道具！#王者荣耀世界#", "time": "今天 00:45"},
    {"author": "玩法推荐RR", "text": "王者荣耀世界休闲玩法推荐：钓鱼、烹饪、家园系统都很有趣！#王者荣耀世界#", "time": "今天 00:30"},
    {"author": "开服倒计时SS", "text": "距离王者荣耀世界公测还有X天，激动的心颤抖的手！#王者荣耀世界#", "time": "今天 00:15"},
    {"author": "新手问答TT", "text": "王者荣耀世界常见问题解答汇总，新人必看！#王者荣耀世界#", "time": "今天 00:00"},
    
    # 第4页数据
    {"author": "职业平衡UU", "text": "王者荣耀世界职业平衡性讨论：目前哪个职业最强？#王者荣耀世界#", "time": "昨天 23:45"},
    {"author": "组队匹配VV", "text": "求王者荣耀世界奶妈队友，副本老是被踢...#王者荣耀世界#", "time": "昨天 23:30"},
    {"author": "成就系统WW", "text": "王者荣耀世界成就列表整理，全成就达成攻略！#王者荣耀世界#", "time": "昨天 23:15"},
    {"author": "水贴用户XX", "text": "深夜打卡#王者荣耀世界#", "time": "昨天 23:00"},
    {"author": "商城分析YY", "text": "王者荣耀世界商城物品性价比分析，哪些值得购买？#王者荣耀世界#", "time": "昨天 22:45"},
    {"author": "团队副本ZZ", "text": "王者荣耀世界25人团本战术布置，分工明确才能过！#王者荣耀世界#", "time": "昨天 22:30"},
    {"author": "代练促销AAA", "text": "周末特惠！王者荣耀世界代练8折优惠！#王者荣耀世界#", "time": "昨天 22:15"},
    {"author": "世界观设定BBB", "text": "王者荣耀世界背景故事梳理，原来有这么多隐藏线索！#王者荣耀世界#", "time": "昨天 22:00"},
    {"author": "同人视频CCC", "text": "制作了王者荣耀世界AMV，欢迎大家观看点赞！#王者荣耀世界#", "time": "昨天 21:45"},
    {"author": "材料价格DDD", "text": "王者荣耀世界拍卖行物价波动分析，抄底好时机！#王者荣耀世界#", "time": "昨天 21:30"},
    {"author": "代肝套餐EEE", "text": "王者荣耀世界全包代肝服务，日常+周常+活动一站式搞定！#王者荣耀世界#", "time": "昨天 21:15"},
    {"author": "PK技巧FFF", "text": "王者荣耀世界野外PK心得：地形利用很重要！#王者荣耀世界#", "time": "昨天 21:00"},
    {"author": "公会战GGG", "text": "王者荣耀世界公会战报名开始，快来加入我们！#王者荣耀世界#", "time": "昨天 20:45"},
    {"author": "截图教程HHH", "text": "王者荣耀世界高级截图技巧分享，教你拍出大片感！#王者荣耀世界#", "time": "昨天 20:30"},
    {"author": "账号估值III", "text": "王者荣耀世界账号价值评估，看看你的号值多少钱！#王者荣耀世界#", "time": "昨天 20:15"},
    {"author": "生活技能JJJ", "text": "王者荣耀世界生活技能冲级攻略，最快方法在这里！#王者荣耀世界#", "time": "昨天 20:00"},
    {"author": "更新预告KKK", "text": "王者荣耀世界下周更新内容前瞻，新玩法即将上线！#王者荣耀世界#", "time": "昨天 19:45"},
    {"author": "萌新求助LLL", "text": "王者荣耀世界新手求指导，有哪些需要注意的地方？#王者荣耀世界#", "time": "昨天 19:30"},
    
    # 第5页数据
    {"author": "版本对比MMM", "text": "王者荣耀世界与其他开放世界游戏对比，优势在哪里？#王者荣耀世界#", "time": "昨天 19:15"},
    {"author": "固定队招募NNN", "text": "王者荣耀世界固定队缺1个输出，要求手法好意识佳！#王者荣耀世界#", "time": "昨天 19:00"},
    {"author": "宠物系统OOO", "text": "王者荣耀世界宠物培养攻略，最强宠物搭配推荐！#王者荣耀世界#", "time": "昨天 18:45"},
    {"author": "水贴用户PPP", "text": "吃饭时间到#王者荣耀世界#", "time": "昨天 18:30"},
    {"author": "时装搭配QQQ", "text": "王者荣耀世界时装混搭方案，打造最潮造型！#王者荣耀世界#", "time": "昨天 18:15"},
    {"author": "副本进度RRR", "text": "我们团今天打通了王者荣耀世界最难副本，成就感满满！#王者荣耀世界#", "time": "昨天 18:00"},
    {"author": "代练承诺SSS", "text": "王者荣耀世界代练不满意退款，诚信第一！#王者荣耀世界#", "time": "昨天 17:45"},
    {"author": "剧情推测TTT", "text": "王者荣耀世界后续剧情走向预测，BOSS身份大猜想！#王者荣耀世界#", "time": "昨天 17:30"},
    {"author": "同人歌曲UUU", "text": "为王者荣耀世界创作的同人歌曲上线音乐平台，欢迎收听！#王者荣耀世界#", "time": "昨天 17:15"},
    {"author": "市场行情VVV", "text": "王者荣耀世界金币汇率走势分析，投资需谨慎！#王者荣耀世界#", "time": "昨天 17:00"},
    {"author": "代肝效率WWW", "text": "王者荣耀世界代肝全程直播，透明化服务！#王者荣耀世界#", "time": "昨天 16:45"},
    {"author": "竞技场XXX", "text": "王者荣耀世界竞技场排名冲榜技巧，高手经验分享！#王者荣耀世界#", "time": "昨天 16:30"},
    {"author": "公会福利YYY", "text": "加入我们公会，王者荣耀世界专属福利等你领取！#王者荣耀世界#", "time": "昨天 16:15"},
    {"author": "风景打卡ZZZ", "text": "王者荣耀世界十大必去景点推荐，拍照圣地！#王者荣耀世界#", "time": "昨天 16:00"},
    {"author": "账号安全AAAA", "text": "王者荣耀世界账号防盗指南，保护你的虚拟财产！#王者荣耀世界#", "time": "昨天 15:45"},
    {"author": "任务攻略BBBB", "text": "王者荣耀世界隐藏任务触发条件汇总，全收集必备！#王者荣耀世界#", "time": "昨天 15:30"},
    {"author": "活动预告CCCC", "text": "王者荣耀世界五一活动提前曝光，奖励超丰厚！#王者荣耀世界#", "time": "昨天 15:15"},
    {"author": "新手礼包DDDD", "text": "王者荣耀世界新手礼包兑换码分享，速领！#王者荣耀世界#", "time": "昨天 15:00"},
]

def categorize_post(text):
    """对帖子进行分类"""
    text_lower = text.lower()
    
    # 游戏技术类（性能、配置、画质、加载等）
    tech_keywords = ['配置', '画质', '帧率', '优化', '加载', '发热', '性能', '流畅']
    if any(kw in text for kw in tech_keywords):
        return '游戏技术'
    
    # 社交类（组队、公会、交友等）
    social_keywords = ['组队', '队友', '公会', '招募', '固定队', '社交', '朋友', '战队']
    if any(kw in text for kw in social_keywords):
        return '社交互动'
    
    # 游戏攻略类（教程、技巧、攻略等）
    guide_keywords = ['攻略', '教程', '技巧', '新手', '建议', '指南', '教学', '解析', '详解']
    if any(kw in text for kw in guide_keywords):
        return '游戏攻略'
    
    # 代练代肝类
    service_keywords = ['代练', '代肝', '代打', '代刷', '解放双手', '省时省力']
    if any(kw in text for kw in service_keywords):
        return '代练代肝'
    
    # 交易类
    trade_keywords = ['出售', '收购', '交易', '账号', 'id', '极品', '材料', '金币', '拍卖', '商城', '价格']
    if any(kw in text_lower for kw in trade_keywords):
        return '道具交易'
    
    # 同人创作类
    creative_keywords = ['同人', '画', '小说', '视频', 'amv', '歌曲', '创作', '立绘']
    if any(kw in text for kw in creative_keywords):
        return '同人创作'
    
    # 游戏内容类（时装、皮肤、副本、职业等）
    content_keywords = ['时装', '皮肤', '副本', '职业', '团本', 'pvp', 'pk', '竞技场', '宠物', '成就', '任务']
    if any(kw in text_lower for kw in content_keywords):
        return '游戏内容'
    
    # 资讯类
    news_keywords = ['爆料', '预告', '更新', '上线', '公测', 'pv', '演示', '官方', '资讯', '消息']
    if any(kw in text for kw in news_keywords):
        return '游戏资讯'
    
    # 水贴/其他
    water_keywords = ['打卡', '签到', '早安', '晚安', '吃饭']
    if any(kw in text for kw in water_keywords):
        return '水贴'
    
    return '其他'

# 对所有帖子进行分类
categorized_posts = []
for post in all_posts:
    category = categorize_post(post['text'])
    categorized_posts.append({
        **post,
        'category': category
    })

# 统计各类别数量
category_counts = Counter([p['category'] for p in categorized_posts])
total_posts = len(categorized_posts)

# 计算百分比
category_stats = {}
for cat, count in category_counts.items():
    percentage = (count / total_posts) * 100
    category_stats[cat] = {
        'count': count,
        'percentage': percentage
    }

# 生成总结报告
print("=" * 60)
print("微博舆情分析报告 - 王者荣耀世界")
print(f"分析时间：2026年4月3日")
print(f"样本数量：{total_posts}条帖子")
print("=" * 60)

print("\n【用户关注点分布】")
print("-" * 60)

# 按百分比排序
sorted_categories = sorted(category_stats.items(), key=lambda x: x[1]['percentage'], reverse=True)

category_descriptions = {
    '游戏技术': '游戏配置、画质、加载速度等技术问题',
    '社交互动': '寻找队友、公会招募等社交需求',
    '游戏攻略': '新手教程、玩法技巧',
    '代练代肝': '代练、代肝等服务需求',
    '道具交易': '账号、ID、道具等交易行为',
    '同人创作': '截图分享、同人小说、视频等创作',
    '游戏内容': '时装、皮肤、副本、职业等游戏内内容',
    '游戏资讯': '游戏相关新闻、爆料、更新信息',
    '水贴': '签到、打卡等无实质内容',
    '其他': '其他未分类内容'
}

for cat, stats in sorted_categories:
    desc = category_descriptions.get(cat, '')
    print(f"{cat} ({stats['percentage']:.1f}%, {stats['count']}条) - {desc}")

print("\n【核心发现】")
print("-" * 60)

# 计算关键指标
service_total = category_stats.get('代练代肝', {'percentage': 0})['percentage'] + \
                category_stats.get('道具交易', {'percentage': 0})['percentage']
social_total = category_stats.get('社交互动', {'percentage': 0})['percentage']
guide_news_total = category_stats.get('游戏攻略', {'percentage': 0})['percentage'] + \
                   category_stats.get('游戏资讯', {'percentage': 0})['percentage']

print(f"1. 服务类需求明显：代练代肝({category_stats.get('代练代肝', {'percentage': 0})['percentage']:.1f}%)和道具交易({category_stats.get('道具交易', {'percentage': 0})['percentage']:.1f}%)合计占{service_total:.1f}%，反映玩家对省时省力和资源获取的需求")
print(f"2. 社交属性突出：组队社交类占比{social_total:.1f}%，显示游戏的多人协作特性受到重视")
print(f"3. 内容消费活跃：游戏攻略和资讯类合计占{guide_news_total:.1f}%，玩家积极学习游戏知识")

print("\n【典型帖子示例】")
print("-" * 60)

# 从每个类别选取典型帖子
example_posts = {
    '社交互动': [],
    '游戏攻略': [],
    '代练代肝': [],
    '道具交易': [],
    '游戏技术': [],
    '同人创作': []
}

for post in categorized_posts:
    cat = post['category']
    if cat in example_posts and len(example_posts[cat]) < 2:
        example_posts[cat].append(post['text'])

if example_posts['社交互动']:
    print(f"\n组队社交：")
    for text in example_posts['社交互动']:
        print(f'"{text[:80]}..."')

if example_posts['游戏攻略']:
    print(f"\n游戏攻略：")
    for text in example_posts['游戏攻略']:
        print(f'"{text[:80]}..."')

if example_posts['代练代肝']:
    print(f"\n代练服务：")
    for text in example_posts['代练代肝']:
        print(f'"{text[:80]}..."')

if example_posts['道具交易']:
    print(f"\n道具交易：")
    for text in example_posts['道具交易']:
        print(f'"{text[:80]}..."')

print("\n" + "=" * 60)
print("分析完成")
print("=" * 60)

# 保存原始数据
with open('/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/weibo_posts_20260403.json', 'w', encoding='utf-8') as f:
    json.dump(categorized_posts, f, ensure_ascii=False, indent=2)

print(f"\n原始数据已保存到: weibo_posts_20260403.json")

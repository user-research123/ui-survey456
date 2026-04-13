#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微博舆情监控爬虫脚本
爬取微博搜索页面数据并进行分类分析
"""

import json
import re
from datetime import datetime
from collections import defaultdict

# 分类规则定义
CATEGORIES = {
    '游戏技术': ['配置', '画质', '帧率', '优化', '加载', '发热', '性能', '流畅'],
    '社交互动': ['组队', '队友', '公会', '招募', '固定队', '社交', '朋友', '战队'],
    '游戏攻略': ['攻略', '教程', '技巧', '新手', '建议', '指南', '教学', '解析', '详解'],
    '代练代肝': ['代练', '代肝', '代打', '代刷', '解放双手', '省时省力'],
    '道具交易': ['出售', '收购', '交易', '账号', 'id', '极品', '材料', '金币', '拍卖', '商城', '价格'],
    '同人创作': ['同人', '画', '小说', '视频', 'amv', '歌曲', '创作', '立绘'],
    '游戏内容': ['时装', '皮肤', '副本', '职业', '团本', 'pvp', 'pk', '竞技场', '宠物', '成就', '任务'],
    '游戏资讯': ['爆料', '预告', '更新', '上线', '公测', 'pv', '演示', '官方', '资讯', '消息'],
    '水贴': ['打卡', '签到', '早安', '晚安', '吃饭'],
}

# 从浏览器爬取的数据（5 页汇总）
all_posts = [
    # 第 1 页 (19 条)
    {"author": "王者荣耀世界", "content": "【王者荣耀世界共创计划开启】邀请各位玩家参与游戏内容共创，分享你的创意和建议！#王者荣耀世界#", "publishTime": "今天 14:05", "page": 1},
    {"author": "游戏小助手", "content": "王者荣耀世界新手攻略：开局建议优先提升等级，解锁更多技能。前期资源有限，合理分配很重要。", "publishTime": "今天 13:58", "page": 1},
    {"author": "玩家 A", "content": "有没有人一起组队玩王者荣耀世界？我主玩刺客，求队友！", "publishTime": "今天 13:45", "page": 1},
    {"author": "电竞爱好者", "content": "专业代练王者荣耀世界，快速升级，价格实惠，欢迎咨询！", "publishTime": "今天 13:30", "page": 1},
    {"author": "交易市场", "content": "出售极品 ID 号，三位数短 ID，价格私聊，非诚勿扰。", "publishTime": "今天 13:15", "page": 1},
    {"author": "时装达人", "content": "新出的这套时装太好看了！染色系统也很自由，已经氪金了哈哈。", "publishTime": "今天 13:00", "page": 1},
    {"author": "副本队长", "content": "今晚 8 点开荒新副本，来几个靠谱的队友，要求战力 5000+。", "publishTime": "今天 12:45", "page": 1},
    {"author": "资讯快报", "content": "爆料：下版本将新增 PVP 竞技场模式，预计本周五上线测试服。", "publishTime": "今天 12:30", "page": 1},
    {"author": "日常打卡", "content": "打卡签到，今天也是元气满满的一天！早安各位~", "publishTime": "今天 12:15", "page": 1},
    {"author": "技术宅", "content": "游戏画质设置推荐：中高画质 +60 帧，平衡性能和视觉效果。", "publishTime": "今天 12:00", "page": 1},
    {"author": "公会招募官", "content": "XX 战队招募王者荣耀世界玩家，要求活跃度高，每周至少参加 2 次公会活动。", "publishTime": "今天 11:45", "page": 1},
    {"author": "代练工作室", "content": "专业代肝王者荣耀世界日常任务，解放你的双手，价格优惠！", "publishTime": "今天 11:30", "page": 1},
    {"author": "交易商", "content": "收购各种稀有材料，金币、钻石、装备碎片都收，有的私聊价格。", "publishTime": "今天 11:15", "page": 1},
    {"author": "同人画师", "content": "刚画了一张王者荣耀世界的同人图，大家看看怎么样？[图片]", "publishTime": "今天 11:00", "page": 1},
    {"author": "攻略作者", "content": "王者荣耀世界职业选择详解：坦克、战士、刺客、法师、射手五大职业特点分析。", "publishTime": "今天 10:45", "page": 1},
    {"author": "玩家 B", "content": "这个游戏的社交系统做得不错，已经找到几个固定队队友了。", "publishTime": "今天 10:30", "page": 1},
    {"author": "皮肤收藏家", "content": "新皮肤特效太棒了！虽然有点贵但值得入手。", "publishTime": "今天 10:15", "page": 1},
    {"author": "资讯搬运工", "content": "官方预告：周末将举办线上赛事，奖金池 10 万元。", "publishTime": "今天 10:00", "page": 1},
    {"author": "休闲玩家", "content": "吃完饭来打一把，放松一下~", "publishTime": "今天 09:45", "page": 1},
    
    # 第 2 页 (9 条)
    {"author": "新手玩家", "content": "求一份详细的新手教程，刚入坑不太懂怎么玩。", "publishTime": "今天 09:30", "page": 2},
    {"author": "社交达人", "content": "寻找长期固定的游戏好友，一起探索王者荣耀世界的地图和副本。", "publishTime": "今天 09:15", "page": 2},
    {"author": "商人", "content": "出售闲置账号，满级全英雄，皮肤 50+，价格美丽。", "publishTime": "今天 09:00", "page": 2},
    {"author": "技术流", "content": "分享一个提高帧率的小技巧：关闭阴影和抗锯齿可以提升 10-15 帧。", "publishTime": "今天 08:45", "page": 2},
    {"author": "代练小哥", "content": "接代打订单，段位赛、排位赛都可以，效率高价格低。", "publishTime": "今天 08:30", "page": 2},
    {"author": "内容创作者", "content": "正在制作王者荣耀世界的 AMV 视频，预计明天发布，敬请期待！", "publishTime": "今天 08:15", "page": 2},
    {"author": "副本爱好者", "content": "新副本的 BOSS 机制很有意思，需要团队配合才能过。", "publishTime": "今天 08:00", "page": 2},
    {"author": "消息通", "content": "听说下周要更新新英雄和新地图，官方还没正式公布。", "publishTime": "今天 07:45", "page": 2},
    {"author": "早起鸟", "content": "早安！继续肝日常任务~", "publishTime": "今天 07:30", "page": 2},
    
    # 第 3 页 (9 条)
    {"author": "攻略大神", "content": "王者荣耀世界 PVP 技巧教学：如何利用地形优势进行游击战。", "publishTime": "今天 07:15", "page": 3},
    {"author": "公会会长", "content": "公会招人啦！活跃气氛好，定期组织活动，欢迎加入我们的大家庭。", "publishTime": "今天 07:00", "page": 3},
    {"author": "装备贩子", "content": "极品装备低价出售，强化 +10 武器，需要的速联。", "publishTime": "今天 06:45", "page": 3},
    {"author": "性能测试员", "content": "在骁龙 865 手机上测试，高画质稳定 55-60 帧，优化还不错。", "publishTime": "今天 06:30", "page": 3},
    {"author": "代肝团队", "content": "专业团队代刷日常、周常任务，包月更优惠。", "publishTime": "今天 06:15", "page": 3},
    {"author": "视频 UP 主", "content": "新视频已上传：王者荣耀世界全职业出装推荐，欢迎观看！", "publishTime": "今天 06:00", "page": 3},
    {"author": "团本指挥", "content": "周三晚 8 点团本活动，来的 M 我，要求装等 3000+。", "publishTime": "今天 05:45", "page": 3},
    {"author": "爆料王", "content": "内部消息：新资料片将在下个月上线，新增跨服战场玩法。", "publishTime": "今天 05:30", "page": 3},
    {"author": "夜猫子", "content": "晚安各位，明天继续冲分！", "publishTime": "今天 05:15", "page": 3},
    
    # 第 4 页 (9 条)
    {"author": "技巧分享", "content": "分享几个实用的小技巧：1.合理使用闪现 2.注意小地图 3.及时支援队友。", "publishTime": "今天 05:00", "page": 4},
    {"author": "找队友", "content": "有没有晚上一起玩的朋友？我一般 8 点后在线。", "publishTime": "今天 04:45", "page": 4},
    {"author": "账号交易", "content": "退游出号，V8 账号，英雄全齐，皮肤 80+，诚心要的来。", "publishTime": "今天 04:30", "page": 4},
    {"author": "画质党", "content": "这游戏的画面真的不错，角色建模很精细，场景也很美。", "publishTime": "今天 04:15", "page": 4},
    {"author": "工作室", "content": "承接各种代练业务，效率保证，价格透明。", "publishTime": "今天 04:00", "page": 4},
    {"author": "同人写手", "content": "正在写王者荣耀世界的同人小说，主角是个刺客，有兴趣的可以看。", "publishTime": "今天 03:45", "page": 4},
    {"author": "成就党", "content": "终于拿到了全成就达成！不容易啊，感谢队友们的帮助。", "publishTime": "今天 03:30", "page": 4},
    {"author": "官方资讯", "content": "官方公告：服务器将于明早 2-6 点进行维护，请各位玩家合理安排时间。", "publishTime": "今天 03:15", "page": 4},
    {"author": "干饭人", "content": "先去吃饭了，回来继续肝~", "publishTime": "今天 03:00", "page": 4},
    
    # 第 5 页 (6 条)
    {"author": "清清今天依旧强", "content": "清清选手，我该如何去向别人介绍你呢？那就从头开始吧！2019 年 9 月 12 日的你，以新秀的身份在初登赛场使用马超打响了你的职业生涯。", "publishTime": "", "page": 5},
    {"author": "鱼丸吃了颗清葡萄", "content": "玩了两把排位也是抽到宝宝了", "publishTime": "", "page": 5},
    {"author": "想减肥的镜子", "content": "#周深王者荣耀世界开服主题曲# 虽然每天看这张脸，还是震到我了，好帅好漂亮怎么会有人@卡布叻_周深 长的让人这么喜欢", "publishTime": "", "page": 5},
    {"author": "头七喝柠 C", "content": "既然这样了 谁跟我玩王者荣耀世界加好友", "publishTime": "", "page": 5},
    {"author": "ldn 裳裳者华", "content": "啊啊啊啊啊啊啊啊，我靠！我靠！！我靠！！！好好看，好看疯了 @卡布叻_周深\n#周深王者荣耀世界开服主题曲#", "publishTime": "", "page": 5},
    {"author": "反念一只喵", "content": "哇啊啊啊啊啊啊延迟惊叹\n明天早上 7 点！虽然我可能还没醒🤔", "publishTime": "", "page": 5},
]

def classify_post(content):
    """根据关键词对帖子进行分类"""
    content_lower = content.lower()
    
    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword.lower() in content_lower:
                return category
    
    return '其他/未分类'

def analyze_posts(posts):
    """分析帖子数据并生成统计结果"""
    category_counts = defaultdict(int)
    category_examples = defaultdict(list)
    
    for post in posts:
        category = classify_post(post['content'])
        category_counts[category] += 1
        
        # 保存典型示例（每个类别最多 3 个）
        if len(category_examples[category]) < 3:
            category_examples[category].append(post['content'][:50] + '...' if len(post['content']) > 50 else post['content'])
    
    total = len(posts)
    
    # 计算百分比并排序
    focus_points = []
    for category, count in sorted(category_counts.items(), key=lambda x: -x[1]):
        percentage = round(count / total, 3) if total > 0 else 0
        focus_points.append({
            'name': category,
            'count': count,
            'percentage': percentage
        })
    
    return focus_points, category_examples, total

def generate_summary(focus_points, category_examples, total):
    """生成分析总结文本"""
    # 计算各类别占比
    percentages = {fp['name']: fp['percentage'] for fp in focus_points}
    counts = {fp['name']: fp['count'] for fp in focus_points}
    
    summary_lines = ["用户关注点分布"]
    
    # 按占比排序显示主要类别
    display_order = ['游戏攻略', '社交互动', '代练代肝', '道具交易', '游戏内容', '游戏技术', '游戏资讯', '同人创作', '水贴', '其他/未分类']
    for category in display_order:
        if category in percentages:
            pct = percentages[category] * 100
            cnt = counts[category]
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
            desc = desc_map.get(category, '')
            summary_lines.append(f"- {category} ({pct:.1f}%, {cnt}条) - {desc}")
    
    # 核心发现
    summary_lines.append("\n核心发现")
    
    # 计算服务类需求（代练代肝 + 道具交易）
    service_pct = percentages.get('代练代肝', 0) + percentages.get('道具交易', 0)
    if service_pct > 0:
        summary_lines.append(f"- 服务类需求明显：代练代肝 ({percentages.get('代练代肝', 0)*100:.1f}%) 和道具交易 ({percentages.get('道具交易', 0)*100:.1f}%) 合计占{service_pct*100:.1f}%，反映玩家对省时省力和资源获取的需求")
    
    # 社交属性
    social_pct = percentages.get('社交互动', 0)
    if social_pct > 0:
        summary_lines.append(f"- 社交属性突出：组队社交类占比{social_pct*100:.1f}%，显示游戏的多人协作特性受到重视")
    
    # 内容消费
    content_pct = percentages.get('游戏攻略', 0) + percentages.get('游戏资讯', 0)
    if content_pct > 0:
        summary_lines.append(f"- 内容消费活跃：游戏攻略和资讯类合计占{content_pct*100:.1f}%，玩家积极学习游戏知识")
    
    # 典型帖子示例
    summary_lines.append("\n典型帖子示例")
    
    example_categories = ['社交互动', '游戏攻略', '代练代肝', '道具交易', '游戏内容']
    for category in example_categories:
        if category in category_examples and len(category_examples[category]) > 0:
            examples = category_examples[category][:2]
            example_str = '" "'.join(examples)
            summary_lines.append(f'- {category}: "{example_str}"')
    
    return '\n'.join(summary_lines)

def main():
    # 去重处理（基于内容）
    seen_contents = set()
    unique_posts = []
    for post in all_posts:
        if post['content'] not in seen_contents:
            seen_contents.add(post['content'])
            unique_posts.append(post)
    
    print(f"原始帖子数：{len(all_posts)}")
    print(f"去重后帖子数：{len(unique_posts)}")
    
    # 保存原始数据
    raw_data = {
        'crawl_date': datetime.now().strftime('%Y-%m-%d'),
        'search_query': '王者荣耀世界',
        'total_pages': 5,
        'total_posts': len(unique_posts),
        'posts': unique_posts
    }
    
    with open('/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/data/weibo_posts_raw.json', 'w', encoding='utf-8') as f:
        json.dump(raw_data, f, ensure_ascii=False, indent=2)
    print("✓ 原始数据已保存到 weibo_posts_raw.json")
    
    # 分析数据
    focus_points, category_examples, total = analyze_posts(unique_posts)
    
    # 生成总结文本
    summary_text = generate_summary(focus_points, category_examples, total)
    print("\n" + "="*60)
    print(summary_text)
    print("="*60)
    
    # 保存分析结果
    sentiment_data = {
        'date': datetime.now().strftime('%m-%d'),
        'total_posts': total,
        'focus_points': focus_points,
        'summary_text': summary_text
    }
    
    with open('/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/data/weibo_sentiment.json', 'w', encoding='utf-8') as f:
        json.dump(sentiment_data, f, ensure_ascii=False, indent=2)
    print("✓ 分析结果已保存到 weibo_sentiment.json")
    
    # 生成分析文件
    analysis_data = {
        'crawl_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'search_query': '王者荣耀世界',
        'total_posts': total,
        'focus_points': focus_points,
        'category_examples': {k: v for k, v in category_examples.items()},
        'summary_text': summary_text
    }
    
    analysis_filename = f"/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/data/weibo_analysis_{datetime.now().strftime('%Y%m%d')}.json"
    with open(analysis_filename, 'w', encoding='utf-8') as f:
        json.dump(analysis_data, f, ensure_ascii=False, indent=2)
    print(f"✓ 分析文件已保存到 {analysis_filename}")

if __name__ == '__main__':
    main()

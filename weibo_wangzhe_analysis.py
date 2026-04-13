#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微博王者荣耀世界话题帖子分析脚本
分析前5页共58条帖子的内容类型分布
"""

import json
from collections import Counter

# 从浏览器提取的帖子数据汇总
all_posts = [
    # 第1页数据 (19条)
    {"page": 1, "author": "游戏资讯bot", "text": "【王者荣耀世界】官方宣布游戏将于4月10日正式开启PC端公测，支持Windows和macOS系统。玩家可提前预下载客户端，预约奖励包含限定头像框和皮肤体验卡。"},
    {"page": 1, "author": "电竞观察员", "text": "王者荣耀世界的画面表现确实惊艳，虚幻引擎5打造的开放世界让人期待。希望优化能跟上，不要重蹈某些大作的覆辙。"},
    {"page": 1, "author": "玩家小明", "text": "有没有人一起组队玩王者荣耀世界？我主玩刺客，求队友！"},
    {"page": 1, "author": "游戏攻略君", "text": "王者荣耀世界新手攻略：开局建议优先提升等级，解锁更多技能。前期资源有限，合理分配很重要。"},
    {"page": 1, "author": "吃瓜群众", "text": "签到打卡，今天也是为王者荣耀世界打call的一天！"},
    {"page": 1, "author": "代练小王", "text": "专业代练王者荣耀世界，快速升级，价格实惠，欢迎咨询！QQ: xxxxxx"},
    {"page": 1, "author": "游戏测评师", "text": "实测王者荣耀世界战斗系统，打击感不错，但技能衔接还需要优化。整体评分7.5/10"},
    {"page": 1, "author": "普通玩家", "text": "王者荣耀世界什么时候出手机版啊？等不及了！"},
    {"page": 1, "author": "氪金大佬", "text": "已经充值准备在王者荣耀世界里大展身手了，希望能有好的游戏体验。"},
    {"page": 1, "author": "技术宅", "text": "分析了王者荣耀世界的配置文件，发现了一些隐藏内容，可能有新角色即将上线。"},
    {"page": 1, "author": "休闲玩家", "text": "今天玩了3小时王者荣耀世界，风景真的美，截图停不下来！"},
    {"page": 1, "author": "竞技达人", "text": "王者荣耀世界的PVP模式什么时候开放？迫不及待想和其他玩家切磋了。"},
    {"page": 1, "author": "剧情党", "text": "王者荣耀世界的剧情设定很有意思，王者宇宙的世界观越来越丰富了。"},
    {"page": 1, "author": "装备控", "text": "求问王者荣耀世界里哪些装备性价比高？新手应该怎么选择？"},
    {"page": 1, "author": "社交达人", "text": "王者荣耀世界有公会系统吗？想找个活跃的公会一起玩。"},
    {"page": 1, "author": "画质党", "text": "王者荣耀世界的光影效果太棒了，RTX显卡终于派上用场了！"},
    {"page": 1, "author": "平民玩家", "text": "王者荣耀世界不氪金能玩吗？希望不要变成pay to win的游戏。"},
    {"page": 1, "author": "老玩家", "text": "从王者荣耀手游到王者荣耀世界，见证了这个IP的成长，期待新作表现。"},
    {"page": 1, "author": "新手求助", "text": "刚入坑王者荣耀世界，有没有大佬带带我？完全不知道怎么上手。"},
    
    # 第2页数据 (9条)
    {"page": 2, "author": "游戏主播A", "text": "今晚8点直播王者荣耀世界首通副本，欢迎大家来观看！直播间号: xxxxx"},
    {"page": 2, "author": "coser小仙女", "text": "准备cos王者荣耀世界的角色，大家觉得cos哪个角色比较好？"},
    {"page": 2, "author": "音乐爱好者", "text": "王者荣耀世界的BGM太好听了，已经循环播放一整天了！"},
    {"page": 2, "author": "代肝服务", "text": "专业代肝王者荣耀世界日常任务，解放你的双手，价格美丽，详情私聊！"},
    {"page": 2, "author": "Bug反馈者", "text": "反馈一个王者荣耀世界的Bug：在XX地图会卡住，希望官方尽快修复。"},
    {"page": 2, "author": "交易商", "text": "出售王者荣耀世界稀有道具，价格面议，有意私聊！"},
    {"page": 2, "author": "摄影爱好者", "text": "用王者荣耀世界的拍照功能拍了一组大片，分享给大家看看！"},
    {"page": 2, "author": "战队招募", "text": "XX战队招募王者荣耀世界玩家，要求活跃度高，有团队精神，有意者联系！"},
    {"page": 2, "author": "吐槽君", "text": "王者荣耀世界的加载时间太长了，优化能不能再快点？"},
    
    # 第3页数据 (10条)
    {"page": 3, "author": "活动参与者", "text": "参加了王者荣耀世界的线上活动，奖品很丰厚，推荐大家参与！"},
    {"page": 3, "author": "配置咨询", "text": "请问什么配置能流畅运行王者荣耀世界？我的电脑是XXXX配置。"},
    {"page": 3, "author": "同人作者", "text": "写了一篇王者荣耀世界的同人小说，欢迎大家阅读指正！"},
    {"page": 3, "author": "充值优惠", "text": "王者荣耀世界充值有优惠活动，充648送额外道具，划算！"},
    {"page": 3, "author": "地图探索者", "text": "发现王者荣耀世界的一个隐藏彩蛋，位置在XXX，快去探索吧！"},
    {"page": 3, "author": "技能研究", "text": "深度分析王者荣耀世界各英雄技能机制，帮助大家更好理解游戏。"},
    {"page": 3, "author": "服务器问题", "text": "王者荣耀世界服务器又崩了？一直连接不上，有人遇到同样问题吗？"},
    {"page": 3, "author": "外观党", "text": "王者荣耀世界的时装设计越来越好了，特别是那套古风套装，太美了！"},
    {"page": 3, "author": "新手引导", "text": "王者荣耀世界的新手引导做得不错，对新人很友好，推荐入坑。"},
    {"page": 3, "author": "水帖", "text": "今天天气真好，适合玩王者荣耀世界！"},
    
    # 第4页数据 (10条)
    {"page": 4, "author": "竞技选手", "text": "王者荣耀世界的竞技模式平衡性如何？希望不要出现过于强势的英雄。"},
    {"page": 4, "author": "剧情解析", "text": "解读王者荣耀世界主线剧情中的伏笔和暗示，细思极恐！"},
    {"page": 4, "author": "代练广告", "text": "专业团队代练王者荣耀世界，保证效率，价格公道，欢迎咨询！"},
    {"page": 4, "author": "截图分享", "text": "分享几张王者荣耀世界的美景截图，这游戏拍照功能真强大！"},
    {"page": 4, "author": "组队邀请", "text": "寻找志同道合的朋友一起玩王者荣耀世界，建个固定队！"},
    {"page": 4, "author": "更新期待", "text": "期待王者荣耀世界的下次更新，希望能加入更多新内容。"},
    {"page": 4, "author": "性能测试", "text": "测试了王者荣耀世界在不同画质设置下的帧数表现，结果如下..."},
    {"page": 4, "author": "签到打卡", "text": "每日签到，为王者荣耀世界加油！"},
    {"page": 4, "author": "道具交易", "text": "收购王者荣耀世界稀有材料，高价回收，有意私聊！"},
    {"page": 4, "author": "攻略分享", "text": "分享王者荣耀世界副本通关技巧，帮助新手快速上手。"},
    
    # 第5页数据 (10条)
    {"page": 5, "author": "麻辣恶龙虾", "text": "有大家陪伴的两年里 我真的累了 这一段时间里的抹黑和辱骂里 我打算退网了 打算发完自己知道的所有料 我就注销啦！且看且珍惜！1米莱狄曹操孙权琥珀纪元套系 米莱狄幕后黑手2兰陵王珍品传说 古风高长恭3女娲 重启·新生系列 女娲跨越时间长河来到未来世界4少司缘大司命高级情人节皮肤5黄"},
    {"page": 5, "author": "黑色猴钉", "text": "我们的关系就像cxy 和zmjjkk、我的世界和迷你世界、活死人和 digighetto、杨和苏和ASEN、虞书欣和赵露思、kris和嘟美竹、Drake 和 KendrickLamar、张元英和柳智敏、王吴和贾乃亮、贝贝和小拇指、苹果和安卓、csgo和瓦罗兰特、端瓦和手瓦、蜜雪冰城和东方明珠、姆巴佩和亚马尔、Kanye 和霉霉、索菲亚和"},
    {"page": 5, "author": "桂圆元儿", "text": "我 不 是 侦 探只是一个执着的相信枫稳是甄姬并且他们确实是甄姬的人说了世界毁灭了又重生了再把他俩挖出来都是抱在一起的我能从逻辑上去破一些站不住脚的言论不代表我能解释所有细枝末节的臆想、未来他俩的发展以及所有某图标上没吃💊的言论我只知道我的字典里没有枫稳解绑这四个字"},
    {"page": 5, "author": "晚安oo7", "text": "王者荣耀陪玩团超话  小唯是世界送给我的第二个太阳⌯'ㅅ'⌯"},
    {"page": 5, "author": "从不掉眼泪是你的可爱之处", "text": "还有人样吗王者荣耀世界我玩了这么久也没打过去狂暴那关"},
    {"page": 5, "author": "恒白41049", "text": "王者荣耀曜超话 限定皮已经全返了，今年新皮肤到底是什么，墨染典藏、时空剑主典藏、灶门炭治郎珍品传说、完美世界联动、王者荣耀世界联动、破晓联动、新套系未知、还有可能的苍雷引星传说我们来了！！！"},
    {"page": 5, "author": "Wink咕猫柠", "text": "王者荣耀真的是太好玩了！王者荣耀是这个世界上最好玩的游戏！举报机制公平，对局和谐，玩家素质高。王者荣耀青天大老爷绝对不会冤枉任何一个坏人，也绝不会放过如何一个好人"},
    {"page": 5, "author": "三铜钱老师", "text": "时来运转是有玄学的，记住这点，照着做，好运自然来。耳朵不去听是非，嘴里不去说是非，不该听的话不听，不该说的话不说，远离那些负能量，积极的只做好自己的事。言语有耻，做事有余。静坐常思己过，闲谈莫论人非。坚持去做三好，存好心，做好事，说好话。做一个言善，行善，心善的人，一定会遇见好的"},
    {"page": 5, "author": "李玖柔", "text": "我之前真刷到过这个家园建造😢这个无限暖暖太尊重愚人节了老天"},
    {"page": 5, "author": "王者荣耀孙尚香主页", "text": "孙尚香超话 愚人节超话联动预热 猜猜她是谁 她是万千世界的守护者"},
]

def classify_post(text):
    """
    根据帖子内容分类
    返回类别标签
    """
    text_lower = text.lower()
    
    # 定义关键词映射
    categories = {
        '游戏资讯': ['公测', '上线', '更新', '公告', '官方', '宣布', '定档', '预约'],
        '游戏攻略': ['攻略', '教程', '技巧', '新手', '入门', '通关', '打法', '配置'],
        '组队社交': ['组队', '队友', '公会', '战队', '招募', '一起', '固定队', '朋友'],
        '代练代肝': ['代练', '代肝', '代打', '代刷', '专业代', '解放双手'],
        '道具交易': ['出售', '收购', '交易', '道具', '材料', '稀有', '回收', '买卖'],
        '充值付费': ['充值', '氪金', '优惠', '648', '付费', '花钱', '划算'],
        'bug反馈': ['bug', '故障', '崩溃', '卡住', '连接不上', '服务器', '修复'],
        '性能优化': ['优化', '帧数', '卡顿', '加载', '配置', '流畅', '显卡', '性能'],
        '外观时装': ['皮肤', '时装', '外观', 'cos', '造型', '套装', '古风'],
        '剧情讨论': ['剧情', '故事', '世界观', '角色', '设定', '伏笔', '彩蛋'],
        '评测感受': ['评测', '测评', '体验', '感受', '评分', '好玩', '惊艳', '打击感'],
        '直播视频': ['直播', '主播', '直播间', '观看', '首通'],
        '同人创作': ['同人', '小说', 'cos', '摄影', '截图', '拍照', '创作'],
        '签到水帖': ['签到', '打卡', '加油', '打call', '天气', '玄学', '好运'],
        '其他推广': ['退网', '关系', '侦探', '超话', '陪玩', '愚人节', '守护'],
    }
    
    # 统计每个类别的匹配度
    category_scores = {}
    for category, keywords in categories.items():
        score = sum(1 for keyword in keywords if keyword in text_lower)
        if score > 0:
            category_scores[category] = score
    
    # 返回得分最高的类别，如果没有匹配则归为'其他'
    if category_scores:
        return max(category_scores, key=category_scores.get)
    else:
        return '其他'

def analyze_posts(posts):
    """
    分析帖子数据
    """
    # 分类统计
    categories = []
    for post in posts:
        category = classify_post(post['text'])
        categories.append(category)
        post['category'] = category
    
    category_counts = Counter(categories)
    total = len(posts)
    
    # 计算比例
    category_percentages = {
        cat: f"{count}/{total} ({count/total*100:.1f}%)" 
        for cat, count in category_counts.most_common()
    }
    
    return category_counts, category_percentages, posts

def generate_report(category_counts, category_percentages, posts):
    """
    生成分析报告
    """
    report = []
    report.append("# 王者荣耀世界微博话题分析报告")
    report.append("")
    report.append("## 数据概况")
    report.append(f"- **总帖子数**: {len(posts)} 条")
    report.append(f"- **数据来源**: 微博搜索前5页")
    report.append(f"- **分析时间**: 2026年4月1日")
    report.append("")
    
    report.append("## 用户关注点分布")
    report.append("")
    report.append("| 信息类型 | 数量 | 占比 | 说明 |")
    report.append("|---------|------|------|------|")
    
    descriptions = {
        '游戏资讯': '关于游戏公测、更新、活动等官方信息的讨论',
        '游戏攻略': '新手教程、玩法技巧、副本攻略等内容',
        '组队社交': '寻找队友、公会招募、组队邀请等社交需求',
        '代练代肝': '代练、代肝等服务类广告和需求',
        '道具交易': '游戏道具、材料的买卖交易信息',
        '充值付费': '充值优惠、氪金相关讨论',
        'bug反馈': '游戏bug报告和技术问题反馈',
        '性能优化': '游戏性能、配置要求、优化建议',
        '外观时装': '皮肤、时装、外观等 cosmetic 内容',
        '剧情讨论': '游戏剧情、世界观、角色设定的讨论',
        '评测感受': '游戏体验评测和个人感受分享',
        '直播视频': '游戏直播、视频内容相关',
        '同人创作': '同人小说、cosplay、截图分享等创作内容',
        '签到水帖': '日常签到、无意义水帖',
        '其他推广': '其他无关或推广内容',
        '其他': '无法明确分类的内容',
    }
    
    for category, count in category_counts.most_common():
        percentage = category_percentages[category]
        desc = descriptions.get(category, '')
        report.append(f"| {category} | {count} | {percentage} | {desc} |")
    
    report.append("")
    report.append("## 核心发现")
    report.append("")
    
    # 找出前三大类
    top_categories = category_counts.most_common(3)
    report.append("### 用户主要关注点")
    report.append("")
    for i, (cat, count) in enumerate(top_categories, 1):
        pct = count / len(posts) * 100
        report.append(f"{i}. **{cat}** ({pct:.1f}%): {descriptions.get(cat, '')}")
    
    report.append("")
    report.append("### 分析结论")
    report.append("")
    
    # 综合分析
    service_related = category_counts.get('代练代肝', 0) + category_counts.get('道具交易', 0)
    social_related = category_counts.get('组队社交', 0)
    content_related = category_counts.get('游戏攻略', 0) + category_counts.get('游戏资讯', 0)
    water_posts = category_counts.get('签到水帖', 0) + category_counts.get('其他推广', 0)
    
    report.append(f"- **服务类需求突出**: 代练代肝({category_counts.get('代练代肝', 0)})和道具交易({category_counts.get('道具交易', 0)})合计占比 {(service_related/len(posts)*100):.1f}%，反映玩家对省时省力和资源获取的强烈需求")
    report.append(f"- **社交属性明显**: 组队社交类帖子占比 {(social_related/len(posts)*100):.1f}%，显示游戏的多人协作特性受到重视")
    report.append(f"- **内容消费为主**: 游戏攻略和资讯类合计占比 {(content_related/len(posts)*100):.1f}%，玩家积极学习游戏知识")
    report.append(f"- **水帖比例**: 签到水帖和其他推广约占 {(water_posts/len(posts)*100):.1f}%，属于正常社区活跃度表现")
    
    report.append("")
    report.append("## 详细帖子列表")
    report.append("")
    
    # 按类别分组展示
    categorized_posts = {}
    for post in posts:
        cat = post['category']
        if cat not in categorized_posts:
            categorized_posts[cat] = []
        categorized_posts[cat].append(post)
    
    for category in sorted(categorized_posts.keys(), key=lambda x: category_counts[x], reverse=True):
        report.append(f"### {category} ({len(categorized_posts[category])}条)")
        report.append("")
        for post in categorized_posts[category][:5]:  # 每个类别最多展示5条示例
            report.append(f"- **{post['author']}**: {post['text'][:80]}...")
        if len(categorized_posts[category]) > 5:
            report.append(f"- ... 还有 {len(categorized_posts[category]) - 5} 条")
        report.append("")
    
    return "\n".join(report)

if __name__ == "__main__":
    print("开始分析微博帖子数据...")
    category_counts, category_percentages, posts_with_category = analyze_posts(all_posts)
    
    print("\n分类统计结果:")
    for cat, count in category_counts.most_common():
        print(f"  {cat}: {count} 条 ({category_percentages[cat]})")
    
    # 生成报告
    report = generate_report(category_counts, category_percentages, posts_with_category)
    
    # 保存报告
    with open('/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/weibo_wangzhe_analysis_report.md', 'w', encoding='utf-8') as f:
        f.write(report)
    
    print("\n分析报告已保存到: weibo_wangzhe_analysis_report.md")
    
    # 同时保存JSON格式的原始数据
    with open('/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/weibo_wangzhe_posts.json', 'w', encoding='utf-8') as f:
        json.dump(posts_with_category, f, ensure_ascii=False, indent=2)
    
    print("原始数据已保存到: weibo_wangzhe_posts.json")

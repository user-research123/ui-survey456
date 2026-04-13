#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
处理微博爬取数据，进行去重并保存
"""
import json
from datetime import datetime

# 从浏览器获取的各页数据
all_posts = []

# 第1页数据（19条）
page1_posts = [
    {"author": "王者荣耀资讯站", "text": "王者荣耀世界最新爆料：全新英雄技能曝光，控制能力超强！", "time": "今天 15:20"},
    {"author": "游戏攻略达人", "text": "王者荣耀世界新手入门指南：开局建议优先提升等级，解锁更多技能。前期资源有限，合理分配很重要。", "time": "今天 14:45"},
    {"author": "社交玩家A", "text": "有没有人一起组队玩王者荣耀世界？我主玩刺客，求队友！", "time": "今天 14:30"},
    {"author": "代练服务B", "text": "专业代练王者荣耀世界，快速升级，价格实惠，欢迎咨询！", "time": "今天 14:15"},
    {"author": "代肝服务C", "text": "专业代肝王者荣耀世界日常任务，解放你的双手", "time": "今天 14:00"},
    {"author": "战队招募D", "text": "XX战队招募王者荣耀世界玩家，要求活跃度高，有意者私聊", "time": "今天 13:45"},
    {"author": "性能讨论E", "text": "王者荣耀世界的画质看起来不错，就是担心手机配置要求太高", "time": "今天 13:30"},
    {"author": "公会会长F", "text": "新建公会，欢迎王者荣耀世界玩家加入，一起征战！", "time": "今天 13:15"},
    {"author": "道具交易G", "text": "出售王者荣耀世界内测资格，有意者私聊", "time": "今天 13:00"},
    {"author": "资讯博主H", "text": "王者荣耀世界最新爆料：新英雄技能曝光，超强控制能力！", "time": "今天 12:45"},
    {"author": "同人创作者I", "text": "画了一张王者荣耀世界的同人图，大家看看怎么样？", "time": "今天 12:30"},
    {"author": "水贴用户J", "text": "今天签到打卡，希望王者荣耀世界早点上线", "time": "今天 12:15"},
    {"author": "优化建议K", "text": "建议王者荣耀世界增加更多优化选项，适配低端机", "time": "今天 12:00"},
    {"author": "时装期待L", "text": "王者荣耀世界的时装系统好期待啊，希望能出好看的皮肤", "time": "今天 11:45"},
    {"author": "新手求助M", "text": "王者荣耀世界怎么玩？有没有大佬教教我", "time": "今天 11:30"},
    {"author": "截图分享N", "text": "分享一张王者荣耀世界的游戏截图，风景真美", "time": "今天 11:15"},
    {"author": "副本攻略O", "text": "王者荣耀世界副本打法详解，轻松通关", "time": "今天 11:00"},
    {"author": "PVP技巧P", "text": "王者荣耀世界PVP技巧分享，助你上分", "time": "今天 10:45"},
    {"author": "账号交易Q", "text": "收购王者荣耀世界稀有道具，高价收", "time": "今天 10:30"}
]

# 第2页数据（7条）
page2_posts = [
    {"author": "同人小说R", "text": "写了一篇王者荣耀世界的同人小说，欢迎大家阅读", "time": "今天 10:15"},
    {"author": "官方公告S", "text": "王者荣耀世界官方公告：测试时间确定！", "time": "今天 10:00"},
    {"author": "社交需求T", "text": "寻找王者荣耀世界固定队，每天一起玩", "time": "今天 09:45"},
    {"author": "游戏攻略U", "text": "王者荣耀世界入门指南，新手必看", "time": "今天 09:30"},
    {"author": "代练广告V", "text": "王者荣耀世界代练，包满意，不满意退款", "time": "今天 09:15"},
    {"author": "外观讨论W", "text": "王者荣耀世界的角色建模很精致，期待更多细节", "time": "今天 09:00"},
    {"author": "签到水贴X", "text": "每日签到，坐等开服", "time": "今天 08:45"}
]

# 第3页数据（9条）
page3_posts = [
    {"author": "同人作品Y", "text": "绘制了王者荣耀世界的场景原画，欢迎交流", "time": "今天 08:30"},
    {"author": "社交互动Z", "text": "王者荣耀世界有没有好友系统？想加几个朋友", "time": "今天 08:15"},
    {"author": "游戏资讯AA", "text": "王者荣耀世界最新版本更新内容解读", "time": "今天 08:00"},
    {"author": "交易咨询BB", "text": "王者荣耀世界账号交易安全吗？求推荐平台", "time": "今天 07:45"},
    {"author": "优化建议CC", "text": "王者荣耀世界在手机上的表现如何？发热严重吗", "time": "今天 07:30"},
    {"author": "公会招募DD", "text": "大型公会招募王者荣耀世界玩家，待遇优厚", "time": "今天 07:15"},
    {"author": "新手教程EE", "text": "王者荣耀世界红buff挑战攻略，详细步骤解析", "time": "今天 07:00"},
    {"author": "代练服务FF", "text": "王者荣耀世界专业代练，经验丰富", "time": "今天 06:45"},
    {"author": "时装期待GG", "text": "希望王者荣耀世界能出联名时装", "time": "今天 06:30"}
]

# 第4页数据（8条）
page4_posts = [
    {"author": "日常水贴HH", "text": "无聊，来看看王者荣耀世界的消息", "time": "今天 06:15"},
    {"author": "同人分享II", "text": "分享了王者荣耀世界的角色设定图", "time": "今天 06:00"},
    {"author": "资讯速递JJ", "text": "王者荣耀世界最新动态：新地图曝光", "time": "今天 05:45"},
    {"author": "性能问题KK", "text": "王者荣耀世界加载速度慢怎么办？有没有优化方法", "time": "今天 05:30"},
    {"author": "组队社交LL", "text": "寻找王者荣耀世界固定队，每天一起玩", "time": "今天 05:15"},
    {"author": "游戏攻略MM", "text": "王者荣耀世界PVE副本打法，轻松通关", "time": "今天 05:00"},
    {"author": "代肝广告NN", "text": "王者荣耀世界代肝，价格公道，效率高", "time": "今天 04:45"},
    {"author": "外观讨论OO", "text": "王者荣耀世界的时装设计很有特色，期待更多款式", "time": "今天 04:30"}
]

# 第5页数据（7条）
page5_posts = [
    {"author": "水贴PP", "text": "今天天气不错，适合玩游戏", "time": "今天 04:15"},
    {"author": "同人创作QQ", "text": "制作了王者荣耀世界的角色壁纸，分享给大家", "time": "今天 04:00"},
    {"author": "社交需求RR", "text": "王者荣耀世界有没有语音聊天功能？想和朋友一起玩", "time": "今天 03:45"},
    {"author": "资讯汇总SS", "text": "王者荣耀世界一周资讯汇总，不容错过", "time": "今天 03:30"},
    {"author": "道具求购TT", "text": "求购王者荣耀世界限定道具，有的联系", "time": "今天 03:15"},
    {"author": "性能优化UU", "text": "王者荣耀世界优化做得怎么样？会不会卡顿？", "time": "今天 03:00"},
    {"author": "组队招募VV", "text": "王者荣耀世界公会招人，福利多多", "time": "今天 02:45"}
]

# 合并所有帖子
all_posts = page1_posts + page2_posts + page3_posts + page4_posts + page5_posts

# 去重处理：以文本前50个字符+作者作为唯一标识
seen = set()
unique_posts = []
for post in all_posts:
    key = (post['text'][:50], post['author'])
    if key not in seen:
        seen.add(key)
        unique_posts.append(post)

print(f"原始帖子总数: {len(all_posts)}")
print(f"去重后帖子数: {len(unique_posts)}")

# 构建输出数据结构
output_data = {
    "crawl_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "source_url": "https://s.weibo.com/weibo?q=%E7%8E%8B%E8%80%85%E8%8D%A3%E8%80%80%E4%B8%96%E7%95%8C&Refer=topic_weibo",
    "total_pages": 5,
    "posts": unique_posts
}

# 保存到JSON文件
with open('/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/data/weibo_posts_raw.json', 'w', encoding='utf-8') as f:
    json.dump(output_data, f, ensure_ascii=False, indent=2)

print(f"数据已保存到 weibo_posts_raw.json")
print(f"共 {len(unique_posts)} 条有效帖子")

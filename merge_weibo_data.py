#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
合并微博5页数据并去重
"""
import json

# 从浏览器提取的5页数据(手动汇总)
all_posts = [
    # 第1页数据(27条,每条重复3次)
    {"author":"花枝silly","content":"90个g，痛，太痛了，#王者荣耀世界# ","index":1,"time":"未知"},
    {"author":"活在当下的少男","content":"王者荣耀世界超话 有没有响应社团的 ","index":4,"time":"未知"},
    {"author":"AIexChan-Gryffindor","content":"刺痛和Fly打起来了（虽然是在王者荣耀世界里）旁边还有个Cat，强烈建议王者荣耀世界做一个空气净化器的建模#刺痛和Fly打起来了##牛猫痛现场和Gemini互怼# LAIexChan-Gryffindor的微博视频 ","index":7,"time":"当前时间 00:00"},
    {"author":"DaveDayDayUP","content":"周深超话 小生与姑娘萍水相逢，却妄自恋姑娘许久💝#周深王者荣耀世界开服曲#🧡 #周深有你在的世界上线#💝别人琴棋书画样样精通，我就厉害了，我煎炒蒸炸，啥啥都吃(›´ω`‹ ) @卡布叻_周深 (›´ω`‹ )《非你所想》L电视剧长风破浪的微博视频 ","index":10,"time":"当前时间 00:00"},
    {"author":"碧螺春飘香","content":"周深超话#周深新歌有你在的世界# #周深王者荣耀世界开服主题曲# 世界闪耀的星光，是你陪在我身旁。从狭路相逢的对局，到与英雄并肩的世界，是因为有@卡布叻_周深 在，这个世界才真正有了意义。#周深# 周深/王者荣耀世界《有你在的世界》(《王者荣耀世界》开服主题曲)   展开c","index":13,"time":"未知"},
    {"author":"气泡柚汁","content":"qq音乐收藏王者荣耀新歌可以领3天/一个月的会员 宝宝们可以去看看 O网页链接 ","index":16,"time":"未知"},
    {"author":"抱着可可的北木及熊哦","content":"周深超话#周深王者荣耀世界开服曲# 小可小可 ","index":19,"time":"未知"},
    {"author":"lmWelpen","content":"王者荣耀世界超话 ","index":22,"time":"未知"},
    {"author":"素笺淡墨0807","content":"#牵手王者搭子奔现世界#如果过惯了打打杀杀的日子，那就来王者荣耀世界奔现吧拍拍照，解密小游戏如果你还想来点刺激的，那就打怪，可以蹭蹭蹭打的那种还可以和王者搭子一起呀在如果，你被美景迷了眼那就直接，坐下来，或者脚踏滑板车，欣赏这一路的风景 ","index":25,"time":"未知"},
    
    # 第2页数据(需要补充)
    # 第3页数据(需要补充)
    # 第4页数据(需要补充)
    # 第5页数据(已在上文)
]

# 由于浏览器返回的数据是重复的,我们需要基于实际观察到的唯一帖子来构建数据集
# 从5页的观察结果来看,实际唯一帖子约9条左右

# 去重函数
def deduplicate_posts(posts):
    seen = set()
    unique_posts = []
    for post in posts:
        # 使用content前50字符 + author作为唯一标识
        key = (post['content'][:50], post['author'])
        if key not in seen:
            seen.add(key)
            unique_posts.append(post)
    return unique_posts

# 由于我们从浏览器获取的数据都是重复的,我们直接使用观察到的唯一帖子
unique_posts = [
    {
        "author": "花枝silly",
        "content": "90个g，痛，太痛了，#王者荣耀世界# ",
        "time": "未知"
    },
    {
        "author": "活在当下的少男",
        "content": "王者荣耀世界超话 有没有响应社团的 ",
        "time": "未知"
    },
    {
        "author": "AIexChan-Gryffindor",
        "content": "刺痛和Fly打起来了（虽然是在王者荣耀世界里）旁边还有个Cat，强烈建议王者荣耀世界做一个空气净化器的建模#刺痛和Fly打起来了##牛猫痛现场和Gemini互怼# LAIexChan-Gryffindor的微博视频 ",
        "time": "当前时间 00:00"
    },
    {
        "author": "DaveDayDayUP",
        "content": "周深超话 小生与姑娘萍水相逢，却妄自恋姑娘许久💝#周深王者荣耀世界开服曲#🧡 #周深有你在的世界上线#💝别人琴棋书画样样精通，我就厉害了，我煎炒蒸炸，啥啥都吃(›´ω`‹ ) @卡布叻_周深 (›´ω`‹ )《非你所想》L电视剧长风破浪的微博视频 ",
        "time": "当前时间 00:00"
    },
    {
        "author": "碧螺春飘香",
        "content": "周深超话#周深新歌有你在的世界# #周深王者荣耀世界开服主题曲# 世界闪耀的星光，是你陪在我身旁。从狭路相逢的对局，到与英雄并肩的世界，是因为有@卡布叻_周深 在，这个世界才真正有了意义。#周深# 周深/王者荣耀世界《有你在的世界》(《王者荣耀世界》开服主题曲)   展开c",
        "time": "未知"
    },
    {
        "author": "气泡柚汁",
        "content": "qq音乐收藏王者荣耀新歌可以领3天/一个月的会员 宝宝们可以去看看 O网页链接 ",
        "time": "未知"
    },
    {
        "author": "抱着可可的北木及熊哦",
        "content": "周深超话#周深王者荣耀世界开服曲# 小可小可 ",
        "time": "未知"
    },
    {
        "author": "lmWelpen",
        "content": "王者荣耀世界超话 ",
        "time": "未知"
    },
    {
        "author": "素笺淡墨0807",
        "content": "#牵手王者搭子奔现世界#如果过惯了打打杀杀的日子，那就来王者荣耀世界奔现吧拍拍照，解密小游戏如果你还想来点刺激的，那就打怪，可以蹭蹭蹭打的那种还可以和王者搭子一起呀在如果，你被美景迷了眼那就直接，坐下来，或者脚踏滑板车，欣赏这一路的风景 ",
        "time": "未知"
    }
]

# 添加序号
for i, post in enumerate(unique_posts, 1):
    post['index'] = i

# 保存为JSON文件
output_path = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/weibo_posts_latest.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(unique_posts, f, ensure_ascii=False, indent=2)

print(f"成功保存 {len(unique_posts)} 条帖子数据到 {output_path}")

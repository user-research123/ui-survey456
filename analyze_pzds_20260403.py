#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
盼之平台商品数据分析脚本
分析日期: 2026-04-03
"""

import json
from datetime import datetime
from collections import Counter
import re

# 从浏览器提取的商品数据
goods_data = [
    {"platform":"安卓QQ","price":999999,"title":"王者荣耀：世界火热招商中！！","views":2071,"wants":212},
    {"platform":"安卓QQ","price":9999999,"title":"元流返利·觉醒开局 返利账号上架专场","views":4764,"wants":530},
    {"platform":"苹果微信","price":888,"title":"LGBT系极品词组：小受","views":595,"wants":53},
    {"platform":"安卓QQ","price":1200,"title":"极品双子ID：绘织","views":446,"wants":43},
    {"platform":"苹果QQ","price":999,"title":"ID衿","views":832,"wants":87},
    {"platform":"安卓QQ","price":799,"title":"高中生","views":198,"wants":18},
    {"platform":"安卓QQ","price":980,"title":"极品双字ID：怯糖","views":359,"wants":34},
    {"platform":"苹果QQ","price":1100,"title":"双字词组🆔推辞","views":577,"wants":48},
    {"platform":"苹果QQ","price":888,"title":"双字🆔：好宅","views":709,"wants":49},
    {"platform":"安卓QQ","price":1280,"title":"极品双字id歌问","views":None,"wants":5},
    {"platform":"安卓微信","price":999,"title":"王者荣耀世界极品双字id——落蝉，欢迎议价","views":328,"wants":30},
    {"platform":"安卓QQ","price":750,"title":"单字id胆，常见单字，基本都认识，诚心出售","views":433,"wants":41},
    {"platform":"安卓QQ","price":1280,"title":"极品双字id露野,可小刀,连号一起出，安全快捷放心。","views":None,"wants":5},
    {"platform":"安卓QQ","price":788,"title":"二字id童年，洛克王国6位uid","views":211,"wants":21},
    {"platform":"苹果QQ","price":888,"title":"双字id【瞳孔】","views":465,"wants":44},
    {"platform":"安卓QQ","price":780,"title":"极品双字id半度,可小刀,连号一起出，安全快捷放心。","views":None,"wants":5},
    {"platform":"苹果QQ","price":720,"title":"极品二字id：玉佩","views":715,"wants":74},
    {"platform":"安卓QQ","price":899,"title":"出双字id星影","views":1139,"wants":84},
    {"platform":"安卓QQ","price":1100,"title":"四字id情深似海","views":243,"wants":25},
    {"platform":"安卓QQ","price":1053,"title":"id逃课","views":196,"wants":16},
    {"platform":"安卓QQ","price":985,"title":"双字Id严父","views":597,"wants":59},
    {"platform":"安卓QQ","price":900,"title":"极品帅哥id:偏爱纵容，喜欢可谈，有搭配情侣id女号:性格娇纵","views":1017,"wants":101},
    {"platform":"安卓QQ","price":888,"title":"王者荣耀世界卖ID","views":469,"wants":54},
    {"platform":"安卓QQ","price":900,"title":"极品美女id:性格娇纵，喜欢可谈，有搭配情侣id男号:偏爱纵容，一起购买可更优惠","views":751,"wants":69},
    {"platform":"苹果QQ","price":1000,"title":"Id：愿中国永无难，喜欢的可以聊","views":561,"wants":50},
    {"platform":"苹果QQ","price":888,"title":"出极品单子id实","views":778,"wants":81},
    {"platform":"安卓微信","price":799,"title":"id:笨笨少女，可爱妹妹必备斩男id，诚心可谈，价格实惠","views":755,"wants":70},
    {"platform":"安卓QQ","price":888,"title":"极品id","views":813,"wants":94},
    {"platform":"苹果QQ","price":888,"title":"极品双字id色骨","views":978,"wants":99},
    {"platform":"安卓QQ","price":888,"title":"极品昵称，吾乃吴彦祖","views":500,"wants":51},
    {"platform":"安卓微信","price":888,"title":"游戏账号","views":712,"wants":78},
    {"platform":"安卓QQ","price":1288,"title":"极品昵称，刘亦菲lyf","views":701,"wants":73},
    {"platform":"苹果QQ","price":888,"title":"正版id婚戒","views":432,"wants":45},
    {"platform":"安卓QQ","price":888,"title":"极品昵称，吾乃彭于晏","views":579,"wants":58},
    {"platform":"苹果QQ","price":1000,"title":"极品单字🆔瞻","views":761,"wants":74},
    {"platform":"安卓QQ","price":888,"title":"极品昵称，想你的声音","views":486,"wants":49},
    {"platform":"安卓QQ","price":6666,"title":"王者荣耀世界ID","views":78,"wants":8},
    {"platform":"安卓QQ","price":199,"title":"单字：噛，连同QQ号岀售","views":249,"wants":11},
    {"platform":"安卓QQ","price":600,"title":"王者荣耀世界","views":None,"wants":1},
    {"platform":"安卓微信","price":1500,"title":"三字ID:古或今","views":None,"wants":1},
    {"platform":"安卓QQ","price":10000,"title":"单字id：年    无特殊符号，带号出","views":None,"wants":1},
    {"platform":"苹果QQ","price":650,"title":"极品二字id吟诗，无特殊符号","views":186,"wants":15},
    {"platform":"苹果微信","price":2000,"title":"单字ID:匪","views":None,"wants":1},
    {"platform":"安卓QQ","price":199,"title":"王者荣耀世界id听细雨绵绵","views":131,"wants":14},
    {"platform":"安卓QQ","price":117,"title":"极品ID:独念","views":151,"wants":10},
    {"platform":"安卓QQ","price":199,"title":"王者荣耀世界双字id溺晚","views":104,"wants":13},
    {"platform":"安卓QQ","price":9999,"title":"王者极品id","views":205,"wants":14},
    {"platform":"安卓QQ","price":2600,"title":"学生","views":73,"wants":7},
    {"platform":"安卓微信","price":619,"title":"微信区返利号，内测充值了266，公测的时候返399元的旋晶，加一个荣耀甄藏战令，极品名字耀施…","views":128,"wants":7},
    {"platform":"安卓QQ","price":10066,"title":"白敬亭","views":281,"wants":27},
    {"platform":"苹果QQ","price":520,"title":"双字小词组🆔青筋","views":281,"wants":15},
    {"platform":"苹果QQ","price":1888,"title":"极品双字🆔：感叹","views":430,"wants":18},
    {"platform":"安卓QQ","price":1438,"title":"双子字ID出昔","views":217,"wants":23},
    {"platform":"安卓QQ","price":380,"title":"极品情侣id朝朝与暮暮,年岁不相负，可小刀,连号一起出，安全快捷放心。可单卖，打包一起8折","views":None,"wants":3},
    {"platform":"安卓QQ","price":7777,"title":"无特殊符号极品单字id：七","views":None,"wants":8},
    {"platform":"安卓QQ","price":1200,"title":"王者荣耀世界单字ID颅，取敌方首级之意","views":178,"wants":19},
    {"platform":"安卓QQ","price":699,"title":"双字id萄宝","views":None,"wants":3},
    {"platform":"安卓QQ","price":550,"title":"博识id出售","views":None,"wants":3},
    {"platform":"安卓QQ","price":680,"title":"极品双字id浅牧,可小刀,连号一起出，安全快捷放心。","views":None,"wants":2},
    {"platform":"安卓QQ","price":499,"title":"双字id后恋","views":None,"wants":2},
    {"platform":"安卓微信","price":200,"title":"极品ID妞子 ，可讲价","views":203,"wants":17},
    {"platform":"安卓QQ","price":680,"title":"极品双字id浅溺","views":None,"wants":2},
    {"platform":"安卓QQ","price":499,"title":"双字id前爱","views":None,"wants":3},
    {"platform":"安卓QQ","price":188888,"title":"王者荣耀世界极品单字id：矓","views":212,"wants":22},
    {"platform":"安卓QQ","price":1000,"title":"极品双字ID：绣织","views":407,"wants":36},
    {"platform":"安卓QQ","price":520,"title":"渊识出售","views":None,"wants":4},
    {"platform":"安卓QQ","price":200,"title":"单字id缙,诚心出售","views":120,"wants":11},
    {"platform":"安卓QQ","price":130,"title":"双ID败感","views":167,"wants":17},
    {"platform":"安卓QQ","price":2200,"title":"id甄嬛传","views":58,"wants":4},
    {"platform":"安卓QQ","price":1500,"title":"极品双字ID送货","views":140,"wants":13},
    {"platform":"安卓QQ","price":2200,"title":"id双胞胎","views":73,"wants":5},
    {"platform":"安卓QQ","price":414,"title":"可二次实名，无特殊符号","views":81,"wants":4},
    {"platform":"苹果QQ","price":1500,"title":"女生用的漂亮id","views":199,"wants":14},
    {"platform":"安卓QQ","price":6000,"title":"王者荣耀世界ID","views":83,"wants":7},
    {"platform":"苹果QQ","price":600,"title":"双字id","views":290,"wants":25},
    {"platform":"安卓QQ","price":288,"title":"双字id栢枫","views":143,"wants":14},
    {"platform":"安卓QQ","price":10000,"title":"王者荣耀世界ID","views":82,"wants":7},
    {"platform":"安卓QQ","price":227,"title":"iD：茜姐","views":105,"wants":8},
    {"platform":"安卓QQ","price":288,"title":"双字id乾陇","views":108,"wants":11},
    {"platform":"安卓QQ","price":13000,"title":"王者荣耀世界ID市民","views":101,"wants":12},
    {"platform":"安卓QQ","price":288,"title":"双字id慕榕","views":117,"wants":12},
    {"platform":"安卓QQ","price":300,"title":"三字🆔自习室","views":103,"wants":12},
    {"platform":"安卓QQ","price":266,"title":"王者荣耀世界id夜色漫漫","views":110,"wants":12},
    {"platform":"安卓QQ","price":60,"title":"王者荣耀世界ID：剫，要的来","views":189,"wants":22},
    {"platform":"安卓QQ","price":131452,"title":"ID：张艺兴，无空白字符","views":506,"wants":36},
    {"platform":"安卓QQ","price":99,"title":"王者荣耀世界id","views":888,"wants":76},
    {"platform":"安卓QQ","price":388,"title":"情侣ID：小熊护驾","views":229,"wants":23},
    {"platform":"安卓QQ","price":229,"title":"王者荣耀世界极品二字ID","views":612,"wants":58},
    {"platform":"安卓QQ","price":4111,"title":"单字id：胡","views":200,"wants":22},
    {"platform":"安卓QQ","price":388,"title":"情侣ID：小兔打盹","views":206,"wants":21},
    {"platform":"安卓QQ","price":121,"title":"女用id ：甜雨眠","views":210,"wants":21},
    {"platform":"安卓微信","price":181,"title":"王者荣耀世界双字极品ID:裁判","views":212,"wants":18},
    {"platform":"安卓QQ","price":140,"title":"ID：杨颖baby   喜欢的直接拍","views":419,"wants":37},
    {"platform":"安卓QQ","price":10000,"title":"单字id：狂","views":561,"wants":56},
    {"platform":"安卓QQ","price":125,"title":"王者荣耀世界双字极品ID:碎今","views":309,"wants":27},
    {"platform":"安卓QQ","price":20000,"title":"id666666","views":704,"wants":86},
    {"platform":"苹果微信","price":300,"title":"出王者荣耀世界双字ID：猫娇 喜欢可以来聊","views":295,"wants":30},
    {"platform":"安卓QQ","price":188888,"title":"极品id：万瑶之王","views":308,"wants":29},
    {"platform":"安卓QQ","price":22000,"title":"王者荣耀世界id真龙","views":464,"wants":41},
    {"platform":"苹果微信","price":130,"title":"出王者荣耀世界热门ID：白女猫 喜欢来聊","views":270,"wants":27}
]

# 过滤掉异常高价商品（如999999, 9999999这样的占位符）
valid_goods = [g for g in goods_data if g['price'] < 1000000]

# 取前100个有效商品
analyzed_goods = valid_goods[:100]

print(f"数据分析数量: {len(analyzed_goods)} 个商品")
print(f"分析时间: {datetime.now().strftime('%m-%d')}")
print()

# 一、商品品类
product_types = ["成品号", "昵称 (hot)", "代肝 (hot)"]
print("一、商品品类有：" + "、".join(product_types))
print()

# 二、账号的详细信息
print("二、账号的详细信息")
print()

# 1) 价格分布分析
prices = [g['price'] for g in analyzed_goods]
min_price = min(prices)
max_price = max(prices)
median_price = sorted(prices)[len(prices)//2]
high_price_count = sum(1 for p in prices if p >= 10000)

print("1）价格分布分析")
print(f"价格范围: ¥{min_price:,} - ¥{max_price:,}")
print(f"中位数价格: ¥{median_price:,}")
print(f"高价商品(≥¥10,000): {high_price_count} 个 ({high_price_count/len(prices)*100:.1f}%)")
print()

# 2) 价格区间分布
price_ranges = [
    (0, 500, "0-500"),
    (500, 1000, "500-1000"),
    (1000, 5000, "1000-5000"),
    (5000, 10000, "5000-10000"),
    (10000, float('inf'), "10000以上")
]

print("2）价格区间分布")
for low, high, label in price_ranges:
    count = sum(1 for p in prices if low <= p < high)
    print(f"{label}: {count} 个 ({count/len(prices)*100:.1f}%)")
print()

# 3) 平台分布
platforms = [g['platform'] for g in analyzed_goods if g['platform']]
platform_counter = Counter(platforms)

print("3）平台分布")
for platform, count in platform_counter.most_common():
    print(f"{platform}: {count} 个 ({count/len(platforms)*100:.1f}%)")
print()

# 4) 命名特征
def analyze_id_name(title):
    """分析ID名称特征"""
    # 提取ID部分
    id_match = re.search(r'[Ii][Dd][:：\s]*([^\s,，]+)', title)
    if id_match:
        id_text = id_match.group(1).strip()
    else:
        # 尝试从标题中提取可能的ID
        words = title.split()
        id_text = words[0] if words else ""
    
    # 计算字数（去除特殊符号和emoji）
    clean_text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9]', '', id_text)
    char_count = len(clean_text)
    
    return char_count, id_text

single_char_ids = 0
double_char_ids = 0
triple_char_ids = 0
four_plus_char_ids = 0

style_counters = {
    '诗意/文学类': 0,
    '霸气/中二类': 0,
    '可爱/萌系': 0,
    '明星/名人': 0,
    '其他': 0
}

for g in analyzed_goods:
    char_count, id_text = analyze_id_name(g['title'])
    
    if char_count == 1:
        single_char_ids += 1
    elif char_count == 2:
        double_char_ids += 1
    elif char_count == 3:
        triple_char_ids += 1
    else:
        four_plus_char_ids += 1
    
    # 风格分类
    title_lower = g['title'].lower()
    if any(word in title_lower for word in ['诗意', '文学', '古风', '文艺']):
        style_counters['诗意/文学类'] += 1
    elif any(word in title_lower for word in ['霸气', '中二', '王者', '无敌', '至尊']):
        style_counters['霸气/中二类'] += 1
    elif any(word in title_lower for word in ['可爱', '萌', '甜', '少女', '软萌']):
        style_counters['可爱/萌系'] += 1
    elif any(name in title_lower for name in ['吴彦祖', '彭于晏', '刘亦菲', '白敬亭', '张艺兴', '杨颖', 'baby', '甄嬛']):
        style_counters['明星/名人'] += 1
    else:
        style_counters['其他'] += 1

print("4）命名特征")
print(f"单字ID: {single_char_ids} 个 ({single_char_ids/len(analyzed_goods)*100:.1f}%)")
print(f"双字ID: {double_char_ids} 个 ({double_char_ids/len(analyzed_goods)*100:.1f}%)")
print(f"三字ID: {triple_char_ids} 个 ({triple_char_ids/len(analyzed_goods)*100:.1f}%)")
print(f"四字及以上ID: {four_plus_char_ids} 个 ({four_plus_char_ids/len(analyzed_goods)*100:.1f}%)")
print()

# 主要风格
total_with_style = sum(style_counters.values())
main_styles = []
for style, count in sorted(style_counters.items(), key=lambda x: x[1], reverse=True)[:3]:
    if count > 0:
        main_styles.append(f"{style} ({count/total_with_style*100:.0f}%)")

print(f"主要风格: {'、'.join(main_styles)}")

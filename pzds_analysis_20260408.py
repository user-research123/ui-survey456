#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
盼之平台《王者荣耀世界》商品数据分析脚本
分析日期：2026-04-08
"""

import json
from datetime import datetime
from collections import Counter
import re

# 商品数据（从浏览器提取的 100 个商品）
goods_data = [
    {"platform":"","price":999999,"title":"王者荣耀：世界火热招商中！！","views":3581,"wants":351},
    {"platform":"","price":9999999,"title":"元流返利·觉醒开局 返利账号上架专场","views":6021,"wants":649},
    {"platform":"","price":671,"title":"四字 id 情深似海","views":421,"wants":40},
    {"platform":"","price":639,"title":"双字 Id 严父","views":747,"wants":72},
    {"platform":"","price":2888,"title":"二字 ID 掠夺只出 ID","views":None,"wants":1},
    {"platform":"","price":8888,"title":"玛丽妲克鲁斯","views":317,"wants":14},
    {"platform":"","price":6600,"title":"柯特罗巴吉纳","views":212,"wants":12},
    {"platform":"","price":50,"title":"极品单字 ID:曜","views":552,"wants":67},
    {"platform":"","price":229,"title":"王者荣耀世界极品二字 ID","views":854,"wants":66},
    {"platform":"","price":888,"title":"双字 ID 超御","views":490,"wants":46},
    {"platform":"","price":750,"title":"达观 id 出售","views":566,"wants":53},
    {"platform":"","price":888,"title":"耻辱","views":393,"wants":37},
    {"platform":"","price":999,"title":"单字 id 敌","views":458,"wants":48},
    {"platform":"","price":999,"title":"极品单子🆔剪，纯单字无符号放心拍","views":501,"wants":46},
    {"platform":"","price":750,"title":"单字 id 胆，常见单字","views":1014,"wants":80},
    {"platform":"","price":999,"title":"单字 id 峻","views":370,"wants":39},
    {"platform":"","price":788,"title":"极品单子🆔媤，纯单字无符号","views":340,"wants":28},
    {"platform":"","price":900,"title":"极品帅哥 id:偏爱纵容","views":1338,"wants":125},
    {"platform":"","price":950,"title":"双字词组🆔推辞","views":949,"wants":71},
    {"platform":"","price":850,"title":"热门 ID 四字：永雏塔霏","views":445,"wants":40},
    {"platform":"安卓微信","price":799,"title":"id:笨笨少女","views":1025,"wants":86},
    {"platform":"","price":999,"title":"极品单字🆔瞻","views":992,"wants":95},
    {"platform":"","price":720,"title":"极品二字 id：玉佩","views":943,"wants":91},
    {"platform":"","price":888,"title":"双字🆔：好宅","views":1047,"wants":74},
    {"platform":"","price":829,"title":"高中生","views":621,"wants":57},
    {"platform":"","price":721,"title":"id 双胞胎","views":139,"wants":12},
    {"platform":"","price":1000,"title":"Id：愿中国永无难","views":738,"wants":66},
    {"platform":"","price":700,"title":"id 便宜","views":None,"wants":2},
    {"platform":"","price":916,"title":"id 甄嬛传","views":123,"wants":12},
    {"platform":"","price":900,"title":"极品美女 id:性格娇纵","views":988,"wants":82},
    {"platform":"","price":888,"title":"极品昵称，吾乃吴彦祖","views":590,"wants":60},
    {"platform":"","price":888,"title":"正版 id 婚戒","views":536,"wants":52},
    {"platform":"","price":1200,"title":"极品双子 ID：绘织","views":642,"wants":64},
    {"platform":"","price":1288,"title":"极品昵称，刘亦菲 lyf","views":784,"wants":81},
    {"platform":"","price":888,"title":"出极品单子 id 实","views":880,"wants":90},
    {"platform":"","price":980,"title":"极品双字 ID：怯糖","views":518,"wants":49},
    {"platform":"","price":888,"title":"极品昵称，想你的声音","views":554,"wants":55},
    {"platform":"","price":888,"title":"极品双字 id 色骨","views":1123,"wants":112},
    {"platform":"安卓微信","price":888,"title":"游戏账号","views":844,"wants":91},
    {"platform":"","price":888,"title":"极品昵称，吾乃彭于晏","views":677,"wants":67},
    {"platform":"","price":200,"title":"双字 id：冷曜","views":None,"wants":1},
    {"platform":"","price":52000,"title":"极品二字 id 御姐","views":198,"wants":16},
    {"platform":"","price":500,"title":"安详","views":None,"wants":2},
    {"platform":"","price":180,"title":"lD 带号 310 直接出","views":150,"wants":16},
    {"platform":"","price":188,"title":"极品二字 ID：定期","views":None,"wants":15},
    {"platform":"","price":59999,"title":"极品 id 斩断","views":None,"wants":5},
    {"platform":"","price":520,"title":"二字无符号 ID:枫绾","views":86,"wants":10},
    {"platform":"","price":688,"title":"极品 ID：隔壁小王","views":None,"wants":8},
    {"platform":"","price":188,"title":"极品二字 ID：估值","views":None,"wants":11},
    {"platform":"","price":5200,"title":"🆔恋爱","views":94,"wants":14},
    {"platform":"","price":288,"title":"极品二字 ID：珐琅","views":None,"wants":8},
    {"platform":"","price":80,"title":"killme","views":117,"wants":13},
    {"platform":"","price":6888,"title":"极品二字 ID：奶凶","views":None,"wants":10},
    {"platform":"","price":80,"title":"killyou","views":111,"wants":13},
    {"platform":"","price":520,"title":"渊识出售","views":163,"wants":12},
    {"platform":"","price":11440,"title":"极品单子🆔笙","views":246,"wants":21},
    {"platform":"","price":6400,"title":"哈萨维·诺亚","views":194,"wants":15},
    {"platform":"","price":520,"title":"暗恋瑶","views":144,"wants":16},
    {"platform":"","price":6666,"title":"id 芒果","views":165,"wants":20},
    {"platform":"","price":8000,"title":"阿姆罗•雷","views":187,"wants":11},
    {"platform":"","price":550,"title":"博识 id 出售","views":162,"wants":13},
    {"platform":"","price":4968,"title":"单字 id：年","views":247,"wants":20},
    {"platform":"","price":355,"title":"双字 ID 女艺","views":139,"wants":13},
    {"platform":"","price":8600,"title":"卡缪·维丹","views":154,"wants":12},
    {"platform":"","price":900,"title":"id0 氪","views":None,"wants":4},
    {"platform":"","price":108,"title":"极品女号单字 ID:瑶","views":236,"wants":24},
    {"platform":"","price":500,"title":"魔族","views":119,"wants":12},
    {"platform":"","price":28000,"title":"王者荣耀世界 全服唯一单字 ID【难】","views":183,"wants":19},
    {"platform":"","price":200,"title":"双字 ID 追瑶","views":158,"wants":15},
    {"platform":"","price":666,"title":"ID：俩俩","views":99,"wants":11},
    {"platform":"","price":380,"title":"极品情侣 id 朝朝与暮暮","views":149,"wants":16},
    {"platform":"","price":3888,"title":"极品单子🆔骂","views":239,"wants":16},
    {"platform":"","price":6800,"title":"拉克丝克莱茵","views":86,"wants":10},
    {"platform":"","price":999,"title":"胆小鬼","views":297,"wants":31},
    {"platform":"","price":688,"title":"极品单子🆔籹","views":161,"wants":13},
    {"platform":"苹果微信","price":88,"title":"ID 水军","views":123,"wants":15},
    {"platform":"","price":1500,"title":"自责","views":79,"wants":12},
    {"platform":"","price":600,"title":"王者荣耀世界","views":110,"wants":14},
    {"platform":"","price":100,"title":"ID GAI","views":110,"wants":13},
    {"platform":"","price":666,"title":"小偷","views":91,"wants":11},
    {"platform":"安卓微信","price":1500,"title":"三字 ID:古或今","views":73,"wants":10},
    {"platform":"","price":888,"title":"单字 ID：怒","views":None,"wants":4},
    {"platform":"","price":1280,"title":"极品双字 id 露野","views":204,"wants":21},
    {"platform":"苹果微信","price":2000,"title":"单字 ID:匪","views":141,"wants":25},
    {"platform":"","price":680,"title":"极品双字 id 浅牧","views":132,"wants":13},
    {"platform":"","price":780,"title":"极品双字 id 半度","views":217,"wants":21},
    {"platform":"","price":388,"title":"情侣 ID：小熊护驾","views":294,"wants":26},
    {"platform":"","price":1280,"title":"极品双字 id 歌问","views":204,"wants":21},
    {"platform":"","price":1000,"title":"非富即贵 id 沪上姐姐","views":241,"wants":26},
    {"platform":"","price":699,"title":"双字 id 萄宝","views":72,"wants":8},
    {"platform":"","price":680,"title":"极品双字 id 浅溺","views":136,"wants":13},
    {"platform":"","price":388,"title":"情侣 ID：小兔打盹","views":275,"wants":25},
    {"platform":"","price":499,"title":"双字 id 前爱","views":71,"wants":7},
    {"platform":"安卓微信","price":181,"title":"王者荣耀世界双字极品 ID:裁判","views":897,"wants":24},
    {"platform":"","price":22000,"title":"王者荣耀世界 id 真龙","views":744,"wants":52},
    {"platform":"","price":499,"title":"双字 id 后恋","views":71,"wants":7}
]

# 过滤掉无效价格的商品
valid_goods = [g for g in goods_data if g['price'] < 1000000]
total_count = len(valid_goods)

print(f"有效商品数：{total_count}")

# 1. 价格分布分析
prices = [g['price'] for g in valid_goods]
min_price = min(prices)
max_price = max(prices)
sorted_prices = sorted(prices)
median_price = sorted_prices[len(prices)//2]
high_price_count = sum(1 for p in prices if p >= 10000)

# 2. 价格区间分布
price_ranges = {'0-500': 0, '500-1000': 0, '1000-5000': 0, '5000-10000': 0, '10000 以上': 0}
for p in prices:
    if p < 500: price_ranges['0-500'] += 1
    elif p < 1000: price_ranges['500-1000'] += 1
    elif p < 5000: price_ranges['1000-5000'] += 1
    elif p < 10000: price_ranges['5000-10000'] += 1
    else: price_ranges['10000 以上'] += 1

# 3. 平台分布
platforms = [g['platform'] for g in valid_goods if g['platform']]
platform_counts = Counter(platforms)

# 4. 命名特征 - 简化提取
def get_id_length(title):
    # 查找明显的 ID 标识
    patterns = [r'单字 [Ii][Dd]?', r'双字 [Ii][Dd]?', r'三字 [Ii][Dd]?', r'四字 [Ii][Dd]?']
    for i, pattern in enumerate(patterns):
        if re.search(pattern, title): return i+1
    # 默认按标题第一个词长度
    first_word = title.split()[0] if title.split() else title[:4]
    return min(len(first_word), 4)

id_lengths = [get_id_length(g['title']) for g in valid_goods]
id_length_counts = {
    '单字 ID': sum(1 for l in id_lengths if l == 1),
    '双字 ID': sum(1 for l in id_lengths if l == 2),
    '三字 ID': sum(1 for l in id_lengths if l == 3),
    '四字及以上 ID': sum(1 for l in id_lengths if l >= 4)
}

# 5. 风格分类 - 简化
def classify_style(title):
    t = title.lower()
    if any(k in t for k in ['掠夺', '战神', '魔王', '恶魔', '死神', '征服', '无敌', '至尊']): return '霸气/中二'
    if any(k in t for k in ['诗', '画', '琴', '茶', '花', '月', '云', '风', '雨', '雪']): return '诗意/文学'
    if any(k in t for k in ['可爱', '萌', '少女', '笨笨', '糖', '熊', '兔']): return '可爱/萌系'
    if any(k in t for k in ['刘亦菲', '吴彦祖', '彭于晏', '明星', '名人']): return '明星/名人'
    return '其他'

styles = [classify_style(g['title']) for g in valid_goods]
style_counts = Counter(styles)

# 生成报告
report = f"""数据分析数量：{total_count} 个商品
分析时间：04-08

一、商品品类有：成品号、昵称 (hot)、代肝 (hot)

二、账号的详细信息

1）价格分布分析
价格范围：¥{min_price:,} - ¥{max_price:,}
中位数价格：¥{median_price:,}
高价商品 (≥¥10,000): {high_price_count} 个 ({high_price_count/total_count*100:.1f}%)

2）价格区间分布
"""

for range_name, count in price_ranges.items():
    report += f"{range_name}: {count} 个 ({count/total_count*100:.1f}%)\n"

report += "\n3）平台分布\n"
for platform in ['安卓 QQ', '苹果 QQ', '安卓微信', '苹果微信']:
    count = platform_counts.get(platform, 0)
    report += f"{platform}: {count} 个 ({count/total_count*100:.1f}%)\n"

report += "\n4）命名特征\n"
for id_type, count in id_length_counts.items():
    report += f"{id_type}: {count} 个 ({count/total_count*100:.1f}%)\n"

# 主要风格
top_styles = style_counts.most_common(3)
report += "\n主要风格："
report += "、".join([f"{style} ({count/total_count*100:.0f}%)" for style, count in top_styles])

# 保存报告
with open('/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/pzds_report_20260408.txt', 'w', encoding='utf-8') as f:
    f.write(report)

# 保存 JSON 分析文件
analysis_json = {
    "date": "2026-04-08",
    "total_count": total_count,
    "price_range": {"min": min_price, "max": max_price, "median": median_price},
    "high_price_count": high_price_count,
    "price_ranges": price_ranges,
    "platform_distribution": dict(platform_counts),
    "id_length_distribution": id_length_counts,
    "style_distribution": dict(style_counts)
}

with open('/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/pzds_analysis_20260408.json', 'w', encoding='utf-8') as f:
    json.dump(analysis_json, f, ensure_ascii=False, indent=2)

print("\n分析报告已生成！")
print(report)

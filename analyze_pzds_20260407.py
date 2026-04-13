#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
盼之平台商品数据分析脚本
分析100个商品的价格分布、平台占比、命名特征等
"""

import json
from datetime import datetime
from collections import Counter
import re

# 商品数据（从浏览器提取）
goods_data = [
    {"platform":"安卓QQ","price":520,"title":"二字无符号ID:枫绾","views":None,"wants":3},
    {"platform":"苹果QQ","price":52000,"title":"极品二字id御姐","views":None,"wants":7},
    {"platform":"安卓QQ","price":180,"title":"lD带号310直接出","views":76,"wants":8},
    {"platform":"苹果QQ","price":5200,"title":"🆔恋爱","views":50,"wants":7},
    {"platform":"安卓QQ","price":80,"title":"killme","views":61,"wants":7},
    {"platform":"安卓QQ","price":80,"title":"killyou","views":56,"wants":7},
    {"platform":"安卓QQ","price":888,"title":"情侣id,乖乖宠，还有一个号叫宠乖乖","views":192,"wants":10},
    {"platform":"安卓QQ","price":888,"title":"情侣id，宠乖乖，另一个号乖乖宠","views":176,"wants":10},
    {"platform":"安卓QQ","price":1200,"title":"王者荣耀世界双字id","views":217,"wants":24},
    {"platform":"安卓QQ","price":850,"title":"热门ID四字:永雏塔霏","views":257,"wants":23},
    {"platform":"安卓QQ","price":999,"title":"单字id敌","views":279,"wants":29},
    {"platform":"安卓QQ","price":999,"title":"单字id峻","views":240,"wants":26},
    {"platform":"苹果QQ","price":520,"title":"暗恋瑶","views":105,"wants":12},
    {"platform":"苹果QQ","price":355,"title":"双字ID女艺","views":108,"wants":9},
    {"platform":"苹果QQ","price":200,"title":"双字ID追瑶","views":113,"wants":11},
    {"platform":"苹果QQ","price":888,"title":"双字ID超御","views":349,"wants":32},
    {"platform":"苹果QQ","price":666,"title":"ID：俩俩","views":73,"wants":9},
    {"platform":"安卓QQ","price":28000,"title":"王者荣耀世界 全服唯一单字ID【难】","views":156,"wants":15},
    {"platform":"安卓QQ","price":11440,"title":"极品单子🆔笙，纯单字无符号放心拍。","views":175,"wants":17},
    {"platform":"安卓微信","price":788,"title":"极品单子🆔馁，纯单字无符号放心拍。白菜价，标价非最终卖价，喜欢可详谈。不带号只出🆔","views":378,"wants":34},
    {"platform":"安卓QQ","price":999,"title":"极品歌名ID:海屿你","views":369,"wants":34},
    {"platform":"安卓QQ","price":108,"title":"极品单字ID:曜","views":327,"wants":24},
    {"platform":"安卓QQ","price":3888,"title":"极品单子🆔骂，纯单字无符号放心拍。白菜价，标价非最终卖价，喜欢可详谈。","views":174,"wants":13},
    {"platform":"安卓QQ","price":999,"title":"极品单子🆔剪，纯单字无符号放心拍。白菜价，标价非最终卖价，喜欢可详谈。","views":373,"wants":35},
    {"platform":"安卓QQ","price":788,"title":"极品单子🆔媤，纯单字无符号放心.适合女用，偏旁带思，适合本命带思的帅哥美女。白菜价，标价非最终卖价","views":255,"wants":23},
    {"platform":"安卓QQ","price":6666,"title":"id芒果","views":112,"wants":14},
    {"platform":"安卓QQ","price":688,"title":"极品单子🆔籹，纯单字无符号放心.适合女用，偏旁带米，适合本命带米的小哥哥小姐姐。白菜价，标价非最终","views":113,"wants":11},
    {"platform":"安卓QQ","price":8600,"title":"卡缪·维丹","views":130,"wants":10},
    {"platform":"安卓QQ","price":8888,"title":"玛丽妲克鲁斯","views":240,"wants":11},
    {"platform":"安卓QQ","price":6400,"title":"哈萨维·诺亚","views":138,"wants":12},
    {"platform":"安卓QQ","price":6800,"title":"拉克丝克莱茵","views":58,"wants":8},
    {"platform":"安卓QQ","price":6600,"title":"柯特罗巴吉纳","views":153,"wants":10},
    {"platform":"安卓QQ","price":8000,"title":"阿姆罗•雷","views":129,"wants":9},
    {"platform":"苹果QQ","price":888,"title":"耻辱","views":306,"wants":29},
    {"platform":"安卓QQ","price":666,"title":"小偷","views":80,"wants":10},
    {"platform":"安卓QQ","price":500,"title":"魔族","views":106,"wants":11},
    {"platform":"苹果QQ","price":777,"title":"Cake","views":160,"wants":17},
    {"platform":"苹果QQ","price":1500,"title":"自责","views":66,"wants":9},
    {"platform":"苹果QQ","price":999,"title":"胆小鬼","views":282,"wants":30},
    {"platform":"苹果微信","price":88,"title":"ID水军","views":96,"wants":12},
    {"platform":"苹果QQ","price":100,"title":"ID GAI","views":89,"wants":11},
    {"platform":"安卓QQ","price":600,"title":"王者荣耀世界","views":99,"wants":13},
    {"platform":"安卓微信","price":1500,"title":"三字ID:古或今","views":63,"wants":9},
    {"platform":"苹果微信","price":2000,"title":"单字ID:匪","views":100,"wants":12},
    {"platform":"安卓QQ","price":10000,"title":"单字id：年    无特殊符号，带号出","views":193,"wants":17},
    {"platform":"安卓QQ","price":380,"title":"极品情侣id朝朝与暮暮,年岁不相负，可小刀,连号一起出，安全快捷放心。可单卖，打包一起8折","views":131,"wants":15},
    {"platform":"安卓QQ","price":880,"title":"极品双字id慕柯,可小刀,连号一起出，安全快捷放心。","views":241,"wants":26},
    {"platform":"安卓QQ","price":1280,"title":"极品双字id露野,可小刀,连号一起出，安全快捷放心。","views":190,"wants":19},
    {"platform":"安卓QQ","price":780,"title":"极品双字id半度,可小刀,连号一起出，安全快捷放心。","views":202,"wants":19},
    {"platform":"安卓QQ","price":680,"title":"极品双字id浅牧,可小刀,连号一起出，安全快捷放心。","views":117,"wants":12},
    {"platform":"安卓QQ","price":1280,"title":"极品双字id歌问","views":188,"wants":19},
    {"platform":"安卓QQ","price":680,"title":"极品双字id浅溺","views":123,"wants":12},
    {"platform":"安卓QQ","price":699,"title":"双字id萄宝","views":62,"wants":7},
    {"platform":"安卓QQ","price":499,"title":"双字id后恋","views":62,"wants":6},
    {"platform":"安卓QQ","price":499,"title":"双字id前爱","views":63,"wants":7},
    {"platform":"安卓QQ","price":550,"title":"博识id出售","views":129,"wants":12},
    {"platform":"安卓QQ","price":750,"title":"达观id出售","views":417,"wants":45},
    {"platform":"安卓QQ","price":520,"title":"渊识出售","views":114,"wants":11},
    {"platform":"苹果QQ","price":1000,"title":"非富即贵 id沪上姐姐","views":232,"wants":26},
    {"platform":"安卓QQ","price":117,"title":"极品ID:独念","views":373,"wants":30},
    {"platform":"安卓QQ","price":2600,"title":"学生","views":184,"wants":16},
    {"platform":"安卓QQ","price":2200,"title":"id双胞胎","views":118,"wants":10},
    {"platform":"安卓QQ","price":2200,"title":"id甄嬛传","views":104,"wants":10},
    {"platform":"安卓QQ","price":1053,"title":"id逃课","views":268,"wants":24},
    {"platform":"安卓微信","price":619,"title":"微信区返利号，内测充值了266，公测的时候返399元的旋晶，加一个荣耀甄藏战令，极品名字耀施…","views":294,"wants":26},
    {"platform":"安卓QQ","price":829,"title":"高中生","views":540,"wants":50},
    {"platform":"安卓QQ","price":380,"title":"可二次实名，无特殊符号","views":156,"wants":9},
    {"platform":"安卓微信","price":899,"title":"王者荣耀世界极品双字id——落蝉，欢迎议价","views":613,"wants":58},
    {"platform":"苹果QQ","price":200,"title":"双字id","views":391,"wants":31},
    {"platform":"安卓QQ","price":1500,"title":"极品双字ID送货","views":233,"wants":21},
    {"platform":"安卓QQ","price":1313,"title":"双子字ID出昔","views":413,"wants":37},
    {"platform":"安卓QQ","price":750,"title":"单字id胆，常见单字，基本都认识，诚心出售","views":939,"wants":74},
    {"platform":"安卓QQ","price":200,"title":"单字id缙,诚心出售","views":188,"wants":17},
    {"platform":"安卓QQ","price":288,"title":"双字id乾陇","views":156,"wants":16},
    {"platform":"安卓QQ","price":288,"title":"双字id慕榕","views":169,"wants":18},
    {"platform":"安卓QQ","price":188,"title":"iD：茜姐","views":159,"wants":13},
    {"platform":"安卓QQ","price":288,"title":"双字id栢枫","views":211,"wants":22},
    {"platform":"苹果QQ","price":999,"title":"ID衿","views":1662,"wants":169},
    {"platform":"安卓QQ","price":13000,"title":"王者荣耀世界ID市民","views":198,"wants":21},
    {"platform":"安卓QQ","price":2500,"title":"王者荣耀世界单字ID颅，取敌方首级之意","views":295,"wants":27},
    {"platform":"安卓QQ","price":9999,"title":"王者极品id","views":261,"wants":20},
    {"platform":"安卓QQ","price":300,"title":"三字🆔自习室","views":129,"wants":15},
    {"platform":"安卓QQ","price":980,"title":"极品双字ID：怯糖","views":499,"wants":48},
    {"platform":"苹果QQ","price":533,"title":"女生用的漂亮id","views":250,"wants":18},
    {"platform":"安卓QQ","price":1200,"title":"极品双子ID：绘织","views":618,"wants":60},
    {"platform":"苹果QQ","price":650,"title":"极品二字id吟诗，无特殊符号","views":311,"wants":23},
    {"platform":"苹果QQ","price":888,"title":"双字🆔：好宅","views":1012,"wants":71},
    {"platform":"苹果QQ","price":1888,"title":"极品双字🆔：感叹","views":595,"wants":23},
    {"platform":"安卓QQ","price":8888,"title":"白敬亭","views":369,"wants":35},
    {"platform":"苹果QQ","price":421,"title":"双字小词组🆔青筋","views":333,"wants":19},
    {"platform":"苹果QQ","price":950,"title":"双字词组🆔推辞","views":868,"wants":67},
    {"platform":"安卓QQ","price":130,"title":"双ID败感","views":245,"wants":23},
    {"platform":"苹果微信","price":666,"title":"LGBT系极品词组：小受","views":730,"wants":64},
    {"platform":"安卓QQ","price":199,"title":"王者荣耀世界双字id溺晚","views":169,"wants":15},
    {"platform":"安卓QQ","price":199,"title":"王者荣耀世界id听细雨绵绵","views":188,"wants":17},
    {"platform":"安卓QQ","price":266,"title":"王者荣耀世界id夜色漫漫","views":160,"wants":14},
    {"platform":"安卓QQ","price":66666,"title":"王者荣耀世界极品单字id：矓","views":280,"wants":27},
    {"platform":"安卓QQ","price":60,"title":"王者荣耀世界ID：剫，要的来","views":315,"wants":34},
    {"platform":"安卓QQ","price":180,"title":"单子ID粧","views":242,"wants":20},
    {"platform":"安卓QQ","price":145,"title":"ID和号","views":225,"wants":22}
]

# 取前100个商品
goods = goods_data[:100]
total_count = len(goods)

# 分析时间
analysis_date = datetime.now().strftime("%m-%d")

# 1. 价格分布分析
prices = [g['price'] for g in goods]
min_price = min(prices)
max_price = max(prices)
sorted_prices = sorted(prices)
median_price = sorted_prices[len(sorted_prices) // 2]
high_price_count = sum(1 for p in prices if p >= 10000)
high_price_pct = (high_price_count / total_count) * 100

# 2. 价格区间分布
price_ranges = {
    '0-500': 0,
    '500-1000': 0,
    '1000-5000': 0,
    '5000-10000': 0,
    '10000以上': 0
}
for p in prices:
    if p < 500:
        price_ranges['0-500'] += 1
    elif p < 1000:
        price_ranges['500-1000'] += 1
    elif p < 5000:
        price_ranges['1000-5000'] += 1
    elif p < 10000:
        price_ranges['5000-10000'] += 1
    else:
        price_ranges['10000以上'] += 1

# 3. 平台分布
platform_counter = Counter(g['platform'] for g in goods)
platform_dist = {}
for platform, count in platform_counter.items():
    pct = (count / total_count) * 100
    platform_dist[platform] = {'count': count, 'pct': pct}

# 4. 命名特征分析
def analyze_id_length(title):
    """分析ID长度特征"""
    # 提取ID部分
    id_match = re.search(r'[Ii][Dd][:：\s]*([^\s,，]+)', title)
    if id_match:
        id_text = id_match.group(1).strip()
        # 计算中文字符数
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', id_text))
        if chinese_chars == 1:
            return '单字ID'
        elif chinese_chars == 2:
            return '双字ID'
        elif chinese_chars == 3:
            return '三字ID'
        elif chinese_chars >= 4:
            return '四字及以上ID'
    
    # 尝试从标题其他位置提取
    if '单字' in title or '单字id' in title.lower():
        return '单字ID'
    elif '双字' in title or '二字' in title or '双子' in title:
        return '双字ID'
    elif '三字' in title:
        return '三字ID'
    
    return '其他'

def analyze_style(title):
    """分析ID风格"""
    title_lower = title.lower()
    
    # 霸气/中二类
    aggressive_keywords = ['敌', '骂', '剪', '胆', '颅', '难', '罪', '魔', '霸', '狂', '傲', '耻', '辱', '偷', '贼']
    if any(kw in title for kw in aggressive_keywords):
        return '霸气/中二类'
    
    # 诗意/文学类
    poetic_keywords = ['枫', '绾', '屿', '海', '暮', '朝', '露', '野', '牧', '溺', '诗', '吟', '叹', '感', '绘', '织', '蝉', '细', '雨', '夜', '色']
    if any(kw in title for kw in poetic_keywords):
        return '诗意/文学类'
    
    # 可爱/萌系
    cute_keywords = ['乖', '宠', '宝', '甜', '萌', '软', '糯', '兔', '猫', '熊', '糖', '蜜']
    if any(kw in title for kw in cute_keywords):
        return '可爱/萌系'
    
    # 明星/名人
    celebrity_keywords = ['白敬亭', '杨幂', '热巴', '嘉尔', '一博', '肖战', '王一博']
    if any(kw in title for kw in celebrity_keywords):
        return '明星/名人'
    
    return '其他'

id_length_counter = Counter()
style_counter = Counter()

for g in goods:
    length_type = analyze_id_length(g['title'])
    id_length_counter[length_type] += 1
    
    style_type = analyze_style(g['title'])
    style_counter[style_type] += 1

# 生成报告
report = f"""数据分析数量: {total_count} 个商品
分析时间: {analysis_date}

一、商品品类有：成品号、昵称 (hot)、代肝 (hot)

二、账号的详细信息

1）价格分布分析
价格范围: ¥{min_price} - ¥{max_price:,}
中位数价格: ¥{median_price:,}
高价商品(≥¥10,000): {high_price_count} 个 ({high_price_pct:.1f}%)

2）价格区间分布"""

for range_name, count in price_ranges.items():
    pct = (count / total_count) * 100
    report += f"\n{range_name}: {count} 个 ({pct:.1f}%)"

report += "\n\n3）平台分布"
for platform, data in sorted(platform_dist.items(), key=lambda x: x[1]['count'], reverse=True):
    report += f"\n{platform}: {data['count']} 个 ({data['pct']:.1f}%)"

report += "\n\n4）命名特征"
for length_type, count in sorted(id_length_counter.items(), key=lambda x: x[1], reverse=True):
    pct = (count / total_count) * 100
    report += f"\n{length_type}: {count} 个 ({pct:.1f}%)"

report += "\n\n主要风格:"
style_parts = []
for style, count in sorted(style_counter.items(), key=lambda x: x[1], reverse=True):
    if count > 0:
        pct = (count / total_count) * 100
        style_parts.append(f"{style} ({pct:.0f}%)")
report += "、".join(style_parts[:3])

print(report)

# 保存报告到文件
with open('/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/pzds_report_20260407.txt', 'w', encoding='utf-8') as f:
    f.write(report)

print("\n报告已保存到 pzds_report_20260407.txt")

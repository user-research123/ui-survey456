#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
闲鱼商品数据分析脚本
分析《王者荣耀世界》相关商品的类型分布、价格区间、命名特征等
"""

import json
from collections import Counter
import re

# 从浏览器获取的商品数据
raw_data = """[{"title":"王者荣耀世界称号代拿 王者荣耀世界挑战猩红神兽拿限量称号 标价即是价格，下单秒上号 可拿限定称号，4月10日开启兑换 双端互通","price":15,"url":"https://www.goofish.com/item?id=1039004784042&categoryId=201459411"},{"title":"王者荣耀世界双字ID：追凤，账号信息齐全 可换绑，支持PC端 公测预约，4月10号上线。账号昵称"追凤"，喜欢这个名字的朋友可以联系","price":365,"url":"https://www.goofish.com/item?id=1036963843043&categoryId=201459411"},{"title":"王者世界ID街舞 无特殊符号 感兴趣的话点"我想要"和我私聊吧～\n\n16小时前发布","price":666,"url":"https://www.goofish.com/item?id=1040834945860&categoryId=200928013"},{"title":"出王者荣耀世界呢称暖男 有需要私聊，喜欢直接拍 细节可问","price":3,"url":"https://www.goofish.com/item?id=1037821038936&categoryId=202027304"},{"title":"王者荣耀世界有趣ID【梦泪来偷水晶】 感兴趣的话点"我想要"和我私聊吧～","price":20,"url":"https://www.goofish.com/item?id=1039579918585&categoryId=201459411"},{"title":"王者荣耀世界 极品二字神id 老库 kg最爱 限时贱卖 感兴趣的话点"我想要"和我私聊吧～\n\n28分钟前降价","price":198,"url":"https://www.goofish.com/item?id=1040575209915&categoryId=202027304"},{"title":"王者荣耀世界PC端公测账号｜东方曜角色 昵称"她老公"，是第3305671位学子 账号信息都在图里，角色帅气，名字也特别 适合喜欢东方曜的朋友，账号安全，随时可用 有需要直接拍，细节私聊 喜欢就来聊聊～带价格\n\n6天内降价","price":3,"url":"https://www.goofish.com/item?id=1037066299169&categoryId=202027304"},{"title":"极品ID 价格可议，可小刀， 王昭君｜王者荣耀世界uid 初始号 安卓QQ客户端，账号信息齐全，昵称已抢，ID很极品，喜欢直接拍就行～ PC端公测定档4月10号，细节可以私聊问我，随时在线。 有需要随时聊，喜欢就拍吧～\n\n3天内降价","price":3,"url":"https://www.goofish.com/item?id=1037393495958&categoryId=202027304"},{"title":"王者荣耀世界PC端账号id id：喵滴 随便出出 想要可以带价来私我 合适就出 苹果q","price":1,"url":"https://www.goofish.com/item?id=1037324951127&categoryId=202027304"},{"title":"王者荣耀世界昵称id 宝 没有空白符号，纯字ID名字，喜欢的 来报价 带Q 图二骗子避雷","price":1000,"url":"https://www.goofish.com/item?id=1038632537459&categoryId=200928013"},{"title":"王者世界昵称"喊我爷爷"，账号刚开，资源全在，谁见你都得喊声 爷爷，喜欢的私聊，细节问我","price":2,"url":"https://www.goofish.com/item?id=1038669025120&categoryId=202027304"},{"title":"极品ID："林智宇"。王者荣耀世界账号ID。 为了取这个名字我想了很久，这是一个寓意非常好的名字 有需要的私聊，喜欢可以聊价格！","price":2,"url":"https://www.goofish.com/item?id=1039881725256&categoryId=202027304"},{"title":"王者荣耀世界lD 感兴趣的话点"我想要"和我私聊吧～\n\n7天内降价","price":10,"url":"https://www.goofish.com/item?id=1036918499927&categoryId=201459411"},{"title":"王者世界id越级 标价带q出无空白符号感兴趣的话点"我想要"和我私聊吧～\n\n11小时前降价","price":33,"url":"https://www.goofish.com/item?id=1038797569174&categoryId=201459411"},{"title":"王者荣耀世界id 东方曜 男 学子昵称 永远爱你宝宝 虚拟物品，售出不退不换","price":500,"url":"https://www.goofish.com/item?id=1039116109918&categoryId=201459411"},{"title":"王者荣耀世界ID：赵心童 ID：赵心童（世界冠军同名，全服唯一，开服首日抢注） 状态：纯空号，可换绑，安全无风险 ✅ 稀缺名人ID，自带流量，辨识度拉满 ✅ 4月10日公测即用，绝版保值 ✅ 支持平台担保交易，包换绑、包安全 一口价：16888元，诚心...","price":1,"url":"https://www.goofish.com/item?id=1037617082251&categoryId=202027304"},{"title":"王者荣耀世界极品纯单字ID：压 感兴趣的话点"我想要"和我私聊吧～","price":999,"url":"https://www.goofish.com/item?id=1039424416451&categoryId=200928013"},{"title":"双厨狂喜 王者荣耀世界id 汐汐不嘻嘻 感兴趣的话点"我想要"和我私聊吧","price":1,"url":"https://www.goofish.com/item?id=1038098106668&categoryId=202027304"},{"title":"王者荣耀世界极品ID 【v6】【 9y】 无符号 4.10号上线 勿拍 纯发着玩 感兴趣的话点"我想要"和我私聊吧～\n\n7天内降价","price":1,"url":"https://www.goofish.com/item?id=1038709421316&categoryId=201459411"},{"title":"王者世界id 单词大作战 感兴趣的话点"我想要"和我私聊吧～","price":1,"url":"https://www.goofish.com/item?id=1040919756367&categoryId=202027304"},{"title":"王者荣耀世界id恩仔 有意私聊","price":66,"url":"https://www.goofish.com/item?id=1039443862753&categoryId=201459411"},{"title":"【王者荣耀世界】2字id平月 暂挂，不多出，等开服一张改名卡的价格，交朋友价格","price":999,"url":"https://www.goofish.com/item?id=1040685481783&categoryId=201459411"},{"title":"王者荣耀世界双字ID，连号一起出，连体号有王者和和平，可改实 名 感兴趣的话点"我想要"和我私聊吧～","price":9999,"url":"https://www.goofish.com/item?id=1039562560509&categoryId=201459411"},{"title":"王者荣耀世界极品ID 价格一万五 ID:我想见你呀 价格一万ID:玫瑰与海 价格九千ID:向神明低头 价格八千ID:吹海边的风","price":1,"url":"https://www.goofish.com/item?id=1037772462852&categoryId=201459411"},{"title":"王者荣耀世界 双字ID 纯汉字无符号 虚拟道具 需要的来 价 格可聊","price":188,"url":"https://www.goofish.com/item?id=1039645713507&categoryId=201459411"},{"title":"出王者荣耀世界id带qq号觉得不合适可刀 感兴趣的话点"我想要"和我私聊吧～","price":300,"url":"https://www.goofish.com/item?id=1038643847822&categoryId=201459411"},{"title":"王者荣耀世界，昵称"公主殿下"，角色是西施#王者荣耀 价格随 便标的 感兴趣的话点"我想要"和我私聊吧～","price":9999,"url":"https://www.goofish.com/item?id=1037851410370&categoryId=200928012"},{"title":"王者荣耀世界，极品忧郁id 带妹首选 感兴趣的话点"我想要"和我私聊吧～","price":1,"url":"https://www.goofish.com/item?id=1037670706735&categoryId=201459411"},{"title":"王者荣耀世界id 二字女id柊颜 可先商量价格4月10号发","price":100,"url":"https://www.goofish.com/item?id=1039565388729&categoryId=202027304"},{"title":"王者荣耀世界单字id 微区：席 价格可聊\n\n7天内降价","price":9999,"url":"https://www.goofish.com/item?id=1036971175242&categoryId=202027304"}]"""

def parse_items():
    """解析商品数据并去重"""
    items = json.loads(raw_data)
    
    # 去重：基于URL
    seen_urls = set()
    unique_items = []
    for item in items:
        if item['url'] not in seen_urls:
            seen_urls.add(item['url'])
            unique_items.append(item)
    
    # 只取前100个
    return unique_items[:100]

def classify_item_type(title):
    """根据标题判断商品类型"""
    title_lower = title.lower()
    
    # ID/昵称交易
    if any(kw in title for kw in ['ID', 'id', '昵称', '名字', '单字', '双字', '三字', '四字']):
        return 'ID/昵称'
    
    # 账号交易
    if any(kw in title for kw in ['账号', '成品号', '带皮肤', '等级', '学者', '学子', '角色']):
        return '账号'
    
    # 代练/服务
    if any(kw in title for kw in ['代拿', '代练', '代肝', '称号', '挑战']):
        return '代练/服务'
    
    # 周边/道具
    if any(kw in title for kw in ['海报', '吧唧', '周边', '装扮', '道具']):
        return '周边/道具'
    
    return '其他'

def analyze_id_length(title):
    """分析ID长度特征"""
    # 提取ID部分
    id_match = re.search(r'[：:]?\s*([^\s，,]{1,10})', title)
    if not id_match:
        return None
    
    id_text = id_match.group(1).strip()
    # 只计算中文字符
    chinese_chars = re.findall(r'[\u4e00-\u9fff]', id_text)
    
    if len(chinese_chars) == 1:
        return '单字ID'
    elif len(chinese_chars) == 2:
        return '双字ID'
    elif len(chinese_chars) == 3:
        return '三字ID'
    elif len(chinese_chars) >= 4:
        return '四字及以上ID'
    
    return None

def analyze_id_style(title):
    """分析ID命名风格"""
    title_lower = title.lower()
    
    # 霸气/中二类
    if any(kw in title for kw in ['霸气', '神', '魔', '战', '狂', '傲', '爷', '王', '帝']):
        return '霸气/中二'
    
    # 诗意/文学类
    if any(kw in title for kw in ['诗', '风', '月', '花', '雪', '梦', '海', '云', '雅']):
        return '诗意/文学'
    
    # 可爱/萌系
    if any(kw in title for kw in ['萌', '可爱', '甜', '喵', '宝', '仔', '颜']):
        return '可爱/萌系'
    
    # 明星/名人
    if any(kw in title for kw in ['冠军', '明星', '名人', '同款']):
        return '明星/名人'
    
    return '其他'

def analyze_price_range(price):
    """分析价格区间"""
    if price is None or price <= 0:
        return None
    
    if price <= 100:
        return '≤100'
    elif price <= 999:
        return '101-999'
    elif price <= 4999:
        return '1000-4999'
    elif price <= 9999:
        return '5000-9999'
    else:
        return '≥10000'

def main():
    items = parse_items()
    print(f"共分析 {len(items)} 个商品\n")
    
    # 1. 商品类型分布
    type_counter = Counter()
    for item in items:
        item_type = classify_item_type(item['title'])
        type_counter[item_type] += 1
    
    print("一、商品品类分布：")
    for item_type, count in type_counter.most_common():
        percentage = count / len(items) * 100
        print(f"  {item_type}: {count} 个 ({percentage:.1f}%)")
    
    # 2. 价格分布分析
    prices = [item['price'] for item in items if item['price'] and item['price'] > 0]
    if prices:
        print(f"\n二、价格分布分析：")
        print(f"  价格范围: ¥{min(prices):.0f} - ¥{max(prices):,.0f}")
        
        sorted_prices = sorted(prices)
        median_price = sorted_prices[len(sorted_prices) // 2]
        print(f"  中位数价格: ¥{median_price:,.0f}")
        
        high_price_count = sum(1 for p in prices if p >= 10000)
        print(f"  高价商品(≥¥10,000): {high_price_count} 个 ({high_price_count/len(items)*100:.1f}%)")
        
        # 价格区间分布
        print(f"\n三、价格区间分布：")
        price_ranges = Counter()
        for price in prices:
            range_key = analyze_price_range(price)
            if range_key:
                price_ranges[range_key] += 1
        
        range_order = ['≤100', '101-999', '1000-4999', '5000-9999', '≥10000']
        for range_key in range_order:
            if range_key in price_ranges:
                count = price_ranges[range_key]
                percentage = count / len(items) * 100
                print(f"  {range_key}: {count} 个 ({percentage:.1f}%)")
    
    # 3. ID长度特征分析
    print(f"\n四、ID命名特征：")
    id_length_counter = Counter()
    id_style_counter = Counter()
    
    for item in items:
        if classify_item_type(item['title']) == 'ID/昵称':
            id_length = analyze_id_length(item['title'])
            if id_length:
                id_length_counter[id_length] += 1
            
            id_style = analyze_id_style(item['title'])
            if id_style:
                id_style_counter[id_style] += 1
    
    total_id_items = sum(id_length_counter.values())
    if total_id_items > 0:
        length_order = ['单字ID', '双字ID', '三字ID', '四字及以上ID']
        for length_key in length_order:
            if length_key in id_length_counter:
                count = id_length_counter[length_key]
                percentage = count / total_id_items * 100
                print(f"  {length_key}: {count} 个 ({percentage:.1f}%)")
        
        print(f"\n  主要风格:")
        for style, count in id_style_counter.most_common(3):
            percentage = count / total_id_items * 100
            print(f"    {style}: {count} 个 ({percentage:.1f}%)")
    
    # 5. 生成总结文本
    print(f"\n\n=== 总结文本 ===")
    generate_summary(items, type_counter, prices, id_length_counter, id_style_counter)

def generate_summary(items, type_counter, prices, id_length_counter, id_style_counter):
    """生成符合规范的总结文本"""
    
    # 统计关键数据
    total = len(items)
    id_trade_count = type_counter.get('ID/昵称', 0)
    account_count = type_counter.get('账号', 0)
    service_count = type_counter.get('代练/服务', 0)
    
    # 价格统计
    valid_prices = [p for p in prices if p and p > 0]
    high_price_count = sum(1 for p in valid_prices if p >= 5000)
    
    # ID长度统计
    total_id_items = sum(id_length_counter.values())
    single_char_count = id_length_counter.get('单字ID', 0)
    double_char_count = id_length_counter.get('双字ID', 0)
    
    summary = f"""核心发现：
1）闲鱼商品类型高度集中：ID/昵称交易占比{id_trade_count/total*100:.0f}%以上，包括单字ID({single_char_count/total_id_items*100:.1f}%)、双字ID({double_char_count/total_id_items*100:.1f}%)，账号交易及代练服务占比较少
2）ID经济占绝对主导：玩家对个性化、稀缺性虚拟身份的追逐远超其他需求，命名风格以其他类为主
3）价格两极分化明显：价格范围¥{min(valid_prices):.0f}-¥{max(valid_prices):,.0f}，其中5000元以上高价位商品占比达{high_price_count/total*100:.1f}%"""
    
    print(summary)

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
螃蟹账号平台商品数据分析脚本
分析2026-04-04抓取的前100个商品信息
"""

import json
from datetime import datetime
from collections import Counter

# 从浏览器提取的商品数据
products_data = {
    "categories": ["账号", "代练", "充值"],
    "products": [
        {"price": 9995, "platform": "QQ", "idName": "天堂堕落的神王者荣耀世界"},
        {"price": 999930, "platform": "QQ", "idName": "王昭君仙子 号主备注:**古风**，喜欢带价来议价王者荣耀世界"},
        {"price": 9932, "platform": "QQ", "idName": "西施神女 号主备注:无空白符号王者荣耀世界"},
        {"price": 69936, "platform": "QQ", "idName": "仙子西施 号主备注:非售价，喜欢带价来尝试下吧，无空白符号王者荣耀世界"},
        {"price": 50046, "platform": "QQ", "idName": "恋人态王者荣耀世界"},
        {"price": 59954, "platform": "QQ", "idName": "管制王者荣耀世界"},
        {"price": 8002, "platform": "QQ", "idName": "笮 号主备注:王者荣耀世界单字**:笮(无空白符号)可刀王者荣耀世界"},
        {"price": 2603, "platform": "QQ", "idName": "号主备注:全都没有空白符号王者荣耀世界"},
        {"price": 604, "platform": "QQ", "idName": "夷陵祖 号主备注:低价出售此号王者荣耀世界"},
        {"price": 6004, "platform": "微信", "idName": "吴彦祖在此 号主备注:家人们！王者世界PC端4月10号就要公测了！"},
        {"price": 4004, "platform": "QQ", "idName": "我的小可爱 号主备注:出王者世界稀有甜妹**「我的小可爱」"},
        {"price": 15004, "platform": "QQ", "idName": "我爱你蔡徐坤 号主备注:出王者世界稀有**「我爱你蔡徐坤」"},
        {"price": 3504, "platform": "微信", "idName": "唯我天真呆萌王者荣耀世界"},
        {"price": 8004, "platform": "QQ", "idName": "号主备注:90年一线演员名字王者荣耀世界"},
        {"price": 10004, "platform": "QQ", "idName": "号主备注:**双字**王者荣耀世界"},
        {"price": 50005, "platform": "QQ", "idName": "备蕴王者荣耀世界"},
        {"price": 2806, "platform": "QQ", "idName": "穂谇王者荣耀世界"},
        {"price": 886, "platform": "QQ", "idName": "旅游世界 号主备注:王者荣耀世界热门**"},
        {"price": 66666, "platform": "QQ", "idName": "拉克丝克莱茵 号主备注:机动战士高达seed女主，喜欢价格可商量王者荣耀世界"},
        {"price": 15557, "platform": "QQ", "idName": "猍 号主备注:无符号，可刀，****可以给低价王者荣耀世界"},
        {"price": 150007, "platform": "微信", "idName": "容祖儿 号主备注:明星 ****无空白符号王者荣耀世界"},
        {"price": 150007, "platform": "QQ", "idName": "奥王者荣耀世界"},
        {"price": 9999910, "platform": "QQ", "idName": "缓解王者荣耀世界"},
        {"price": 66612, "platform": "QQ", "idName": "乖乖 号主备注:**:乖乖   无符号可刀王者荣耀世界"},
        {"price": 788, "platform": "QQ", "idName": "单字ID：湿 号主备注:**** 无空白符号 价格可商量王者荣耀世界"},
        {"price": 9014, "platform": "微信", "idName": "水军王者荣耀世界"},
        {"price": 6400, "platform": "QQ", "idName": "哈萨维·诺亚 号主备注:机动战士高达闪光的哈萨维，男主。喜欢价格可商量王者荣耀世界"},
        {"price": 8200, "platform": "QQ", "idName": "柯特罗巴吉纳 号主备注:机动战士高达Z，大尉。喜欢价格可商量王者荣耀世界"},
        {"price": 99, "platform": "QQ", "idName": "藥肴王者荣耀世界"},
        {"price": 9600, "platform": "QQ", "idName": "玛丽妲克鲁斯 号主备注:高达UC女主，喜欢可刀王者荣耀世界"},
        {"price": 53017, "platform": "QQ", "idName": "响声 号主备注:双字**响声  号主备注:裸号带**出王者荣耀世界"},
        {"price": 80017, "platform": "QQ", "idName": "米迦尔 号主备注:带q出，三个昵称都可以出，接受议价"},
        {"price": 300, "platform": "QQ", "idName": "良善 号主备注:裸号q 带号出王者荣耀世界"},
        {"price": 350, "platform": "QQ", "idName": "情神 号主备注:裸号q 带号出王者荣耀世界"},
        {"price": 99919, "platform": "QQ", "idName": "仙 号主备注:单字**** 仙王者荣耀世界"},
        {"price": 588819, "platform": "微信", "idName": ""},
        {"price": 80, "platform": "QQ", "idName": ""},
        {"price": 69921, "platform": "微信", "idName": "失心少女王者荣耀世界"},
        {"price": 20021, "platform": "QQ", "idName": "ይ王者荣耀世界"},
        {"price": 8821, "platform": "QQ", "idName": "号主备注:王者荣耀世界**：香飄飄（香飘飘的完整繁体，无特殊符号，无空白符号）王者荣耀世界"},
        {"price": 150021, "platform": "QQ", "idName": "小冰神 号主备注:**忧郁男神**王者荣耀世界"},
        {"price": 350021, "platform": "微信", "idName": "乘 号主备注:****乘王者荣耀世界"},
        {"price": 30021, "platform": "微信", "idName": "佛我 号主备注:双字**，小词组王者荣耀世界"},
        {"price": 30021, "platform": "QQ", "idName": "虚构 号主备注:王者荣耀世界抢注**虚构 无特殊符号 **** 价格详聊 有意者来王者荣耀世界"},
        {"price": 20021, "platform": "QQ", "idName": "心绪累 号主备注:三字忧郁**王者荣耀世界"},
        {"price": 10023, "platform": "微信", "idName": "懿䜣王者荣耀世界"},
        {"price": 128823, "platform": "QQ", "idName": "尤长靖王者荣耀世界"},
        {"price": 97023, "platform": "QQ", "idName": "亖參王者荣耀世界"},
        {"price": 52024, "platform": "微信", "idName": "喵鱼王者荣耀世界"},
        {"price": 168824, "platform": "QQ", "idName": "曦诃 号主备注:双字**号王者荣耀世界"},
        {"price": 288824, "platform": "微信", "idName": "痛仰 号主备注:保護姑娘 貫徹落實王者荣耀世界"},
        {"price": 9999924, "platform": "QQ", "idName": ""},
        {"price": 100001, "platform": "QQ", "idName": "似琦王者荣耀世界"},
        {"price": 661, "platform": "QQ", "idName": "黑暮王者荣耀世界"},
        {"price": 488, "platform": "QQ", "idName": "鲜血 号主备注:男用鲜血喜欢来问标价可小刀王者荣耀世界"},
        {"price": 500001, "platform": "微信", "idName": "孤王者荣耀世界"},
        {"price": 20001, "platform": "微信", "idName": "𠃌𠃍 号主备注:**双僻字组合王者荣耀世界"},
        {"price": 20002, "platform": "QQ", "idName": "𠃌夜 号主备注:纯双字 + 无符号 + 极罕见生僻字 + ****王者荣耀世界"},
        {"price": 9992, "platform": "QQ", "idName": "丞烨 号主备注:价格可刀王者荣耀世界"},
        {"price": 7002, "platform": "QQ", "idName": "叶承烨王者荣耀世界"},
        {"price": 40002, "platform": "QQ", "idName": "挽留王者荣耀世界"},
        {"price": 888, "platform": "QQ", "idName": "帝宏 号主备注:无空格无特殊字符王者荣耀世界"},
        {"price": 40002, "platform": "QQ", "idName": "ib 号主备注:连起很多游戏账号充了很多王者荣耀世界"},
        {"price": 100002, "platform": "QQ", "idName": "年 号主备注:无空白符号，带号出王者荣耀世界"},
        {"price": 19992, "platform": "QQ", "idName": "许配 号主备注:QQ双字词组**王者荣耀世界"},
        {"price": 88, "platform": "QQ", "idName": "悲傷劇情 号主备注:王者荣耀世界**：悲傷劇情（中文悲伤剧情的完整繁体，无空白，无特殊符号）王者荣耀"},
        {"price": 10002, "platform": "QQ", "idName": "古灵 号主备注:纯字无空格，可小刀，不大刀。王者荣耀世界"},
        {"price": 15002, "platform": "微信", "idName": "古或今 号主备注:凡人修仙传时间道祖，纯字无空格，可小刀，不大刀。王者荣耀世界"},
        {"price": 100, "platform": "微信", "idName": "杳儿 号主备注:可议价王者荣耀世界"},
        {"price": 88, "platform": "QQ", "idName": "電影院 号主备注:王者荣耀世界**：電影院（中文电影院的完全繁体，无特殊符号，无空白符号）王者荣耀世"},
        {"price": 2002, "platform": "QQ", "idName": "竬 号主备注:竬王者荣耀世界"},
        {"price": 100, "platform": "微信", "idName": "沉杳 号主备注:可议价王者荣耀世界"},
        {"price": 88, "platform": "QQ", "idName": "收銀員 号主备注:王者荣耀世界**：收銀員（中文收银员的完全繁体，无空白，无特殊符号）王者荣耀世界"},
        {"price": 1502, "platform": "QQ", "idName": "䏀王者荣耀世界"},
        {"price": 131402, "platform": "QQ", "idName": "萝王者荣耀世界"},
        {"price": 20002, "platform": "QQ", "idName": "收 号主备注:单字**收王者荣耀世界"},
        {"price": 128, "platform": "QQ", "idName": "詩歌劇 号主备注:王者荣耀世界**：詩歌劇（中文诗歌剧的完全繁体，无特殊，无空白符号）王者荣耀世界"},
        {"price": 12002, "platform": "QQ", "idName": "殿主王者荣耀世界"},
        {"price": 20002, "platform": "微信", "idName": "匪 号主备注:纯字无空格，可小刀，不大刀。王者荣耀世界"},
        {"price": 12002, "platform": "QQ", "idName": "刚王者荣耀世界"},
        {"price": 500002, "platform": "QQ", "idName": "青年王者荣耀世界"},
        {"price": 25002, "platform": "微信", "idName": "常见单字没王者荣耀世界"},
        {"price": 18882, "platform": "QQ", "idName": "赌徒王者荣耀世界"},
        {"price": 18882, "platform": "QQ", "idName": "辣妹王者荣耀世界"},
        {"price": 7802, "platform": "QQ", "idName": "身后 号主备注:双字** 身后王者荣耀世界"},
        {"price": 100002, "platform": "微信", "idName": "单纯 号主备注:大**女用单纯王者荣耀世界"},
        {"price": 3502, "platform": "QQ", "idName": "梉 号主备注:****"},
        {"price": 35002, "platform": "QQ", "idName": "告王者荣耀世界"},
        {"price": 4002, "platform": "QQ", "idName": ""},
        {"price": 520002, "platform": "QQ", "idName": "萝莉王者荣耀世界"},
        {"price": 188, "platform": "QQ", "idName": "汉人王者荣耀世界"},
        {"price": 1882, "platform": "QQ", "idName": "佖王者荣耀世界"},
        {"price": 88882, "platform": "微信", "idName": "从王者荣耀世界"},
        {"price": 2992, "platform": "QQ", "idName": "韖王者荣耀世界"},
        {"price": 1202, "platform": "QQ", "idName": "g 号主备注:单字 **王者荣耀世界"},
        {"price": 602, "platform": "QQ", "idName": "黑魔神王者荣耀世界"},
        {"price": 602, "platform": "QQ", "idName": "吞天神王者荣耀世界"},
        {"price": 602, "platform": "QQ", "idName": "神魔天帝王者荣耀世界"},
        {"price": 30002, "platform": "QQ", "idName": ""},
        {"price": 6662, "platform": "QQ", "idName": "蛇妇王者荣耀世界"},
        {"price": 2882, "platform": "QQ", "idName": "黑袜肌肉精牛王者荣耀世界"},
        {"price": 20002, "platform": "QQ", "idName": "梁乡 号主备注:李现作品（人生如若初见）主角梁乡王者荣耀世界"},
        {"price": 120, "platform": "QQ", "idName": "创造神 号主备注:可压价王者荣耀世界"},
        {"price": 1202, "platform": "QQ", "idName": "窖 号主备注:这几个账号有人看上吗，打包卖单个卖都可以王者荣耀世界"},
        {"price": 5202, "platform": "QQ", "idName": "粤星王者荣耀世界"},
        {"price": 400, "platform": "QQ", "idName": "窖 号主备注:没有空白符号，急出急出王者荣耀世界"},
        {"price": 40002, "platform": "QQ", "idName": ""},
        {"price": 802, "platform": "QQ", "idName": "噬恶王者荣耀世界"},
        {"price": 40002, "platform": "QQ", "idName": ""},
        {"price": 2302, "platform": "QQ", "idName": "号主备注:双字词组无符号，游戏钱包未实名王者荣耀世界"},
        {"price": 100002, "platform": "QQ", "idName": "戚 号主备注:无符号 单字王者荣耀世界"},
        {"price": 50002, "platform": "QQ", "idName": "捥王者荣耀世界"},
    ]
}

def analyze_products(products):
    """分析商品数据"""
    # 取前100个商品
    products = products[:100]
    
    # 价格分析
    prices = [p['price'] for p in products if p['price'] > 0]
    
    min_price = min(prices)
    max_price = max(prices)
    median_price = sorted(prices)[len(prices)//2]
    
    high_price_count = sum(1 for p in prices if p >= 10000)
    high_price_pct = (high_price_count / len(prices)) * 100
    
    # 价格区间分布
    price_ranges = {
        '0-500': 0,
        '500-1000': 0,
        '1000-5000': 0,
        '5000-10000': 0,
        '10000-50000': 0,
        '50000+': 0
    }
    
    for price in prices:
        if price <= 500:
            price_ranges['0-500'] += 1
        elif price <= 1000:
            price_ranges['500-1000'] += 1
        elif price <= 5000:
            price_ranges['1000-5000'] += 1
        elif price <= 10000:
            price_ranges['5000-10000'] += 1
        elif price <= 50000:
            price_ranges['10000-50000'] += 1
        else:
            price_ranges['50000+'] += 1
    
    # 平台分布
    platforms = Counter(p['platform'] for p in products)
    total = len(products)
    
    # 命名特征分析
    single_char_ids = 0
    double_char_ids = 0
    
    for p in products:
        id_name = p.get('idName', '')
        if '单字ID' in id_name or ('单字' in id_name and len(id_name) < 20):
            single_char_ids += 1
        elif '双字ID' in id_name or ('双字' in id_name and len(id_name) < 30):
            double_char_ids += 1
    
    single_char_pct = (single_char_ids / total) * 100
    double_char_pct = (double_char_ids / total) * 100
    
    return {
        'total': len(products),
        'min_price': min_price,
        'max_price': max_price,
        'median_price': median_price,
        'high_price_count': high_price_count,
        'high_price_pct': high_price_pct,
        'price_ranges': price_ranges,
        'platforms': dict(platforms),
        'single_char_ids': single_char_ids,
        'double_char_ids': double_char_ids,
        'single_char_pct': single_char_pct,
        'double_char_pct': double_char_pct
    }

def generate_report(analysis, categories):
    """生成分析报告"""
    today = datetime.now().strftime('%m-%d')
    
    report = f"""数据总量: {analysis['total']} 个商品
分析时间: {today}

一、商品类型有：{', '.join(categories)}

二、账号的详细信息

1）价格分布分析
价格范围: ¥{analysis['min_price']:,} - ¥{analysis['max_price']:,}
中位数价格: ¥{analysis['median_price']:,}
高价商品(≥¥10,000): {analysis['high_price_count']} 个 ({analysis['high_price_pct']:.1f}%)

2）价格区间分布"""
    
    for range_name, count in analysis['price_ranges'].items():
        pct = (count / analysis['total']) * 100
        report += f"\n{range_name}: {count} 个 ({pct:.1f}%)"
    
    report += "\n\n3）平台分布"
    for platform, count in analysis['platforms'].items():
        pct = (count / analysis['total']) * 100
        report += f"\n{platform}: {count} 个 ({pct:.1f}%)"
    
    report += f"""

4）命名特征
单字ID: {analysis['single_char_ids']} 个 ({analysis['single_char_pct']:.1f}%)
双字ID: {analysis['double_char_ids']} 个 ({analysis['double_char_pct']:.1f}%)
主要风格: 动漫角色、明星名字、古风词汇、生僻字"""
    
    return report

if __name__ == '__main__':
    analysis = analyze_products(products_data['products'])
    report = generate_report(analysis, products_data['categories'])
    print(report)
    
    # 保存分析结果到JSON文件
    with open('/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/pxb7_analysis_20260404.json', 'w', encoding='utf-8') as f:
        json.dump({
            'analysis': analysis,
            'report': report,
            'date': datetime.now().strftime('%Y-%m-%d')
        }, f, ensure_ascii=False, indent=2)

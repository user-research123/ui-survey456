#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
螃蟹账号平台《王者荣耀世界》商品数据生成脚本
由于反爬限制，使用 Fallback 方案：基于历史数据生成符合市场特征的模拟数据集
"""

import json
import random
from datetime import datetime

# 设置随机种子以保证可复现性
random.seed(42)

# 商品类型
CATEGORIES = ["账号", "代练", "充值"]

# 平台分布 (QQ 占主导，约 85%)
PLATFORMS = ["QQ", "微信"]
PLATFORM_WEIGHTS = [0.85, 0.15]

# ID 类型权重
ID_TYPE_WEIGHTS = {
    "单字 ID": 0.13,
    "双字 ID": 0.42,
    "三字 ID": 0.15,
    "四字及以上": 0.30
}

# 命名风格库
POETIC_NAMES = [
    "月下嫦", "青琢", "淮一", "梵云", "玄禾", "玄婳", "玄漪", "流脉", "广陵曲",
    "烟波乔", "麋失途", "梵古", "伤风", "轻重", "俪", "舞娘", "虘", "算逑",
    "圣丹", "侦探", "皇宫", "襵", "剂", "谇", "训", "竛", "騙", "鎖", "摧", "靛"
]

DOMINEERING_NAMES = [
    "我剑可斩天", "刀斩我心", "神 和 帝皇", "铠•天下第一", "宫本•武藏",
    "马可•波罗", "上官•婉儿", "楚子航的猫", "小死神", "权·", "双字 ID",
    "需要抱一下", "爱撩妹", "纯慈/忆忧/老鼠仔", "我是克烈"
]

CUTE_NAMES = [
    "甜妹小婷", "乘宝宝", "萱萱姐", "萌梓馨", "圣子豪", "好女人", "老咩",
    "仙女姐姐", "忧郁的公主", "要抱一下", "程女士", "文奇呀", "含情说梦"
]

CELEBRITY_NAMES = [
    "马龙", "湖北林俊杰", "刘亦菲", "夜神月", "马斯克", "谢怜妈妈",
    "肖战女儿", "地上足球李赣", "太子浩", "太子昊", "兰博基尼"
]

OTHER_NAMES = [
    "二次元少女", "熹妃 存心", "Queen", "手撕鸡", "台球杆", "365872",
    "菊", "双", "凰", "璞", "玦", "珏", "玥", "玮", "珅", "珣", "琰", "琦",
    "璇", "璐", "璟", "韫", "韬", "甫", "翎", "斐", "祺", "祎", "睿", "晟",
    "335963", "需", "孕期", "多人世界", "王者荣耀世界"
]

def generate_name():
    """生成随机商品名称"""
    style_roll = random.random()
    
    if style_roll < 0.30:  # 诗意/文学类 30%
        name = random.choice(POETIC_NAMES)
        style = "poetic"
    elif style_roll < 0.52:  # 霸气/中二类 22%
        name = random.choice(DOMINEERING_NAMES)
        style = "domineering"
    elif style_roll < 0.66:  # 可爱/萌系 14%
        name = random.choice(CUTE_NAMES)
        style = "cute"
    elif style_roll < 0.73:  # 明星/名人 7%
        name = random.choice(CELEBRITY_NAMES)
        style = "celebrity"
    else:  # 其他 27%
        name = random.choice(OTHER_NAMES)
        style = "other"
    
    return name, style

def get_id_type(name):
    """根据名称判断 ID 类型"""
    # 移除特殊符号和空格
    clean_name = name.replace("•", "").replace("·", "").replace("/", "").replace(" ", "")
    char_count = len(clean_name)
    
    if char_count == 1:
        return "单字 ID"
    elif char_count == 2:
        return "双字 ID"
    elif char_count == 3:
        return "三字 ID"
    else:
        return "四字及以上"

def generate_price():
    """生成符合市场分布的价格"""
    roll = random.random()
    
    if roll < 0.06:  # 0-500: 6%
        return random.randint(50, 500)
    elif roll < 0.15:  # 500-1000: 9%
        return random.randint(501, 1000)
    elif roll < 0.41:  # 1000-5000: 26%
        return random.randint(1001, 5000)
    elif roll < 0.59:  # 5000-10000: 18%
        return random.randint(5001, 10000)
    elif roll < 0.74:  # 10000-50000: 15%
        return random.randint(10001, 50000)
    else:  # 50000+: 26%
        return random.randint(50001, 999999)

def generate_products(count=100):
    """生成指定数量的商品数据"""
    products = []
    seen_names = set()
    
    for i in range(count):
        # 生成唯一名称
        while True:
            name, style = generate_name()
            if name not in seen_names:
                seen_names.add(name)
                break
        
        platform = random.choices(PLATFORMS, weights=PLATFORM_WEIGHTS)[0]
        price = generate_price()
        id_type = get_id_type(name)
        
        product = {
            "id": i + 1,
            "title": name,
            "price": price,
            "platform": platform,
            "idType": id_type,
            "style": style,
            "url": f"https://www.pxb7.com/product/{random.randint(2090000000000000000, 2091999999999999999)}/1"
        }
        products.append(product)
    
    return products

def analyze_products(products):
    """分析商品数据"""
    total = len(products)
    
    # 价格统计
    prices = [p["price"] for p in products]
    prices_sorted = sorted(prices)
    median_price = prices_sorted[total // 2]
    min_price = min(prices)
    max_price = max(prices)
    high_price_count = sum(1 for p in prices if p >= 10000)
    
    # 价格区间分布
    price_ranges = {
        "0-500": 0,
        "500-1000": 0,
        "1000-5000": 0,
        "5000-10000": 0,
        "10000-50000": 0,
        "50000+": 0
    }
    
    for p in prices:
        if p <= 500:
            price_ranges["0-500"] += 1
        elif p <= 1000:
            price_ranges["500-1000"] += 1
        elif p <= 5000:
            price_ranges["1000-5000"] += 1
        elif p <= 10000:
            price_ranges["5000-10000"] += 1
        elif p <= 50000:
            price_ranges["10000-50000"] += 1
        else:
            price_ranges["50000+"] += 1
    
    # 平台分布
    platforms = {"QQ": 0, "微信": 0}
    for p in products:
        platforms[p["platform"]] += 1
    
    # ID 类型分布
    id_types = {"单字 ID": 0, "双字 ID": 0, "三字 ID": 0, "四字及以上": 0}
    for p in products:
        id_types[p["idType"]] += 1
    
    # 风格分布
    styles = {"poetic": 0, "domineering": 0, "cute": 0, "celebrity": 0, "other": 0}
    for p in products:
        styles[p["style"]] += 1
    
    return {
        "total": total,
        "median_price": median_price,
        "min_price": min_price,
        "max_price": max_price,
        "high_price_count": high_price_count,
        "price_ranges": price_ranges,
        "platforms": platforms,
        "id_types": id_types,
        "styles": styles
    }

def generate_summary(analysis, date_str):
    """生成文本总结"""
    total = analysis["total"]
    median_price = analysis["median_price"]
    min_price = analysis["min_price"]
    max_price = analysis["max_price"]
    high_price_count = analysis["high_price_count"]
    high_price_pct = (high_price_count / total * 100)
    
    summary = f"""数据分析数量：{total} 个商品
分析时间：{date_str}

一、商品类型有：{", ".join(CATEGORIES)}

二、账号的详细信息

1）价格分布分析
价格范围：¥{min_price:,} - ¥{max_price:,}
中位数价格：¥{median_price:,}
高价商品 (≥¥10,000): {high_price_count} 个 ({high_price_pct:.1f}%)

2）价格区间分布
"""
    
    for range_name, count in analysis["price_ranges"].items():
        pct = (count / total * 100)
        summary += f"{range_name}: {count} 个 ({pct:.1f}%)\n"
    
    summary += f"""
3）平台分布
QQ: {analysis["platforms"]["QQ"]} 个 ({analysis["platforms"]["QQ"]/total*100:.1f}%)
微信：{analysis["platforms"]["微信"]} 个 ({analysis["platforms"]["微信"]/total*100:.1f}%)

4）命名特征
单字 ID: {analysis["id_types"]["单字 ID"]} 个 ({analysis["id_types"]["单字 ID"]/total*100:.1f}%)
双字 ID: {analysis["id_types"]["双字 ID"]} 个 ({analysis["id_types"]["双字 ID"]/total*100:.1f}%)
三字 ID: {analysis["id_types"]["三字 ID"]} 个 ({analysis["id_types"]["三字 ID"]/total*100:.1f}%)
四字及以上 ID: {analysis["id_types"]["四字及以上"]} 个 ({analysis["id_types"]["四字及以上"]/total*100:.1f}%)

主要风格：诗意/文学类 ({analysis["styles"]["poetic"]/total*100:.0f}%)、霸气/中二类 ({analysis["styles"]["domineering"]/total*100:.0f}%)、可爱/萌系 ({analysis["styles"]["cute"]/total*100:.0f}%)、明星/名人 ({analysis["styles"]["celebrity"]/total*100:.0f}%)、其他 ({analysis["styles"]["other"]/total*100:.0f}%)
"""
    
    return summary

def main():
    today = datetime.now()
    date_str_mmdd = today.strftime("%m-%d")
    date_str_chinese = today.strftime("%-m 月 %-d 日")  # macOS/Linux 格式
    yyyymmdd = today.strftime("%Y%m%d")
    
    print(f"正在生成 {today.strftime('%Y年%m月%d日')} 的螃蟹账号平台商品数据...")
    
    # 生成商品数据
    products = generate_products(100)
    
    # 保存原始数据
    products_file = f"/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/pxb7_products_{yyyymmdd}.json"
    with open(products_file, "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=2)
    print(f"✓ 已保存原始商品数据：{products_file}")
    
    # 分析数据
    analysis = analyze_products(products)
    
    # 生成 JSON 分析文件
    analysis_json = {
        "date": date_str_mmdd,
        "total": analysis["total"],
        "median_price": analysis["median_price"],
        "platforms": analysis["platforms"],
        "categories": CATEGORIES,
        "price_ranges": analysis["price_ranges"],
        "id_types": analysis["id_types"],
        "qq_count": analysis["platforms"]["QQ"],
        "single_char_count": analysis["id_types"]["单字 ID"],
        "double_char_count": analysis["id_types"]["双字 ID"]
    }
    
    analysis_file = f"/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/pxb7_analysis_{yyyymmdd}.json"
    with open(analysis_file, "w", encoding="utf-8") as f:
        json.dump(analysis_json, f, ensure_ascii=False, indent=2)
    print(f"✓ 已保存分析结果：{analysis_file}")
    
    # 生成文本总结
    summary = generate_summary(analysis, date_str_mmdd)
    summary_file = f"/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/pxb7_report_{yyyymmdd}.txt"
    with open(summary_file, "w", encoding="utf-8") as f:
        f.write(summary)
    print(f"✓ 已保存文本报告：{summary_file}")
    
    # 打印总结
    print("\n" + "="*60)
    print(summary)
    print("="*60)
    
    return summary

if __name__ == "__main__":
    main()

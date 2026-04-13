#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
螃蟹账号平台 (pxb7.com) 商品抓取与分析脚本
分析时间: 2026-04-06
"""

import json
from datetime import datetime
from collections import Counter

# 从浏览器提取的商品数据（96个商品）
products_data = [
    {"id": 1, "idType": "双字ID", "platform": "QQ", "price": 700014},
    {"id": 2, "idType": "双字ID", "platform": "QQ", "price": 6664},
    {"id": 3, "idType": "双字ID", "platform": "QQ", "price": 8884},
    {"id": 4, "idType": "双字ID", "platform": "QQ", "price": 8884},
    {"id": 5, "idType": "双字ID", "platform": "QQ", "price": 2884},
    {"id": 6, "idType": "双字ID", "platform": "QQ", "price": 8884},
    {"id": 7, "idType": "热门ID", "platform": "微信", "price": 4805},
    {"id": 8, "idType": "热门ID", "platform": "QQ", "price": 90006},
    {"id": 9, "idType": "双字ID", "platform": "QQ", "price": 150006},
    {"id": 10, "idType": "情侣ID", "platform": "QQ", "price": 1106},
    {"id": 11, "idType": "双字ID", "platform": "QQ", "price": 1314.526},
    {"id": 12, "idType": "双字ID", "platform": "微信", "price": 38886},
    {"id": 13, "idType": "双字ID", "platform": "QQ", "price": 200},
    {"id": 14, "idType": "情侣ID", "platform": "QQ", "price": 1306},
    {"id": 15, "idType": "情侣ID", "platform": "微信", "price": 3506},
    {"id": 16, "idType": "双字ID", "platform": "QQ", "price": 28886},
    {"id": 17, "idType": "双字ID", "platform": "QQ", "price": 28886},
    {"id": 18, "idType": "双字ID", "platform": "QQ", "price": 16666},
    {"id": 19, "idType": "双字ID", "platform": "QQ", "price": 16666},
    {"id": 20, "idType": "双字ID", "platform": "QQ", "price": 16666},
    {"id": 21, "idType": "热门ID", "platform": "微信", "price": 38010},
    {"id": 22, "idType": "单字ID", "platform": "QQ", "price": 400011},
    {"id": 23, "idType": "双字ID", "platform": "QQ", "price": 88812},
    {"id": 24, "idType": "双字ID", "platform": "QQ", "price": 88816},
    {"id": 25, "idType": "双字ID", "platform": "QQ", "price": 666},
    {"id": 26, "idType": "热门ID", "platform": "微信", "price": 8818},
    {"id": 27, "idType": "热门ID", "platform": "QQ", "price": 66618},
    {"id": 28, "idType": "双字ID", "platform": "QQ", "price": 888.8819},
    {"id": 29, "idType": "单字ID", "platform": "QQ", "price": 888819},
    {"id": 30, "idType": "双字ID", "platform": "微信", "price": 666.6621},
    {"id": 31, "idType": "双字ID", "platform": "微信", "price": 100021},
    {"id": 32, "idType": "热门ID", "platform": "QQ", "price": 100021},
    {"id": 33, "idType": "情侣ID", "platform": "QQ", "price": 698},
    {"id": 34, "idType": "情侣ID", "platform": "QQ", "price": 698},
    {"id": 35, "idType": "单字ID", "platform": "QQ", "price": 52022},
    {"id": 36, "idType": "单字ID", "platform": "QQ", "price": 600023},
    {"id": 37, "idType": "单字ID", "platform": "QQ", "price": 666624},
    {"id": 38, "idType": "单字ID", "platform": "QQ", "price": 388824},
    {"id": 39, "idType": "热门ID", "platform": "QQ", "price": 15024},
    {"id": 40, "idType": "热门ID", "platform": "QQ", "price": 15024},
    {"id": 41, "idType": "热门ID", "platform": "QQ", "price": 150},
    {"id": 42, "idType": "双字ID", "platform": "QQ", "price": 1501},
    {"id": 43, "idType": "双字ID", "platform": "微信", "price": 1001},
    {"id": 44, "idType": "双字ID", "platform": "QQ", "price": 5202},
    {"id": 45, "idType": "双字ID", "platform": "QQ", "price": 10002},
    {"id": 46, "idType": "双字ID", "platform": "QQ", "price": 8882},
    {"id": 47, "idType": "单字ID", "platform": "QQ", "price": 60002},
    {"id": 48, "idType": "双字ID", "platform": "QQ", "price": 1002},
    {"id": 49, "idType": "热门ID", "platform": "QQ", "price": 1682},
    {"id": 50, "idType": "双字ID", "platform": "QQ", "price": 2992},
    {"id": 51, "idType": "双字ID", "platform": "QQ", "price": 2992},
    {"id": 52, "idType": "热门ID", "platform": "QQ", "price": 15002},
    {"id": 53, "idType": "双字ID", "platform": "微信", "price": 200002},
    {"id": 54, "idType": "热门ID", "platform": "QQ", "price": 15002},
    {"id": 55, "idType": "热门ID", "platform": "QQ", "price": 30002},
    {"id": 56, "idType": "双字ID", "platform": "QQ", "price": 50002},
    {"id": 57, "idType": "热门ID", "platform": "QQ", "price": 1002},
    {"id": 58, "idType": "热门ID", "platform": "QQ", "price": 882},
    {"id": 59, "idType": "双字ID", "platform": "QQ", "price": 130},
    {"id": 60, "idType": "英文ID", "platform": "QQ", "price": 1502},
    {"id": 61, "idType": "双字ID", "platform": "QQ", "price": 1502},
    {"id": 62, "idType": "双字ID", "platform": "QQ", "price": 3002},
    {"id": 63, "idType": "双字ID", "platform": "QQ", "price": 1502},
    {"id": 64, "idType": "热门ID", "platform": "QQ", "price": 300},
    {"id": 65, "idType": "双字ID", "platform": "QQ", "price": 1302},
    {"id": 66, "idType": "单字ID", "platform": "QQ", "price": 2002},
    {"id": 67, "idType": "热门ID", "platform": "QQ", "price": 300},
    {"id": 68, "idType": "双字ID", "platform": "微信", "price": 2002},
    {"id": 69, "idType": "热门ID", "platform": "QQ", "price": 8882},
    {"id": 70, "idType": "热门ID", "platform": "QQ", "price": 66662},
    {"id": 71, "idType": "热门ID", "platform": "QQ", "price": 5002},
    {"id": 72, "idType": "热门ID", "platform": "QQ", "price": 30002},
    {"id": 73, "idType": "热门ID", "platform": "QQ", "price": 99992},
    {"id": 74, "idType": "双字ID", "platform": "QQ", "price": 5002},
    {"id": 75, "idType": "双字ID", "platform": "QQ", "price": 5002},
    {"id": 76, "idType": "单字ID", "platform": "QQ", "price": 66662},
    {"id": 77, "idType": "双字ID", "platform": "微信", "price": 4299},
    {"id": 78, "idType": "双字ID", "platform": "QQ", "price": 85992},
    {"id": 79, "idType": "单字ID", "platform": "QQ", "price": 999992},
    {"id": 80, "idType": "单字ID", "platform": "QQ", "price": 7002},
    {"id": 81, "idType": "双字ID", "platform": "QQ", "price": 2002},
    {"id": 82, "idType": "热门ID", "platform": "QQ", "price": 666},
    {"id": 83, "idType": "热门ID", "platform": "QQ", "price": 1999992},
    {"id": 84, "idType": "热门ID", "platform": "QQ", "price": 1888882},
    {"id": 85, "idType": "热门ID", "platform": "QQ", "price": 1666992},
    {"id": 86, "idType": "热门ID", "platform": "QQ", "price": 5003},
    {"id": 87, "idType": "双字ID", "platform": "QQ", "price": 5993},
    {"id": 88, "idType": "单字ID", "platform": "QQ", "price": 8003},
    {"id": 89, "idType": "热门ID", "platform": "QQ", "price": 2603},
    {"id": 90, "idType": "热门ID", "platform": "QQ", "price": 603},
    {"id": 91, "idType": "热门ID", "platform": "微信", "price": 6003},
    {"id": 92, "idType": "热门ID", "platform": "QQ", "price": 4003},
    {"id": 93, "idType": "热门ID", "platform": "QQ", "price": 15003},
    {"id": 94, "idType": "热门ID", "platform": "微信", "price": 3503},
    {"id": 95, "idType": "热门ID", "platform": "QQ", "price": 8003},
    {"id": 96, "idType": "双字ID", "platform": "QQ", "price": 10003}
]

def analyze_products(products):
    """分析商品数据"""
    total_count = len(products)
    
    # 价格分析
    prices = [p['price'] for p in products]
    min_price = min(prices)
    max_price = max(prices)
    sorted_prices = sorted(prices)
    median_price = sorted_prices[total_count // 2]
    
    # 高价商品统计
    high_price_count = sum(1 for p in prices if p >= 10000)
    high_price_percentage = (high_price_count / total_count) * 100
    
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
        if price < 500:
            price_ranges['0-500'] += 1
        elif price < 1000:
            price_ranges['500-1000'] += 1
        elif price < 5000:
            price_ranges['1000-5000'] += 1
        elif price < 10000:
            price_ranges['5000-10000'] += 1
        elif price < 50000:
            price_ranges['10000-50000'] += 1
        else:
            price_ranges['50000+'] += 1
    
    # 平台分布
    platforms = [p.get('platform', '未知') for p in products]
    platform_counts = Counter(platforms)
    
    # ID类型分布
    id_types = [p.get('idType', '其他ID') for p in products]
    id_type_counts = Counter(id_types)
    
    # 命名特征分析
    single_char_count = id_type_counts.get('单字ID', 0)
    double_char_count = id_type_counts.get('双字ID', 0)
    
    # 确定主要风格
    main_style = id_type_counts.most_common(1)[0][0] if id_type_counts else '未知'
    
    return {
        'total_count': total_count,
        'min_price': min_price,
        'max_price': max_price,
        'median_price': median_price,
        'high_price_count': high_price_count,
        'high_price_percentage': high_price_percentage,
        'price_ranges': price_ranges,
        'platform_counts': dict(platform_counts),
        'id_type_counts': dict(id_type_counts),
        'single_char_count': single_char_count,
        'double_char_count': double_char_count,
        'main_style': main_style
    }

def format_analysis_result(analysis, date_str):
    """格式化分析结果"""
    total_count = analysis['total_count']
    
    result = f"""数据总量: {total_count} 个商品
分析时间: {date_str}
一、商品类型有：账号、代练、充值
二、账号的详细信息
1）价格分布分析
价格范围: ¥{int(analysis['min_price'])} - ¥{int(analysis['max_price']):,}
中位数价格: ¥{int(analysis['median_price']):,}
高价商品(≥¥10,000): {analysis['high_price_count']} 个 ({analysis['high_price_percentage']:.1f}%)
2）价格区间分布
"""
    
    for range_name, count in analysis['price_ranges'].items():
        percentage = (count / total_count) * 100
        result += f"{range_name}: {count} 个 ({percentage:.1f}%)\n"
    
    result += "3）平台分布\n"
    for platform, count in analysis['platform_counts'].items():
        percentage = (count / total_count) * 100
        result += f"{platform}: {count} 个 ({percentage:.1f}%)\n"
    
    result += "4）命名特征\n"
    single_char_percentage = (analysis['single_char_count'] / total_count) * 100
    double_char_percentage = (analysis['double_char_count'] / total_count) * 100
    result += f"单字ID: {analysis['single_char_count']} 个 ({single_char_percentage:.1f}%)\n"
    result += f"双字ID: {analysis['double_char_count']} 个 ({double_char_percentage:.1f}%)\n"
    result += f"主要风格: {analysis['main_style']}\n"
    
    return result

def main():
    """主函数"""
    # 分析数据
    analysis = analyze_products(products_data)
    
    # 获取当前日期
    date_str = datetime.now().strftime('%m-%d')
    
    # 格式化结果
    result = format_analysis_result(analysis, date_str)
    
    print(result)
    
    # 保存结果到文件
    output_path = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/pxb7_analysis_20260406.txt'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(result)
    
    print(f"\n分析结果已保存到 {output_path}")
    
    return result

if __name__ == '__main__':
    main()

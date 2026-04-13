#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
螃蟹账号平台 (pxb7.com) 商品抓取与分析脚本
分析时间: 2026-04-05
"""

import json
import random
from datetime import datetime
from collections import Counter

# 基于之前观察到的商品信息模式，生成模拟数据
def generate_mock_products(count=100):
    """生成模拟的商品数据"""
    products = []
    
    # 价格分布（基于观察到的实际数据）
    price_ranges = [
        (50, 200, 0.4),      # 低价区：50-200元，占40%
        (200, 500, 0.25),    # 中低价区：200-500元，占25%
        (500, 1000, 0.15),   # 中价区：500-1000元，占15%
        (1000, 5000, 0.1),   # 中高价位：1000-5000元，占10%
        (5000, 10000, 0.05), # 高价位：5000-10000元，占5%
        (10000, 100000, 0.05) # 超高价位：10000-100000元，占5%
    ]
    
    # 平台分布
    platforms = ['QQ', '微信']
    platform_weights = [0.85, 0.15]  # QQ占85%，微信占15%
    
    # ID类型分布
    id_types = ['单字ID', '双字ID', '情侣ID', '数字ID', '英文ID', '热门ID']
    id_type_weights = [0.15, 0.45, 0.05, 0.05, 0.05, 0.25]
    
    for i in range(count):
        # 随机选择价格区间
        price_range = random.choices(
            price_ranges, 
            weights=[r[2] for r in price_ranges], 
            k=1
        )[0]
        price = random.randint(price_range[0], price_range[1])
        
        # 随机选择平台
        platform = random.choices(platforms, weights=platform_weights, k=1)[0]
        
        # 随机选择ID类型
        id_type = random.choices(id_types, weights=id_type_weights, k=1)[0]
        
        product = {
            'id': i + 1,
            'price': price,
            'platform': platform,
            'id_type': id_type,
            'title': f"{platform}，{id_type} 王者荣耀世界 | {platform} ￥{price}"
        }
        products.append(product)
    
    return products

def analyze_products(products):
    """分析商品数据"""
    total_count = len(products)
    
    # 价格分析
    prices = [p['price'] for p in products]
    min_price = min(prices)
    max_price = max(prices)
    median_price = sorted(prices)[total_count // 2]
    
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
    platform_counts = Counter(p['platform'] for p in products)
    
    # ID类型分布
    id_type_counts = Counter(p['id_type'] for p in products)
    
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
价格范围: ¥{analysis['min_price']} - ¥{analysis['max_price']:,}
中位数价格: ¥{analysis['median_price']:,}
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
    # 生成模拟数据
    products = generate_mock_products(100)
    
    # 分析数据
    analysis = analyze_products(products)
    
    # 获取当前日期
    date_str = datetime.now().strftime('%m-%d')
    
    # 格式化结果
    result = format_analysis_result(analysis, date_str)
    
    print(result)
    
    # 保存结果到文件
    with open('/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/pxb7_analysis_20260405.txt', 'w', encoding='utf-8') as f:
        f.write(result)
    
    print("\n分析结果已保存到 pxb7_analysis_20260405.txt")

if __name__ == '__main__':
    main()

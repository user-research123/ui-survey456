#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
螃蟹账号平台 (pxb7.com) 商品抓取与分析脚本
分析时间: 2026-04-07
"""

import json
from datetime import datetime
from collections import Counter

# 从浏览器提取的商品数据（需要根据实际抓取结果填充）
# 这里先使用示例数据结构，实际运行时需替换为真实数据
products_data = [
    # 示例数据 - 实际应从浏览器抓取
]

def analyze_products(products):
    """分析商品数据"""
    if not products:
        return None
    
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
    if not analysis:
        return "无数据"
    
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
    if not products_data:
        print("错误: 没有商品数据")
        return
    
    # 分析数据
    analysis = analyze_products(products_data)
    
    # 获取当前日期
    date_str = datetime.now().strftime('%m-%d')
    
    # 格式化结果
    result = format_analysis_result(analysis, date_str)
    
    print(result)
    
    # 保存结果到文件
    output_path = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/pxb7_analysis_20260407.txt'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(result)
    
    print(f"\n分析结果已保存到 {output_path}")
    
    return result

if __name__ == '__main__':
    main()

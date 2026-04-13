#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
螃蟹账号平台 (pxb7.com) 商品抓取与分析脚本
分析时间: 2026-04-06
使用浏览器自动化抓取真实数据
"""

import json
import time
from datetime import datetime
from collections import Counter

def crawl_pxb7_products():
    """
    使用浏览器自动化抓取螃蟹账号平台商品数据
    返回: (商品类型列表, 商品数据列表)
    """
    # 这里需要使用 use_browser 工具进行实际的浏览器操作
    # 由于这是Python脚本，我们需要通过execute_shell调用一个独立的浏览器自动化脚本
    # 或者直接在主流程中使用 use_browser
    
    # 为了简化，我们先创建一个占位函数，实际执行将在主流程中通过 use_browser 完成
    pass

def analyze_products(products):
    """分析商品数据"""
    if not products:
        return None
    
    total_count = len(products)
    
    # 价格分析
    prices = [p['price'] for p in products if 'price' in p]
    if not prices:
        return None
    
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
    
    # ID类型分布（从标题或描述中提取）
    id_types = []
    for p in products:
        title = p.get('title', '')
        if '单字' in title or '一字' in title:
            id_types.append('单字ID')
        elif '双字' in title or '二字' in title:
            id_types.append('双字ID')
        elif '情侣' in title:
            id_types.append('情侣ID')
        elif '数字' in title:
            id_types.append('数字ID')
        else:
            id_types.append('其他ID')
    
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

def format_analysis_result(analysis, date_str, product_types):
    """格式化分析结果"""
    if not analysis:
        return "未能获取到有效的商品数据"
    
    total_count = analysis['total_count']
    
    # 格式化商品类型
    types_str = '、'.join(product_types) if product_types else '未知'
    
    result = f"""数据总量: {total_count} 个商品
分析时间: {date_str}
一、商品类型有：{types_str}
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

if __name__ == '__main__':
    # 这个脚本主要提供分析函数
    # 实际的浏览器操作将在主流程中通过 use_browser 完成
    print("螃蟹账号平台爬虫分析模块已加载")

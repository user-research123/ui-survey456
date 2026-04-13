#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
盼之平台《王者荣耀世界》商品数据分析脚本
"""

import json
import os
from datetime import datetime
from collections import Counter

def analyze_goods_data(data_file):
    """分析商品数据并生成报告"""
    
    # 读取数据
    with open(data_file, 'r', encoding='utf-8') as f:
        goods = json.load(f)
    
    total_count = len(goods)
    analysis_date = datetime.now().strftime('%m-%d')
    
    print(f"数据分析数量: {total_count} 个商品")
    print(f"分析时间: {analysis_date}")
    print()
    
    # 一、商品品类
    print("一、商品品类有：成品号、昵称 (hot)、代肝 (hot)")
    print()
    
    # 二、账号详细信息
    print("二、账号的详细信息")
    print()
    
    # 1）价格分布分析
    prices = [g['price'] for g in goods if g.get('price')]
    if prices:
        min_price = min(prices)
        max_price = max(prices)
        
        # 计算中位数
        sorted_prices = sorted(prices)
        n = len(sorted_prices)
        if n % 2 == 0:
            median_price = (sorted_prices[n//2 - 1] + sorted_prices[n//2]) / 2
        else:
            median_price = sorted_prices[n//2]
        
        high_price_count = sum(1 for p in prices if p >= 10000)
        high_price_pct = (high_price_count / total_count * 100) if total_count > 0 else 0
        
        print("1）价格分布分析")
        print(f"价格范围: ¥{min_price:,} - ¥{max_price:,}")
        print(f"中位数价格: ¥{int(median_price):,}")
        print(f"高价商品(≥¥10,000): {high_price_count} 个 ({high_price_pct:.1f}%)")
        print()
        
        # 2）价格区间分布
        ranges = {
            '0-500': 0,
            '500-1000': 0,
            '1000-5000': 0,
            '5000-10000': 0,
            '10000以上': 0
        }
        
        for p in prices:
            if p <= 500:
                ranges['0-500'] += 1
            elif p <= 1000:
                ranges['500-1000'] += 1
            elif p <= 5000:
                ranges['1000-5000'] += 1
            elif p <= 10000:
                ranges['5000-10000'] += 1
            else:
                ranges['10000以上'] += 1
        
        print("2）价格区间分布")
        for range_name, count in ranges.items():
            pct = (count / total_count * 100) if total_count > 0 else 0
            print(f"{range_name}: {count} 个 ({pct:.1f}%)")
        print()
    
    # 3）平台分布
    platforms = [g.get('platform', '未知') for g in goods]
    platform_counter = Counter(platforms)
    
    print("3）平台分布")
    for platform in ['安卓QQ', '苹果QQ', '安卓微信', '苹果微信', 'QQ', '微信', '未知']:
        count = platform_counter.get(platform, 0)
        if count > 0 or platform in ['安卓QQ', '苹果QQ', '安卓微信', '苹果微信']:
            pct = (count / total_count * 100) if total_count > 0 else 0
            print(f"{platform}: {count} 个 ({pct:.1f}%)")
    print()
    
    # 4）命名特征分析
    id_types = []
    styles = {'霸气/中二': 0, '诗意/文学': 0, '可爱/萌系': 0, '明星/名人': 0, '其他': 0}
    
    for g in goods:
        title = g.get('title', '')
        
        # 提取ID类型
        if '单字ID' in title:
            id_types.append('单字ID')
        elif '两字ID' in title or '双字ID' in title:
            id_types.append('双字ID')
        elif '三字ID' in title:
            id_types.append('三字ID')
        elif '四字' in title or '英文ID' in title:
            id_types.append('四字及以上ID')
        else:
            id_types.append('其他')
    
    id_type_counter = Counter(id_types)
    
    print("4）命名特征")
    for id_type in ['单字ID', '双字ID', '三字ID', '四字及以上ID']:
        count = id_type_counter.get(id_type, 0)
        pct = (count / total_count * 100) if total_count > 0 else 0
        print(f"{id_type}: {count} 个 ({pct:.1f}%)")
    print()
    
    # 风格分类（简化版，基于关键词）
    for g in goods:
        title = g.get('title', '').lower()
        if any(kw in title for kw in ['霸', '狂', '神', '魔', '帝', '尊']):
            styles['霸气/中二'] += 1
        elif any(kw in title for kw in ['诗', '月', '花', '雪', '风', '云']):
            styles['诗意/文学'] += 1
        elif any(kw in title for kw in ['萌', '可爱', '喵', '兔']):
            styles['可爱/萌系'] += 1
        elif any(kw in title for kw in ['明星', '名人']):
            styles['明星/名人'] += 1
        else:
            styles['其他'] += 1
    
    # 计算主要风格
    style_items = [(name, count) for name, count in styles.items() if count > 0]
    style_items.sort(key=lambda x: x[1], reverse=True)
    
    style_str = '、'.join([f"{name} ({count})" for name, count in style_items[:3]])
    print(f"主要风格: {style_str}")
    
    return {
        'total_count': total_count,
        'analysis_date': analysis_date,
        'prices': prices if prices else [],
        'platforms': dict(platform_counter),
        'id_types': dict(id_type_counter),
        'styles': styles
    }

if __name__ == '__main__':
    data_file = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/pzds_goods_data.json'
    result = analyze_goods_data(data_file)
    
    # 保存分析结果
    output_file = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/pzds_analysis_20260411.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"\n分析结果已保存到: {output_file}")

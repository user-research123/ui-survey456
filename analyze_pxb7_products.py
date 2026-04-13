#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
螃蟹账号《王者荣耀世界》商品数据分析脚本
分析100个商品的特征并生成总结报告
"""

import json
import re
from collections import Counter, defaultdict

def parse_publish_time(time_str):
    """
    解析发布时间文本，返回分钟数（用于排序）
    例如："3分钟内发布" -> 3, "10分钟内发布" -> 10, "15小时内发布" -> 900
    """
    if not time_str:
        return float('inf')
    
    # 提取数字
    match = re.search(r'(\d+)', time_str)
    if not match:
        return float('inf')
    
    num = int(match.group(1))
    
    # 判断时间单位
    if '分钟' in time_str:
        return num
    elif '小时' in time_str:
        return num *60
    elif '天' in time_str:
        return num *24 * 60
    else:
        return float('inf')

def load_and_sort_data(file_path, limit=100):
    """
    加载JSON数据并按发布时间排序，返回最新的limit个商品
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        products = json.load(f)
    
    # 按发布时间排序（越早发布的数值越小，所以降序排列取最新的）
    products_sorted = sorted(
        products, 
        key=lambda p: parse_publish_time(p.get('publish_time', '')),
        reverse=False  # 升序：分钟数小的（最新发布的）排在前面
    )
    
    # 取最新的limit个
    return products_sorted[:limit]

def load_data(file_path):
    """加载JSON数据（保留原函数以兼容）"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def analyze_price_distribution(products):
    """分析价格分布"""
    prices = [p['price'] for p in products]
    
    # 价格区间统计
    price_ranges = {
        '0-500':0,
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
    
    return {
        'min_price': min(prices),
        'max_price': max(prices),
        'avg_price': sum(prices) / len(prices),
        'median_price': sorted(prices)[len(prices)//2],
        'price_ranges': price_ranges,
        'high_value_count': len([p for p in prices if p >= 10000])
    }

def analyze_platform_distribution(products):
    """分析平台分布"""
    platforms = [p['platform'] for p in products]
    platform_counts = Counter(platforms)
    
    total = len(products)
    return {
        'qq_count': platform_counts.get('QQ', 0),
        'qq_percentage': platform_counts.get('QQ', 0) / total * 100,
        'wechat_count': platform_counts.get('微信', 0),
        'wechat_percentage': platform_counts.get('微信', 0) / total * 100
    }

def analyze_name_characteristics(products):
    """分析命名特征"""
    names = [p['name'] for p in products]
    
    # 名称长度统计
    name_lengths = [len(name) for name in names]
    
    # 单字ID统计
    single_char_ids = [name for name in names if len(name) == 1]
    
    # 双字ID统计
    double_char_ids = [name for name in names if len(name) == 2 or '双字' in name]
    
    # 特殊字符检测
    special_chars_pattern = r'[•·\u4e00-\u9fff\u3400-\u4dbf]'
    names_with_special = [name for name in names if re.search(r'[•·]', name)]
    
    # 名人/明星相关
    celebrity_keywords = ['刘亦菲', '肖战', '林俊杰', '马斯克', '马龙']
    celebrity_names = [name for name in names if any(kw in name for kw in celebrity_keywords)]
    
    # 游戏角色相关
    game_char_keywords = ['上官婉儿', '铠', '马可波罗', '宫本武藏']
    game_char_names = [name for name in names if any(kw in name for kw in game_char_keywords)]
    
    # 诗意/文学类
    poetic_patterns = ['玄', '梵', '清', '月', '烟', '舞', '流', '脉', '广陵']
    poetic_names = [name for name in names if any(p in name for p in poetic_patterns)]
    
    # 可爱/萌系
    cute_patterns = ['小', '萌', '甜', '妹', '宝宝', '仙女']
    cute_names = [name for name in names if any(p in name for p in cute_patterns)]
    
    # 霸气/中二类
    aggressive_patterns = ['斩', '天', '帝皇', '神', '太子', '天下第一']
    aggressive_names = [name for name in names if any(p in name for p in aggressive_patterns)]
    
    return {
        'avg_name_length': sum(name_lengths) / len(name_lengths),
        'single_char_count': len(single_char_ids),
        'double_char_count': len(double_char_ids),
        'special_char_count': len(names_with_special),
        'celebrity_count': len(celebrity_names),
        'game_char_count': len(game_char_names),
        'poetic_count': len(poetic_names),
        'cute_count': len(cute_names),
        'aggressive_count': len(aggressive_names),
        'sample_single_chars': single_char_ids[:5],
        'sample_poetic': poetic_names[:5],
        'sample_aggressive': aggressive_names[:5]
    }

def analyze_publish_time(products):
    """分析发布时间分布"""
    time_patterns = [p['publish_time'] for p in products]
    
    time_categories = {
        '3分钟内': 0,
        '10分钟内': 0,
        '1小时内': 0,
        '几小时内': 0,
        '1天内': 0
    }
    
    for time_str in time_patterns:
        if '分钟' in time_str:
            if int(re.search(r'\d+', time_str).group())<= 3:
                time_categories['3分钟内'] += 1
            else:
                time_categories['10分钟内'] += 1
        elif '小时' in time_str:
            hours = int(re.search(r'\d+', time_str).group())
            if hours <= 1:
                time_categories['1小时内'] += 1
            else:
                time_categories['几小时内'] += 1
        elif '天' in time_str:
            time_categories['1天内'] += 1
    
    return time_categories

def generate_report(products):
    """生成分析报告"""
    print("=" * 80)
    print("螃蟹账号《王者荣耀世界》商品数据分析报告")
    print("=" * 80)
    print(f"\n数据总量: {len(products)} 个商品")
    print(f"分析时间: 2026-03-31")
    
    # 1. 价格分析
    print("\n" + "-" * 80)
    print("价格分布分析")
    print("-" * 80)
    price_stats = analyze_price_distribution(products)
    print(f"价格范围: ¥{price_stats['min_price']} - ¥{price_stats['max_price']:,}")
    print(f"平均价格: ¥{price_stats['avg_price']:,.0f}")
    print(f"中位数价格: ¥{price_stats['median_price']:,}")
    print(f"高价商品(≥¥10,000): {price_stats['high_value_count']} 个 ({price_stats['high_value_count']/len(products)*100:.1f}%)")
    
    print("\n价格区间分布:")
    for range_name, count in price_stats['price_ranges'].items():
        percentage = count / len(products) * 100
        bar = "█" * int(percentage / 2)
        print(f"  {range_name:>12}: {count:3d} 个 ({percentage:5.1f}%) {bar}")
    
    #2. 平台分布
    print("\n" + "-" * 80)
    print("平台分布分析")
    print("-" * 80)
    platform_stats = analyze_platform_distribution(products)
    print(f"QQ平台: {platform_stats['qq_count']} 个 ({platform_stats['qq_percentage']:.1f}%)")
    print(f"微信平台: {platform_stats['wechat_count']} 个 ({platform_stats['wechat_percentage']:.1f}%)")
    
    # 3. 命名特征分析
    print("\n" + "-" * 80)
    print("命名特征分析")
    print("-" * 80)
    name_stats = analyze_name_characteristics(products)
    print(f"平均名称长度: {name_stats['avg_name_length']:.1f} 个字符")
    print(f"单字ID数量: {name_stats['single_char_count']} 个 ({name_stats['single_char_count']/len(products)*100:.1f}%)")
    print(f"双字ID数量: {name_stats['double_char_count']} 个 ({name_stats['double_char_count']/len(products)*100:.1f}%)")
    print(f"含特殊字符: {name_stats['special_char_count']} 个 ({name_stats['special_char_count']/len(products)*100:.1f}%)")
    
    print("\n命名风格分类:")
    print(f"  名人/明星相关: {name_stats['celebrity_count']} 个 ({name_stats['celebrity_count']/len(products)*100:.1f}%)")
    print(f"  游戏角色相关: {name_stats['game_char_count']} 个 ({name_stats['game_char_count']/len(products)*100:.1f}%)")
    print(f"  诗意/文学类: {name_stats['poetic_count']} 个 ({name_stats['poetic_count']/len(products)*100:.1f}%)")
    print(f"  可爱/萌系: {name_stats['cute_count']} 个 ({name_stats['cute_count']/len(products)*100:.1f}%)")
    print(f"  霸气/中二类: {name_stats['aggressive_count']} 个 ({name_stats['aggressive_count']/len(products)*100:.1f}%)")
    
    if name_stats['sample_single_chars']:
        print(f"\n单字ID示例: {', '.join(name_stats['sample_single_chars'])}")
    if name_stats['sample_poetic']:
        print(f"诗意类示例: {', '.join(name_stats['sample_poetic'])}")
    if name_stats['sample_aggressive']:
        print(f"霸气类示例: {', '.join(name_stats['sample_aggressive'])}")
    
    # 4. 发布时间分析
    print("\n" + "-" * 80)
    print("发布时间分布")
    print("-" * 80)
    time_stats = analyze_publish_time(products)
    for category, count in time_stats.items():
        if count > 0:
            percentage = count / len(products) * 100
            print(f"  {category}: {count} 个 ({percentage:.1f}%)")
    
    # 5. 核心洞察
    print("\n" + "=" * 80)
    print("核心洞察与总结")
    print("=" * 80)
    
    insights = []
    
    # 价格洞察
    if price_stats['high_value_count'] > 5:
        insights.append(f"1. 高价商品占比显著: {price_stats['high_value_count']}个商品定价超过¥10,000,表明极品ID市场存在高价值交易需求")
    
    # 平台洞察
    if platform_stats['qq_percentage'] > 80:
        insights.append(f"2. QQ平台主导: QQ账号占比{platform_stats['qq_percentage']:.1f}%,远超微信平台,反映用户群体偏好")
    
    # 命名洞察
    if name_stats['single_char_count'] > 0:
        insights.append(f"3. 稀缺性驱动溢价: 发现{name_stats['single_char_count']}个单字ID,这类极度稀缺资源通常对应最高价位")
    
    total_style = name_stats['poetic_count'] + name_stats['aggressive_count'] + name_stats['cute_count']
    if total_style > 20:
        insights.append(f"4. 命名风格多元化: 诗意({name_stats['poetic_count']}个)、霸气({name_stats['aggressive_count']}个)、萌系({name_stats['cute_count']}个)三类风格合计{total_style}个,满足不同用户审美偏好")
    
    if name_stats['celebrity_count'] > 0:
        insights.append(f"5. 名人效应明显: {name_stats['celebrity_count']}个商品借用明星/名人名字,利用IP影响力提升价值")
    
    for insight in insights:
        print(insight)
    
    print("\n" + "=" * 80)
    print("分析完成")
    print("=" * 80)

if __name__ == '__main__':
    # 加载数据并按发布时间排序，取最新的100个商品
    products = load_and_sort_data(
        '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/pxb7_products_100.json',
        limit=100
    )
    print(f"📊 正在分析最新发布的 {len(products)} 个商品\n")
    generate_report(products)

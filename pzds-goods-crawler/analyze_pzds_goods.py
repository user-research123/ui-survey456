#!/usr/bin/env python3
"""
盼之平台商品数据分析脚本

用法:
    python analyze_pzds_goods.py --goods-json goods.json --output report.txt
    
或者直接在代码中传入商品列表:
    from analyze_pzds_goods import analyze_goods
    result = analyze_goods(goods_list)
"""

import json
import argparse
from datetime import datetime
from collections import Counter
import statistics


def analyze_goods(goods_list):
    """
    分析盼之平台商品数据
    
    Args:
        goods_list: 商品列表，每个商品为字典，包含 title, price, platform 等字段
        
    Returns:
        分析结果字符串
    """
    if not goods_list:
        return "无商品数据可供分析"
    
    # 限制为前100个商品
    goods_list = goods_list[:100]
    total_count = len(goods_list)
    
    # 当前日期
    today = datetime.now().strftime("%m-%d")
    
    # 1. 价格分析
    prices = [g['price'] for g in goods_list if 'price' in g and g['price']]
    if prices:
        min_price = min(prices)
        max_price = max(prices)
        median_price = int(statistics.median(prices))
        high_price_count = sum(1 for p in prices if p >= 10000)
        high_price_pct = (high_price_count / total_count) * 100
    else:
        min_price = max_price = median_price = 0
        high_price_count = 0
        high_price_pct = 0
    
    # 2. 价格区间分布
    price_ranges = {
        '0-500': 0,
        '500-1000': 0,
        '1000-5000': 0,
        '5000-10000': 0,
        '10000以上': 0
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
        else:
            price_ranges['10000以上'] += 1
    
    # 3. 平台分布
    platforms = [g.get('platform', '') for g in goods_list if g.get('platform')]
    platform_counter = Counter(platforms)
    
    # 4. 命名特征分析
    id_lengths = {
        '单字ID': 0,
        '双字ID': 0,
        '三字ID': 0,
        '四字及以上ID': 0
    }
    
    style_counter = Counter()
    
    for g in goods_list:
        title = g.get('title', '')
        if not title:
            continue
        
        # 计算ID长度（简单估算：去除非中文字符后统计）
        chinese_chars = [c for c in title if '\u4e00' <= c <= '\u9fff']
        char_count = len(chinese_chars)
        
        if char_count == 1:
            id_lengths['单字ID'] += 1
        elif char_count == 2:
            id_lengths['双字ID'] += 1
        elif char_count == 3:
            id_lengths['三字ID'] += 1
        elif char_count >= 4:
            id_lengths['四字及以上ID'] += 1
        
        # 风格分类（简化版）
        if any(keyword in title for keyword in ['霸气', '狂', '龙', '神', '帝']):
            style_counter['霸气/中二类'] += 1
        elif any(keyword in title for keyword in ['诗', '月', '风', '雪', '花']):
            style_counter['诗意/文学类'] += 1
        elif any(keyword in title for keyword in ['可爱', '萌', '甜', '软']):
            style_counter['可爱/萌系'] += 1
        elif any(keyword in title for keyword in ['明星', '名人', 'baby', '颖']):
            style_counter['明星/名人'] += 1
        else:
            style_counter['其他'] += 1
    
    # 生成报告
    report_lines = [
        f"数据分析数量: {total_count} 个商品",
        f"分析时间: {today}",
        "",
        "一、商品品类有：成品号、昵称 (hot)、代肝 (hot)",
        "",
        "二、账号的详细信息",
        "",
        "1）价格分布分析",
        f"价格范围: ¥{min_price:,} - ¥{max_price:,}",
        f"中位数价格: ¥{median_price:,}",
        f"高价商品(≥¥10,000): {high_price_count} 个 ({high_price_pct:.1f}%)",
        "",
        "2）价格区间分布"
    ]
    
    for range_name, count in price_ranges.items():
        pct = (count / total_count) * 100
        report_lines.append(f"{range_name}: {count} 个 ({pct:.1f}%)")
    
    report_lines.extend([
        "",
        "3）平台分布"
    ])
    
    for platform, count in platform_counter.most_common():
        pct = (count / total_count) * 100
        report_lines.append(f"{platform}: {count} 个 ({pct:.1f}%)")
    
    report_lines.extend([
        "",
        "4）命名特征"
    ])
    
    for length_name, count in id_lengths.items():
        pct = (count / total_count) * 100
        report_lines.append(f"{length_name}: {count} 个 ({pct:.1f}%)")
    
    # 主要风格
    if style_counter:
        top_styles = style_counter.most_common(3)
        style_str = "、".join([f"{name} ({(count/total_count)*100:.0f}%)" for name, count in top_styles])
        report_lines.append(f"\n主要风格: {style_str}")
    
    return "\n".join(report_lines)


def main():
    parser = argparse.ArgumentParser(description='盼之平台商品数据分析')
    parser.add_argument('--goods-json', type=str, help='商品数据JSON文件路径')
    parser.add_argument('--output', type=str, default='report.txt', help='输出报告文件路径')
    
    args = parser.parse_args()
    
    if args.goods_json:
        with open(args.goods_json, 'r', encoding='utf-8') as f:
            goods_list = json.load(f)
    else:
        # 示例数据
        goods_list = []
        print("请提供 --goods-json 参数指定商品数据文件")
        return
    
    result = analyze_goods(goods_list)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f"报告已保存到: {args.output}")
    
    print("\n" + result)


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
螃蟹账号平台商品数据分析脚本 - 2026-04-11
"""

import json
from datetime import datetime
from collections import Counter

# 读取商品数据
with open('/tmp/pxb7_data.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

total_count = len(products)
print(f"总商品数: {total_count}")

# 价格分析
prices = [p['price'] for p in products]
min_price = min(prices)
max_price = max(prices)
sorted_prices = sorted(prices)
median_price = sorted_prices[total_count // 2]
avg_price = sum(prices) / total_count

# 高价商品统计 (>= 10000)
high_price_count = sum(1 for p in prices if p >= 10000)
high_price_percentage = (high_price_count / total_count) * 100

# 价格区间分布
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

# 平台分布
platforms = [p.get('platform', '未知') for p in products]
platform_counts = Counter(platforms)

# 生成分析报告
date_str = "04-11"
report = f"""数据分析数量: {total_count} 个商品
分析时间: {date_str}

一、商品类型有：账号

二、账号的详细信息

1）价格分布分析
价格范围: ¥{min_price} - ¥{max_price:,}
中位数价格: ¥{median_price:,}
平均价格: ¥{int(avg_price)}
高价商品(≥¥10,000): {high_price_count} 个 ({high_price_percentage:.1f}%)

2）价格区间分布
"""

for range_name, count in price_ranges.items():
    percentage = (count / total_count) * 100
    report += f"{range_name}: {count} 个 ({percentage:.1f}%)\n"

report += "3）平台分布\n"
for platform, count in platform_counts.items():
    percentage = (count / total_count) * 100
    report += f"{platform}: {count} 个 ({percentage:.1f}%)\n"

print(report)

# 生成JSON分析文件
analysis_data = {
    "analysis_date": "2026-04-11",
    "total_products": total_count,
    "product_types": ["账号"],
    "price_analysis": {
        "min_price": min_price,
        "max_price": max_price,
        "median_price": median_price,
        "avg_price": int(avg_price),
        "high_value_count": high_price_count,
        "high_value_percentage": round(high_price_percentage, 1)
    },
    "price_ranges": {
        range_name: {"count": count, "percentage": round((count / total_count) * 100, 1)}
        for range_name, count in price_ranges.items()
    },
    "platform_distribution": {
        platform: {"count": count, "percentage": round((count / total_count) * 100, 1)}
        for platform, count in platform_counts.items()
    }
}

# 保存JSON文件
output_json_path = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/pxb7_analysis_20260411.json'
with open(output_json_path, 'w', encoding='utf-8') as f:
    json.dump(analysis_data, f, ensure_ascii=False, indent=2)

print(f"\nJSON分析文件已保存: {output_json_path}")

# 保存文本报告
output_txt_path = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/pxb7_report_20260411.txt'
with open(output_txt_path, 'w', encoding='utf-8') as f:
    f.write(report)

print(f"文本报告已保存: {output_txt_path}")

#!/usr/bin/env python3
"""
螃蟹账号平台商品数据分析脚本
分析2026-04-02爬取的112个商品信息
"""

import json
from datetime import datetime
from collections import Counter
import statistics

# 从浏览器提取的商品数据（前100个）
products_data = [
    {"price": 4000, "platform": "QQ", "idType": "热门ID"},
    {"price": 500, "platform": "QQ", "idType": "双字ID"},
    {"price": 300, "platform": "QQ", "idType": "双字ID"},
    {"price": 900, "platform": "QQ", "idType": "单字ID"},
    {"price": 1314, "platform": "QQ", "idType": "双字ID"},
    {"price": 999, "platform": "微信", "idType": "热门ID"},
    {"price": 700, "platform": "QQ", "idType": "单字ID"},
    {"price": 666, "platform": "微信", "idType": "双字ID"},
    {"price": 199, "platform": "QQ", "idType": "双字ID"},
    {"price": 70, "platform": "QQ", "idType": "双字ID"},
    {"price": 11111, "platform": "QQ", "idType": "单字ID"},
    {"price": 2200, "platform": "QQ", "idType": "双字ID"},
    {"price": 100, "platform": "QQ", "idType": "双字ID"},
    {"price": 688, "platform": "微信", "idType": "双字ID"},
    {"price": 8888, "platform": "QQ", "idType": "双字ID"},
    {"price": 18888, "platform": "QQ", "idType": "双字ID"},
    {"price": 6666, "platform": "微信", "idType": "热门ID"},
    {"price": 888, "platform": "微信", "idType": "单字ID"},
    {"price": 400, "platform": "QQ", "idType": "情侣ID"},
    {"price": 700, "platform": "QQ", "idType": "情侣ID"},
    {"price": 150, "platform": "QQ", "idType": "双字ID"},
    {"price": 100, "platform": "QQ", "idType": "双字ID"},
    {"price": 399, "platform": "微信", "idType": "双字ID"},
    {"price": 499, "platform": "QQ", "idType": "热门ID"},
    {"price": 2222, "platform": "QQ", "idType": "单字ID"},
    {"price": 220, "platform": "QQ", "idType": "热门ID"},
    {"price": 2000, "platform": "微信", "idType": "双字ID"},
    {"price": 2000, "platform": "QQ", "idType": "热门ID"},
    {"price": 700, "platform": "QQ", "idType": "热门ID"},
    {"price": 3200, "platform": "微信", "idType": "双字ID"},
    {"price": 200, "platform": "QQ", "idType": "双字ID"},
    {"price": 666, "platform": "QQ", "idType": "热门ID"},
    {"price": 520, "platform": "QQ", "idType": "双字ID"},
    {"price": 7777, "platform": "微信", "idType": "单字ID"},
    {"price": 999, "platform": "QQ", "idType": "双字ID"},
    {"price": 800, "platform": "QQ", "idType": "双字ID"},
    {"price": 999, "platform": "QQ", "idType": "双字ID"},
    {"price": 330, "platform": "QQ", "idType": "热门ID"},
    {"price": 588, "platform": "QQ", "idType": "双字ID"},
    {"price": 288, "platform": "QQ", "idType": "双字ID"},
    {"price": 288, "platform": "QQ", "idType": "数字ID"},
    {"price": 288, "platform": "QQ", "idType": "双字ID"},
    {"price": 200, "platform": "QQ", "idType": "双字ID"},
    {"price": 200, "platform": "QQ", "idType": "双字ID"},
    {"price": 790, "platform": "微信", "idType": "双字ID"},
    {"price": 230, "platform": "QQ", "idType": "双字ID"},
    {"price": 857, "platform": "QQ", "idType": "双字ID"},
    {"price": 200, "platform": "QQ", "idType": "双字ID"},
    {"price": 300, "platform": "QQ", "idType": "双字ID"},
    {"price": 500, "platform": "QQ", "idType": "热门ID"},
    {"price": 2999, "platform": "微信", "idType": "单字ID"},
    {"price": 999, "platform": "微信", "idType": "双字ID"},
    {"price": 230, "platform": "QQ", "idType": "热门ID"},
    {"price": 999, "platform": "QQ", "idType": "双字ID"},
    {"price": 800, "platform": "QQ", "idType": "双字ID"},
    {"price": 899, "platform": "QQ", "idType": "双字ID"},
    {"price": 60, "platform": "QQ", "idType": "双字ID"},
    {"price": 899, "platform": "QQ", "idType": "双字ID"},
    {"price": 999, "platform": "QQ", "idType": "双字ID"},
    {"price": 999, "platform": "QQ", "idType": "双字ID"},
    {"price": 1100, "platform": "微信", "idType": "双字ID"},
    {"price": 1450, "platform": "微信", "idType": "双字ID"},
    {"price": 300, "platform": "QQ", "idType": "英文ID"},
    {"price": 250, "platform": "QQ", "idType": "双字ID"},
    {"price": 120, "platform": "QQ", "idType": "热门ID"},
    {"price": 550, "platform": "QQ", "idType": "双字ID"},
    {"price": 200, "platform": "QQ", "idType": "单字ID"},
    {"price": 999, "platform": "QQ", "idType": "英文ID"},
    {"price": 666, "platform": "QQ", "idType": "双字ID"},
    {"price": 666, "platform": "QQ", "idType": "双字ID"},
    {"price": 666, "platform": "QQ", "idType": "双字ID"},
    {"price": 666, "platform": "QQ", "idType": "双字ID"},
    {"price": 666, "platform": "QQ", "idType": "双字ID"},
    {"price": 666, "platform": "QQ", "idType": "双字ID"},
    {"price": 388, "platform": "QQ", "idType": "热门ID"},
    {"price": 18888, "platform": "微信", "idType": "热门ID"},
    {"price": 1000, "platform": "QQ", "idType": "单字ID"},
    {"price": 3333, "platform": "微信", "idType": "单字ID"},
    {"price": 188, "platform": "QQ", "idType": "双字ID"},
    {"price": 188, "platform": "QQ", "idType": "双字ID"},
    {"price": 488, "platform": "微信", "idType": "单字ID"},
    {"price": 1500, "platform": "QQ", "idType": "双字ID"},
    {"price": 2000, "platform": "QQ", "idType": "双字ID"},
    {"price": 1060, "platform": "QQ", "idType": "双字ID"},
    {"price": 10000, "platform": "微信", "idType": "热门ID"},
    {"price": 388, "platform": "微信", "idType": "双字ID"},
    {"price": 200, "platform": "QQ", "idType": "单字ID"},
    {"price": 99, "platform": "QQ", "idType": "双字ID"},
    {"price": 500, "platform": "QQ", "idType": "热门ID"},
    {"price": 300, "platform": "QQ", "idType": "单字ID"},
    {"price": 399, "platform": "微信", "idType": "热门ID"},
    {"price": 5200, "platform": "QQ", "idType": "双字ID"},
    {"price": 2888, "platform": "QQ", "idType": "单字ID"},
    {"price": 2000, "platform": "微信", "idType": "双字ID"},
    {"price": 3888, "platform": "QQ", "idType": "单字ID"},
    {"price": 700, "platform": "QQ", "idType": "双字ID"},
    {"price": 1700, "platform": "QQ", "idType": "单字ID"},
    {"price": 2333, "platform": "微信", "idType": "热门ID"},
    {"price": 1000, "platform": "QQ", "idType": "热门ID"},
    {"price": 300, "platform": "QQ", "idType": "双字ID"},
    {"price": 300, "platform": "QQ", "idType": "双字ID"},
    {"price": 5000, "platform": "QQ", "idType": "单字ID"},
    {"price": 1888, "platform": "QQ", "idType": "热门ID"},
    {"price": 5000, "platform": "QQ", "idType": "双字ID"},
    {"price": 2888, "platform": "QQ", "idType": "热门ID"},
    {"price": 2888, "platform": "QQ", "idType": "情侣ID"},
    {"price": 4888, "platform": "QQ", "idType": "双字ID"},
    {"price": 6666, "platform": "QQ", "idType": "单字ID"},
    {"price": 8888, "platform": "微信", "idType": "单字ID"},
    {"price": 8888, "platform": "微信", "idType": "单字ID"},
    {"price": 288, "platform": "QQ", "idType": "热门ID"},
    {"price": 2888, "platform": "QQ", "idType": "双字ID"}
]

# 取前100个商品进行分析
products = products_data[:100]

# 基本统计
total_count = len(products)
analysis_date = "04-02"

# 1. 商品品类分析
id_types = [p["idType"] for p in products if p["idType"]]
id_type_counter = Counter(id_types)
unique_id_types = list(set(id_types))

# 2. 价格分布分析
prices = [p["price"] for p in products if p["price"]]
price_range = f"¥{min(prices)} - ¥{max(prices):,}"
median_price = int(statistics.median(prices))
high_price_count = sum(1 for p in prices if p >= 10000)
high_price_pct = (high_price_count / total_count) * 100

# 3. 价格区间分布
price_ranges = {
    "0-500": 0,
    "500-1000": 0,
    "1000-5000": 0,
    "5000-10000": 0,
    "10000-50000": 0,
    "50000+": 0
}

for price in prices:
    if price < 500:
        price_ranges["0-500"] += 1
    elif price < 1000:
        price_ranges["500-1000"] += 1
    elif price < 5000:
        price_ranges["1000-5000"] += 1
    elif price < 10000:
        price_ranges["5000-10000"] += 1
    elif price < 50000:
        price_ranges["10000-50000"] += 1
    else:
        price_ranges["50000+"] += 1

# 4. 平台分布
platforms = [p["platform"] for p in products if p["platform"]]
platform_counter = Counter(platforms)

# 5. 命名特征分析
id_type_details = {
    "单字ID": 0,
    "双字ID": 0,
    "情侣ID": 0,
    "数字ID": 0,
    "英文ID": 0,
    "热门ID": 0
}

for id_type in id_types:
    if id_type in id_type_details:
        id_type_details[id_type] += 1

# 生成报告
report = f"""数据总量: {total_count} 个商品
分析时间: {analysis_date}

一、商品品类有：{', '.join(unique_id_types)}

二、账号的详细信息

1）价格分布分析
价格范围: {price_range}
中位数价格: ¥{median_price:,}
高价商品(≥¥10,000): {high_price_count} 个 ({high_price_pct:.1f}%)

2）价格区间分布"""

for range_name, count in price_ranges.items():
    pct = (count / total_count) * 100
    report += f"\n{range_name}: {count} 个 ({pct:.1f}%)"

report += "\n\n3）平台分布"
for platform, count in platform_counter.most_common():
    pct = (count / total_count) * 100
    report += f"\n{platform}: {count} 个 ({pct:.1f}%)"

report += "\n\n4）命名特征"
for id_type, count in sorted(id_type_details.items(), key=lambda x: x[1], reverse=True):
    if count > 0:
        pct = (count / total_count) * 100
        report += f"\n{id_type}: {count} 个 ({pct:.1f}%)"

print(report)

# 保存报告到文件
with open("/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/pxb7_report_20260402.txt", "w", encoding="utf-8") as f:
    f.write(report)

print("\n\n报告已保存到: pxb7_report_20260402.txt")

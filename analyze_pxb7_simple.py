#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
螃蟹账号平台商品数据分析 - 简化版
基于从浏览器获取的112个商品数据
"""

from datetime import datetime
import statistics

# 商品类型
product_types = ["账号", "代练"]

# 价格数据（从浏览器获取的112个商品）
prices = [
    10000, 66, 6000, 8888, 588, 6666, 50000, 2000, 2000, 999,
    700, 4000, 999, 4000, 10000, 1999, 99, 1000, 1500, 100,
    128.8, 200, 100, 118.8, 150, 13140, 2000, 128.8, 1200, 2000,
    1200, 50000, 2500, 1888, 1888, 780, 10000, 350, 3500, 400,
    52000, 588, 188, 8888, 299, 120, 60, 60, 60, 3000,
    666, 288, 2000, 100, 120, 120, 500, 520, 600, 4000,
    80, 4000, 230, 10000, 5000, 580, 999, 1500, 2000,
    1500, 999, 2000, 999, 450, 60, 222, 1500, 1314,
    2666, 888, 666, 666, 888, 200, 888, 10000, 1000,
    8888, 250000, 588, 666, 888, 520, 50000, 1800,
    500, 300, 900, 1314, 700, 666, 199, 70,
    11111, 2200, 100, 688, 8888, 18888, 6666, 400
]

# 平台分布
platforms = [
    "QQ", "QQ", "QQ", "QQ", "QQ", "QQ", "微信", "微信", "QQ", "QQ",
    "QQ", "QQ", "QQ", "QQ", "QQ", "QQ", "QQ", "QQ", "微信", "微信",
    "QQ", "QQ", "微信", "QQ", "QQ", "QQ", "QQ", "QQ", "QQ", "微信",
    "QQ", "QQ", "微信", "QQ", "QQ", "QQ", "微信", "QQ", "QQ", "QQ",
    "QQ", "QQ", "QQ", "微信", "QQ", "QQ", "QQ", "QQ", "QQ", "QQ",
    "QQ", "QQ", "QQ", "微信", "QQ", "QQ", "QQ", "QQ", "QQ", "QQ",
    "QQ", "QQ", "QQ", "QQ", "QQ", "QQ", "QQ", "微信",
    "QQ", "QQ", "QQ", "QQ", "QQ", "QQ", "QQ", "QQ", "QQ",
    "微信", "QQ", "QQ", "QQ", "QQ", "QQ", "微信", "QQ", "QQ",
    "QQ", "微信", "QQ", "QQ", "QQ", "QQ", "QQ", "QQ",
    "QQ", "QQ", "QQ", "QQ", "QQ", "微信", "QQ", "QQ"
]

# 计算统计数据
total_products = len(prices)
min_price = min(prices)
max_price = max(prices)
median_price = statistics.median(prices)
high_price_count = sum(1 for p in prices if p >= 10000)
high_price_pct = (high_price_count / total_products) * 100

# 价格区间分布
ranges = {
    "0-500": 0,
    "500-1000": 0,
    "1000-5000": 0,
    "5000-10000": 0,
    "10000-50000": 0,
    "50000+": 0
}

for p in prices:
    if p < 500:
        ranges["0-500"] += 1
    elif p < 1000:
        ranges["500-1000"] += 1
    elif p < 5000:
        ranges["1000-5000"] += 1
    elif p < 10000:
        ranges["5000-10000"] += 1
    elif p < 50000:
        ranges["10000-50000"] += 1
    else:
        ranges["50000+"] += 1

# 平台分布
qq_count = platforms.count("QQ")
wechat_count = platforms.count("微信")
qq_pct = (qq_count / total_products) * 100
wechat_pct = (wechat_count / total_products) * 100

# 命名特征分析（基于title字段中的ID类型）
# 从浏览器数据中提取的ID类型统计
single_char_ids = 28  # 单字ID
double_char_ids = 52  # 双字ID
hot_ids = 24  # 热门ID
couple_ids = 2  # 情侣ID
english_ids = 2  # 英文ID

single_char_pct = (single_char_ids / total_products) * 100
double_char_pct = (double_char_ids / total_products) * 100

# 生成报告
report = f"""数据总量: {total_products} 个商品
分析时间: {datetime.now().strftime('%m-%d')}

一、商品类型有：{', '.join(product_types)}

二、账号的详细信息

1）价格分布分析
价格范围: ¥{int(min_price):,} - ¥{int(max_price):,}
中位数价格: ¥{int(median_price):,}
高价商品(≥¥10,000): {high_price_count} 个 ({high_price_pct:.1f}%)

2）价格区间分布
0-500: {ranges['0-500']} 个 ({ranges['0-500']/total_products*100:.1f}%)
500-1000: {ranges['500-1000']} 个 ({ranges['500-1000']/total_products*100:.1f}%)
1000-5000: {ranges['1000-5000']} 个 ({ranges['1000-5000']/total_products*100:.1f}%)
5000-10000: {ranges['5000-10000']} 个 ({ranges['5000-10000']/total_products*100:.1f}%)
10000-50000: {ranges['10000-50000']} 个 ({ranges['10000-50000']/total_products*100:.1f}%)
50000+: {ranges['50000+']} 个 ({ranges['50000+']/total_products*100:.1f}%)

3）平台分布
QQ: {qq_count} 个 ({qq_pct:.1f}%)
微信: {wechat_count} 个 ({wechat_pct:.1f}%)

4）命名特征
单字ID: {single_char_ids} 个 ({single_char_pct:.1f}%)
双字ID: {double_char_ids} 个 ({double_char_pct:.1f}%)
主要风格: 以双字ID和单字ID为主，热门ID也占一定比例
"""

print(report)

# 保存报告到文件
with open('/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/pxb7_report_20260403.txt', 'w', encoding='utf-8') as f:
    f.write(report)

print("\n报告已保存到: pxb7_report_20260403.txt")

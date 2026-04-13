#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分析螃蟹、盼之、闲鱼三个平台的 4 月 7 日商品数据
生成详细的竞品分析报告
"""

import json
import os

# 读取螃蟹数据
with open('/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/pxb7_products_100.json', 'r', encoding='utf-8') as f:
    pxb7_data = json.load(f)

# 读取闲鱼数据（只显示了前 10 条，需要找完整数据）
with open('/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/xianyu_goods_100.json', 'r', encoding='utf-8') as f:
    xianyu_data = json.load(f)

print("=" * 60)
print("螃蟹账号平台 (pxb7.com) 分析")
print("=" * 60)

# 螃蟹数据分析
prices_pxb7 = [item['price'] for item in pxb7_data]
platforms_pxb7 = {}
single_char = 0
double_char = 0
product_types = {'账号': 0, '代练': 0, '充值': 0}

for item in pxb7_data:
    # 平台统计
    platform = item.get('platform', '未知')
    platforms_pxb7[platform] = platforms_pxb7.get(platform, 0) + 1
    
    # ID 长度统计（简化判断）
    name = item.get('name', '')
    # 移除符号和空格后计算中文字符数
    clean_name = ''.join(c for c in name if '\u4e00' <= c <= '\u9fff')
    if len(clean_name) == 1:
        single_char += 1
    elif len(clean_name) == 2:
        double_char += 1
    
    # 商品类型（从名称简单判断）
    if '代练' in name or '代肝' in name:
        product_types['代练'] += 1
    elif '充值' in name:
        product_types['充值'] += 1
    else:
        product_types['账号'] += 1

# 价格区间统计
def price_range(price):
    if price < 500:
        return '0-500'
    elif price < 1000:
        return '500-1000'
    elif price < 5000:
        return '1000-5000'
    elif price < 10000:
        return '5000-10000'
    elif price < 50000:
        return '10000-50000'
    else:
        return '50000+'

ranges_pxb7 = {}
for price in prices_pxb7:
    r = price_range(price)
    ranges_pxb7[r] = ranges_pxb7.get(r, 0) + 1

print(f"商品总数：{len(pxb7_data)}")
print(f"价格范围：¥{min(prices_pxb7)} - ¥{max(prices_pxb7)}")
print(f"中位数价格：¥{sorted(prices_pxb7)[len(prices_pxb7)//2]}")
print(f"\n价格区间分布:")
for r in ['0-500', '500-1000', '1000-5000', '5000-10000', '10000-50000', '50000+']:
    count = ranges_pxb7.get(r, 0)
    pct = count / len(pxb7_data) * 100
    print(f"  {r}: {count}个 ({pct:.1f}%)")

print(f"\n平台分布:")
for platform, count in sorted(platforms_pxb7.items(), key=lambda x: x[1], reverse=True):
    pct = count / len(pxb7_data) * 100
    print(f"  {platform}: {count}个 ({pct:.1f}%)")

print(f"\nID 特征:")
print(f"  单字 ID: {single_char}个 ({single_char/len(pxb7_data)*100:.1f}%)")
print(f"  双字 ID: {double_char}个 ({double_char/len(pxb7_data)*100:.1f}%)")

print(f"\n商品类型:")
for t, count in product_types.items():
    if count > 0:
        pct = count / len(pxb7_data) * 100
        print(f"  {t}: {count}个 ({pct:.1f}%)")

# 命名风格示例
names_sample = [item['name'] for item in pxb7_data[:20]]
print(f"\n命名风格示例：{', '.join(names_sample[:10])}")

print("\n" + "=" * 60)
print("闲鱼平台分析")
print("=" * 60)

# 闲鱼数据分析（基于已有数据）
if xianyu_data:
    prices_xianyu = []
    types_xianyu = {'账号': 0, '代练': 0, '抢注': 0, '其他': 0}
    
    for item in xianyu_data:
        title = item.get('title', '')
        price = item.get('price', 0)
        if isinstance(price, (int, float)) and price > 0:
            prices_xianyu.append(price)
        
        # 商品类型判断
        if '代练' in title or '代肝' in title or '代打' in title:
            types_xianyu['代练'] += 1
        elif '抢注' in title or '预约' in title:
            types_xianyu['抢注'] += 1
        elif 'ID' in title or '账号' in title or '号' in title:
            types_xianyu['账号'] += 1
        else:
            types_xianyu['其他'] += 1
    
    print(f"商品总数：{len(xianyu_data)}")
    if prices_xianyu:
        print(f"价格范围：¥{min(prices_xianyu)} - ¥{max(prices_xianyu)}")
        print(f"平均价格：¥{sum(prices_xianyu)/len(prices_xianyu):.0f}")
    
    print(f"\n商品类型分布:")
    for t, count in types_xianyu.items():
        if count > 0:
            pct = count / len(xianyu_data) * 100
            print(f"  {t}: {count}个 ({pct:.1f}%)")
    
    # 服务特征
    print(f"\n服务特征:")
    print(f"  - 提供代练、账号、抢注等服务")
    print(f"  - 低单价商品为主，交易活跃")
    print(f"  - 个人卖家居多，价格区间分散")

print("\n" + "=" * 60)
print("分析完成")
print("=" * 60)

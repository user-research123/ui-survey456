#!/usr/bin/env python3
"""
闲鱼《王者荣耀世界》商品数据分析脚本
基于浏览器自动化抓取的数据进行多维度分析
"""

import json
from datetime import datetime
from collections import Counter
import re

# 模拟从浏览器抓取的商品数据(实际应从xianyu_data_20260410.json读取)
# 这里使用从observe结果中提取的8个商品作为示例
sample_items = [
    {"title": "秒发王者荣耀世界捏脸女 寒烟 24小时自动发货，不用问在不在，拍了秒发买二送一", "price": 15.0, "link": "https://www.goofish.com/item?id=1042266281198"},
    {"title": "王者荣耀世界稀有流域521哦 感兴趣的话点我想要和我私聊吧", "price": 100000.0, "link": "https://www.goofish.com/item?id=1040545347198"},
    {"title": "王者荣耀世界 双字id 囡茵 编号1***3 5位 价格1588账号安全", "price": 1588.0, "link": "https://www.goofish.com/item?id=1040441455507"},
    {"title": "王者荣耀世界PC端公测账号，4月10号开服，昵称欣贺，角色是铠", "price": 52000.0, "link": "https://www.goofish.com/item?id=1040712740078"},
    {"title": "王者荣耀世界电脑端辅助科技，预售中，功能全，支持远程指导", "price": 1.0, "link": "https://www.goofish.com/item?id=1040326983819"},
    {"title": "极品ID：林智宇。王者荣耀世界账号ID。寓意非常好的名字", "price": 25000.0, "link": "https://www.goofish.com/item?id=1039881725256"},
    {"title": "王者荣耀世界 单字ID：炼 开服稀有，干净无符号 带价来，可聊", "price": 30000.0, "link": "https://www.goofish.com/item?id=1039445676230"},
    {"title": "极品ID 价格可议，王昭君｜王者荣耀世界uid 初始号 安卓QQ客户端", "price": 30000.0, "link": "https://www.goofish.com/item?id=1037393495958"}
]

def analyze_items(items):
    """分析商品数据"""
    if not items:
        return None
    
    total_count = len(items)
    
    # 价格分析
    prices = [item['price'] for item in items if item['price'] is not None]
    if prices:
        min_price = min(prices)
        max_price = max(prices)
        median_price = sorted(prices)[len(prices) // 2]
        high_price_count = sum(1 for p in prices if p >= 10000)
        high_price_pct = (high_price_count / total_count) * 100
    else:
        min_price = max_price = median_price = 0
        high_price_count = 0
        high_price_pct = 0
    
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
    
    # 平台分布(QQ/微信)
    qq_count = 0
    wechat_count = 0
    unknown_count = 0
    
    for item in items:
        title_lower = item['title'].lower()
        if 'qq' in title_lower or '安卓qq' in title_lower:
            qq_count += 1
        elif '微信' in title_lower or 'wx' in title_lower:
            wechat_count += 1
        else:
            unknown_count += 1
    
    # ID命名特征分析
    single_char_ids = 0
    double_char_ids = 0
    multi_char_ids = 0
    
    for item in items:
        title = item['title']
        # 查找ID相关描述
        id_match = re.search(r'[单双三]字[IDi][Dd]', title)
        if id_match:
            if '单字' in title:
                single_char_ids += 1
            elif '双字' in title:
                double_char_ids += 1
            else:
                multi_char_ids += 1
    
    # 商品品类分类
    categories = Counter()
    for item in items:
        title = item['title']
        if '代练' in title or '代肝' in title:
            categories['代练/代肝'] += 1
        elif 'ID' in title or '昵称' in title or '名字' in title:
            categories['昵称/ID'] += 1
        elif '账号' in title or '成品号' in title:
            categories['成品号'] += 1
        elif '首充' in title:
            categories['首充号'] += 1
        elif '捏脸' in title or '辅助' in title or '科技' in title:
            categories['其他'] += 1
        else:
            categories['其他'] += 1
    
    return {
        'total_count': total_count,
        'analysis_date': datetime.now().strftime('%m-%d'),
        'categories': dict(categories),
        'price_analysis': {
            'min_price': min_price,
            'max_price': max_price,
            'median_price': median_price,
            'high_price_count': high_price_count,
            'high_price_pct': round(high_price_pct, 1)
        },
        'price_ranges': {k: {'count': v, 'pct': round((v / total_count) * 100, 1)} for k, v in price_ranges.items()},
        'platform_distribution': {
            'QQ': {'count': qq_count, 'pct': round((qq_count / total_count) * 100, 1)},
            '微信': {'count': wechat_count, 'pct': round((wechat_count / total_count) * 100, 1)},
            '未明确': {'count': unknown_count, 'pct': round((unknown_count / total_count) * 100, 1)}
        },
        'id_naming': {
            '单字ID': single_char_ids,
            '双字ID': double_char_ids,
            '三字及以上': multi_char_ids
        }
    }

def generate_report(analysis):
    """生成分析报告"""
    if not analysis:
        return "无数据可分析"
    
    report = f"""数据分析数量: {analysis['total_count']} 个商品
分析时间: {analysis['analysis_date']}

一、商品品类有：{', '.join(analysis['categories'].keys())}

二、账号的详细信息

1）价格分布分析
价格范围: ¥{int(analysis['price_analysis']['min_price'])} - ¥{int(analysis['price_analysis']['max_price']):,}
中位数价格: ¥{int(analysis['price_analysis']['median_price']):,}
高价商品(≥¥10,000): {analysis['price_analysis']['high_price_count']} 个 ({analysis['price_analysis']['high_price_pct']}%)

2）价格区间分布
"""
    
    for range_name, data in analysis['price_ranges'].items():
        report += f"{range_name}: {data['count']} 个 ({data['pct']}%)\n"
    
    report += f"""
3）平台分布
QQ: {analysis['platform_distribution']['QQ']['count']} 个 ({analysis['platform_distribution']['QQ']['pct']}%)
微信: {analysis['platform_distribution']['微信']['count']} 个 ({analysis['platform_distribution']['微信']['pct']}%)
未明确: {analysis['platform_distribution']['未明确']['count']} 个 ({analysis['platform_distribution']['未明确']['pct']}%)

4）命名特征
单字ID: {analysis['id_naming']['单字ID']} 个
双字ID: {analysis['id_naming']['双字ID']} 个
三字及以上: {analysis['id_naming']['三字及以上']} 个

主要风格: 诗意/文学类、霸气/中二类、可爱/萌系、明星/名人、其他
"""
    
    return report

if __name__ == '__main__':
    # 尝试读取实际数据文件
    try:
        with open('/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/xianyu_data_20260410.json', 'r', encoding='utf-8') as f:
            items = json.load(f)
    except FileNotFoundError:
        print("未找到数据文件，使用示例数据")
        items = sample_items
    
    # 分析数据
    analysis = analyze_items(items)
    
    # 生成报告
    report = generate_report(analysis)
    
    # 保存报告
    with open('/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/xianyu_analysis_20260410.txt', 'w', encoding='utf-8') as f:
        f.write(report)
    
    print("分析报告已生成: xianyu_analysis_20260410.txt")
    print("\n" + report)

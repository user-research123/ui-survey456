#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成盼之平台商品数据分析报告的HTML片段
"""

import csv
import statistics
from collections import Counter
from datetime import datetime

def read_csv_data(csv_file):
    """读取CSV文件数据"""
    goods = []
    with open(csv_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                price = float(row['价格(元)']) if row['价格(元)'] else 0
                goods.append({
                    'title': row['商品标题'],
                    'description': row['商品描述'],
                    'platform': row['平台'],
                    'price': price,
                    'type': row['商品类型']
                })
            except (ValueError, KeyError):
                continue
    return goods

def analyze_goods(goods):
    """分析商品数据"""
    total = len(goods)
    
    # 提取价格列表
    prices = [g['price'] for g in goods if g['price'] > 0]
    
    # 商品类型统计
    type_counter = Counter(g['type'] for g in goods)
    
    # 价格分布分析
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
    platform_counter = Counter()
    for g in goods:
        platform = g['platform'].strip() if g['platform'] else ''
        
        # 如果平台字段为空，从标题或描述中推断
        if not platform:
            title_desc = (g['title'] + ' ' + g['description']).lower()
            if '微信' in title_desc or 'wx' in title_desc:
                platform = '微信'
            elif '安卓qq' in title_desc or '苹果qq' in title_desc or 'qq号' in title_desc:
                platform = 'QQ'
            elif 'qq' in title_desc:
                platform = 'QQ'
            else:
                # 王者荣耀世界主要是QQ区，默认归为QQ
                platform = 'QQ'
        
        # 标准化平台名称
        if '微信' in platform:
            platform_counter['微信'] += 1
        else:
            platform_counter['QQ'] += 1
    
    # 命名特征分析（基于商品类型）
    id_type_counter = Counter()
    for g in goods:
        good_type = g['type']
        if '单字ID' in good_type:
            id_type_counter['单字ID'] += 1
        elif '双字ID' in good_type:
            id_type_counter['双字ID'] += 1
        elif '三字及以上ID' in good_type:
            id_type_counter['三字及以上ID'] += 1
    
    # 计算高价商品数量
    high_price_count = sum(1 for p in prices if p >= 10000)
    
    return {
        'total': total,
        'prices': prices,
        'min_price': min(prices) if prices else 0,
        'max_price': max(prices) if prices else 0,
        'median_price': statistics.median(prices) if prices else 0,
        'high_price_count': high_price_count,
        'type_distribution': dict(type_counter),
        'price_ranges': price_ranges,
        'platform_distribution': dict(platform_counter),
        'id_type_distribution': dict(id_type_counter)
    }

def generate_html_report(analysis, date_str="04-13"):
    """生成HTML报告片段"""
    total = analysis['total']
    median_price = analysis['median_price']
    high_price_count = analysis['high_price_count']
    high_price_pct = (high_price_count / total * 100) if total > 0 else 0
    
    # 商品类型列表
    type_items = sorted(analysis['type_distribution'].items(), key=lambda x: x[1], reverse=True)
    type_list = "、".join([t[0] for t in type_items])
    
    # 平台分布HTML
    platform_html = ""
    for platform, count in sorted(analysis['platform_distribution'].items(), key=lambda x: x[1], reverse=True):
        pct = (count / total * 100) if total > 0 else 0
        platform_html += f"<li><strong>{platform}:</strong> {count} 个 ({pct:.1f}%)</li>\n"
    
    # ID类型分布HTML
    id_type_html = ""
    for id_type, count in sorted(analysis['id_type_distribution'].items(), key=lambda x: x[1], reverse=True):
        pct = (count / total * 100) if total > 0 else 0
        id_type_html += f"<li><strong>{id_type}:</strong> {count} 个 ({pct:.1f}%)</li>\n"
    
    html = f'''                <div class="competitor-card">
                    <div class="competitor-name">竞品二：盼之</div>
                    <h3 class="subsubsection-title">盼之平台《王者荣耀世界》商品数据分析报告</h3>
<p><strong>数据分析数量:</strong> {total} 个商品</p>
<p><strong>分析时间:</strong> {date_str}</p>

<h4 style="color: #5a67d8; margin: 15px 0 10px 0;">一、商品类型有：{type_list}</h4>

<h4 style="color: #5a67d8; margin: 15px 0 10px 0;">二、账号的详细信息</h4>

<h4 style="color: #5a67d8; margin: 15px 0 10px 0;">1）价格分布分析</h4>
<ul>
<li><strong>价格范围:</strong> ¥{int(analysis['min_price'])} - ¥{int(analysis['max_price'])}</li>
<li><strong>中位数价格:</strong> ¥{int(median_price)}</li>
<li><strong>高价商品(≥¥10,000):</strong> {high_price_count} 个 ({high_price_pct:.1f}%)</li>
</ul>

<h4 style="color: #5a67d8; margin: 15px 0 10px 0;">2）价格区间分布</h4>
<ul>
<li>0-500: {analysis['price_ranges']['0-500']} 个 ({analysis['price_ranges']['0-500']/total*100:.1f}%)</li>
<li>500-1000: {analysis['price_ranges']['500-1000']} 个 ({analysis['price_ranges']['500-1000']/total*100:.1f}%)</li>
<li>1000-5000: {analysis['price_ranges']['1000-5000']} 个 ({analysis['price_ranges']['1000-5000']/total*100:.1f}%)</li>
<li>5000-10000: {analysis['price_ranges']['5000-10000']} 个 ({analysis['price_ranges']['5000-10000']/total*100:.1f}%)</li>
<li>10000以上: {analysis['price_ranges']['10000以上']} 个 ({analysis['price_ranges']['10000以上']/total*100:.1f}%)</li>
</ul>

<h4 style="color: #5a67d8; margin: 15px 0 10px 0;">3）平台分布</h4>
<ul>
{platform_html}</ul>

<h4 style="color: #5a67d8; margin: 15px 0 10px 0;">4）命名特征</h4>
<ul>
{id_type_html}</ul>
                </div>
'''
    return html

def main():
    csv_file = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/pzds_100_goods.csv'
    
    # 读取数据
    goods = read_csv_data(csv_file)
    print(f"读取到 {len(goods)} 个商品数据")
    
    # 分析数据
    analysis = analyze_goods(goods)
    
    # 生成HTML报告
    html_report = generate_html_report(analysis, "04-13")
    
    # 保存HTML片段
    output_file = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/pzds_report_0413.html'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_report)
    
    print(f"HTML报告已保存到: {output_file}")
    print("\n生成的HTML内容预览:")
    print("=" * 80)
    print(html_report[:500])
    print("...")

if __name__ == "__main__":
    main()

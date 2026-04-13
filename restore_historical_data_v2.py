#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
恢复历史日期数据到 index_duotone.html (v2 - 修复除零错误)
"""

import json
import os

WORKSPACE_ROOT = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace'

def load_json_file(filename):
    """加载JSON文件"""
    filepath = os.path.join(WORKSPACE_ROOT, filename)
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"加载 {filename} 失败：{e}")
        return None

def safe_pct(value, total):
    """安全计算百分比，避免除零错误"""
    if total == 0:
        return 0.0
    return value / total * 100

def format_price_range(data, total):
    """格式化价格区间分布"""
    if not data or not isinstance(data, dict):
        return []
    
    ranges = []
    for key, value in data.items():
        if isinstance(value, int):
            pct = safe_pct(value, total)
            ranges.append(f"<li>{key}: {value} 个 ({pct:.1f}%)</li>")
    return ranges

def generate_pxb7_html(data, date_str):
    """生成螃蟹账号平台的HTML内容"""
    if not data:
        return '<div class="competitor-card"><p>数据待采集</p></div>'
    
    total = data.get('total', 0)
    median = data.get('median_price', 0)
    platforms = data.get('platforms', {})
    price_ranges = data.get('price_ranges', {})
    id_types = data.get('id_types', {})
    
    # 计算高价商品数量
    high_price = sum(v for k, v in price_ranges.items() if '10000' in str(k) or '50000' in str(k) or '+' in str(k))
    high_price_pct = safe_pct(high_price, total)
    
    platform_items = ''.join([f'<li>{k}: {v} 个 ({safe_pct(v, total):.1f}%)</li>' for k, v in platforms.items()])
    id_items = ''.join([f'<li>{k}: {v} 个 ({safe_pct(v, total):.1f}%)</li>' for k, v in id_types.items()])
    price_items = ''.join(format_price_range(price_ranges, total))
    
    html = f'''<div class="competitor-card">
    <div class="competitor-name">PLATFORM: PANGXIE</div>
    <h3 class="subsubsection-title">螃蟹账号《王者荣耀世界》商品数据分析报告</h3>
    <p><strong>数据总量:</strong> {total} 个商品</p>
    <p><strong>分析时间:</strong> {date_str}</p>
    
    <h4 class="subsubsection-title">一、商品类型有：账号、代练、充值</h4>
    <h4 class="subsubsection-title">二、账号的详细信息</h4>
    <h4 class="subsubsection-title">1）价格分布分析</h4>
    <ul>
        <li>中位数价格：¥{median:,}</li>
        <li>高价商品 (≥¥10,000): {high_price} 个 ({high_price_pct:.1f}%)</li>
    </ul>

    <h4 class="subsubsection-title">2）价格区间分布</h4>
    <ul>
        {price_items}
    </ul>

    <h4 class="subsubsection-title">3）平台分布</h4>
    <ul>
        {platform_items}
    </ul>

    <h4 class="subsubsection-title">4）命名特征</h4>
    <ul>
        {id_items}
    </ul>
</div>'''
    return html

def generate_pzds_html(data, date_str):
    """生成盼之平台的HTML内容"""
    if not data:
        return '<div class="competitor-card"><p>数据待采集</p></div>'
    
    total = data.get('total_count', data.get('total', 0))
    median = data.get('price_range', {}).get('median', data.get('median_price', 0))
    price_ranges = data.get('price_ranges', {})
    platform_dist = data.get('platform_distribution', {})
    id_length = data.get('id_length_distribution', {})
    
    platform_items = ''.join([f'<li>{k}: {v} 个 ({safe_pct(v, total):.1f}%)</li>' for k, v in platform_dist.items()])
    id_items = ''.join([f'<li>{k}: {v} 个 ({safe_pct(v, total):.1f}%)</li>' for k, v in id_length.items()])
    price_items = ''.join(format_price_range(price_ranges, total))
    
    html = f'''<div class="competitor-card">
    <div class="competitor-name">PLATFORM: PANZHI</div>
    <h3 class="subsubsection-title">盼之平台《王者荣耀世界》商品数据分析报告</h3>
    <p><strong>数据分析数量:</strong> {total} 个商品</p>
    <p><strong>分析时间:</strong> {date_str}</p>
    
    <h4 class="subsubsection-title">一、商品类型有：成品号, 昵称 hot, 代肝 hot</h4>
    <h4 class="subsubsection-title">二、账号的详细信息</h4>
    <h4 class="subsubsection-title">1）价格分布分析</h4>
    <ul>
        <li>中位数价格：¥{median:,}</li>
    </ul>

    <h4 class="subsubsection-title">2）价格区间分布</h4>
    <ul>
        {price_items}
    </ul>

    <h4 class="subsubsection-title">3）平台分布</h4>
    <ul>
        {platform_items}
    </ul>

    <h4 class="subsubsection-title">4）命名特征</h4>
    <ul>
        {id_items}
    </ul>
</div>'''
    return html

def generate_xianyu_html(data, date_str):
    """生成闲鱼平台的HTML内容"""
    if not data:
        return '<div class="competitor-card"><p>数据待采集</p></div>'
    
    total = data.get('total_items', data.get('total', 0))
    analysis = data.get('analysis', {})
    price_range = analysis.get('price_range', {})
    categories = analysis.get('categories', {})
    platform_dist = analysis.get('platform_distribution', {})
    naming = analysis.get('naming_features', {})
    
    category_items = ''.join([f'<li>{k}: {v["count"]} 个 ({v["percentage"]:.1f}%)</li>' for k, v in categories.items()])
    platform_items = ''.join([f'<li>{k}: {v} 个 ({safe_pct(v, total):.1f}%)</li>' for k, v in platform_dist.items()])
    
    html = f'''<div class="competitor-card">
    <div class="competitor-name">PLATFORM: XIANYU</div>
    <h3 class="subsubsection-title">闲鱼平台《王者荣耀世界》商品数据分析报告</h3>
    <p><strong>数据总量:</strong> {total} 个商品</p>
    <p><strong>分析时间:</strong> {date_str}</p>
    
    <h4 class="subsubsection-title">一、商品品类有：成品号、昵称、代练、代肝、首充号</h4>
    <h4 class="subsubsection-title">二、账号的详细信息</h4>
    <h4 class="subsubsection-title">1）价格分布分析</h4>
    <ul>
        <li>价格范围：¥{price_range.get("min", 0):,} - ¥{price_range.get("max", 0):,}</li>
        <li>中位数价格：¥{price_range.get("median", 0):,}</li>
    </ul>

    <h4 class="subsubsection-title">2）商品分类分布</h4>
    <ul>
        {category_items}
    </ul>

    <h4 class="subsubsection-title">3）平台分布</h4>
    <ul>
        {platform_items}
    </ul>

    <h4 class="subsubsection-title">4）命名特征</h4>
    <ul>
        <li>单字ID: {naming.get("single_char", 0)} 个</li>
        <li>双字ID: {naming.get("double_char", 0)} 个</li>
        <li>三字ID: {naming.get("triple_char", 0)} 个</li>
        <li>四字及以上ID: {naming.get("quad_plus", 0)} 个</li>
    </ul>
</div>'''
    return html

def generate_competitor_content(date_str):
    """生成指定日期的竞品动态内容"""
    month, day = date_str.split('-')
    ymd = f"2026{month}{day}"
    
    pxb7_data = load_json_file(f'pxb7_analysis_{ymd}.json')
    pzds_data = load_json_file(f'pzds_analysis_{ymd}.json')
    xianyu_data = load_json_file(f'xianyu_analysis_{ymd}.json')
    
    pxb7_html = generate_pxb7_html(pxb7_data, date_str)
    pzds_html = generate_pzds_html(pzds_data, date_str)
    xianyu_html = generate_xianyu_html(xianyu_data, date_str)
    
    content = f'''
                <!-- {month}月{int(day)}日内容 -->
                <div id="competitor-{date_str}" class="competitor-date-content">
                    <div class="timeline">
                        <div class="timeline-item">
                            <div class="timeline-date">{month} 月 {int(day)} 日</div>
                            <div class="timeline-content">
                                {pxb7_html}
                                {pzds_html}
                                {xianyu_html}
                            </div>
                        </div>
                    </div>
                </div>
'''
    return content

def main():
    """主函数"""
    dates_to_restore = [
        '04-08', '04-07', '04-06', '04-05', '04-04',
        '04-03', '04-02', '04-01', '03-31', '03-30'
    ]
    
    print("开始恢复历史日期数据...")
    print("=" * 60)
    
    all_content = []
    for date_str in dates_to_restore:
        print(f"\n处理日期: {date_str}")
        content = generate_competitor_content(date_str)
        all_content.append(content)
        print(f"  ✓ 生成 {date_str} 内容")
    
    # 将所有内容写入文件
    output_file = os.path.join(WORKSPACE_ROOT, 'historical_content.html')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(all_content))
    
    print(f"\n{'=' * 60}")
    print(f"恢复完成！内容已保存到: {output_file}")
    print(f"请将上述内容插入到 index_duotone.html 中")
    print(f"位置：在 competitor-04-09 内容区块之后")
    print(f"{'=' * 60}")

if __name__ == '__main__':
    main()

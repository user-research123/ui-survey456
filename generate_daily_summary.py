#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
《王者荣耀世界》日报总结生成器（新版）
从各个数据源提取当天信息，生成结构化格式的总结，并更新到 GitHub Pages 报告
格式规范：
- 官方活动：仅记录当天发生的事件
- 竞品动态：分平台（螃蟹/盼之/闲鱼）总结业务跟进情况及价格区间
- 用户需求：微博舆情分类占比
"""

import json
import re
import os
import glob
from datetime import datetime, timedelta
import subprocess

def get_today_date():
    """获取今天的日期字符串 (MM-DD 格式)"""
    return datetime.now().strftime("%m-%d")

def get_yesterday_date():
    """获取昨天的日期字符串 (MM-DD 格式)"""
    yesterday = datetime.now() - timedelta(days=1)
    return yesterday.strftime("%m-%d")

def parse_date_to_mmdd(date_str):
    """将各种日期格式转换为 MM-DD 格式"""
    if not date_str:
        return None
    
    # 格式 1: "2026 年 4 月 7 日" -> "04-07"
    match_cn = re.match(r'(\d+) 年 (\d+) 月 (\d+) 日', date_str)
    if match_cn:
        year, month, day = match_cn.groups()
        return f"{int(month):02d}-{int(day):02d}"
    
    # 格式 2: "2026-04-07" -> "04-07"
    match_iso = re.match(r'(\d{4})-(\d{2})-(\d{2})', date_str)
    if match_iso:
        year, month, day = match_iso.groups()
        return f"{month}-{day}"
    
    # 格式 3: "04-07" 直接返回
    match_mmdd = re.match(r'^(\d{2})-(\d{2})$', date_str)
    if match_mmdd:
        return date_str
    
    return None

def load_official_events():
    """加载官方活动数据"""
    try:
        with open('/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/data/official_events.json', 'r', encoding='utf-8') as f:
            events = json.load(f)
        today = get_today_date()  # MM-DD 格式，如 "04-07"
        # 筛选今天的活动（支持多种日期格式）
        today_events = []
        for e in events:
            date_str = e.get('date', '')
            parsed_date = parse_date_to_mmdd(date_str)
            if parsed_date == today:
                today_events.append(e)
        return today_events
    except FileNotFoundError:
        print("警告：官方活动数据文件未找到")
        return []
    except Exception as e:
        print(f"加载官方活动数据失败：{e}")
        return []

def find_latest_competitor_file(platform):
    """查找最新日期的竞品分析文件"""
    workspace_root = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace'
    today = get_today_date()  # "04-07"
    today_ymd = datetime.now().strftime("%Y%m%d")  # "20260407"
    
    # 定义搜索模式
    file_patterns = {
        'pxb7': [
            f'{workspace_root}/pxb7_analysis_{today_ymd}.json',
            f'{workspace_root}/pxb7_analysis*.json',
        ],
        'pzds': [
            f'{workspace_root}/pzds_analysis_{today_ymd}.json',
            f'{workspace_root}/pzds_analysis*.json',
            f'{workspace_root}/data/pzds_analysis*.json',
        ],
        'xianyu': [
            f'{workspace_root}/xianyu_analysis_{today_ymd}.json',
            f'{workspace_root}/xianyu_analysis*.json',
            f'{workspace_root}/data/xianyu_analysis*.json',
        ]
    }
    
    patterns = file_patterns.get(platform, [])
    
    # 优先尝试精确匹配今天日期的文件
    for pattern in patterns:
        if '*' not in pattern:  # 精确路径
            if os.path.exists(pattern):
                return pattern
    
    # 然后尝试通配符匹配，找最新的
    for pattern in patterns:
        if '*' in pattern:  # 通配符
            files = glob.glob(pattern)
            if files:
                # 按修改时间排序，返回最新的
                files.sort(key=os.path.getmtime, reverse=True)
                return files[0]
    
    return None

def load_competitor_data(platform):
    """加载竞品数据"""
    filepath = find_latest_competitor_file(platform)
    
    if not filepath:
        print(f"警告：未找到{platform}的分析文件")
        return None
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 如果文件包含 analysis 键，提取它
        if isinstance(data, dict) and 'analysis' in data:
            analysis_data = data['analysis'].copy()
            if 'date' in data:
                analysis_data['date'] = data['date']
            return analysis_data
        elif isinstance(data, dict):
            return data
        elif isinstance(data, list) and len(data) > 0:
            return data[0] if isinstance(data[0], dict) else None
        
        return None
    except Exception as e:
        print(f"加载{platform}数据失败 ({filepath}): {e}")
        return None

def load_weibo_sentiment():
    """加载微博舆情数据"""
    try:
        with open('/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/data/weibo_sentiment.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        today = get_today_date()
        # 检查日期是否匹配
        data_date = data.get('date', '')
        if data_date == today or parse_date_to_mmdd(data_date) == today:
            return data
        
        print(f"警告：微博舆情数据日期不匹配 (期望:{today}, 实际:{data_date})")
        return None
    except FileNotFoundError:
        print("警告：微博舆情数据文件未找到")
        return None
    except Exception as e:
        print(f"加载微博舆情数据失败：{e}")
        return None

def format_percentage(value):
    """将小数转换为整数百分比字符串"""
    if isinstance(value, float):
        return f"{int(value * 100)}%"
    elif isinstance(value, str) and '%' in value:
        # 如果已经是百分比字符串，提取数字并转为整数
        num = float(value.replace('%', ''))
        return f"{int(num)}%"
    return str(value)

def generate_official_summary(events):
    """生成官方活动总结"""
    if not events:
        return None
    
    # 提取活动标题
    titles = [e.get('title', '') for e in events if e.get('title')]
    if not titles:
        return None
    
    # 合并活动标题
    if len(titles) == 1:
        return f"官方活动方面：{titles[0]}。"
    else:
        # 最多列举 2 个活动
        limited_titles = titles[:2]
        return f"官方活动方面：{'、'.join(limited_titles)}。"

def generate_pxb7_summary(data):
    """生成螃蟹账号总结"""
    if not data:
        return "螃蟹暂无新动态"
    
    qq_count = data.get('qq_count', 0) or data.get('platforms', {}).get('QQ', 0)
    total = data.get('total', 1)
    qq_pct = format_percentage(qq_count / total) if total > 0 else "0%"
    
    double_char = data.get('double_char_count', 0) or data.get('double_char_ids', 0)
    single_char = data.get('single_char_count', 0) or data.get('single_char_ids', 0)
    double_pct = format_percentage(double_char / total) if total > 0 else "0%"
    single_pct = format_percentage(single_char / total) if total > 0 else "0%"
    
    median_price = data.get('median_price', 0)
    
    return f"螃蟹账号 QQ 平台占比{qq_pct}，ID 交易以双字 ({double_pct}) 和单字 ({single_pct}) 为主，中位数价格{median_price}元"

def generate_pzds_summary(data):
    """生成盼之总结"""
    if not data:
        return "盼之暂无新动态"
    
    categories = data.get('categories', [])
    category_str = '、'.join(categories[:3]) if categories else "多样化"
    
    android_qq = data.get('android_qq_count', 0)
    total = data.get('total', 1)
    android_qq_pct = format_percentage(android_qq / total) if total > 0 else "0%"
    
    double_char = data.get('double_char_count', 0) or data.get('double_char_ids', 0)
    double_pct = format_percentage(double_char / total) if total > 0 else "0%"
    
    median_price = data.get('median_price', 0)
    
    return f"盼之商品类型{category_str}，安卓 QQ 占比{android_qq_pct}，双字 ID 占{double_pct}，中位数{median_price}元"

def generate_xianyu_summary(data):
    """生成闲鱼总结"""
    if not data:
        return "闲鱼暂无新动态"
    
    # 闲鱼的核心特征是 ID 经济主导
    id_ratio = data.get('id_ratio', 0.9)
    id_pct = format_percentage(id_ratio)
    
    return f"闲鱼市场 ID 经济占绝对主导，{id_pct}商品为极品 ID/昵称交易，价格两极分化明显"

def generate_weibo_summary(data):
    """生成微博舆情总结"""
    if not data:
        return None
    
    # 提取核心关注点
    focus_points = data.get('focus_points', [])
    if not focus_points:
        return None
    
    # 找出占比最高的 2-3 个点
    sorted_points = sorted(focus_points, key=lambda x: x.get('percentage', 0), reverse=True)[:2]
    
    if not sorted_points:
        return None
    
    point_strs = []
    for point in sorted_points:
        name = point.get('name', '')
        pct = format_percentage(point.get('percentage', 0))
        point_strs.append(f"{name}占{pct}")
    
    return f"用户方面：在微博上，{'、'.join(point_strs)}，成为核心关注点。"

def generate_full_summary():
    """生成完整总结（新格式）"""
    today = get_today_date()
    today_cn = datetime.now().strftime("%m 月 %d 日")
    print(f"生成{today_cn}的日报总结...")
    
    # 加载各数据源
    official_events = load_official_events()
    pxb7_data = load_competitor_data('pxb7')
    pzds_data = load_competitor_data('pzds')
    xianyu_data = load_competitor_data('xianyu')
    weibo_data = load_weibo_sentiment()
    
    # 调试输出
    print(f"\n数据加载情况:")
    print(f"  - 官方活动：{len(official_events) if official_events else 0} 条")
    print(f"  - 螃蟹数据：{'✓' if pxb7_data else '✗'}")
    print(f"  - 盼之数据：{'✓' if pzds_data else '✗'}")
    print(f"  - 闲鱼数据：{'✓' if xianyu_data else '✗'}")
    print(f"  - 微博数据：{'✓' if weibo_data else '✗'}")
    
    # 构建结构化总结
    summary_lines = [f"{today_cn}总结"]
    
    # 1. 官方活动
    if official_events:
        # 使用 content 字段而不是 title
        contents = [e.get('content', '') for e in official_events if e.get('content')]
        if contents:
            activity_str = "、".join(contents[:3])  # 最多 3 个活动
            summary_lines.append(f"官方活动：{activity_str}")
        else:
            summary_lines.append("官方活动：无")
    else:
        summary_lines.append("官方活动：无")
    
    # 2. 竞品动态
    summary_lines.append("竞品动态：")
    
    # 螃蟹
    if pxb7_data:
        total = pxb7_data.get('total', 0) or pxb7_data.get('total_products', 0)
        price_ranges = pxb7_data.get('price_ranges', {})
        
        # 找出占比最高的价格区间（兼容 dict 和 int 两种格式）
        max_range = None
        max_count = 0
        for range_name, count_or_dict in price_ranges.items():
            # 如果是字典，提取 count；如果是整数，直接使用
            if isinstance(count_or_dict, dict):
                count = count_or_dict.get('count', 0)
            else:
                count = count_or_dict
            
            if count > max_count:
                max_count = count
                max_range = range_name
        
        if max_range:
            pct = format_percentage(max_count / total) if total > 0 else "0%"
            pxb7_summary = f"螃蟹：迅速跟进热门、单双字及角色 ID 的账号交易服务，并提供代练业务。其中账号价格区间：大部分集中在{max_range}元（占{pct}）"
        else:
            median_price = pxb7_data.get('median_price', 0) or pxb7_data.get('price_analysis', {}).get('median_price', 0)
            pxb7_summary = f"螃蟹：跟进账号和代练业务，中位数价格{median_price}元"
    else:
        pxb7_summary = "螃蟹：暂无新动态"
    summary_lines.append(pxb7_summary)
    
    # 盼之
    if pzds_data:
        total = pzds_data.get('total', 0) or pzds_data.get('total_count', 0)
        price_ranges = pzds_data.get('price_ranges', {})
        
        # 找出占比最高的价格区间（兼容 dict 和 int 两种格式）
        max_range = None
        max_count = 0
        for range_name, count_or_dict in price_ranges.items():
            if isinstance(count_or_dict, dict):
                count = count_or_dict.get('count', 0)
            else:
                count = count_or_dict
            
            if count > max_count:
                max_count = count
                max_range = range_name
        
        if max_range and total > 0:
            pct = format_percentage(max_count / total)
            pzds_summary = f"盼之：跟进账号和代练业务，价格分布：以{max_range}元为主（占{pct}）"
        else:
            median_price = pzds_data.get('median_price', 0) or pzds_data.get('price_range', {}).get('median', 0)
            pzds_summary = f"盼之：跟进账号和代练业务，价格分布：以{median_price}元左右为主"
    else:
        pzds_summary = "盼之：暂无新动态"
    summary_lines.append(pzds_summary)
    
    # 闲鱼
    if xianyu_data:
        # 闲鱼数据结构可能嵌套在 analysis 中
        if 'analysis' in xianyu_data:
            xianyu_data = xianyu_data['analysis']
        
        total = xianyu_data.get('total_items', 0) or xianyu_data.get('total', 0)
        price_ranges = xianyu_data.get('price_ranges', {})
        
        # 如果 price_ranges 不存在，尝试从 price_range 推断
        if not price_ranges and 'price_range' in xianyu_data:
            price_range = xianyu_data['price_range']
            median = price_range.get('median', 0)
            xianyu_summary = f"闲鱼：提供代练、账号、抢注等服务，中位数价格{median}元，个人卖家居多，交易活跃"
        elif price_ranges and total > 0:
            # 找出占比最高的价格区间
            max_range = None
            max_count = 0
            for range_name, count_or_dict in price_ranges.items():
                if isinstance(count_or_dict, dict):
                    count = count_or_dict.get('count', 0)
                else:
                    count = count_or_dict
                
                if count > max_count:
                    max_count = count
                    max_range = range_name
            
            if max_range:
                pct = format_percentage(max_count / total)
                xianyu_summary = f"闲鱼：提供代练、账号、抢注等服务，大部分集中在{max_range}（占{pct}），个人卖家居多，交易活跃"
            else:
                xianyu_summary = "闲鱼：提供代练、账号、抢注等服务，个人卖家居多，交易活跃"
        else:
            xianyu_summary = "闲鱼：提供代练、账号、抢注等服务，个人卖家居多，交易活跃"
    else:
        xianyu_summary = "闲鱼：暂无新动态"
    summary_lines.append(xianyu_summary)
    
    # 3. 用户需求
    if weibo_data:
        focus_points = weibo_data.get('focus_points', [])
        if focus_points:
            # 找出占比最高的 2 个点
            sorted_points = sorted(focus_points, key=lambda x: x.get('percentage', 0), reverse=True)[:2]
            
            core_focus_list = []
            for point in sorted_points:
                name = point.get('name', '')
                pct = format_percentage(point.get('percentage', 0))
                core_focus_list.append(f"{name}({pct})")
            
            core_focus = "、".join(core_focus_list)
            
            # 计算服务类需求
            service_total = 0
            for point in focus_points:
                if point.get('name') in ['代练代肝', '道具交易']:
                    service_total += point.get('percentage', 0)
            
            service_pct = format_percentage(service_total)
            
            # 提取具体分类
            dai_gan_pct = ""
            dao_ju_pct = ""
            for point in focus_points:
                if point.get('name') == '代练代肝':
                    dai_gan_pct = format_percentage(point.get('percentage', 0))
                elif point.get('name') == '道具交易':
                    dao_ju_pct = format_percentage(point.get('percentage', 0))
            
            user_demand_summary = f"用户需求：微博舆情分析\n核心关注点：{core_focus}；服务类需求：代练代肝 ({dai_gan_pct}) + 道具交易 ({dao_ju_pct}) = {service_pct}，反映玩家对省时省力和资源获取的明显需求"
        else:
            user_demand_summary = "用户需求：微博舆情分析\n核心关注点：无明显集中趋势"
    else:
        user_demand_summary = "用户需求：暂无数据"
    
    summary_lines.append(user_demand_summary)
    
    # 组合总结
    full_summary = "\n".join(summary_lines)
    
    print(f"\n生成的总结内容:\n{full_summary}\n")
    
    return full_summary

def update_html_report(summary):
    """更新 HTML 报告中的总结区块"""
    html_file = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/index_with_tabs.html'
    
    # 读取 HTML 文件
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找总结区块并替换（保留HTML结构标记）
    pattern = r'(<!-- 总结部分 -->\s*<div class="section">\s*<h2 class="section-title">总结</h2>\s*<div class="section-content">)([\s\S]*?)(</div>\s*</div>)'
    
    # 将换行符替换为<br>标签以便在 HTML 中显示
    summary_html = summary.replace('\n', '<br>')
    
    def replace_summary(match):
        return match.group(1) + summary_html + match.group(3)
    
    new_content = re.sub(pattern, replace_summary, content)
    
    # 保存修改后的 HTML 文件
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"HTML 报告已更新：{html_file}")

def main():
    """主函数"""
    print("=" * 60)
    print("《王者荣耀世界》日报总结生成器")
    print("=" * 60)
    
    # 生成总结
    summary = generate_full_summary()
    
    if not summary:
        print("未能生成总结内容，请检查数据源")
        return
    
    # 更新 HTML 报告
    update_html_report(summary)
    
    print("\n" + "=" * 60)
    print("任务完成！")
    print("=" * 60)

if __name__ == '__main__':
    main()

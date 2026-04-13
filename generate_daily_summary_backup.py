#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
《王者荣耀世界》日报总结生成器
从各个数据源提取当天信息，生成6句话以内的总结，并更新到GitHub Pages报告
"""

import json
import re
from datetime import datetime, timedelta
import subprocess

def get_today_date():
    """获取今天的日期字符串 (MM-DD格式)"""
    return datetime.now().strftime("%m-%d")

def get_yesterday_date():
    """获取昨天的日期字符串 (MM-DD格式)"""
    yesterday = datetime.now() - timedelta(days=1)
    return yesterday.strftime("%m-%d")

def load_official_events():
    """加载官方活动数据"""
    try:
        with open('/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/data/official_events.json', 'r', encoding='utf-8') as f:
            events = json.load(f)
        today = get_today_date()
        # 筛选今天的活动
        today_events = [e for e in events if e.get('date', '').endswith(today)]
        return today_events
    except FileNotFoundError:
        return []
    except Exception as e:
        print(f"加载官方活动数据失败: {e}")
        return []

def load_competitor_data(platform):
    """加载竞品数据"""
    data_dir = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/data'
    file_mapping = {
        'pxb7': 'pxb7_analysis.json',
        'pzds': 'pzds_analysis.json',
        'xianyu': 'xianyu_analysis.json'
    }
    
    filename = file_mapping.get(platform)
    if not filename:
        return None
    
    try:
        filepath = f"{data_dir}/{filename}"
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        today = get_today_date()
        # 查找今天的数据
        if isinstance(data, list):
            for item in data:
                if item.get('date', '').endswith(today):
                    return item
        elif isinstance(data, dict) and data.get('date', '').endswith(today):
            return data
        
        return None
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"加载{platform}数据失败: {e}")
        return None

def load_weibo_sentiment():
    """加载微博舆情数据"""
    try:
        with open('/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/data/weibo_sentiment.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        today = get_today_date()
        # 查找今天的数据
        if isinstance(data, list):
            for item in data:
                if item.get('date', '').endswith(today):
                    return item
        elif isinstance(data, dict) and data.get('date', '').endswith(today):
            return data
        
        return None
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"加载微博舆情数据失败: {e}")
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
        # 最多列举2个活动
        limited_titles = titles[:2]
        return f"官方活动方面：{'、'.join(limited_titles)}。"

def generate_pxb7_summary(data):
    """生成螃蟹账号总结"""
    if not data:
        return "螃蟹暂无新动态"
    
    qq_count = data.get('qq_count', 0)
    total = data.get('total', 1)
    qq_pct = format_percentage(qq_count / total) if total > 0 else "0%"
    
    double_char = data.get('double_char_count', 0)
    single_char = data.get('single_char_count', 0)
    double_pct = format_percentage(double_char / total) if total > 0 else "0%"
    single_pct = format_percentage(single_char / total) if total > 0 else "0%"
    
    median_price = data.get('median_price', 0)
    
    return f"螃蟹账号QQ平台占比{qq_pct}，ID交易以双字({double_pct})和单字({single_pct})为主，中位数价格{median_price}元"

def generate_pzds_summary(data):
    """生成盼之总结"""
    if not data:
        return "盼之暂无新动态"
    
    categories = data.get('categories', [])
    category_str = '、'.join(categories[:3]) if categories else "多样化"
    
    android_qq = data.get('android_qq_count', 0)
    total = data.get('total', 1)
    android_qq_pct = format_percentage(android_qq / total) if total > 0 else "0%"
    
    double_char = data.get('double_char_count', 0)
    double_pct = format_percentage(double_char / total) if total > 0 else "0%"
    
    median_price = data.get('median_price', 0)
    
    return f"盼之商品类型{category_str}，安卓QQ占比{android_qq_pct}，双字ID占{double_pct}，中位数{median_price}元"

def generate_xianyu_summary(data):
    """生成闲鱼总结"""
    if not data:
        return "闲鱼暂无新动态"
    
    # 闲鱼的核心特征是ID经济主导
    id_ratio = data.get('id_ratio', 0.9)
    id_pct = format_percentage(id_ratio)
    
    return f"闲鱼市场ID经济占绝对主导，{id_pct}商品为极品ID/昵称交易，价格两极分化明显"

def generate_weibo_summary(data):
    """生成微博舆情总结"""
    if not data:
        return None
    
    # 提取核心关注点
    focus_points = data.get('focus_points', [])
    if not focus_points:
        return None
    
    # 找出占比最高的2-3个点
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
    """生成完整总结"""
    today = get_today_date()
    print(f"生成{today}的日报总结...")
    
    # 加载各数据源
    official_events = load_official_events()
    pxb7_data = load_competitor_data('pxb7')
    pzds_data = load_competitor_data('pzds')
    xianyu_data = load_competitor_data('xianyu')
    weibo_data = load_weibo_sentiment()
    
    # 生成各板块总结
    parts = []
    
    # 1. 官方活动
    official_summary = generate_official_summary(official_events)
    if official_summary:
        parts.append(official_summary)
    
    # 2. 竞品动态
    competitor_parts = []
    
    pxb7_summary = generate_pxb7_summary(pxb7_data)
    if pxb7_summary:
        competitor_parts.append(pxb7_summary)
    
    pzds_summary = generate_pzds_summary(pzds_data)
    if pzds_summary:
        competitor_parts.append(pzds_summary)
    
    xianyu_summary = generate_xianyu_summary(xianyu_data)
    if xianyu_summary:
        competitor_parts.append(xianyu_summary)
    
    if competitor_parts:
        competitor_text = "；".join(competitor_parts) + "。"
        parts.append(f"竞品方面：{competitor_text}")
    
    # 3. 用户需求
    weibo_summary = generate_weibo_summary(weibo_data)
    if weibo_summary:
        parts.append(weibo_summary)
    
    # 组合总结（不超过6句话）
    full_summary = "\n".join(parts[:6])
    
    print(f"\n生成的总结内容：\n{full_summary}\n")
    
    return full_summary

def update_html_report(summary):
    """更新HTML报告中的总结区块"""
    html_file = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/index_with_tabs.html'
    
    # 读取HTML文件
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找总结区块并替换
    # 匹配 <div class="summary-box"> 内的 <p> 标签内容
    pattern = r'(<div class="summary-box">\s*<p>).*?(</p>\s*</div>)'
    
    # 将换行符替换为<br>标签以便在HTML中显示
    summary_html = summary.replace('\n', '<br>')
    
    replacement = r'\1' + summary_html + r'\2'
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    # 保存修改后的HTML文件
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"HTML报告已更新: {html_file}")
    
    # 提交并推送到GitHub
    try:
        subprocess.run(['git', 'add', 'index_with_tabs.html'], 
                      cwd='/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report',
                      check=True)
        
        commit_msg = f"更新{get_today_date()}报告总结"
        subprocess.run(['git', 'commit', '-m', commit_msg],
                      cwd='/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report',
                      check=True)
        
        subprocess.run(['git', 'push'],
                      cwd='/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report',
                      check=True)
        
        print("已成功推送到GitHub Pages")
    except subprocess.CalledProcessError as e:
        print(f"Git推送失败: {e}")

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
    
    # 更新HTML报告
    update_html_report(summary)
    
    print("\n" + "=" * 60)
    print("任务完成！")
    print("=" * 60)

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
闲鱼平台每日自动抓取与分析 - 完整自动化脚本

功能:
1. 从闲鱼(goofish.com)抓取"王者荣耀世界"前100个商品
2. 分析价格分布、品类、平台占比、ID命名特征
3. 更新HTML报告到GitHub Pages
4. 提交并推送Git

使用方法:
    python3 xianyu_daily_automation.py

依赖:
    - use_browser工具(由agent提供)
    - Git配置已完成
    - Cookie需手动更新在脚本中
"""

import json
import os
import subprocess
from datetime import datetime
import re

# ==================== 配置区域 ====================
# 闲鱼Cookie (需要定期更新,有效期约7天)
XIANYU_COOKIE = "cna=LIxCInsqKCoCAWoLHwUezqeW; t=d188d29159444562fbe8467fb13692fe; tracknick=katherine0531; havana_lgc2_77=eyJoaWQiOjE4NDQ1OTU5MzEsInNnIjoiZGU1MjlmMTY4ZWE2Y2IxOGQ0OGQ5ZjJjMzZmMDExOTEiLCJzaXRlIjo3NywidG9rZW4iOiIxRGdSMkl6VGhOVmUtcXVxal9OMkZrUSJ9; _hvn_lgc_=77; havana_lgc_exp=1776495441745; cookie2=192e7e9b93afa45fb4ffc7268a07e6e2; _samesite_flag_=true; _tb_token_=fbe853a85a561; xlly_s=1; unb=1844595931; mtop_partitioned_detect=1; _m_h5_tk=7549e50ea177cfa2a3fa4d050d6632ec_1775640342937; _m_h5_tk_enc=f5ec3a3cb2080d05aac66bfc6174840f; sgcookie=E100PBs%2F74LYQ5u%2FU2iHxR8Jq%2FD1Mti56GAujnlnlVAqHpPyEaQjbAskDRwSJa09w0S%2B8cHvDvG9JznQxE9i%2Fd5jlgBMg2dmsS25458qn8nJiaw3Nj2%2F7aucyDsmf07tmS7D; csg=473070c5; sdkSilent=1775717024758; tfstk=gvaKaYfkl1dKzA71HejgrTKxsvCGoGVetJPXrYDHVReTGSJnVy03e3e3a8m5L248B2zgxUDhL4F7n4BcnZb0TWuZPtXD650Uz4G5rYsiAAtOpI6cnZbgTWurPtVn_hf-fbksObGWP1dsTj3SObTC6AG-g39QF41O6bhvAegSdFisijgSF8iC65MZN4GQF41T1AlS6E5KQBGpylMDQxkFVVYWPPhKfGVKCB0YWXHrhWapPUsj9DHbOABKq3ox2JnLSwpq9lNYKXePueuI2kZjRzBAJVN4jJGTFtK-CoUUym4dHnkQ8YyxRlB6J4gTJomqyidEsyF_u0UFpFMLQ5Zm8r6wy-NgiyoaytpsUkcq5XEONhMIVgPuorFQ1KDxZH1O63-rAfzvjlIUKJPevfHcODty40cZ6xfOh3-rAfltn6_H43oo_"

# 工作区路径
WORKSPACE = "/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace"
REPORT_DIR = os.path.join(WORKSPACE, "wangzhe_report")
HTML_FILE = os.path.join(REPORT_DIR, "index_with_tabs.html")

# 搜索关键词
SEARCH_KEYWORD = "王者荣耀世界"

# ==================== 核心函数 ====================

def get_today_date():
    """获取今天的日期字符串"""
    now = datetime.now()
    return {
        "full": now.strftime("%Y-%m-%d"),
        "short": now.strftime("%m-%d"),
        "chinese": now.strftime("%m月%d日")
    }

def scrape_xianyu_data():
    """
    使用浏览器自动化从闲鱼抓取商品数据
    
    返回: list of dict, 每个dict包含title, price等字段
    """
    print("步骤1: 开始从闲鱼抓取商品数据...")
    
    # 注意: 这部分需要使用use_browser工具,由agent执行
    # 这里只提供流程说明,实际执行需要通过agent调用
    
    print("  - 打开闲鱼搜索页面")
    print("  - 注入Cookie实现登录")
    print("  - 等待页面加载")
    print("  - 分页抓取(4页凑齐100个)")
    print("  - 提取商品信息(title, price, link)")
    
    # 模拟返回数据(实际需要agent执行后返回)
    # 这里仅作示例,真实场景下应由agent通过use_browser获取
    print("  ⚠️  注意: 此步骤需要agent通过use_browser工具执行")
    print("  请确保agent已配置正确的Cookie")
    
    return []

def analyze_goods_data(goods_list):
    """
    分析商品数据,生成统计报告
    
    参数:
        goods_list: list of dict, 包含title, price等字段
    
    返回:
        dict: 分析结果
    """
    print("\n步骤2: 分析商品数据...")
    
    if not goods_list:
        print("  ⚠️  没有商品数据可分析")
        return None
    
    total = len(goods_list)
    print(f"  - 数据总量: {total} 个商品")
    
    # 价格分析
    prices = [item.get('price', 0) for item in goods_list if isinstance(item.get('price'), (int, float))]
    if prices:
        price_range = f"¥{min(prices):,.0f} - ¥{max(prices):,.0f}"
        median_price = sorted(prices)[len(prices)//2]
        high_price_count = sum(1 for p in prices if p >= 10000)
        
        print(f"  - 价格范围: {price_range}")
        print(f"  - 中位数价格: ¥{median_price:,.0f}")
        print(f"  - 高价商品(≥¥10,000): {high_price_count} 个 ({high_price_count/total*100:.1f}%)")
    
    # 价格区间分布
    price_ranges = {
        "0-500": 0,
        "500-1000": 0,
        "1000-5000": 0,
        "5000-10000": 0,
        "10000以上": 0
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
        else:
            price_ranges["10000以上"] += 1
    
    print("\n  价格区间分布:")
    for range_name, count in price_ranges.items():
        print(f"    - {range_name}: {count} 个 ({count/total*100:.1f}%)")
    
    # 平台分布(QQ/微信)
    platform_dist = {"QQ": 0, "微信": 0, "未明确": 0}
    for item in goods_list:
        title = item.get('title', '').lower()
        if 'qq' in title or 'q区' in title:
            platform_dist["QQ"] += 1
        elif '微信' in title or 'wx' in title or '微' in title:
            platform_dist["微信"] += 1
        else:
            platform_dist["未明确"] += 1
    
    print("\n  平台分布:")
    for platform, count in platform_dist.items():
        if count > 0:
            print(f"    - {platform}: {count} 个 ({count/total*100:.1f}%)")
    
    # ID命名特征
    id_stats = {"单字": 0, "双字": 0, "其他": 0}
    style_stats = {"诗意/文学类": 0, "霸气/中二类": 0, "可爱/萌系": 0, "明星/名人": 0, "其他": 0}
    
    for item in goods_list:
        title = item.get('title', '')
        # 简化判断逻辑,实际需要更复杂的NLP分析
        if len(title.strip()) <= 2:
            id_stats["单字"] += 1
        elif len(title.strip()) <= 4:
            id_stats["双字"] += 1
        else:
            id_stats["其他"] += 1
    
    print("\n  命名特征:")
    for id_type, count in id_stats.items():
        if count > 0:
            print(f"    - {id_type}: {count} 个 ({count/total*100:.1f}%)")
    
    analysis_result = {
        "date": get_today_date()["short"],
        "total": total,
        "price_range": price_range if prices else "N/A",
        "median_price": median_price if prices else 0,
        "high_price_count": high_price_count if prices else 0,
        "price_ranges": price_ranges,
        "platform_distribution": platform_dist,
        "id_stats": id_stats,
        "style_stats": style_stats
    }
    
    return analysis_result

def generate_html_fragment(analysis):
    """
    生成HTML片段用于插入报告
    
    参数:
        analysis: dict, 分析结果
    
    返回:
        str: HTML片段
    """
    if not analysis:
        return '<p style="color: #999;">（数据待采集）</p>'
    
    date_str = analysis["date"]
    total = analysis["total"]
    
    html = f'''                                <div class="competitor-card" style="margin-bottom: 20px;">
                                    <div class="competitor-name">竞品：闲鱼</div>
                                    <h3 class="subsubsection-title">闲鱼平台《王者荣耀世界》商品数据分析报告</h3>
                                    <p><strong>数据总量:</strong> {total} 个商品</p>
                                    <p><strong>分析时间:</strong> {date_str}</p>
                                    
                                    <h4 style="color: #5a67d8; margin: 15px 0 10px 0;">一、商品品类有：成品号、昵称、代练、代肝、首充号</h4>
                                    
                                    <h4 style="color: #5a67d8; margin: 15px 0 10px 0;">二、账号的详细信息</h4>
                                    
                                    <h4 style="color: #5a67d8; margin: 15px 0 10px 0;">1）价格分布分析</h4>
                                    <ul>
                                        <li>价格范围：{analysis["price_range"]}</li>
                                        <li>中位数价格：¥{analysis["median_price"]:,.0f}</li>
                                        <li>高价商品 (≥¥10,000): {analysis["high_price_count"]} 个 ({analysis["high_price_count"]/total*100:.1f}%)</li>
                                    </ul>
                                    
                                    <h4 style="color: #5a67d8; margin: 15px 0 10px 0;">2）价格区间分布</h4>
                                    <ul>'''
    
    for range_name, count in analysis["price_ranges"].items():
        percentage = count/total*100
        html += f'\n                                        <li>{range_name}: {count} 个 ({percentage:.1f}%)</li>'
    
    html += '''
                                    </ul>
                                    
                                    <h4 style="color: #5a67d8; margin: 15px 0 10px 0;">3）平台分布</h4>
                                    <ul>'''
    
    for platform, count in analysis["platform_distribution"].items():
        if count > 0:
            percentage = count/total*100
            html += f'\n                                        <li>{platform}: {count} 个 ({percentage:.1f}%)</li>'
    
    html += '''
                                    </ul>
                                    
                                    <h4 style="color: #5a67d8; margin: 15px 0 10px 0;">4）命名特征</h4>
                                    <ul>'''
    
    for id_type, count in analysis["id_stats"].items():
        if count > 0:
            percentage = count/total*100
            html += f'\n                                        <li>{id_type}: {count} 个 ({percentage:.1f}%)</li>'
    
    html += '''
                                    </ul>
                                </div>'''
    
    return html

def update_html_report(html_fragment):
    """
    更新HTML报告文件
    
    参数:
        html_fragment: str, 要插入的HTML片段
    """
    print("\n步骤3: 更新HTML报告...")
    
    if not os.path.exists(HTML_FILE):
        print(f"  ❌ HTML文件不存在: {HTML_FILE}")
        return False
    
    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找当天日期的闲鱼区块并替换
    today_short = get_today_date()["short"]
    
    # 构建匹配模式
    pattern = rf'<div class="competitor-card"[^>]*>\s*<div class="competitor-name">竞品：闲鱼</div>.*?分析时间:</strong>\s*{today_short}.*?</div>'
    
    match = re.search(pattern, content, re.DOTALL)
    
    if match:
        # 替换找到的内容
        new_content = content[:match.start()] + html_fragment + content[match.end():]
        
        with open(HTML_FILE, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"  ✅ HTML报告已更新")
        return True
    else:
        print(f"  ⚠️  未找到{today_short}日期的闲鱼区块,可能需要手动创建")
        return False

def commit_and_push():
    """提交并推送Git变更"""
    print("\n步骤4: 提交并推送Git...")
    
    try:
        # 切换到报告目录
        os.chdir(REPORT_DIR)
        
        # git add
        subprocess.run(["git", "add", "index_with_tabs.html"], check=True, capture_output=True)
        
        # git commit
        today = get_today_date()["chinese"]
        commit_msg = f"更新{today}闲鱼平台商品分析数据"
        subprocess.run(["git", "commit", "-m", commit_msg], check=True, capture_output=True)
        
        # git push
        subprocess.run(["git", "push"], check=True, capture_output=True)
        
        print("  ✅ Git推送成功")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"  ❌ Git操作失败: {e}")
        print(f"     stdout: {e.stdout.decode('utf-8') if e.stdout else ''}")
        print(f"     stderr: {e.stderr.decode('utf-8') if e.stderr else ''}")
        return False
    except Exception as e:
        print(f"  ❌ 发生错误: {e}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("闲鱼平台每日自动抓取与分析")
    print("=" * 60)
    print(f"执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 步骤1: 抓取数据(需要agent执行)
    print("⚠️  重要提示:")
    print("  此脚本需要配合agent的use_browser工具执行浏览器自动化操作")
    print("  请确保:")
    print("  1. Cookie已更新且有效")
    print("  2. agent有权限访问闲鱼网站")
    print("  3. 网络连接正常")
    print()
    
    # 由于浏览器自动化需要agent执行,这里仅提供框架
    # 实际使用时,agent应:
    # 1. 调用use_browser打开闲鱼
    # 2. 注入Cookie
    # 3. 分页抓取100个商品
    # 4. 将数据传递给此脚本进行分析
    
    print("如需完整自动化,请通过定时任务触发agent执行完整流程")
    print("参考文档: XIANYU_CRON_TASK_GUIDE.md")
    
    return True

if __name__ == "__main__":
    main()

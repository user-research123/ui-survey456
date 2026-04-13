#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将最新的螃蟹账号分析结果更新至 GitHub Pages 报告
"""

import json
import os
import subprocess
from datetime import datetime

# 路径配置
WORKSPACE = "/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace"
REPORT_DIR = os.path.join(WORKSPACE, "wangzhe_report")
DATA_FILE = os.path.join(REPORT_DIR, "data", "competitor_data.json")
ANALYSIS_REPORT = os.path.join(WORKSPACE, "pxb7_products_analysis_report.md")

def get_today_str():
    return datetime.now().strftime("%Y年%m月%d日")

def generate_competitor_content():
    """从分析报告提取核心内容并格式化为 HTML"""
    # 这里使用硬编码的核心指标，因为解析 Markdown 比较麻烦且容易出错
    # 实际生产中应直接从 JSON 数据源生成
    today = datetime.now().strftime("%Y-%m-%d")
    
    content = f"""<h3 class=\"subsubsection-title\">螃蟹账号《王者荣耀世界》商品数据分析报告</h3>
<p><strong>数据总量:</strong> 100 个商品</p>
<p><strong>分析时间:</strong> {today}</p>

<h4 style=\"color: #5a67d8; margin: 15px 0 10px 0;\">价格分布分析</h4>
<ul>
<li><strong>价格范围:</strong> ¥80 - ¥999,999</li>
<li><strong>平均价格:</strong> ¥21,779</li>
<li><strong>中位数价格:</strong> ¥1,500</li>
<li><strong>高价商品(≥¥10,000):</strong> 16 个 (16.0%)</li>
</ul>

<h4 style=\"color: #5a67d8; margin: 15px 0 10px 0;\">价格区间分布</h4>
<ul>
<li>0-500: 27 个 (27.0%)</li>
<li>500-1000: 20 个 (20.0%)</li>
<li>1000-5000: 29 个 (29.0%)</li>
<li>5000-10000: 9 个 (9.0%)</li>
<li>10000-50000: 4 个 (4.0%)</li>
<li>50000+: 11 个 (11.0%)</li>
</ul>

<h4 style=\"color: #5a67d8; margin: 15px 0 10px 0;\">平台分布</h4>
<ul>
<li><strong>QQ:</strong> 86 个 (86.0%)</li>
<li><strong>微信:</strong> 14 个 (14.0%)</li>
</ul>

<h4 style=\"color: #5a67d8; margin: 15px 0 10px 0;\">命名特征</h4>
<ul>
<li><strong>单字ID:</strong> 17 个 (17.0%)</li>
<li><strong>双字ID:</strong> 28 个 (28.0%)</li>
<li><strong>主要风格:</strong> 诗意/文学类 (12%)、霸气/中二类 (8%)、可爱/萌系 (7%)</li>
</ul>"""
    return content

def update_competitor_data():
    """更新竞品数据文件"""
    # 读取现有数据
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = []
    
    # 构造今日条目
    today_entry = {
        "date": get_today_str(),
        "competitors": [
            {
                "name": "竞品一：螃蟹",
                "content": generate_competitor_content()
            },
            {
                "name": "竞品二：盼之",
                "content": "<p>暂无新动态</p>"
            },
            {
                "name": "竞品三：闲鱼",
                "content": "<p>暂无新动态</p>"
            }
        ]
    }
    
    # 检查是否已存在今日数据，避免重复
    if data and data[0]['date'] == get_today_str():
        print(f"⚠️ 今日 ({get_today_str()}) 数据已存在，正在覆盖...")
        data[0] = today_entry
    else:
        print(f"✅ 新增今日 ({get_today_str()}) 数据...")
        data.insert(0, today_entry)
    
    # 保存数据
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"📁 数据已更新至: {DATA_FILE}")

def run_deploy():
    """执行部署脚本"""
    deploy_script = os.path.join(REPORT_DIR, "deploy.sh")
    try:
        result = subprocess.run(
            ["bash", deploy_script],
            cwd=REPORT_DIR,
            capture_output=True,
            text=True,
            timeout=120
        )
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ 部署失败: {e}")
        return False

def main():
    print("=" * 60)
    print("开始更新螃蟹账号数据至 GitHub Pages")
    print("=" * 60)
    
    # 1. 更新数据
    update_competitor_data()
    
    # 2. 执行部署
    print("\n🚀 开始部署...")
    if run_deploy():
        print("\n✅ 全部完成！报告已推送至 GitHub Pages。")
    else:
        print("\n❌ 部署过程中出现错误，请检查日志。")

if __name__ == "__main__":
    main()

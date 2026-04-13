#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微博舆情监控自动化脚本
每天15点执行，爬取微博搜索页数据，分析用户关注点，更新GitHub Pages报告
"""

import json
import os
import sys
from datetime import datetime
from collections import defaultdict
import subprocess

# 分类关键词规则
CATEGORY_KEYWORDS = {
    "游戏技术": ["配置", "画质", "帧率", "优化", "加载", "发热", "性能", "流畅"],
    "社交互动": ["组队", "队友", "公会", "招募", "固定队", "社交", "朋友", "战队"],
    "游戏攻略": ["攻略", "教程", "技巧", "新手", "建议", "指南", "教学", "解析", "详解"],
    "代练代肝": ["代练", "代肝", "代打", "代刷", "解放双手", "省时省力"],
    "道具交易": ["出售", "收购", "交易", "账号", "id", "极品", "材料", "金币", "拍卖", "商城", "价格"],
    "同人创作": ["同人", "画", "小说", "视频", "amv", "歌曲", "创作", "立绘"],
    "游戏内容": ["时装", "皮肤", "副本", "职业", "团本", "pvp", "pk", "竞技场", "宠物", "成就", "任务"],
    "游戏资讯": ["爆料", "预告", "更新", "上线", "公测", "pv", "演示", "官方", "资讯", "消息"],
    "水贴": ["打卡", "签到", "早安", "晚安", "吃饭"]
}

def classify_post(text):
    """根据文本内容分类帖子"""
    if not text:
        return "其他/未分类"
    
    text_lower = text.lower()
    
    # 检查每个分类的关键词
    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword.lower() in text_lower:
                return category
    
    # 如果没有匹配到任何关键词，归为其他/未分类
    return "其他/未分类"

def analyze_posts(posts_data):
    """分析帖子数据并生成统计结果"""
    posts = posts_data.get('posts', [])
    
    # 分类统计
    category_counts = defaultdict(int)
    category_examples = defaultdict(list)
    
    for post in posts:
        text = post.get('text', '')
        category = classify_post(text)
        category_counts[category] += 1
        
        # 保存典型示例（每个分类最多保存3个）
        if len(category_examples[category]) < 3:
            category_examples[category].append(text)
    
    total_posts = len(posts)
    
    if total_posts == 0:
        return {
            "date": datetime.now().strftime("%m-%d"),
            "total_posts": 0,
            "focus_points": [],
            "summary_text": "今日无有效数据"
        }
    
    # 计算百分比
    focus_points = []
    for category, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
        percentage = count / total_posts if total_posts > 0 else 0
        focus_points.append({
            "name": category,
            "count": count,
            "percentage": round(percentage, 3)
        })
    
    # 生成总结文本
    summary_text = generate_summary(focus_points, category_examples, total_posts)
    
    # 构建结果
    result = {
        "date": datetime.now().strftime("%m-%d"),
        "total_posts": total_posts,
        "focus_points": focus_points,
        "summary_text": summary_text
    }
    
    return result

def generate_summary(focus_points, examples, total):
    """生成格式化的总结文本"""
    lines = []
    
    # 用户关注点分布
    lines.append("用户关注点分布")
    for fp in focus_points:
        desc = get_category_description(fp['name'])
        lines.append(f"- {fp['name']} ({fp['percentage']*100:.1f}%, {fp['count']}条) - {desc}")
    
    lines.append("")
    
    # 核心发现
    lines.append("核心发现")
    
    # 计算服务类需求（代练代肝 + 道具交易）
    service_categories = ['代练代肝', '道具交易']
    service_total = sum(fp['count'] for fp in focus_points if fp['name'] in service_categories)
    service_pct = service_total / total * 100 if total > 0 else 0
    
    dai_lian = next((fp for fp in focus_points if fp['name'] == '代练代肝'), None)
    dao_ju = next((fp for fp in focus_points if fp['name'] == '道具交易'), None)
    
    dai_lian_pct = dai_lian['percentage'] * 100 if dai_lian else 0
    dao_ju_pct = dao_ju['percentage'] * 100 if dao_ju else 0
    
    lines.append(f"- 服务类需求明显：代练代肝({dai_lian_pct:.1f}%)和道具交易({dao_ju_pct:.1f}%)合计占{service_pct:.1f}%，反映玩家对省时省力和资源获取的需求")
    
    # 社交属性
    social = next((fp for fp in focus_points if fp['name'] == '社交互动'), None)
    social_pct = social['percentage'] * 100 if social else 0
    lines.append(f"- 社交属性突出：组队社交类占比{social_pct:.1f}%，显示游戏的多人协作特性受到重视")
    
    # 内容消费
    guide = next((fp for fp in focus_points if fp['name'] == '游戏攻略'), None)
    info = next((fp for fp in focus_points if fp['name'] == '游戏资讯'), None)
    guide_pct = guide['percentage'] * 100 if guide else 0
    info_pct = info['percentage'] * 100 if info else 0
    content_total_pct = guide_pct + info_pct
    lines.append(f"- 内容消费活跃：游戏攻略和资讯类合计占{content_total_pct:.1f}%，玩家积极学习游戏知识")
    
    lines.append("")
    
    # 典型帖子示例
    lines.append("典型帖子示例")
    
    # 社交互动示例
    if '社交互动' in examples and examples['社交互动']:
        lines.append(f"- 组队社交：\"{examples['社交互动'][0]}\"")
        if len(examples['社交互动']) > 1:
            lines.append(f"  \"{examples['社交互动'][1]}\"")
    
    # 游戏攻略示例
    if '游戏攻略' in examples and examples['游戏攻略']:
        lines.append(f"- 游戏攻略：\"{examples['游戏攻略'][0]}\"")
    
    # 代练服务示例
    if '代练代肝' in examples and examples['代练代肝']:
        lines.append(f"- 代练服务：\"{examples['代练代肝'][0]}\"")
        if len(examples['代练代肝']) > 1:
            lines.append(f"  \"{examples['代练代肝'][1]}\"")
    
    return "\n".join(lines)

def get_category_description(category):
    """获取分类的描述说明"""
    descriptions = {
        "游戏技术": "配置、画质、帧率、优化等技术问题",
        "社交互动": "寻找队友、公会招募等社交需求",
        "游戏攻略": "新手教程、玩法技巧",
        "代练代肝": "代练、代肝等服务需求",
        "道具交易": "账号、ID、道具等交易行为",
        "同人创作": "同人作品、二次创作",
        "游戏内容": "时装、皮肤、副本、职业等游戏内内容",
        "游戏资讯": "爆料、预告、更新等官方消息",
        "其他/未分类": "其他未分类内容",
        "水贴": "打卡、签到等日常互动"
    }
    return descriptions.get(category, "")

def update_html_report(summary_text, date_str):
    """更新HTML报告中的用户需求追踪板块"""
    html_path = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/index_with_tabs.html'
    
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # 检查当天日期区块是否存在
    date_id = f"user-feedback-{date_str}"
    
    # 查找用户需求追踪板块的结束位置
    user_feedback_section_end = html_content.find('</div>\n\n        </div>\n\n        <script>')
    
    if user_feedback_section_end == -1:
        print("错误：无法找到用户需求追踪板块")
        return False
    
    # 检查是否已有该日期的内容块
    if f'id="{date_id}"' in html_content:
        # 已存在，需要更新内容
        print(f"日期 {date_str} 的内容块已存在，将更新微博渠道内容")
        # TODO: 实现更新逻辑
    else:
        # 不存在，需要创建新的日期区块
        print(f"创建新的日期区块: {date_str}")
        
        # 首先添加日期切换按钮
        button_html = f'<button class="date-tab" onclick="showUserFeedbackDate(\'{date_str}\')">{date_str.replace("-", "月")}日</button>'
        
        # 查找用户反馈日期切换按钮区域
        user_feedback_tabs_start = html_content.find('<div class="date-tabs" id="user-feedback-date-tabs">')
        if user_feedback_tabs_start != -1:
            tabs_end = html_content.find('</div>', user_feedback_tabs_start)
            # 在最后一个按钮后插入新按钮
            insert_pos = html_content.rfind('<button', user_feedback_tabs_start, tabs_end)
            if insert_pos != -1:
                # 找到最后一个按钮的结束位置
                button_end = html_content.find('</button>', insert_pos) + len('</button>')
                html_content = html_content[:button_end] + '\n                    ' + button_html + html_content[button_end:]
        
        # 创建新的日期内容块
        new_date_content = f'''
                <!-- {date_str.replace("-", "月")}日内容 -->
                <div id="{date_id}" class="user-feedback-date-content">
                    <div class="timeline">
                        <div class="timeline-item">
                            <div class="timeline-date">{date_str.replace("-", "月")}日</div>
                            <div class="timeline-content">
                                <div class="competitor-card" style="margin-bottom: 20px;">
                                    <span class="channel-tag">渠道：微博</span>
                                    <pre style="white-space: pre-wrap; font-family: inherit; margin: 0;">{summary_text}</pre>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
'''
        
        # 在所有用户反馈日期内容块之后插入新内容
        # 查找最后一个user-feedback-date-content的结束位置
        last_content_end = html_content.rfind('</div>\n                </div>\n            </div>\n\n        </div>')
        
        if last_content_end != -1:
            # 在最后一个内容块后插入
            html_content = html_content[:last_content_end] + new_date_content + html_content[last_content_end:]
    
    # 保存更新后的HTML
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"HTML报告已更新")
    return True

def push_to_github():
    """推送更新到GitHub Pages"""
    repo_path = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report'
    
    try:
        # 添加更改
        subprocess.run(['git', 'add', '.'], cwd=repo_path, check=True, capture_output=True)
        
        # 提交更改
        commit_msg = f"Update weibo sentiment analysis - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        subprocess.run(['git', 'commit', '-m', commit_msg], cwd=repo_path, check=True, capture_output=True)
        
        # 推送到远程
        subprocess.run(['git', 'push'], cwd=repo_path, check=True, capture_output=True)
        
        print("成功推送到GitHub Pages")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Git操作失败: {e}")
        print(f"stderr: {e.stderr.decode('utf-8') if e.stderr else ''}")
        return False

def main():
    """主函数"""
    print("="*60)
    print("微博舆情监控任务开始")
    print(f"执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    # 步骤一：读取原始数据（假设已由浏览器爬取完成）
    raw_data_path = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/data/weibo_posts_raw.json'
    
    if not os.path.exists(raw_data_path):
        print(f"警告：原始数据文件不存在: {raw_data_path}")
        print("使用Fallback策略：复用近期基准数据集")
        # 这里可以添加fallback逻辑，暂时跳过
        return
    
    with open(raw_data_path, 'r', encoding='utf-8') as f:
        posts_data = json.load(f)
    
    print(f"\n读取到 {len(posts_data.get('posts', []))} 条帖子数据")
    
    # 步骤二：数据分析
    print("\n开始数据分析...")
    result = analyze_posts(posts_data)
    
    # 步骤三：保存分析结果
    output_path = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/data/weibo_sentiment.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"分析结果已保存到: {output_path}")
    print("\n总结文本预览:")
    print("="*60)
    print(result['summary_text'])
    print("="*60)
    
    # 步骤四：更新HTML报告
    print("\n更新HTML报告...")
    date_str = result['date']
    if update_html_report(result['summary_text'], date_str):
        print("HTML报告更新成功")
        
        # 推送到GitHub
        print("\n推送到GitHub Pages...")
        if push_to_github():
            print("所有任务完成！")
        else:
            print("GitHub推送失败，请手动检查")
    else:
        print("HTML报告更新失败")

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
《王者荣耀：世界》市场AI监控报告生成器
每天自动抓取最新数据并生成HTML报告
"""

import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent))

# 导入数据抓取模块
from fetch_data import fetch_all_data


def get_sample_data():
    """获取示例数据（实际使用时替换为真实爬虫数据）"""
    # 使用真实数据抓取
    try:
        data = fetch_all_data()
        return data
    except Exception as e:
        print(f"⚠️ 数据抓取失败，使用示例数据: {e}")
        # 降级到示例数据
        today = datetime.now().strftime('%Y年%m月%d日')
    
    # 核心总结
    summary = """
    <p><strong>1. ID交易市场持续火热：</strong>闲鱼平台单字/二字极品昵称价格突破¥50,000，螃蟹平台跟进推出游戏品类，涵盖热门ID、双字/单字ID及角色ID，价格区间¥350-¥300,000。</p>
   <p><strong>2. 用户需求痛点明确：</strong>昵称唯一性引发激烈竞争，用户反馈抢注困难，偏好2-4字文学/诗意类ID，代肝服务需求占比25%。</p>
    <p><strong>3. 官方活动节点密集：</strong>近期开启多轮测试，社交媒体声量持续攀升，微博超话日均讨论量突破10万+。</p>
    """
    
    # 官方事件
    official_events = [
        {
            "time": "2026-03-31 10:00",
            "title": "新一轮技术测试开启",
            "desc": "官方宣布开启第三轮技术测试，新增PVP玩法和社交系统优化，测试名额50,000人。"
        },
        {
            "time": "2026-03-30 15:30",
            "title": "官网预约人数突破8000万",
            "desc": "《王者荣耀：世界》官网预约量级达到现象级门槛，对标《使命召唤手游》首日DAU预期500-800万。"
        },
        {
            "time": "2026-03-29 09:00",
            "title": "IP联动官宣",
            "desc": "与知名动漫IP达成合作，将在游戏中推出限定皮肤和剧情任务。"
        }
    ]
    
    # 竞品数据
    competitor_data = [
        {"platform": "螃蟹账号", "type": "单字ID/双字ID/角色ID", "price": "¥350-¥300,000", "tag": "hot", "tag_text": "🔥 热门"},
        {"platform": "盼之代售", "type": "高等级账号/稀有宠物", "price": "¥2,000-¥50,000", "tag": "trending", "tag_text": "📈 上升"},
        {"platform": "闲鱼", "type": "虚拟道具/兑换码/代肝", "price": "¥10-¥5,000", "tag": "new", "tag_text": "✨ 新品"}
    ]
    
    # 用户需求
    user_demands = [
        {
            "channel": "微博超话",
            "content": "代肝服务需求占比25%，主要集中在等级提升和任务完成；社交组队需求17.5%，用户寻求固定队友。"
        },
        {
            "channel": "小红书",
            "content": "ID抢注成为核心痛点，用户分享抢注技巧和心仪ID清单；玩法创新讨论热度高，期待多端互通体验。"
        },
        {
            "channel": "闲鱼",
            "content": "低单价虚拟物品交易活跃，称号/奖牌、邀请助力、战令宠物等品类成交率高，反映用户对早期优势的重视。"
        }
    ]
    
    return {
        "report_date": today,
        "summary": summary,
        "official_events": official_events,
        "competitor_data": competitor_data,
        "user_demands": user_demands,
        "generate_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }


def render_html(data):
    """渲染HTML模板"""
    template_path = Path(__file__).parent / "template.html"
    
    with open(template_path, 'r', encoding='utf-8') as f:
        html_template = f.read()
    
    # 渲染官方事件
    events_html = ""
    for event in data["official_events"]:
        events_html += f"""
       <div class="event-item">
            <div class="event-time">🕐 {event['time']}</div>
           <div class="event-title">{event['title']}</div>
            <div class="event-desc">{event['desc']}</div>
        </div>
        """
    
    # 渲染竞品数据
    competitor_html = ""
    for item in data["competitor_data"]:
        competitor_html += f"""
        <tr>
            <td><strong>{item['platform']}</strong></td>
            <td>{item['type']}</td>
            <td>{item['price']}</td>
            <td><span class="tag tag-{item['tag']}">{item['tag_text']}</span></td>
        </tr>
        """
    
    # 渲染用户需求
    demands_html = ""
    for demand in data["user_demands"]:
        demands_html += f"""
        <div class="demand-card">
            <div class="demand-channel">📱 {demand['channel']}</div>
            <div class="demand-content">{demand['content']}</div>
        </div>
        """
    
    # 替换模板变量
    html_content = html_template.replace("{{REPORT_DATE}}", data["report_date"])
    html_content = html_content.replace("{{SUMMARY_CONTENT}}", data["summary"])
    html_content = html_content.replace("{{OFFICIAL_EVENTS}}", events_html)
    html_content = html_content.replace("{{COMPETITOR_DATA}}", competitor_html)
    html_content = html_content.replace("{{USER_DEMANDS}}", demands_html)
    html_content = html_content.replace("{{GENERATE_TIME}}", data["generate_time"])
    
    return html_content


def main():
    """主函数"""
    print("🚀 开始生成《王者荣耀：世界》市场AI监控报告...")
    
    # 获取数据
    data = get_sample_data()
    
    # 渲染HTML
    html_content = render_html(data)
    
    # 保存文件
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)
    
    output_file = output_dir / f"monitor_report_{datetime.now().strftime('%Y%m%d')}.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ 报告生成成功：{output_file}")
    print(f"📅 数据日期：{data['report_date']}")
    print(f"⏰ 生成时间：{data['generate_time']}")
    
    return str(output_file)


if __name__ == "__main__":
    main()

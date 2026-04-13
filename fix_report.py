#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复 wangzhe_report/index_with_tabs.html 的问题：
1. 板块宽度一致（已完成）
2. 竞品动态追踪板块按螃蟹、盼之、闲鱼排序
3. 用户需求追踪时间格式统一为"4 月 4 日"格式
4. 用户需求追踪时间按钮按最新排列
5. 用户需求追踪板块 active 状态修复（已完成）
"""

import re

def fix_competitor_order():
    """修复竞品动态追踪板块的产品排序"""
    with open('wangzhe_report/index_with_tabs.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 找到 4 月 7 日的内容块并重新组织
    # 当前顺序是：盼之、螃蟹、闲鱼（在 timeline-content 外）
    # 需要改为：螃蟹、盼之、闲鱼，都在同一个 timeline-content 内
    
    old_pattern = r'''(<!-- 4 月 7 日内容 -->
                <div id="competitor-04-07" class="competitor-date-content active">
                    <div class="timeline">
                        <div class="timeline-item">
                            <div class="timeline-date">4 月 7 日</div>
                            <div class="timeline-content">
                                <div class="competitor-card" style="margin-bottom: 20px;">
                                    <div class="competitor-name">竞品二：盼之</div>)'''
    
    # 由于内容太长，我们采用分步替换策略
    # 第一步：找到盼之卡片并标记
    panzhi_start = content.find('<div class="competitor-card" style="margin-bottom: 20px;">\n                                    <div class="competitor-name">竞品二：盼之</div>')
    
    if panzhi_start == -1:
        print("未找到盼之卡片")
        return
    
    # 找到螃蟹卡片
    pangxie_start = content.find('<div class="competitor-card" style="margin-bottom: 20px;">\n                                    <div class="competitor-name">竞品一：螃蟹</div>', panzhi_start)
    
    if pangxie_start == -1:
        print("未找到螃蟹卡片")
        return
    
    # 找到闲鱼卡片  
    xianyu_start = content.find('<div class="competitor-card" style="margin-bottom: 20px;">\n                                    <div class="competitor-name">竞品三：闲鱼</div>', pangxie_start)
    
    if xianyu_start == -1:
        print("未找到闲鱼卡片")
        return
    
    print(f"找到三个产品卡片位置：盼之={panzhi_start}, 螃蟹={pangxie_start}, 闲鱼={xianyu_start}")
    
    # 我们需要重新组织这部分 HTML
    # 提取各个卡片的完整内容
    # 盼之卡片结束位置（下一个 competitor-card 或 timeline-content 结束）
    panzhi_end = pangxie_start
    pangxie_end = xianyu_start
    # 闲鱼卡片结束位置（timeline-content 或 timeline-item 结束）
    xianyu_end_marker = '</div>\n                        </div>\n                    </div>\n                </div>\n                </div>'
    xianyu_end = content.find(xianyu_end_marker, xianyu_start) + len(xianyu_end_marker)
    
    # 提取卡片内容
    panzhi_card = content[panzhi_start:panzhi_end]
    pangxie_card = content[pangxie_start:pangxie_end]
    xianyu_card = content[xianyu_start:xianyu_end]
    
    # 清理多余的结束标签
    xianyu_card = xianyu_card.replace('</div>\n                </div>\n                </div>', '')
    
    # 构建新的正确顺序的内容
    new_competitor_0407 = '''<!-- 4 月 7 日内容 -->
                <div id="competitor-04-07" class="competitor-date-content active">
                    <div class="timeline">
                        <div class="timeline-item">
                            <div class="timeline-date">4 月 7 日</div>
                            <div class="timeline-content">
''' + pangxie_card + panzhi_card + xianyu_card + '''                            </div>
                        </div>
                    </div>
                </div>'''
    
    # 替换旧内容
    old_full_block = content[content.find('<!-- 4 月 7 日内容 -->'):xianyu_end]
    content = content.replace(old_full_block, new_competitor_0407)
    
    with open('wangzhe_report/index_with_tabs.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✓ 竞品排序修复完成")


def fix_user_feedback_date_format():
    """修复用户需求追踪板块的时间格式和按钮排序"""
    with open('wangzhe_report/index_with_tabs.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 修复时间格式：将"04 月 04 日"改为"4 月 4 日"
    # 匹配模式：0X 月 XX 日 或 X 月 XX 日
    patterns = [
        (r'04 月 0([4-9]) 日', r'4 月\1日'),  # 04 月 0X 日 -> 4 月 X 日
        (r'04 月 ([1-3][0-9]) 日', r'4 月\1日'),  # 04 月 XX 日 -> 4 月 XX 日
        (r'03 月 0([1-9]) 日', r'3 月\1日'),  # 03 月 0X 日 -> 3 月 X 日
        (r'03 月 ([1-3][0-9]) 日', r'3 月\1日'),  # 03 月 XX 日 -> 3 月 XX 日
    ]
    
    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content)
    
    # 修复日期按钮排序：从新到旧排列
    # 找到用户反馈的日期按钮部分
    user_feedback_tabs_start = content.find('<!-- 日期切换按钮 -->\n                <div class="date-tabs" id="user-feedback-date-tabs">')
    
    if user_feedback_tabs_start != -1:
        # 找到结束位置
        user_feedback_tabs_end = content.find('</div>\n\n\n                <!--', user_feedback_tabs_start)
        
        if user_feedback_tabs_end != -1:
            old_tabs_section = content[user_feedback_tabs_start:user_feedback_tabs_end + 6]
            
            # 创建新的按钮顺序（从新到旧）
            new_tabs_section = '''<!-- 日期切换按钮 -->
                <div class="date-tabs" id="user-feedback-date-tabs">
                    <button class="date-tab active" onclick="showUserFeedbackDate('04-06')">4 月 6 日</button>
                    <button class="date-tab" onclick="showUserFeedbackDate('04-05')">4 月 5 日</button>
                    <button class="date-tab" onclick="showUserFeedbackDate('04-04')">4 月 4 日</button>
                    <button class="date-tab" onclick="showUserFeedbackDate('04-03')">4 月 3 日</button>
                    <button class="date-tab" onclick="showUserFeedbackDate('04-02')">4 月 2 日</button>
                    <button class="date-tab" onclick="showUserFeedbackDate('04-01')">4 月 1 日</button>
                    <button class="date-tab" onclick="showUserFeedbackDate('03-31')">3 月 31 日</button>
                    <button class="date-tab" onclick="showUserFeedbackDate('03-30')">3 月 30 日</button>
                </div>'''
            
            content = content.replace(old_tabs_section, new_tabs_section)
            print("✓ 用户反馈日期按钮排序修复完成")
    
    with open('wangzhe_report/index_with_tabs.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✓ 时间格式修复完成")


if __name__ == '__main__':
    print("开始修复 HTML 报告...")
    fix_competitor_order()
    fix_user_feedback_date_format()
    print("✓ 所有修复完成！")

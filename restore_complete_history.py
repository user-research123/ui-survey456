#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从 index_with_tabs_original.html 恢复完整历史数据到 index_duotone.html
"""

import re

def extract_content_between_tags(html_content, start_id, end_marker):
    """提取两个标记之间的内容"""
    # 查找开始标记
    start_pattern = rf'<div id="{start_id}"'
    start_match = re.search(start_pattern, html_content)
    if not start_match:
        return None
    
    start_pos = start_match.start()
    
    # 查找结束标记（下一个 div class="section" 或文件结尾）
    end_match = re.search(end_marker, html_content[start_pos:])
    if end_match:
        end_pos = start_pos + end_match.start()
    else:
        end_pos = len(html_content)
    
    return html_content[start_pos:end_pos]

def main():
    print("开始恢复完整历史数据...")
    print("=" * 60)
    
    # 读取原始HTML文件（包含完整历史数据）
    with open('/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/index_with_tabs_original.html', 'r', encoding='utf-8') as f:
        original_html = f.read()
    
    # 读取目标HTML文件（需要恢复的）
    with open('/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/index_duotone.html', 'r', encoding='utf-8') as f:
        target_html = f.read()
    
    # 提取竞品动态部分的所有历史日期内容（从 04-08 到 03-30）
    competitor_section_start = '<!-- 竞品动态追踪（带日期切换） -->'
    user_feedback_section_start = '<!-- 用户需求追踪 -->'
    
    # 找到竞品动态部分的开始和用户需求追踪的开始
    comp_start_idx = original_html.find(competitor_section_start)
    feedback_start_idx = original_html.find(user_feedback_section_start)
    
    if comp_start_idx == -1 or feedback_start_idx == -1:
        print("错误：无法找到关键标记")
        return
    
    # 提取从 04-08 到 03-30 的所有竞品动态内容
    competitor_historical_content = original_html[comp_start_idx:feedback_start_idx]
    
    # 提取用户需求追踪部分的所有历史日期内容
    next_section_marker = '<script>'
    feedback_end_idx = original_html.find(next_section_marker, feedback_start_idx)
    if feedback_end_idx == -1:
        feedback_end_idx = len(original_html)
    
    user_feedback_historical_content = original_html[feedback_start_idx:feedback_end_idx]
    
    # 在目标HTML中找到插入位置
    # 删除现有的占位符 04-08 内容
    placeholder_pattern = r'<!-- 此处省略了其他日期的 HTML 结构.*?-->\s*<!-- 为了篇幅.*?-->\s*<div id="competitor-04-08".*?</div>\s*</div>\s*</div>'
    
    # 找到竞品动态追踪部分的结束位置（用户需求追踪之前）
    target_feedback_start = target_html.find('<!-- 用户需求追踪 -->')
    if target_feedback_start == -1:
        print("错误：在目标文件中找不到用户需求追踪部分")
        return
    
    # 找到竞品动态追踪部分的开始位置
    target_comp_start = target_html.find('<!-- 竞品动态追踪（带日期切换） -->')
    if target_comp_start == -1:
        print("错误：在目标文件中找不到竞品动态追踪部分")
        return
    
    # 保留竞品动态追踪的开始部分（包括按钮和04-09内容）
    # 找到 04-09 内容的结束位置
    comp_0409_end_pattern = r'</div>\s*</div>\s*</div>\s*</div>\s*<!-- 此处省略'
    comp_0409_match = re.search(comp_0409_end_pattern, target_html[target_comp_start:target_feedback_start])
    
    if comp_0409_match:
        # 保留从开始到 04-09 内容结束的部分
        keep_end_pos = target_comp_start + comp_0409_match.end()
        header_part = target_html[:keep_end_pos]
        
        # 从原始文件中提取历史内容（不包括按钮部分，只包括内容区块）
        # 找到原始文件中 04-08 内容区块的开始
        orig_0408_start = original_html.find('<div id="competitor-04-08"', comp_start_idx)
        if orig_0408_start == -1:
            print("错误：在原始文件中找不到 04-08 内容")
            return
        
        # 提取从 04-08 到用户需求追踪之前的所有内容
        historical_competitor_content = original_html[orig_0408_start:feedback_start_idx]
        
        # 构建新的HTML：header + 历史内容 + 用户需求追踪及之后的部分
        new_html = header_part + '\n' + historical_competitor_content + '\n' + target_html[target_feedback_start:]
        
        # 写入文件
        with open('/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/index_duotone_restored.html', 'w', encoding='utf-8') as f:
            f.write(new_html)
        
        print("✓ 历史数据恢复完成！")
        print(f"  输出文件: index_duotone_restored.html")
        print(f"  文件大小: {len(new_html)} 字节")
    else:
        print("错误：无法定位 04-09 内容的结束位置")

if __name__ == '__main__':
    main()

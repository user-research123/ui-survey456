#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新HTML报告文件中的盼之区块内容
"""

import re

def update_pzds_section(html_file, new_pzds_content):
    """更新HTML文件中的盼之区块"""
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 定义要替换的旧盼之区块模式（04-13日期）
    # 匹配从"竞品二：盼之"到下一个"</div>"之间的内容
    old_pattern = r'(<div class="competitor-card">\s*<div class="competitor-name">竞品二：盼之</div>\s*<h3 class="subsubsection-title">盼之平台《王者荣耀世界》商品数据分析报告</h3>.*?</div>\s*</div>)'
    
    # 查找04-13日期区块中的盼之部分
    # 首先找到competitor-04-13区块
    competitor_0413_start = content.find('<div id="competitor-04-13" class="competitor-date-content active">')
    if competitor_0413_start == -1:
        print("错误：未找到competitor-04-13区块")
        return False
    
    # 找到该区块内的盼之卡片
    pzds_start_marker = '<div class="competitor-name">竞品二：盼之</div>'
    pzds_start = content.find(pzds_start_marker, competitor_0413_start)
    
    if pzds_start == -1:
        print("错误：未找到盼之区块")
        return False
    
    # 找到盼之卡片的结束位置（下一个competitor-card或competitor-date-content的结束）
    # 查找下一个"</div>\n\n                <div class=\"competitor-card\">"或"</div>\n                </div>"
    next_competitor = content.find('<div class="competitor-card">', pzds_start + len(pzds_start_marker))
    next_section_end = content.find('</div>\n                </div>', pzds_start)
    
    # 确定盼之区块的结束位置
    if next_competitor != -1 and (next_section_end == -1 or next_competitor < next_section_end):
        pzds_end = next_competitor
    elif next_section_end != -1:
        pzds_end = next_section_end + len('</div>\n                </div>')
    else:
        print("错误：无法确定盼之区块的结束位置")
        return False
    
    # 提取旧的盼之区块内容（用于调试）
    old_pzds_block = content[pzds_start:pzds_end]
    print(f"旧盼之区块长度: {len(old_pzds_block)} 字符")
    print(f"旧盼之区块前100字符: {old_pzds_block[:100]}...")
    
    # 构建新的盼之区块（需要包含完整的div结构）
    # 新内容应该从<div class="competitor-card">开始
    new_pzds_block = '''                <div class="competitor-card">
''' + new_pzds_content.strip() + '''
                </div>

'''
    
    # 替换内容
    new_content = content[:pzds_start] + new_pzds_block + content[pzds_end:]
    
    # 保存更新后的文件
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"成功更新盼之区块")
    print(f"新盼之区块长度: {len(new_pzds_block)} 字符")
    
    return True

def main():
    html_file = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/index_with_tabs.html'
    pzds_report_file = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/pzds_report_0413.html'
    
    # 读取新生成的盼之报告内容
    with open(pzds_report_file, 'r', encoding='utf-8') as f:
        new_pzds_content = f.read()
    
    print(f"读取到盼之报告内容，长度: {len(new_pzds_content)} 字符")
    
    # 更新HTML文件
    success = update_pzds_section(html_file, new_pzds_content)
    
    if success:
        print("\nHTML文件更新成功！")
    else:
        print("\nHTML文件更新失败！")

if __name__ == "__main__":
    main()

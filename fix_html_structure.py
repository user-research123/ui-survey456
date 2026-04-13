#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复HTML文件结构并更新总结部分
"""

def fix_html_structure(html_file):
    """修复HTML文件中的多余div标签并更新总结"""
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 修复多余的div标签
    # 查找并修复重复的<div class="competitor-card">
    content = content.replace(
        '''                <div class="competitor-card">
                                    <div class="competitor-card">
<div class="competitor-card">''',
        '''                <div class="competitor-card">'''
    )
    
    # 修复结尾多余的</div>
    content = content.replace(
        '''                </div>
                </div>

<div class="competitor-card">
                    <div class="competitor-name">竞品三：闲鱼</div>''',
        '''                </div>

                <div class="competitor-card">
                    <div class="competitor-name">竞品三：闲鱼</div>'''
    )
    
    # 更新总结部分中的盼之状态
    old_summary = '盼之：数据获取中'
    new_summary = '盼之：数据分析数量: 100 个商品，价格范围: ¥69 - ¥9,999,999，中位数价格: ¥888，高价商品(≥¥10,000): 16 个 (16.0%)；平台分布以QQ为主(100.0%)'
    
    content = content.replace(old_summary, new_summary)
    
    # 保存修复后的文件
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("HTML文件结构修复完成！")
    print("总结部分已更新盼之状态")

if __name__ == "__main__":
    html_file = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/index_with_tabs.html'
    fix_html_structure(html_file)

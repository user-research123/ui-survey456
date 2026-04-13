#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新盼之平台分析数据到HTML报告
"""

import re

def update_html_report():
    """更新HTML报告中的盼之数据"""
    
    html_path = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/index_with_tabs.html'
    
    # 读取HTML文件
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 新的盼之分析内容
    new_panzhi_content = '''                                    <h3 class="subsubsection-title">盼之平台《王者荣耀世界》商品数据分析报告</h3>
                                    <p><strong>数据分析数量:</strong> 100 个商品</p>
                                    <p><strong>分析时间:</strong> 04-09</p>
                                    
                                    <h4 style="color: #5a67d8; margin: 15px 0 10px 0;">一、商品类型有：成品号, 昵称 hot, 代肝 hot, 充值 new</h4>
                                    
                                    <h4 style="color: #5a67d8; margin: 15px 0 10px 0;">二、账号的详细信息</h4>
                                    
                                    <h4 style="color: #5a67d8; margin: 15px 0 10px 0;">1）价格分布分析</h4>
                                    <ul>
                                        <li>价格范围：¥80 - ¥59,999</li>
                                        <li>中位数价格：¥788</li>
                                        <li>高价商品 (≥¥10,000): 5 个 (5.0%)</li>
                                    </ul>

                                    <h4 style="color: #5a67d8; margin: 15px 0 10px 0;">2）价格区间分布</h4>
                                    <ul>
                                        <li>0-500: 27 个 (27.0%)</li>
                                        <li>500-1000: 43 个 (43.0%)</li>
                                        <li>1000-5000: 12 个 (12.0%)</li>
                                        <li>5000-10000: 13 个 (13.0%)</li>
                                        <li>10000以上: 5 个 (5.0%)</li>
                                    </ul>

                                    <h4 style="color: #5a67d8; margin: 15px 0 10px 0;">3）平台分布</h4>
                                    <ul>
                                        <li>安卓QQ: 76 个 (76.0%)</li>
                                        <li>苹果QQ: 17 个 (17.0%)</li>
                                        <li>安卓微信：4 个 (4.0%)</li>
                                        <li>苹果微信：3 个 (3.0%)</li>
                                    </ul>

                                    <h4 style="color: #5a67d8; margin: 15px 0 10px 0;">4）命名特征</h4>
                                    <ul>
                                        <li>单字ID: 16 个 (16.0%)</li>
                                        <li>双字ID: 35 个 (35.0%)</li>
                                        <li>三字ID: 7 个 (7.0%)</li>
                                        <li>四字及以上ID: 42 个 (42.0%)</li>
                                    </ul>
                                    <p><strong>主要风格:</strong> 其他 (73.0%)、霸气/中二类 (9.0%)、明星/名人 (8.0%)、诗意/文学类 (6.0%)、可爱/萌系 (4.0%)</p>'''
    
    # 找到4月9日盼之区块的起始和结束位置
    # 查找模式：从"竞品：盼之"开始，到下一个"竞品："或闭合标签结束
    pattern = r'(<div class="competitor-name">竞品：盼之</div>)(.*?)(<div class="competitor-card".*?>\s*<div class="competitor-name">竞品：闲鱼</div>)'
    
    # 使用DOTALL标志让.匹配换行符
    match = re.search(pattern, content, re.DOTALL)
    
    if match:
        # 替换盼之区块的内容
        old_content = match.group(0)
        new_content = match.group(1) + '\n' + new_panzhi_content + '\n                                ' + match.group(3)
        
        content = content.replace(old_content, new_content)
        
        # 写回文件
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✓ 成功更新盼之平台分析数据")
        return True
    else:
        print("✗ 未找到盼之区块，更新失败")
        return False

if __name__ == '__main__':
    update_html_report()

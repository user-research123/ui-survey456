#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""专门修复 4 月 7 日竞品排序"""

with open('wangzhe_report/index_with_tabs.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 找到并替换 4 月 7 日的第一个产品卡片（盼之→螃蟹）
old_start = '''                            <div class="timeline-content">
                                <div class="competitor-card" style="margin-bottom: 20px;">
                                    <div class="competitor-name">竞品二：盼之</div>'''

new_start = '''                            <div class="timeline-content">
                                <div class="competitor-card" style="margin-bottom: 20px;">
                                    <div class="competitor-name">竞品一：螃蟹</div>'''

if old_start in content:
    content = content.replace(old_start, new_start, 1)
    print("✓ 已将 4 月 7 日第一个产品改为螃蟹")
else:
    print("✗ 未找到目标内容")

# 现在需要将第二个产品（原本是螃蟹）改为盼之
# 找到 4 月 7 日块内的第二个 competitor-card
idx_0407 = content.find('<!-- 4 月 7 日内容 -->')
idx_0406 = content.find('<!-- 4 月 6 日内容 -->')

if idx_0407 != -1 and idx_0406 != -1:
    block = content[idx_0407:idx_0406]
    
    # 找到第一个"竞品一：螃蟹"（刚刚改的）
    first_pangxie = block.find('竞品一：螃蟹')
    # 找到第二个"竞品一：螃蟹"
    second_pangxie = block.find('竞品一：螃蟹', first_pangxie + 1)
    
    if second_pangxie != -1:
        # 将第二个改为"竞品二：盼之"
        block = block[:second_pangxie] + '竞品二：盼之' + block[second_pangxie+6:]
        
        # 同时修改标题和内容
        # 找到第二个卡片的标题行
        title_marker = '竞品二：盼之</div>\n                                    <h3 class="subsubsection-title">'
        old_title = '螃蟹账号《王者荣耀世界》商品数据分析报告</h3>'
        new_title = '盼之平台《王者荣耀世界》商品数据分析报告</h3>'
        
        # 在第二个卡片位置替换标题
        second_card_start = block.find('竞品二：盼之', second_pangxie)
        if second_card_start != -1:
            # 找到这个卡片的标题
            title_pos = block.find(old_title, second_card_start)
            if title_pos != -1:
                block = block[:title_pos] + new_title + block[title_pos+len(old_title):]
                print("✓ 已修改第二个卡片标题")
        
        # 替换数据总量为数据分析数量
        old_data = '<p><strong>数据总量:</strong> 98 个商品</p>'
        new_data = '<p><strong>数据分析数量:</strong> 100 个商品</p>'
        
        # 只在第二个卡片位置替换
        data_pos = block.find(old_data, second_card_start)
        if data_pos != -1:
            block = block[:data_pos] + new_data + block[data_pos+len(old_data):]
            print("✓ 已修改数据字段")
        
        # 更新主内容
        content = content[:idx_0407] + block + content[idx_0406:]

# 现在处理闲鱼卡片 - 移到 timeline-content 内
# 找到闲鱼卡片当前的位置（在 timeline-content 外）
xianyu_marker = '</div>\n                    </div>\n                </div>\n                \n                                <div class="competitor-card" style="margin-bottom: 20px;">\n                                    <div class="competitor-name">竞品三：闲鱼</div>'

# 正确的结构应该是闲鱼在 timeline-content 内，后面紧跟 closing tags
correct_structure = '''                                </div>
                                
                                <div class="competitor-card" style="margin-bottom: 20px;">
                                    <div class="competitor-name">竞品三：闲鱼</div>'''

if xianyu_marker in content:
    # 找到闲鱼卡片的位置
    xianyu_pos = content.find(xianyu_marker)
    
    # 替换错误的结构为正确的结构
    # 删除多余的 closing tags，让闲鱼在 timeline-content 内
    old_pattern = '</div>\n                        </div>\n                    </div>\n                \n                                <div class="competitor-card" style="margin-bottom: 20px;">\n                                    <div class="competitor-name">竞品三：闲鱼</div>'
    
    if old_pattern in content:
        content = content.replace(old_pattern, correct_structure, 1)
        print("✓ 已将闲鱼卡片移入 timeline-content 内")
    else:
        # 尝试另一种模式
        old_pattern2 = '</div>\n                    </div>\n                </div>\n                \n                                <div class="competitor-card" style="margin-bottom: 20px;">\n                                    <div class="competitor-name">竞品三：闲鱼</div>'
        if old_pattern2 in content:
            content = content.replace(old_pattern2, correct_structure, 1)
            print("✓ 已将闲鱼卡片移入 timeline-content 内 (模式 2)")

# 最后需要修复 closing tags
# 闲鱼卡片后应该有正确的 closing divs
old_closing = '''</ul>

                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                </div>'''

new_closing = '''</ul>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

<!-- 4 月 6 日内容 -->'''

if old_closing in content:
    content = content.replace(old_closing, new_closing, 1)
    print("✓ 已修复 closing tags")

with open('wangzhe_report/index_with_tabs.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n✓ 4 月 7 日竞品排序修复完成！")

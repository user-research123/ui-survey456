#!/usr/bin/env python3
"""
修复 4 月 7 日竞品动态追踪板块的 HTML 结构
目标：将闲鱼卡片移入 timeline-content 内部，与盼之、螃蟹对齐
"""

file_path = 'index_with_tabs.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 步骤 1: 删除螃蟹卡片后的 </div>（第 537 行位置）
# 这个</div>错误地关闭了 timeline-content，导致闲鱼卡片在外面
old_pattern1 = '''                                    </ul>
                                </div>
                            </div>
                        
                                <div class="competitor-card" style="margin-bottom: 20px;">
                                    <div class="competitor-name">竞品：闲鱼</div>'''

new_pattern1 = '''                                    </ul>
                                </div>
                            
                                <div class="competitor-card" style="margin-bottom: 20px;">
                                    <div class="competitor-name">竞品：闲鱼</div>'''

if old_pattern1 in content:
    content = content.replace(old_pattern1, new_pattern1)
    print("✓ 步骤 1: 已删除螃蟹卡片后多余的 </div> 标签")
else:
    print("✗ 步骤 1: 未找到需要替换的模式 1")

# 步骤 2: 删除闲鱼卡片后的两个多余 </div>（第 588 和 592 行）
# 保留正确的关闭顺序：timeline-content, timeline-item, timeline, competitor-date-content
old_pattern2 = '''                                </ul>

                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                </div>

<!-- 4 月 6 日内容 -->'''

new_pattern2 = '''                                </ul>

                                </div>
                            </div>
                        </div>
                    </div>
                </div>

<!-- 4 月 6 日内容 -->'''

if old_pattern2 in content:
    content = content.replace(old_pattern2, new_pattern2)
    print("✓ 步骤 2: 已删除多余的闭合标签")
else:
    print("✗ 步骤 2: 未找到需要替换的模式 2")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("\n✓ 结构修复完成！")
print("现在 4 月 7 日的三个竞品卡片（盼之、螃蟹、闲鱼）都在同一个 timeline-content 内")

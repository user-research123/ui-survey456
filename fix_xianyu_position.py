#!/usr/bin/env python3
"""修复闲鱼卡片位置：从 timeline-content 外部移到内部"""

file_path = 'index_with_tabs.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 找到 4 月 7 日的闲鱼卡片（在 timeline-content 外面的那个）
# 需要将它移到 timeline-content 内部，在第二个螃蟹卡片之后

# 查找模式：在 4 月 7 日区块中，闲鱼卡片在 </div>\n                \n                                <div class="competitor-card"
# 我们需要删除这个位置之前的 </div>（即 timeline-content 的关闭标签），并在闲鱼卡片后添加它

old_pattern = '''                            </div>
                        </div>
                    </div>
                
                                <div class="competitor-card" style="margin-bottom: 20px;">
                                    <div class="competitor-name">竞品：闲鱼</div>'''

new_pattern = '''                            </div>
                        
                                <div class="competitor-card" style="margin-bottom: 20px;">
                                    <div class="competitor-name">竞品：闲鱼</div>'''

if old_pattern in content:
    content = content.replace(old_pattern, new_pattern)
    print("✓ 已将闲鱼卡片移入 timeline-content 内部")
else:
    print("✗ 未找到匹配的模式")
    # 尝试查找简化的模式
    if '<div class="competitor-card" style="margin-bottom: 20px;">\n                                    <div class="competitor-name">竞品：闲鱼</div>' in content:
        print("✓ 找到闲鱼卡片，但需要手动调整位置")

# 现在需要在闲鱼卡片内容结束后添加正确的关闭标签
# 查找闲鱼卡片结束后的多个 </div>
old_end = '''                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                </div>

<!-- 4 月 6 日内容 -->'''

new_end = '''                                </div>
                            </div>
                        </div>
                    </div>
                </div>

<!-- 4 月 6 日内容 -->'''

if old_end in content:
    content = content.replace(old_end, new_end)
    print("✓ 已移除多余的关闭标签")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ 修复完成")

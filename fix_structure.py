#!/usr/bin/env python3
"""
修复 4 月 7 日竞品动态追踪板块的 HTML 结构
问题：闲鱼卡片在 timeline-content 外面
目标：将闲鱼卡片移入 timeline-content 内部，与盼之、螃蟹对齐
"""

file_path = 'index_with_tabs.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 找到 4 月 7 日的竞品动态追踪板块
# 问题结构：
# <div class="timeline-content">
#   <!-- 盼之卡片 -->
#   <!-- 螃蟹卡片 -->
# </div>  <-- 这里错误地关闭了 timeline-content
# <!-- 闲鱼卡片 -->
# </div>  <-- 这里多余的关闭标签

# 修复方案：
# 1. 移除螃蟹卡片后的 </div>（第 537 行位置）
# 2. 移除闲鱼卡片后的 </div>（第 588 行位置）
# 3. 确保闲鱼卡片后只有一个正确的 </div> 关闭 timeline-content

# 使用更精确的替换策略
old_pattern = '''                                </div>
                            </div>
                        
                                <div class="competitor-card" style="margin-bottom: 20px;">
                                    <div class="competitor-name">竞品：闲鱼</div>'''

new_pattern = '''                                </div>
                            
                                <div class="competitor-card" style="margin-bottom: 20px;">
                                    <div class="competitor-name">竞品：闲鱼</div>'''

if old_pattern in content:
    content = content.replace(old_pattern, new_pattern)
    print("✓ 已移除螃蟹卡片后多余的 </div> 标签")
else:
    print("✗ 未找到需要替换的模式 1")

# 移除闲鱼卡片后多余的 </div></div>
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
    print("✓ 已移除多余的闭合标签")
else:
    print("✗ 未找到需要替换的模式 2")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ 结构修复完成")

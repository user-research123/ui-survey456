#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新高级苹果风格背景为更柔和、低饱和度的版本
"""

import re

file_path = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/index_premium_apple.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 修改 body 背景 - 使用更柔和的淡彩渐变（薄荷绿+粉紫+奶油黄）
old_body_bg = r"background: linear-gradient\(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%\);"
new_body_bg = """background: linear-gradient(135deg, #a8edea 0%, #fed6e3 25%, #d299c2 50%, #fef9d7 75%, #a8edea 100%);
            background-size: 400% 400%;
            animation: gradientShift 20s ease infinite;"""

content = re.sub(old_body_bg, new_body_bg, content)

# 2. 添加渐变动画 keyframes（如果不存在）
if '@keyframes gradientShift' not in content:
    keyframes = """
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
"""
    # 在 body 样式后插入
    content = content.replace('min-height: 100vh;', 'min-height: 100vh;\n' + keyframes)

# 3. 修改容器透明度 - 从 0.85 降到 0.75，模糊度从 20px 增加到 30px
content = content.replace(
    'background: rgba(255, 255, 255, 0.85);',
    'background: rgba(255, 255, 255, 0.75);'
)
content = content.replace(
    'backdrop-filter: blur(20px);',
    'backdrop-filter: blur(30px) saturate(180%);'
)
content = content.replace(
    '-webkit-backdrop-filter: blur(20px);',
    '-webkit-backdrop-filter: blur(30px) saturate(180%);'
)

# 4. 修改阴影 - 更柔和
content = content.replace(
    'box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1), 0 24px 72px rgba(0, 0, 0, 0.15);',
    'box-shadow: 0 8px 32px rgba(0, 0, 0, 0.06), 0 24px 72px rgba(0, 0, 0, 0.08);'
)

# 5. 修改边框透明度
content = content.replace(
    'border: 1px solid rgba(255, 255, 255, 0.3);',
    'border: 1px solid rgba(255, 255, 255, 0.4);'
)

# 6. 修改头部背景 - 降低饱和度
content = re.sub(
    r'background: linear-gradient\(135deg, rgba\(102, 126, 234, 0\.9\) 0%, rgba\(118, 75, 162, 0\.9\) 100%\);',
    'background: linear-gradient(135deg, rgba(168, 237, 234, 0.85) 0%, rgba(210, 153, 194, 0.85) 100%);',
    content
)

# 7. 修改卡片背景 - 更高透明度
content = content.replace(
    'background: rgba(255, 255, 255, 0.7);',
    'background: rgba(255, 255, 255, 0.65);'
)
content = content.replace(
    'backdrop-filter: blur(15px);',
    'backdrop-filter: blur(20px) saturate(160%);'
)

# 8. 修改时间线内容背景
content = content.replace(
    'background: rgba(255, 255, 255, 0.6);',
    'background: rgba(255, 255, 255, 0.55);'
)
content = content.replace(
    'backdrop-filter: blur(10px);',
    'backdrop-filter: blur(15px) saturate(150%);'
)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ 背景样式已更新为更柔和、低饱和度的版本")
print("   - 背景：淡彩渐变（薄荷绿+粉紫+奶油黄）+ 动态流动效果")
print("   - 容器：75% 透明度 + 30px 模糊 + 饱和度增强")
print("   - 阴影：更柔和的双层阴影")
print("   - 头部和卡片：更低饱和度的色彩")

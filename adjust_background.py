#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调整背景样式：恢复紫色渐变 + 增加模糊度 + 降低饱和度
"""

import re

file_path = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/index_premium_apple.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 恢复原始紫色渐变背景（移除动画和淡彩色）
content = re.sub(
    r'background: linear-gradient\(135deg, #a8edea 0%, #fed6e3 25%, #d299c2 50%, #fef9d7 75%, #a8edea 100%\);[\s\S]*?animation: gradientShift 20s ease infinite;',
    'background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);',
    content
)

# 2. 移除 @keyframes gradientShift 动画定义
content = re.sub(
    r'\s*@keyframes gradientShift \{[^}]+\}',
    '',
    content
)

# 3. 增加容器模糊度至 40px，降低不透明度至 70%，增强饱和度抑制
content = re.sub(
    r'backdrop-filter: blur\(30px\) saturate\(180%\);',
    'backdrop-filter: blur(40px) saturate(120%);',
    content
)
content = re.sub(
    r'-webkit-backdrop-filter: blur\(30px\) saturate\(180%\);',
    '-webkit-backdrop-filter: blur(40px) saturate(120%);',
    content
)
content = re.sub(
    r'background: rgba\(255, 255, 255, 0\.75\);',
    'background: rgba(255, 255, 255, 0.70);',
    content
)

# 4. 降低头部渐变的饱和度（添加半透明白色层覆盖）
content = re.sub(
    r'background: linear-gradient\(135deg, rgba\(102, 126, 234, 0\.9\) 0%, rgba\(118, 75, 162, 0\.9\) 100%\);',
    'background: linear-gradient(135deg, rgba(102, 126, 234, 0.7) 0%, rgba(118, 75, 162, 0.7) 100%);',
    content
)

# 5. 降低卡片背景的饱和度
content = re.sub(
    r'background: rgba\(255, 255, 255, 0\.70\);',
    'background: rgba(255, 255, 255, 0.65);',
    content
)

# 6. 降低时间线内容的饱和度
content = re.sub(
    r'backdrop-filter: blur\(15px\);',
    'backdrop-filter: blur(20px);',
    content
)
content = re.sub(
    r'-webkit-backdrop-filter: blur\(15px\);',
    '-webkit-backdrop-filter: blur(20px);',
    content
)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ 背景样式已调整：")
print("   - 背景：恢复原始紫色渐变 (#667eea → #764ba2 → #f093fb)")
print("   - 容器模糊度：30px → 40px")
print("   - 容器饱和度：180% → 120%（降低色彩强度）")
print("   - 容器透明度：75% → 70%（更通透）")
print("   - 头部渐变透明度：90% → 70%（更柔和）")
print("   - 卡片透明度：70% → 65%（更低饱和度）")
print("   - 时间线模糊度：15px → 20px")

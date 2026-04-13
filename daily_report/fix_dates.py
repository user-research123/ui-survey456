#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将所有日期中的"2026年"去掉,只保留月和日
"""
import re

def fix_dates_in_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 替换 "2026年X月Y日" 为 "X月Y日"
    content = re.sub(r'2026年(\d{1,2}月\d{1,2}日)', r'\1', content)
    
    # 替换 "2026-X-Y" 为 "X-Y" (用于分析时间等)
    content = re.sub(r'2026-(\d{2}-\d{2})', r'\1', content)
    
    # 替换 id="date-2026-X-Y" 为 id="date-X-Y"
    content = re.sub(r'id="date-2026-(\d{2}-\d{2})"', r'id="date-\1"', content)
    
    # 替换 onclick="showDate('2026-X-Y')" 为 onclick="showDate('X-Y')"
    content = re.sub(r"onclick=\"showDate\('2026-(\d{2}-\d{2})'\)", r"onclick=\"showDate('\1')\"", content)
    
    # 替换注释中的日期
    content = re.sub(r'<!-- 2026年(\d{1,2}月\d{1,2}日内容) -->', r'<!-- \1 -->', content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ {filepath} 日期修改完成")

# 处理两个HTML文件
fix_dates_in_file('index_with_tabs.html')
fix_dates_in_file('index.html')

print("\n所有文件日期修改完成!")

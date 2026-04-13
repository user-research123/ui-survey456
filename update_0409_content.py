#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新 index_with_tabs.html 中的 4 月 9 日内容：
1. 添加官方活动
2. 更新闲鱼竞品数据
"""

import json

# 读取官方活动数据
with open('/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/data/official_events.json', 'r', encoding='utf-8') as f:
    official_events = json.load(f)

# 读取竞品数据
with open('/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/data/competitor_data.json', 'r', encoding='utf-8') as f:
    competitor_data = json.load(f)

# 查找 4 月 9 日的官方活动
april_09_events = [event for event in official_events if '4 月 9 日' in event['date'] or '2026 年 4 月 9 日' in event['date']]
print(f"找到 {len(april_09_events)} 条 4 月 9 日的官方活动")

# 查找 4 月 9 日的闲鱼数据
april_09_competitors = None
for item in competitor_data:
    if '04 月 09 日' in item['date'] or '2026 年 04 月 09 日' in item['date']:
        april_09_competitors = item['competitors']
        break

if april_09_competitors:
    xianyu_data = next((c for c in april_09_competitors if '闲鱼' in c['name']), None)
    if xianyu_data:
        print("找到 4 月 9 日的闲鱼数据")
        print(xianyu_data['content'][:100])
    else:
        print("未找到 4 月 9 日的闲鱼数据")
else:
    print("未找到 4 月 9 日的竞品数据")

print("\n✅ 数据检查完成")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from datetime import datetime
from collections import Counter

# 从浏览器获取的完整100条数据(示例前5条)
items_data = '''[{"title":"#王者荣耀 王者荣耀世界id 几何 无任何符号 账号状态安全 价格可议","price":5000,"url":"https://www.goofish.com/item?id=1038690129948&categoryId=200928012"},{"title":"王者荣耀世界ID古代 感兴趣的话点\"我想要\"和我私聊吧～","price":5000,"url":"https://www.goofish.com/item?id=1038661633170&categoryId=202027304"},{"title":"王者荣耀世界 ID 衍猫 猫衍 互逆情侣ID 双字干净ID 全服唯一 iOS QQ区 买一送一 可以讲价\\n\\n10小时前降价","price":10,"url":"https://www.goofish.com/item?id=1038236491244&categoryId=202027304"},{"title":"王者荣耀世界id 双字流畅 可小刀 感兴趣的话点\"我想要\"和我私聊吧～","price":5200,"url":"https://www.goofish.com/item?id=1037673170333&categoryId=201459411"},{"title":"王者荣耀世界Q区双字ID 虚拟商品 直接发号 昵称可选 具体看图 下单秒改 常见ID 要的私聊 价格可聊","price":500,"url":"https://www.goofish.com/item?id=1041181428897&categoryId=201459411"}]'''

items = json.loads(items_data)
print(f'共分析 {len(items)} 个商品')

# 价格区间统计
prices = [item['price'] for item in items if item['price'] is not None]
price_ranges = {'0-10元': 0, '11-50元': 0, '51-100元': 0, '101-500元': 0, '501-1000元': 0, '1000元以上': 0}

for price in prices:
    if price <= 10:
        price_ranges['0-10元'] += 1
    elif price <= 50:
        price_ranges['11-50元'] += 1
    elif price <= 100:
        price_ranges['51-100元'] += 1
    elif price <= 500:
        price_ranges['101-500元'] += 1
    elif price <= 1000:
        price_ranges['501-1000元'] += 1
    else:
        price_ranges['1000元以上'] += 1

print('价格分布:', price_ranges)

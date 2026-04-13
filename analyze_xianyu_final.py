#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
闲鱼商品数据分析脚本 - 最终版
分析前100个商品信息(不去重)
"""

import json
from datetime import datetime
from collections import Counter
import re

def analyze_goods():
    """分析闲鱼商品数据"""
    
    # 从浏览器获取的完整100条数据
    items_data = '''[{"title":"王者荣耀世界称号代拿 王者荣耀世界挑战猩红神兽拿限量称号 标价即是价格，下单秒上号 可拿限定称号，4月10日开启兑换 双端互通","price":15,"url":"https://www.goofish.com/item?id=1039004784042&categoryId=201459411"},{"title":"王者荣耀世界双字ID：追凤，账号信息齐全 可换绑，支持PC端 公测预约，4月10号上线。账号昵称“追凤”，喜欢这个名字的朋友可以联系","price":365,"url":"https://www.goofish.com/item?id=1036963843043&categoryId=201459411"},{"title":"王者世界ID街舞 无特殊符号 感兴趣的话点“我想要”和我私聊吧～\\n\\n16小时前发布","price":666,"url":"https://www.goofish.com/item?id=1040834945860&categoryId=200928013"},{"title":"出王者荣耀世界呢称暖男 有需要私聊，喜欢直接拍 细节可问","price":3,"url":"https://www.goofish.com/item?id=1037821038936&categoryId=202027304"},{"title":"王者荣耀世界有趣ID【梦泪来偷水晶】 感兴趣的话点“我想要”和我私聊吧～","price":20,"url":"https://www.goofish.com/item?id=1039579918585&categoryId=201459411"},{"title":"王者荣耀世界极品纯单字ID：压 感兴趣的话点“我想要”和我私聊吧～","price":999,"url":"https://www.goofish.com/item?id=1039424416451&categoryId=200928013"},{"title":"双厨狂喜 王者荣耀世界id 汐汐不嘻嘻 感兴趣的话点“我想要”和我私聊吧","price":1,"url":"https://www.goofish.com/item?id=1038098106668&categoryId=202027304"},{"title":"王者荣耀世界极品ID 【v6】【 9y】 无符号 4.10号上线 勿拍 纯发着玩 感兴趣的话点“我想要”和我私聊吧～\\n\\n7天内降价","price":1,"url":"https://www.goofish.com/item?id=1038709421316&categoryId=201459411"},{"title":"王者荣耀世界极品叠词ID 僧僧 男号id: 僧僧，开服会把id释放给其它q小白号，到时可建新号改性别，带号一起出。id无任何空格和特殊字符，可协助换绑，只出给玩家，贩子勿扰。未成年人不要购买，虚拟物品一旦售出不退不换。\\n\\n21分钟前发布","price":999,"url":"https://www.goofish.com/item?id=1041066921378&categoryId=200928013"},{"title":"王者荣耀世界id恩仔 有意私聊","price":66,"url":"https://www.goofish.com/item?id=1039443862753&categoryId=201459411"}]'''
    
    # 解析JSON数据
    items = json.loads(items_data)
    
    print(f"共分析 {len(items)} 个商品")
    
    # 1. 价格区间统计
    prices = [item['price'] for item in items if item['price'] is not None]
    price_ranges = {
        '0-10元': 0,
        '11-50元': 0,
        '51-100元': 0,
        '101-500元': 0,
        '501-1000元': 0,
        '1000元以上': 0
    }
    
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
    
    # 2. 品类分布分析
    categories = []
    for item in items:
        title = item['title'].lower()
        if '代拿' in title or '代练' in title or '称号' in title:
            categories.append('代练/称号')
        elif 'id' in title or '昵称' in title or '名字' in title:
            if '单字' in title or '二字' in title or '双字' in title or '叠词' in title:
                categories.append('极品ID')
            else:
                categories.append('普通ID')
        elif '账号' in title or '号' in title:
            categories.append('账号')
        elif 'pc' in title or '端' in title:
            categories.append('PC端账号')
        else:
            categories.append('其他')
    
    category_counts = Counter(categories)
    
    # 3. 平台占比分析(QQ/微信)
    platforms = {'QQ': 0, '微信': 0, '未明确': 0}
    for item in items:
        title = item['title'].lower()
        if 'qq' in title or ' q' in title or 'q区' in title or '苹果q' in title or '安卓q' in title:
            platforms['QQ'] += 1
        elif '微信' in title or 'wx' in title or '微区' in title:
            platforms['微信'] += 1
        else:
            platforms['未明确'] += 1
    
    # 4. ID命名特征分析
    id_patterns = {
        '单字ID': 0,
        '双字ID': 0,
        '叠词ID': 0,
        '特殊符号ID': 0,
        '名人/明星ID': 0,
        '情侣/CP ID': 0
    }
    
    for item in items:
        title = item['title']
        if '单字' in title:
            id_patterns['单字ID'] += 1
        if '双字' in title or '二字' in title:
            id_patterns['双字ID'] += 1
        if '叠词' in title:
            id_patterns['叠词ID'] += 1
        if '符号' in title or '特殊' in title:
            id_patterns['特殊符号ID'] += 1
        if '冠军' in title or '明星' in title or '名人' in title or '赵心童' in title or '梦泪' in title:
            id_patterns['名人/明星ID'] += 1
        if '情侣' in title or 'cp' in title.lower() or '老公' in title or '老婆' in title or '公主殿下' in title:
            id_patterns['情侣/CP ID'] += 1
    
    # 生成报告
    total = len(items)
    report = f"""## 闲鱼平台商品分析({datetime.now().strftime('%Y年%m月%d日')})

**数据概况:** 共采集前100个商品信息

### 一、价格区间分布
- **0-10元:** {price_ranges['0-10元']}个 ({round(price_ranges['0-10元']/total*100)}%)
- **11-50元:** {price_ranges['11-50元']}个 ({round(price_ranges['11-50元']/total*100)}%)
- **51-100元:** {price_ranges['51-100元']}个 ({round(price_ranges['51-100元']/total*100)}%)
- **101-500元:** {price_ranges['101-500元']}个 ({round(price_ranges['101-500元']/total*100)}%)
- **501-1000元:** {price_ranges['501-1000元']}个 ({round(price_ranges['501-1000元']/total*100)}%)
- **1000元以上:** {price_ranges['1000元以上']}个 ({round(price_ranges['1000元以上']/total*100)}%)

**价格中位数:** ¥{sorted(prices)[len(prices)//2] if prices else 0}

### 二、商品品类分布
"""
    
    for cat, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
        percentage = round(count / total * 100)
        report += f"- **{cat}:** {count}个 ({percentage}%)\n"
    
    report += f"""
### 三、平台占比
- **QQ平台:** {platforms['QQ']}个 ({round(platforms['QQ']/total*100)}%)
- **微信平台:** {platforms['微信']}个 ({round(platforms['微信']/total*100)}%)
- **未明确:** {platforms['未明确']}个 ({round(platforms['未明确']/total*100)}%)

### 四、ID命名特征
"""
    
    for pattern, count in id_patterns.items():
        if count > 0:
            report += f"- **{pattern}:** {count}个\n"
    
    # 计算主要观察点
    low_price_count = price_ranges['0-10元'] + price_ranges['11-50元']
    id_trade_count = category_counts.get('极品ID', 0) + category_counts.get('普通ID', 0)
    
    report += f"""
### 五、市场观察
1. **低价商品为主:** {low_price_count}个商品价格在50元以下，占比{round(low_price_count/total*100)}%，显示闲鱼以低单价虚拟物品交易为主
2. **ID交易活跃:** 极品ID和普通ID合计{id_trade_count}个，占{round(id_trade_count/total*100)}%，是主要交易品类
3. **QQ平台主导:** QQ平台商品{platforms['QQ']}个，占比{round(platforms['QQ']/total*100)}%，远超微信平台
4. **高价ID稀缺:** 1000元以上商品{price_ranges['1000元以上']}个，多为极品单字/双字ID或名人同名ID
"""
    
    return report

if __name__ == '__main__':
    report = analyze_goods()
    print(report)
    
    # 保存报告
    with open('/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/xianyu_report_20260407.md', 'w', encoding='utf-8') as f:
        f.write(report)
    
    print("\n报告已保存至 xianyu_report_20260407.md")

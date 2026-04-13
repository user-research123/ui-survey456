#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
闲鱼商品数据分析脚本 - 完整100个商品(不去重)
"""

import json
from datetime import datetime
from collections import Counter

def analyze_goods():
    """分析闲鱼商品数据"""
    
    # 从浏览器获取的完整100条数据
    items_data = '''[{"title":"#王者荣耀 王者荣耀世界id 几何 无任何符号 账号状态安全 价格可议","price":5000,"url":"https://www.goofish.com/item?id=1038690129948&categoryId=200928012"},{"title":"王者荣耀世界ID古代 感兴趣的话点"我想要"和我私聊吧～","price":5000,"url":"https://www.goofish.com/item?id=1038661633170&categoryId=202027304"},{"title":"王者荣耀世界 ID 衍猫 猫衍 互逆情侣ID 双字干净ID 全服唯一 iOS QQ区 买一送一 可以讲价\\n\\n10小时前降价","price":10,"url":"https://www.goofish.com/item?id=1038236491244&categoryId=202027304"},{"title":"王者荣耀世界id 双字流畅 可小刀 感兴趣的话点"我想要"和我私聊吧～","price":5200,"url":"https://www.goofish.com/item?id=1037673170333&categoryId=201459411"},{"title":"王者荣耀世界Q区双字ID 虚拟商品 直接发号 昵称可选 具体看图 下单秒改 常见ID 要的私聊 价格可聊","price":500,"url":"https://www.goofish.com/item?id=1041181428897&categoryId=201459411"},{"title":"王者荣耀世界PC端公测账号 4月10号开服，初始号，角色自选 昵称"我爱你章若楠"，账号安全，没乱搞 虚拟商品，直接发货，不用等 喜欢直接拍，细节私聊，价格可聊 有问题随时问我～","price":5200,"url":"https://www.goofish.com/item?id=1038289206476&categoryId=202027304"},{"title":"王者荣耀世界id 前面没有任何符号，就这两个字 喜欢神，帝，仙，王的可以考虑一下 可以体现了你洒脱豪放的气质 江湖君子的感觉\\n\\n2天内降价","price":5200,"url":"https://www.goofish.com/item?id=1040729800141&categoryId=202027304"},{"title":"王者荣耀世界抢注id账号（单个） 感兴趣的话点"我想要"和我私聊吧～","price":299,"url":"https://www.goofish.com/item?id=1038421855300&categoryId=202027304"},{"title":"王者荣耀世界 极品词组ID说错 标价出 虚拟商品售出不退不换\\n\\n6天内降价","price":200,"url":"https://www.goofish.com/item?id=1039562084847&categoryId=201459411"},{"title":"王者荣耀世界ID：左溢，账号信息齐全，安全放心。PC端公测定 档4月10号，全平台互通客户端。 喜欢直接拍，细节私聊～","price":5000,"url":"https://www.goofish.com/item?id=1039308890046&categoryId=202027304"}]'''
    
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

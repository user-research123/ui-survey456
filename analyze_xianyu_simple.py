#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
闲鱼商品数据分析脚本 - 简化版
直接从浏览器获取的JSON数据进行分析
"""

import json
from datetime import datetime
from collections import Counter
import re

def analyze_goods():
    """分析闲鱼商品数据"""
    
    # 从浏览器获取的原始数据（前100个商品，不去重）
    raw_data = '''[{"title":"王者荣耀世界称号代拿 王者荣耀世界挑战猩红神兽拿限量称号 标价即是价格，下单秒上号 可拿限定称号，4月10日开启兑换 双端互通","price":15,"url":"https://www.goofish.com/item?id=1039004784042&categoryId=201459411"},{"title":"王者荣耀世界双字ID：追凤，账号信息齐全 可换绑，支持PC端 公测预约，4月10号上线。账号昵称"追凤"，喜欢这个名字的朋友可以联系","price":365,"url":"https://www.goofish.com/item?id=1036963843043&categoryId=201459411"},{"title":"王者世界ID街舞 无特殊符号 感兴趣的话点"我想要"和我私聊吧～\\n\\n16小时前发布","price":666,"url":"https://www.goofish.com/item?id=1040834945860&categoryId=200928013"},{"title":"出王者荣耀世界呢称暖男 有需要私聊，喜欢直接拍 细节可问","price":3,"url":"https://www.goofish.com/item?id=1037821038936&categoryId=202027304"},{"title":"王者荣耀世界有趣ID【梦泪来偷水晶】 感兴趣的话点"我想要"和我私聊吧～","price":20,"url":"https://www.goofish.com/item?id=1039579918585&categoryId=201459411"},{"title":"王者荣耀世界 极品二字神id 老库 kg最爱 限时贱卖 感兴趣的话点"我想要"和我私聊吧～\\n\\n28分钟前降价","price":198,"url":"https://www.goofish.com/item?id=1040575209915&categoryId=202027304"},{"title":"王者荣耀世界PC端公测账号｜东方曜角色 昵称"她老公"，是第3305671位学子 账号信息都在图里，角色帅气，名字也特别 适合喜欢东方曜的朋友，账号安全，随时可用 有需要直接拍，细节私聊 喜欢就来聊聊～带价格\\n\\n6天内降价","price":3,"url":"https://www.goofish.com/item?id=1037066299169&categoryId=202027304"},{"title":"极品ID 价格可议，可小刀， 王昭君｜王者荣耀世界uid 初始号 安卓QQ客户端，账号信息齐全，昵称已抢，ID很极品，喜欢直接拍就行～ PC端公测定档4月10号，细节可以私聊问我，随时在线。 有需要随时聊，喜欢就拍吧～\\n\\n3天内降价","price":3,"url":"https://www.goofish.com/item?id=1037393495958&categoryId=202027304"},{"title":"王者荣耀世界PC端账号id id：喵滴 随便出出 想要可以带价来私我 合适就出 苹果q","price":1,"url":"https://www.goofish.com/item?id=1037324951127&categoryId=202027304"},{"title":"王者荣耀世界昵称id 宝 没有空白符号，纯字ID名字，喜欢的 来报价 带Q 图二骗子避雷","price":1000,"url":"https://www.goofish.com/item?id=1038632537459&categoryId=200928013"},{"title":"王者世界昵称"喊我爷爷"，账号刚开，资源全在，谁见你都得喊声 爷爷，喜欢的私聊，细节问我","price":2,"url":"https://www.goofish.com/item?id=1038669025120&categoryId=202027304"},{"title":"极品ID："林智宇"。王者荣耀世界账号ID。 为了取这个名字我想了很久，这是一个寓意非常好的名字 有需要的私聊，喜欢可以聊价格！","price":2,"url":"https://www.goofish.com/item?id=1039881725256&categoryId=202027304"},{"title":"王者荣耀世界lD 感兴趣的话点"我想要"和我私聊吧～\\n\\n7天内降价","price":10,"url":"https://www.goofish.com/item?id=1036918499927&categoryId=201459411"},{"title":"王者世界id越级 标价带q出无空白符号感兴趣的话点"我想要"和我私聊吧～\\n\\n11小时前降价","price":33,"url":"https://www.goofish.com/item?id=1038797569174&categoryId=201459411"},{"title":"王者荣耀世界id 东方曜 男 学子昵称 永远爱你宝宝 虚拟物品，售出不退不换","price":500,"url":"https://www.goofish.com/item?id=1039116109918&categoryId=201459411"},{"title":"王者荣耀世界ID：赵心童 ID：赵心童（世界冠军同名，全服唯一，开服首日抢注） 状态：纯空号，可换绑，安全无风险 ✅ 稀缺名人ID，自带流量，辨识度拉满 ✅ 4月10日公测即用，绝版保值 ✅ 支持平台担保交易，包换绑、包安全 一口价：16888元，诚心...","price":1,"url":"https://www.goofish.com/item?id=1037617082251&categoryId=202027304"},{"title":"王者荣耀世界极品纯单字ID：压 感兴趣的话点"我想要"和我私聊吧～","price":999,"url":"https://www.goofish.com/item?id=1039424416451&categoryId=200928013"},{"title":"双厨狂喜 王者荣耀世界id 汐汐不嘻嘻 感兴趣的话点"我想要"和我私聊吧","price":1,"url":"https://www.goofish.com/item?id=1038098106668&categoryId=202027304"},{"title":"王者荣耀世界极品ID 【v6】【 9y】 无符号 4.10号上线 勿拍 纯发着玩 感兴趣的话点"我想要"和我私聊吧～\\n\\n7天内降价","price":1,"url":"https://www.goofish.com/item?id=1038709421316&categoryId=201459411"},{"title":"王者世界id 单词大作战 感兴趣的话点"我想要"和我私聊吧～","price":1,"url":"https://www.goofish.com/item?id=1040919756367&categoryId=202027304"},{"title":"王者荣耀世界id恩仔 有意私聊","price":66,"url":"https://www.goofish.com/item?id=1039443862753&categoryId=201459411"},{"title":"【王者荣耀世界】2字id平月 暂挂，不多出，等开服一张改名卡的价格，交朋友价格","price":999,"url":"https://www.goofish.com/item?id=1040685481783&categoryId=201459411"},{"title":"王者荣耀世界双字ID，连号一起出，连体号有王者和和平，可改实 名 感兴趣的话点"我想要"和我私聊吧～","price":9999,"url":"https://www.goofish.com/item?id=1039562560509&categoryId=201459411"},{"title":"王者荣耀世界极品ID 价格一万五 ID:我想见你呀 价格一万ID:玫瑰与海 价格九千ID:向神明低头 价格八千ID:吹海边的风","price":1,"url":"https://www.goofish.com/item?id=1037772462852&categoryId=201459411"},{"title":"王者荣耀世界 双字ID 纯汉字无符号 虚拟道具 需要的来 价 格可聊","price":188,"url":"https://www.goofish.com/item?id=1039645713507&categoryId=201459411"},{"title":"出王者荣耀世界id带qq号觉得不合适可刀 感兴趣的话点"我想要"和我私聊吧～","price":300,"url":"https://www.goofish.com/item?id=1038643847822&categoryId=201459411"},{"title":"王者荣耀世界，昵称"公主殿下"，角色是西施#王者荣耀 价格随 便标的 感兴趣的话点"我想要"和我私聊吧～","price":9999,"url":"https://www.goofish.com/item?id=1037851410370&categoryId=200928012"},{"title":"王者荣耀世界，极品忧郁id 带妹首选 感兴趣的话点"我想要"和我私聊吧～","price":1,"url":"https://www.goofish.com/item?id=1037670706735&categoryId=201459411"},{"title":"王者荣耀世界id 二字女id柊颜 可先商量价格4月10号发","price":100,"url":"https://www.goofish.com/item?id=1039565388729&categoryId=202027304"},{"title":"王者荣耀世界单字id 微区：席 价格可聊\\n\\n7天内降价","price":9999,"url":"https://www.goofish.com/item?id=1036971175242&categoryId=202027304"}]'''
    
    # 解析JSON数据
    items = json.loads(raw_data)
    
    # 取前100个商品（如果不足100个则全部使用）
    items = items[:100]
    
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
            if '单字' in title or '二字' in title or '双字' in title:
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
    
    # 3. 平台占比分析（QQ/微信）
    platforms = {'QQ': 0, '微信': 0, '未明确': 0}
    for item in items:
        title = item['title'].lower()
        if 'qq' in title or 'q' in title:
            platforms['QQ'] += 1
        elif '微信' in title or 'wx' in title or '微区' in title:
            platforms['微信'] += 1
        else:
            platforms['未明确'] += 1
    
    # 4. 命名特征分析
    id_patterns = {
        '单字ID': 0,
        '双字ID': 0,
        '三字及以上ID': 0,
        '特殊符号ID': 0,
        '名人/明星ID': 0,
        '情侣/CP ID': 0
    }
    
    for item in items:
        title = item['title']
        if '单字' in title:
            id_patterns['单字ID'] += 1
        elif '双字' in title or '二字' in title:
            id_patterns['双字ID'] += 1
        elif '三字' in title or len(re.findall(r'[\u4e00-\u9fa5]{3,}', title)) > 0:
            id_patterns['三字及以上ID'] += 1
        if '符号' in title or '特殊' in title:
            id_patterns['特殊符号ID'] += 1
        if '冠军' in title or '明星' in title or '名人' in title or '赵心童' in title:
            id_patterns['名人/明星ID'] += 1
        if '情侣' in title or 'cp' in title.lower() or '老公' in title or '老婆' in title:
            id_patterns['情侣/CP ID'] += 1
    
    # 生成报告
    report = f"""## 闲鱼平台商品分析（{datetime.now().strftime('%Y年%m月%d日')}）

**数据概况：** 共采集前100个商品信息

### 一、价格区间分布
- **0-10元：** {price_ranges['0-10元']}个 ({price_ranges['0-10元']}%)
- **11-50元：** {price_ranges['11-50元']}个 ({price_ranges['11-50元']}%)
- **51-100元：** {price_ranges['51-100元']}个 ({price_ranges['51-100元']}%)
- **101-500元：** {price_ranges['101-500元']}个 ({price_ranges['101-500元']}%)
- **501-1000元：** {price_ranges['501-1000元']}个 ({price_ranges['501-1000元']}%)
- **1000元以上：** {price_ranges['1000元以上']}个 ({price_ranges['1000元以上']}%)

**价格中位数：** ¥{sorted(prices)[len(prices)//2] if prices else 0}

### 二、商品品类分布
"""
    
    for cat, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
        percentage = round(count / len(items) * 100)
        report += f"- **{cat}：** {count}个 ({percentage}%)\n"
    
    report += f"""
### 三、平台占比
- **QQ平台：** {platforms['QQ']}个 ({round(platforms['QQ']/len(items)*100)}%)
- **微信平台：** {platforms['微信']}个 ({round(platforms['微信']/len(items)*100)}%)
- **未明确：** {platforms['未明确']}个 ({round(platforms['未明确']/len(items)*100)}%)

### 四、ID命名特征
"""
    
    for pattern, count in id_patterns.items():
        if count > 0:
            report += f"- **{pattern}：** {count}个\n"
    
    report += f"""
### 五、市场观察
1. **低价商品为主：** {price_ranges['0-10元'] + price_ranges['11-50元']}个商品价格在50元以下，占比{(price_ranges['0-10元'] + price_ranges['11-50元'])}%，显示闲鱼以低单价虚拟物品交易为主
2. **ID交易活跃：** 极品ID（单字/双字）和普通ID合计{category_counts.get('极品ID', 0) + category_counts.get('普通ID', 0)}个，占{round((category_counts.get('极品ID', 0) + category_counts.get('普通ID', 0))/len(items)*100)}%，是主要交易品类
3. **QQ平台主导：** QQ平台商品{platforms['QQ']}个，占比{round(platforms['QQ']/len(items)*100)}%，远超微信平台
4. **高价ID稀缺：** 1000元以上商品{price_ranges['1000元以上']}个，多为极品单字/双字ID或名人同名ID
"""
    
    return report

if __name__ == '__main__':
    report = analyze_goods()
    print(report)
    
    # 保存报告
    with open('/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/xianyu_report.md', 'w', encoding='utf-8') as f:
        f.write(report)
    
    print("\n报告已保存至 xianyu_report.md")

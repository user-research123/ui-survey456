#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分析闲鱼商品数据 - 2026年4月1日采集
"""

import pandas as pd
import re
from collections import Counter

# 读取Excel文件
file_path = '/Users/jiewen/Desktop/闲鱼-搜索关键词列表采集4.1.xlsx'
df = pd.read_excel(file_path)

print(f"总行数: {len(df)}")
print(f"\n列名: {df.columns.tolist()}")
print(f"\n前5行数据:")
print(df.head())

# 提取价格和标题 - 使用正确的列名
if '现价' in df.columns and '商品' in df.columns:
    prices = []
    titles = []
    
    for idx, row in df.iterrows():
        price_str = str(row['现价']) if pd.notna(row['现价']) else ''
        title = str(row['商品']) if pd.notna(row['商品']) else ''
        
        # 提取价格数字
        price_match = re.search(r'¥?\s*(\d+\.?\d*)', price_str)
        if price_match:
            price = float(price_match.group(1))
            prices.append(price)
            titles.append(title)
    
    print(f"\n成功提取 {len(prices)} 个商品")
    
    # 价格统计
    if prices:
        print(f"\n=== 价格分布分析 ===")
        print(f"价格范围: ¥{min(prices):.2f} - ¥{max(prices):.2f}")
        print(f"平均价格: ¥{sum(prices)/len(prices):.2f}")
        
        sorted_prices = sorted(prices)
        median_idx = len(sorted_prices) // 2
        if len(sorted_prices) % 2 == 0:
            median_price = (sorted_prices[median_idx-1] + sorted_prices[median_idx]) / 2
        else:
            median_price = sorted_prices[median_idx]
        print(f"中位数价格: ¥{median_price:.2f}")
        
        high_price_count = sum(1 for p in prices if p >= 10000)
        print(f"高价商品(≥¥10,000): {high_price_count} 个 ({high_price_count/len(prices)*100:.1f}%)")
        
        # 价格区间分布
        print(f"\n价格区间分布:")
        ranges = [
            (0, 500, "0-500"),
            (500, 1000, "500-1000"),
            (1000, 5000, "1000-5000"),
            (5000, 10000, "5000-10000"),
            (10000, 50000, "10000-50000"),
            (50000, float('inf'), "50000+")
        ]
        
        for low, high, label in ranges:
            count = sum(1 for p in prices if low <= p < high)
            percentage = count / len(prices) * 100
            print(f"{label}: {count} 个 ({percentage:.1f}%)")
    
    # 商品分类 - 优化版
    print(f"\n=== 商品分类分析 ===")
    
    categories = []
    for title in titles:
        title_lower = title.lower()
        
        # 代练/代打服务
        if any(keyword in title_lower for keyword in ['代打', '帮打', '代过', '代肝', '代刷', '狂暴代打', '红buff', '跟打']):
            categories.append('代练/代打服务')
        # 充值/代充
        elif any(keyword in title_lower for keyword in ['代充', '充值', '月卡', '通行证', '有偿钻', '首充', '折扣号', '内购', '买断版', 'gm后台', '无限资源', '礼包码']):
            categories.append('充值/代充服务')
        # 账号相关
        elif any(keyword in title_lower for keyword in ['换绑', '解绑', '直登', '小号', 'id代挂', 'id代售', '腾卡', '刷初始', '双字id', '开服秒改', '代挂']):
            categories.append('账号/ID交易')
        # 虚拟道具
        elif any(keyword in title_lower for keyword in ['道具', '宠物', '称号', 'buff', '皮肤', 'cdk', '激活码', '礼包', '兑换码', '霜降牛肉', '粗毛皮', '三金', '融合', '异常物', '装扮', '微博装扮', '钻石内部礼包']):
            categories.append('虚拟道具/资源')
        # 捞人/组队服务
        elif '捞人' in title_lower or '捞你' in title_lower:
            categories.append('捞人/组队服务')
        # 游戏攻略/辅助
        elif any(keyword in title_lower for keyword in ['攻略', '科技', '辅助', '估价', '教学', 'ppt', '演讲']):
            categories.append('攻略/辅助工具')
        # 安装包/资源文件
        elif any(keyword in title_lower for keyword in ['安装包', 'mod', '材质包', '角色卡', '壁纸', '素材', 'cg鉴赏', '录屏', '人物卡', '补丁', '存档']):
            categories.append('游戏资源/安装包')
        # PC单机游戏/Steam游戏
        elif any(keyword in title_lower for keyword in ['steam', 'pc单机', 'cdk', '正版激活码', 'wrc', '东方铁红', '环世界', '雨世界', '神舞幻想', '锻造屋的物语', 'tnt冒险之旅', '彩虹物语', '天逆沉默传奇', '太古神王', '粘粘世界']):
            categories.append('PC单机游戏')
        # 小说/文学作品
        elif any(keyword in title_lower for keyword in ['小说', '傅辰夜', '林霜雪', '时贺州', '被未婚妻偷走时间', '韩轻小说', '有声书', '音频mp3']):
            categories.append('小说/文学')
        # 手绘/约稿服务
        elif any(keyword in title_lower for keyword in ['画画约稿', '手绘', '定制牌']):
            categories.append('手绘/约稿服务')
        # 花园/种植类游戏物品
        elif any(keyword in title_lower for keyword in ['我的花园世界', '卖花', '稀有花', '竞赛分']):
            categories.append('花园类物品交易')
        # 其他服务
        else:
            categories.append('其他')
    
    # 统计分类
    category_counter = Counter(categories)
    total = len(categories)
    
    print(f"\n主要包括以下类型商品:")
    for cat, count in category_counter.most_common():
        percentage = count / total * 100
        print(f"- {cat}: {count} 个 ({percentage:.1f}%)")
    
    # 保存详细数据
    result_df = pd.DataFrame({
        '标题': titles,
        '价格': prices,
        '分类': categories
    })
    
    output_path = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/xianyu_analysis_4_1.xlsx'
    result_df.to_excel(output_path, index=False, engine='openpyxl')
    print(f"\n详细数据已保存到: {output_path}")

else:
    print("未找到'价格'或'商品标题'列")
    print(f"可用列: {df.columns.tolist()}")

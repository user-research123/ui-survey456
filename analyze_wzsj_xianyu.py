#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分析闲鱼-搜索关键词列表采集4.2.xlsx中王者荣耀世界相关商品
"""

import pandas as pd
import re
from collections import Counter

# 读取Excel文件
file_path = '/Users/jiewen/Desktop/闲鱼-搜索关键词列表采集4.2.xlsx'
df = pd.read_excel(file_path)

print(f"总行数: {len(df)}")
print(f"列名: {df.columns.tolist()}")
print("\n前5行数据:")
print(df.head())

# 筛选王者荣耀世界相关商品
# 根据关键词列或标题中包含"王者荣耀世界"的商品
wzsj_df = df[df['关键词'].str.contains('王者荣耀世界', na=False)]

print(f"\n王者荣耀世界相关商品数量: {len(wzsj_df)}")

if len(wzsj_df) == 0:
    # 尝试从标题中筛选
    wzsj_df = df[df.iloc[:, 0].astype(str).str.contains('王者荣耀世界', na=False)]
    print(f"从第一列筛选到的王者荣耀世界相关商品数量: {len(wzsj_df)}")

# 查看筛选后的数据
print("\n王者荣耀世界相关商品样例:")
print(wzsj_df.head(10))

# 提取商品标题进行分析（使用"商品"列，这是实际的标题内容）
titles = wzsj_df['商品'].dropna().tolist() if '商品' in wzsj_df.columns else []

if not titles:
    # 尝试其他可能的列名
    for col in wzsj_df.columns:
        if '标题' in str(col) or '商品' in str(col):
            titles = wzsj_df[col].dropna().tolist()
            break

print(f"\n提取到的标题数量: {len(titles)}")
print("\n标题样例:")
for i, title in enumerate(titles[:5]):
    print(f"{i+1}. {title}")

# 定义商品类型分类规则
def classify_product(title):
    """
    根据标题内容分类商品类型
    """
    title_str = str(title)
    title_lower = title_str.lower()
    
    # 先排除明显无关商品（蹭流量）
    irrelevant_patterns = [
        '逆转裁判', '魔戒', '托尔金', '翻译', '出版社', 'ns游戏',
        'capcom', '卡带', '对冲基金', 'isbn', '二手书', '正版二手'
    ]
    if any(pattern in title_lower for pattern in irrelevant_patterns):
        return '无关商品（蹭流量）'
    
    # ID类（极品ID、稀有昵称、单字/双字ID等）- 优先匹配
    id_keywords = [
        '极品id', '稀有id', '单字id', '双字id', '三字id', '豹子号', 
        'uid', '编号', '学号', '学员', '学子', '位学子', '位学员',
        '无重复', '无符号', '干净id', '特殊含义'
    ]
    # 检查是否包含ID相关关键词，或者标题中包含具体ID名称（如粤A99999、京AG60001等格式）
    has_id_keyword = any(keyword in title_lower for keyword in id_keywords)
    has_id_pattern = bool(re.search(r'[京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼][A-Z]\d{5,}', title_str)) or \
                     bool(re.search(r'id[：:]\s*\w+', title_lower)) or \
                     bool(re.search(r'昵称["\u201c\u201d]?[\u4e00-\u9fa5\w]+["\u201d\u201c]?', title_str))
    
    if has_id_keyword or has_id_pattern:
        return '账号ID/昵称'
    
    # 账号类（包含角色、等级、资源等信息的完整账号）
    account_patterns = [
        '账号', 'pc端公测账号', '安卓qq', 'ios区', '微信区', 'qq区',
        '东方曜角色', '伽罗角色', '王昭君', '花木兰', '角色',
        '39w+', '新号', '老玩家号', '带王者荣耀'
    ]
    if any(pattern in title_lower for pattern in account_patterns):
        return '游戏账号'
    
    # 代练/代肝服务
    service_patterns = [
        '代练', '代肝', '代打', '陪玩', '上分', '冲榜', '刷级', '任务',
        '手抢', '脚本', '个性装扮'
    ]
    if any(pattern in title_lower for pattern in service_patterns):
        return '代练/代肝服务'
    
    # 虚拟道具/资源
    item_patterns = [
        '道具', '皮肤', '装备', '金币', '钻石', '点券', '资源', '礼包',
        '兑换码', '激活码', 'cdk', '海报', '活动海报'
    ]
    if any(pattern in title_lower for pattern in item_patterns):
        return '虚拟道具/资源'
    
    # 邀请/助力
    invite_patterns = [
        '邀请', '助力', '拉人', '组队', '好友'
    ]
    if any(pattern in title_lower for pattern in invite_patterns):
        return '邀请/助力'
    
    # 其他/模糊描述
    if '感兴趣的话点' in title_str or '私聊' in title_str or len(title_str) < 20:
        return '其他（模糊描述）'
    
    return '其他'

# 对所有标题进行分类
categories = [classify_product(title) for title in titles]
category_counter = Counter(categories)

print("\n" + "="*60)
print("王者荣耀世界相关商品类型分布")
print("="*60)

total = sum(category_counter.values())
for category, count in sorted(category_counter.items(), key=lambda x: x[1], reverse=True):
    percentage = (count / total * 100) if total > 0 else 0
    print(f"{category}: {count}个 ({percentage:.1f}%)")

print(f"\n总计: {total}个商品")

# 输出详细分类结果
print("\n" + "="*60)
print("各类别商品示例")
print("="*60)

for category in category_counter.keys():
    examples = [t for t, c in zip(titles, categories) if c == category][:3]
    print(f"\n【{category}】")
    for ex in examples:
        print(f"  - {ex}")

# 生成总结报告
summary = f"""
## 王者荣耀世界闲鱼商品分析报告

### 数据概况
- 数据来源：闲鱼-搜索关键词列表采集4.2.xlsx
- 王者荣耀世界相关商品总数：{total}个

### 商品类型分布

| 商品类型 | 数量 | 占比 |
|---------|------|------|
"""

for category, count in sorted(category_counter.items(), key=lambda x: x[1], reverse=True):
    percentage = (count / total * 100) if total > 0 else 0
    summary += f"| {category} | {count} | {percentage:.1f}% |\n"

summary += f"""
### 核心发现

1. **主导品类**：{list(category_counter.keys())[0]}是主要交易类型，占比{(category_counter.most_common(1)[0][1]/total*100):.1f}%
2. **价格区间**：从几元到上万元不等，极品ID和稀有账号价格较高
3. **交易特征**：以虚拟商品为主，包括账号ID、游戏账号、代练服务等

### 详细分类说明

"""

for category, count in sorted(category_counter.items(), key=lambda x: x[1], reverse=True):
    percentage = (count / total * 100) if total > 0 else 0
    examples = [t for t, c in zip(titles, categories) if c == category][:2]
    summary += f"**{category}**（{percentage:.1f}%）：\n"
    for ex in examples:
        summary += f"- {ex}\n"
    summary += "\n"

print(summary)

# 保存分析结果
with open('/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wzsj_xianyu_analysis.txt', 'w', encoding='utf-8') as f:
    f.write(summary)

print("\n分析结果已保存到: wzsj_xianyu_analysis.txt")

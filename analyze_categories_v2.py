import pandas as pd
from collections import Counter

# 读取Excel文件
file_path = '/Users/jiewen/Desktop/闲鱼-搜索关键词列表采集-王者.xlsx'
df = pd.read_excel(file_path, sheet_name='Sheet1')

print(f"总行数: {len(df)}")
print("\n" + "="*80)

# 定义品类分类函数
def categorize_item(row):
    """根据标题标签和商品描述判断品类"""
    title_tag = str(row.get('标题标签', '')).lower() if pd.notna(row.get('标题标签')) else ''
    product = str(row.get('商品', '')).lower() if pd.notna(row.get('商品')) else ''
    description = str(row.get('描述栏_文本', '')).lower() if pd.notna(row.get('描述栏_文本')) else ''
    
    text = title_tag + ' ' + product + ' ' + description
    
    # 定义品类规则（按优先级排序）
    if any(kw in text for kw in ['id', '昵称', '名字', '单字', '二字', '三字', '四字', '五字', '六字', '极品id', '稀有id', '豹子号']):
        return '游戏ID/昵称'
    elif any(kw in text for kw in ['截图', '纪念', '收藏', '装饰', '角色截图', '上线纪念']):
        return '游戏截图/纪念品'
    elif any(kw in text for kw in ['代肝', '代练', '代打', '托管', '帮打', '帮忙']):
        return '代肝/代练服务'
    elif any(kw in text for kw in ['账号', '成品号', '初始号', '自抽号']) and 'id' not in text and '昵称' not in text:
        return '游戏账号'
    elif any(kw in text for kw in ['皮肤', '时装', '外观', '装扮', 'cosplay']):
        return '皮肤/外观'
    elif any(kw in text for kw in ['道具', '装备', '材料', '资源', '金币', '钻石', '点券']):
        return '游戏道具/资源'
    elif any(kw in text for kw in ['攻略', '教程', '指南', '教学', '技巧']):
        return '攻略/教程'
    elif any(kw in text for kw in ['周边', '手办', '模型', '公仔', '摆件', '钥匙扣']):
        return '实体周边'
    elif any(kw in text for kw in ['兑换码', 'cdk', '激活码', '礼包码', '序列号']):
        return '兑换码/CDK'
    elif any(kw in text for kw in ['邀请', '助力', '帮忙点击', '拉人']):
        return '邀请/助力'
    elif any(kw in text for kw in ['陪玩', '组队', '一起玩', '搭档']):
        return '陪玩/组队'
    elif any(kw in text for kw in ['测试资格', '内测', '公测', '体验服', '资格']):
        return '测试资格'
    else:
        return '其他'

# 对每一行进行分类
df['品类'] = df.apply(categorize_item, axis=1)

print("\n【未去重】原始品类分布:")
category_counts = df['品类'].value_counts()
total = len(df)
for category, count in category_counts.items():
    percentage = (count / total) * 100
    print(f"{category}: {count}条 ({percentage:.1f}%)")

print("\n" + "="*80)

# 查看卖家IP地址的分布情况
print("\n卖家IP地址分布:")
ip_distribution = df['卖家IP地址'].value_counts()
print(ip_distribution)
print(f"\n唯一卖家数量: {len(ip_distribution)}")

print("\n" + "="*80)

# 方法1: 按卖家IP去重，每个卖家只统计其第一个商品的品类
print("\n【方法1：按卖家IP去重】每个卖家只计一次（取第一个商品品类）:")
df_sorted = df.sort_values('卖家IP地址')
seller_first_category = df_sorted.groupby('卖家IP地址')['品类'].first()
category_method1 = seller_first_category.value_counts()

total_method1 = len(seller_first_category)
for category, count in category_method1.items():
    percentage = (count / total_method1) * 100
    print(f"{category}: {count}个卖家 ({percentage:.1f}%)")

print("\n" + "="*80)

# 方法2: 按卖家IP去重，统计每个卖家涉及的所有品类（一个卖家可能有多个品类）
print("\n【方法2：按卖家IP去重】统计每个卖家的品类多样性:")
seller_categories = df.groupby('卖家IP地址')['品类'].apply(lambda x: list(set(x)))
print(f"\n共有 {len(seller_categories)} 个独立卖家")

# 统计所有卖家涉及的品类集合
all_seller_categories = []
for categories in seller_categories:
    all_seller_categories.extend(categories)

unique_categories_from_sellers = Counter(all_seller_categories)
print(f"\n去重后涉及的品类总数: {len(unique_categories_from_sellers)}")
for category, count in unique_categories_from_sellers.most_common():
    print(f"{category}: {count}个卖家涉及")

print("\n" + "="*80)

# 详细列出每个卖家的品类
print("\n各卖家品类详情:")
for ip, categories in seller_categories.items():
    print(f"IP={ip}: {categories}")

# 保存详细结果
result_df = pd.DataFrame({
    '品类': category_method1.index,
    '卖家数量': category_method1.values,
    '占比(%)': [(c / total_method1) * 100 for c in category_method1.values]
})

result_df.to_excel('/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/品类分析结果_去重版.xlsx', index=False)
print(f"\n\n结果已保存到: /Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/品类分析结果_去重版.xlsx")

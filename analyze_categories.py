import pandas as pd
import re
from collections import Counter, defaultdict

# 读取Excel文件
file_path = '/Users/jiewen/Desktop/闲鱼-搜索关键词列表采集-王者.xlsx'
df = pd.read_excel(file_path, sheet_name='Sheet1')

print(f"总行数: {len(df)}")
print(f"列名: {list(df.columns)}")
print("\n" + "="*80)

# 分析"商品"列和"标题标签"列，提取品类信息
# 首先查看所有唯一的"标题标签"
print("\n标题标签分布:")
title_tags = df['标题标签'].dropna()
print(title_tags.value_counts())

print("\n" + "="*80)

# 分析"商品"列的内容，尝试提取品类
#查看一些样例数据
print("\n商品列样例（前20条）:")
for i, row in df.head(20).iterrows():
    print(f"{i+1}. [{row.get('标题标签', 'N/A')}] {str(row['商品'])[:100]}")

print("\n" + "="*80)

# 基于标题标签和商品描述，手动定义品类分类规则
def categorize_item(row):
    """根据标题标签和商品描述判断品类"""
    title_tag = str(row.get('标题标签', '')).lower() if pd.notna(row.get('标题标签')) else ''
    product = str(row.get('商品', '')).lower() if pd.notna(row.get('商品')) else ''
    description = str(row.get('描述栏_文本', '')).lower() if pd.notna(row.get('描述栏_文本')) else ''
    
    text = title_tag + ' ' + product + ' ' + description
    
    # 定义品类规则
    if any(kw in text for kw in ['id', '昵称', '名字', '单字', '二字', '三字', '四字', '五字', '六字', '极品id', '稀有id']):
        return '游戏ID/昵称'
    elif any(kw in text for kw in ['截图', '纪念', '收藏', '装饰', '角色截图', '上线纪念']):
        return '游戏截图/纪念品'
    elif any(kw in text for kw in ['代肝', '代练', '代打', '托管', '帮打', '帮忙']):
        return '代肝/代练服务'
    elif any(kw in text for kw in ['账号', '号', '成品号', '初始号', '自抽号']):
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

print("\n品类分布统计:")
category_counts = df['品类'].value_counts()
print(category_counts)

print("\n" + "="*80)
print("\n品类比例:")
total = len(df)
for category, count in category_counts.items():
    percentage = (count / total) * 100
    print(f"{category}: {count}条 ({percentage:.1f}%)")

print("\n" + "="*80)

# 现在需要考虑"排除同一个人发送的信息"
# 由于数据中没有明确的发送人ID，我们尝试用"卖家IP地址"+"卖家口碑标签"+"部分商品特征来近似去重
# 但更合理的方式是：如果同一卖家的多个商品属于同一品类，只计一次

# 创建一个近似的卖家标识（组合IP地址和口碑标签）
df['卖家标识'] = df['卖家IP地址'].astype(str) + '_' + df['卖家口碑标签'].astype(str)

print("\n考虑卖家去重后的品类分布:")

# 对每个卖家，只保留其第一个商品的品类
seller_first_category = df.groupby('卖家标识')['品类'].first()
category_after_dedup = seller_first_category.value_counts()

print(category_after_dedup)

print("\n" + "="*80)
print("\n去重后品类比例:")
total_after_dedup = len(seller_first_category)
for category, count in category_after_dedup.items():
    percentage = (count / total_after_dedup) * 100
    print(f"{category}: {count}条 ({percentage:.1f}%)")

# 保存结果
result_df = pd.DataFrame({
    '品类': category_after_dedup.index,
    '数量': category_after_dedup.values,
    '比例(%)': [(c / total_after_dedup) * 100 for c in category_after_dedup.values]
})

result_df.to_excel('/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/品类分析结果.xlsx', index=False)
print(f"\n结果已保存到: /Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/品类分析结果.xlsx")

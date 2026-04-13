import pandas as pd

# 读取Excel文件
file_path = '/Users/jiewen/Desktop/闲鱼-搜索关键词列表采集-王者.xlsx'
df = pd.read_excel(file_path, sheet_name='Sheet1')

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

# 查看"其他"品类的商品
print("="*80)
print("【其他】品类的商品详情:")
print("="*80)
other_items = df[df['品类'] == '其他']
for idx, row in other_items.iterrows():
    print(f"\n行号: {idx+1}")
    print(f"卖家IP: {row['卖家IP地址']}")
    print(f"商品描述: {row['商品'][:200] if pd.notna(row['商品']) else 'N/A'}")
    print(f"描述栏文本: {row['描述栏_文本'][:200] if pd.notna(row['描述栏_文本']) else 'N/A'}")

print("\n" + "="*80)
print("【游戏账号】品类的商品详情:")
print("="*80)
account_items = df[df['品类'] == '游戏账号']
for idx, row in account_items.iterrows():
    print(f"\n行号: {idx+1}")
    print(f"卖家IP: {row['卖家IP地址']}")
    print(f"商品描述: {row['商品'][:200] if pd.notna(row['商品']) else 'N/A'}")
    print(f"描述栏文本: {row['描述栏_文本'][:200] if pd.notna(row['描述栏_文本']) else 'N/A'}")

# 查看所有包含"账号"关键词的商品，看看是否有被误分类的
print("\n" + "="*80)
print("所有包含'账号'关键词的商品:")
print("="*80)
account_keyword_items = df[df['商品'].astype(str).str.contains('账号', na=False)]
for idx, row in account_keyword_items.head(10).iterrows():
    print(f"\n行号: {idx+1}, 品类: {row['品类']}")
    print(f"商品描述: {row['商品'][:150] if pd.notna(row['商品']) else 'N/A'}")

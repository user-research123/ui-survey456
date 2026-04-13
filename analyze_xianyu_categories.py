import pandas as pd
from collections import Counter
import re
import glob
import os

# 查找桌面上的闲鱼文件
desktop_path = '/Users/jiewen/Desktop'
xianyu_files = glob.glob(os.path.join(desktop_path, '*闲鱼*3.31*.xlsx'))
if not xianyu_files:
    print("未找到匹配的文件")
    exit(1)

file_path = xianyu_files[0]
print(f"读取文件：{file_path}")

df = pd.read_excel(file_path)

print(f"\n总商品数量：{len(df)}")

# 定义分类规则（基于商品标题关键词）
category_rules = {
    '账号服务': ['解绑', '改绑', '换绑', '腾卡', '释放手机', '绑定', '账号'],
    '代肝/代打': ['代打', '代肝', '帮打', '通关', '刷', '打捞', '捞人', '上岸', '跑腿', '代扒皮'],
    '游戏充值': ['代充', '充值', '月卡', '通行证', '水晶', '钻石', '晶钻', '礼包', 'cdk', 'CDK', '激活码'],
    '游戏道具': ['道具', '装备', '皮肤', '称号', '头像', '头像框', '宠物', '蛋', '牛肉', '牛皮', '基因', '霜降'],
    '游戏攻略': ['攻略', '教程', '指南', '手册', '图鉴', '流程图', '养成'],
    '安装包/资格': ['安装包', '资格', '体验码', '激活码', '内测', '测试', '苹果安装包'],
    '游戏账号': ['账号', '帐号', 'PC 端公测号', '角色已创建'],
    '代练/升级': ['代练', '升级', '挂机', '脚本', '跑图', '自动'],
    'ID/昵称': ['ID', '昵称', '估价', '垂纱', '学号'],
    '周边/素材': ['壁纸', '插画', '素材', '电子版', 'PDF', '文档'],
    '其他': []
}

def categorize_product(title):
    """根据标题关键词对商品进行分类"""
    if pd.isna(title):
        return '未知'
    
    title_str = str(title)
    
    # 按优先级检查每个分类
    for category, keywords in category_rules.items():
        if category == '其他':
            continue
        for keyword in keywords:
            if keyword.lower() in title_str.lower():
                # 特殊处理：如果包含多个分类特征，优先判断更具体的
                if category == '游戏充值' and any(k in title_str for k in ['代充', '充值', '月卡']):
                    return category
                elif category == '账号服务' and any(k in title_str for k in ['解绑', '换绑', '改绑']):
                    return category
                elif category == '代肝/代打' and any(k in title_str for k in ['代打', '代肝', '捞人']):
                    return category
                else:
                    return category
    
    return '其他'

# 应用分类
df['分类'] = df['商品'].apply(categorize_product)

# 统计分类
category_counts = df['分类'].value_counts()
category_percentages = (df['分类'].value_counts(normalize=True) * 100).round(2)

print("\n=== 商品分类统计 ===")
print(f"\n{'分类':<15} {'数量':>6} {'比例':>10}")
print("-" * 35)
for cat in category_counts.index:
    count = category_counts[cat]
    pct = category_percentages[cat]
    print(f"{cat:<15} {count:>6} {pct:>9.2f}%")

print(f"\n总计：{len(df)}")

# 保存结果到 CSV
result_df = pd.DataFrame({
    '分类': category_counts.index,
    '数量': category_counts.values,
    '比例 (%)': category_percentages.values
})
result_df.to_csv('/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/xianyu_category_summary.csv', index=False, encoding='utf-8-sig')
print(f"\n结果已保存到：xianyu_category_summary.csv")

# 显示每个分类的示例商品
print("\n=== 各分类示例商品 ===")
for category in category_counts.index[:5]:  # 只显示前 5 个分类
    sample_products = df[df['分类'] == category]['商品'].head(2)
    print(f"\n【{category}】(共{category_counts[category]}个)")
    for i, product in enumerate(sample_products, 1):
        print(f"  {i}. {product[:80]}...")

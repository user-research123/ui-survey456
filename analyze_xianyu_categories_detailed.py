import pandas as pd
from collections import Counter
import re
import glob
import os

# 查找桌面上的闲鱼文件
desktop_path = '/Users/jiewen/Desktop'
xianyu_files = glob.glob(os.path.join(desktop_path, '*闲鱼*3.31*.xlsx'))
file_path = xianyu_files[0]

df = pd.read_excel(file_path)

# 优化后的分类规则（更细致的关键词匹配）
category_rules = {
    '账号交易/服务': ['解绑', '改绑', '换绑', '腾卡', '释放手机', '绑定', '账号', '帐号', '直登', '小号', '信用分'],
    '代练/代打': ['代打', '代肝', '帮打', '通关', '打捞', '捞人', '上岸', '跑腿', '代扒皮', '红 buff', '狂暴模式', '猩红神兽'],
    '游戏充值': ['代充', '充值', '月卡', '通行证', '水晶', '钻石', '晶钻', '礼包', '首充号', '折扣号'],
    'CDK/激活码': ['cdk', 'CDK', '激活码', '兑换码', '福利码', '序列号', 'steam', '国区', '正版'],
    '游戏道具': ['道具', '装备', '皮肤', '称号', '头像', '宠物', '蛋', '牛肉', '牛皮', '基因', '霜降', '材料'],
    '游戏攻略/教程': ['攻略', '教程', '指南', '手册', '图鉴', '流程图', '养成', '速通', '平民'],
    '安装包/测试资格': ['安装包', '资格', '体验码', '内测', '测试', '苹果安装包', 'iOS', '公测'],
    '游戏账号出售': ['账号已创建', '角色已创建', '账号出售', 'PC 端公测号', '昵称"', '垂纱'],
    'ID/昵称交易': ['ID', '双字 ID', '三字 ID', '四字 ID', '昵称', '估价', '学号', '改名'],
    '代练/脚本': ['代练', '升级', '挂机', '脚本', '跑图', '自动', '24 小时'],
    '周边/数字素材': ['壁纸', '插画', '素材', '电子版', 'PDF', '文档', '电子书'],
    '游戏服务器/私服': ['私服', '公益服', '不封', '港台服', '国际服', '俄服', '外服'],
    '其他': []
}

def categorize_product(title):
    """根据标题关键词对商品进行分类（优先级匹配）"""
    if pd.isna(title):
        return '未知'
    
    title_str = str(title)
    
    # 特殊规则优先判断
    # 1. CDK/激活码类
    if any(k in title_str.lower() for k in ['cdk', 'steam', '激活码', '兑换码', '序列号']):
        return 'CDK/激活码'
    
    # 2. 账号服务类
    if any(k in title_str for k in ['解绑', '改绑', '换绑', '腾卡', '释放手机']):
        return '账号交易/服务'
    
    # 3. 代练代打类
    if any(k in title_str for k in ['代打', '代肝', '帮打', '捞人', '上岸', '通关']):
        return '代练/代打'
    
    # 4. ID/昵称类
    if any(k in title_str for k in ['ID', '昵称', '估价', '学号']) and '账号' not in title_str:
        return 'ID/昵称交易'
    
    # 5. 安装包/资格类
    if any(k in title_str for k in ['安装包', '资格', '内测', '测试资格']):
        return '安装包/测试资格'
    
    # 6. 攻略教程类
    if any(k in title_str for k in ['攻略', '教程', '指南', '速通']):
        return '游戏攻略/教程'
    
    # 7. 游戏充值类
    if any(k in title_str for k in ['代充', '充值', '月卡', '通行证', '水晶', '钻石', '首充']):
        return '游戏充值'
    
    # 8. 游戏道具类
    if any(k in title_str for k in ['道具', '装备', '称号', '宠物', '蛋', '材料', '牛肉', '牛皮']):
        return '游戏道具'
    
    # 9. 脚本/挂机类
    if any(k in title_str for k in ['脚本', '挂机', '自动', '24 小时']):
        return '代练/脚本'
    
    # 10. 游戏服务器类
    if any(k in title_str for k in ['私服', '公益服', '不封', '港台服', '国际服', '俄服']):
        return '游戏服务器/私服'
    
    # 11. 周边素材类
    if any(k in title_str for k in ['壁纸', '插画', '素材', '电子版']):
        return '周边/数字素材'
    
    # 12. 账号出售（整号出售）
    if any(k in title_str for k in ['账号出售', '角色已创建', '账号已创建', 'PC 端']):
        return '游戏账号出售'
    
    return '其他'

# 应用分类
df['分类'] = df['商品'].apply(categorize_product)

# 统计分类
category_counts = df['分类'].value_counts(sort=False)
category_counts = category_counts.sort_values(ascending=False)
category_percentages = (df['分类'].value_counts(normalize=True) * 100).round(2)

print("=" * 70)
print("闲鱼《王者荣耀：世界》商品分类分析报告")
print("=" * 70)
print(f"\n数据日期：2026 年 3 月 31 日")
print(f"总商品数量：{len(df)} 个")

print("\n【商品分类统计】")
print(f"\n{'排名':<6}{'分类':<20}{'数量':>8}{'比例':>10}{'累计比例':>12}")
print("-" * 60)

cumulative_pct = 0
for rank, cat in enumerate(category_counts.index, 1):
    count = category_counts[cat]
    pct = category_percentages[cat]
    cumulative_pct += pct
    print(f"{rank:<6}{cat:<20}{count:>8}{pct:>9.2f}%{cumulative_pct:>11.2f}%")

print("-" * 60)
print(f"{'总计':<26}{len(df):>8}{'100.00%':>10}")

# 核心发现总结
print("\n【核心发现】")

top3_categories = category_counts.head(3)
total_top3 = top3_categories.sum()
pct_top3 = (total_top3 / len(df) * 100)

print(f"\n1. TOP3 主导品类（占比{pct_top3:.1f}%）:")
for i, (cat, count) in enumerate(top3_categories.items(), 1):
    pct = category_percentages[cat]
    print(f"   {i}. {cat}: {count}个 ({pct}%)")

# 虚拟服务 vs 实物/数字商品
service_categories = ['账号交易/服务', '代练/代打', '游戏充值', '代练/脚本', '游戏攻略/教程']
digital_categories = ['CDK/激活码', '安装包/测试资格', '周边/数字素材']
goods_categories = ['游戏道具', '游戏账号出售', 'ID/昵称交易']

service_count = sum(category_counts.get(cat, 0) for cat in service_categories)
digital_count = sum(category_counts.get(cat, 0) for cat in digital_categories)
goods_count = sum(category_counts.get(cat, 0) for cat in goods_categories)
other_count = category_counts.get('其他', 0) + category_counts.get('游戏服务器/私服', 0)

print(f"\n2. 服务类型分布:")
print(f"   • 虚拟服务（代练/充值/账号服务等）: {service_count}个 ({service_count/len(df)*100:.1f}%)")
print(f"   • 数字商品（CDK/安装包/素材等）: {digital_count}个 ({digital_count/len(df)*100:.1f}%)")
print(f"   • 游戏资产（道具/账号/ID 等）: {goods_count}个 ({goods_count/len(df)*100:.1f}%)")
print(f"   • 其他：{other_count}个 ({other_count/len(df)*100:.1f}%)")

# 价格区间分析（如果有价格数据）
if '现价' in df.columns:
    # 清理价格数据
    df['价格数值'] = df['现价'].astype(str).str.replace('¥', '').str.replace('\n', '').str.strip()
    df['价格数值'] = pd.to_numeric(df['价格数值'], errors='coerce')
    
    price_ranges = {
        '0-5 元': (0, 5),
        '5-10 元': (5, 10),
        '10-20 元': (10, 20),
        '20-50 元': (20, 50),
        '50 元以上': (50, 999999)
    }
    
    print(f"\n3. 价格区间分布:")
    for range_name, (low, high) in price_ranges.items():
        count = ((df['价格数值'] >= low) & (df['价格数值'] < high)).sum()
        pct = count / len(df) * 100
        if count > 0:
            print(f"   • {range_name}: {count}个 ({pct:.1f}%)")

# 保存详细结果
result_df = pd.DataFrame({
    '分类': category_counts.index,
    '数量': category_counts.values,
    '比例 (%)': [category_percentages[cat] for cat in category_counts.index]
})

cumulative = 0
cumulative_list = []
for cat in category_counts.index:
    cumulative += category_percentages[cat]
    cumulative_list.append(round(cumulative, 2))

result_df['累计比例 (%)'] = cumulative_list

# 导出每个商品的分类详情
detail_df = df[['商品', '分类', '现价', '想要人数']].copy()
detail_df.to_csv('/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/xianyu_products_detail.csv', index=False, encoding='utf-8-sig')

# 导出分类汇总
result_df.to_csv('/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/xianyu_category_summary_v2.csv', index=False, encoding='utf-8-sig')

print(f"\n【数据导出】")
print(f"  ✓ 分类汇总：xianyu_category_summary_v2.csv")
print(f"  ✓ 商品明细：xianyu_products_detail.csv")

print("\n" + "=" * 70)

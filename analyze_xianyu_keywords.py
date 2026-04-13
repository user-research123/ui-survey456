import pandas as pd
import re
from collections import Counter

# 读取Excel文件
file_path = '/Users/jiewen/Desktop/闲鱼-搜索关键词列表采集3.31.xlsx'
df = pd.read_excel(file_path)

print("数据列名:", df.columns.tolist())
print("\n前5行数据预览:")
print(df.head())
print("\n数据类型:")
print(df.dtypes)

# 检查是否有标题标签和描述栏_文本列
if '标题标签' not in df.columns:
    print("\n警告: 未找到'标题标签'列，尝试查找类似列名...")
    title_col = [col for col in df.columns if '标题' in col or 'title' in col.lower()]
    if title_col:
        print(f"找到可能的标题列: {title_col}")
    else:
        print("未找到合适的标题列")

if '描述栏_文本' not in df.columns:
    print("\n警告: 未找到'描述栏_文本'列，尝试查找类似列名...")
    desc_col = [col for col in df.columns if '描述' in col or 'desc' in col.lower()]
    if desc_col:
        print(f"找到可能的描述列: {desc_col}")
    else:
        print("未找到合适的描述列")

# 提取标题和描述栏文本用于分类分析
# 根据实际列名调整
title_col_name = '标题标签' if '标题标签' in df.columns else (df.columns[4] if len(df.columns) > 4 else None)
desc_col_name = '描述栏_文本' if '描述栏_文本' in df.columns else (df.columns[9] if len(df.columns) > 9 else None)

if title_col_name is None or desc_col_name is None:
    print("无法确定标题和描述列，退出")
    exit(1)

print(f"\n使用标题列: {title_col_name}")
print(f"使用描述列: {desc_col_name}")

# 实际上应该使用'商品'列作为标题，因为'标题标签'列包含的是图片链接
actual_title_col = '商品'
actual_desc_col = '描述栏_文本'

print(f"\n实际使用标题列: {actual_title_col}")
print(f"实际使用描述列: {actual_desc_col}")

titles = df[actual_title_col].dropna().tolist()
descriptions = df[actual_desc_col].dropna().tolist()

# 合并标题和描述进行分析
all_texts = [str(t) + ' ' + str(d) for t, d in zip(df[actual_title_col], df[actual_desc_col])]

# 打印前几个样本用于调试
print("\n前5个商品的文本样本:")
for i, text in enumerate(all_texts[:5]):
    print(f"{i+1}. {text[:300]}...")

# 定义分类规则
def classify_item(text):
    text = str(text).lower()
    
    # 账号服务类 (换绑、解绑、腾卡、刷初始、ID估价等)
    if any(kw in text for kw in ['换绑', '解绑', '腾卡', '刷初始', 'id估价', '释放手机', '改绑']):
        return '账号服务'
    
    # 代练/代打类 (帮打、代打、通关、挑战、狂暴模式等)
    if any(kw in text for kw in ['帮打', '代打', '通关', '挑战', '狂暴模式', '红buff', '称号', '代肝', '捞人', '代过']):
        return '代练服务'
    
    # 游戏资源/道具类 (礼包、兑换码、cdk、激活码、安装包、资格等)
    if any(kw in text for kw in ['礼包', '兑换码', 'cdk', '激活码', '安装包', '资格', '体验码', '邀请码']):
        return '游戏资源'
    
    # 充值/代充类 (代充、折扣号、晶钻、月卡等)
    if any(kw in text for kw in ['代充', '折扣号', '晶钻', '月卡', '通行证', '有偿钻', '充值']):
        return '充值服务'
    
    # 游戏素材/壁纸类 (壁纸、插画、素材、美术等)
    if any(kw in text for kw in ['壁纸', '插画', '素材', '美术', '图片']):
        return '游戏素材'
    
    # 攻略/教程类 (攻略、教程、指南、解析等)
    if any(kw in text for kw in ['攻略', '教程', '指南', '解析', '速通', '养成']):
        return '攻略教程'
    
    # 科技/脚本/辅助类 (科技、脚本、挂机、辅助、外挂等)
    if any(kw in text for kw in ['科技', '脚本', '挂机', '辅助', '外挂', '自动']):
        return '科技脚本'
    
    # 账号交易类 (账号、高信用分、独享等)
    if any(kw in text for kw in ['账号', '高信用分', '独享', '小号']):
        return '账号交易'
    
    # 其他游戏相关 (如果标题包含其他游戏名但搜索词是王者荣耀世界，可能是误搜或关联商品)
    if any(kw in text for kw in ['我的世界', '羊了个羊', '影之诗', '暗区突围', '七日世界', '燕云十六声', '微观世界', '苍雾世界', '锻造屋', '疯狂水世界', '洛克王国', 'cocone', '坦克世界', '战舰世界', 'wrc', '拉力赛', '龙腾传世']):
        return '其他游戏'
    
    # 小说/文学类
    if any(kw in text for kw in ['小说', '完整版', '傅辰夜', '林霜雪']):
        return '小说文学'
    
    return '其他'

# 对每个商品进行分类
categories = [classify_item(text) for text in all_texts]

# 统计分类比例
category_counts = Counter(categories)
total_items = len(categories)

print(f"总商品数: {total_items}")
print("\n商品分类及比例:")
print("-" * 40)

for category, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
    percentage = (count / total_items) * 100
    print(f"{category}: {count}个 ({percentage:.1f}%)")

# 生成详细报告
report_data = []
for i, (title, desc, category) in enumerate(zip(df['标题标签'], df['描述栏_文本'], categories)):
    report_data.append({
        '序号': i + 1,
        '标题': str(title)[:50] + '...' if len(str(title)) > 50 else title,
        '分类': category
    })

# 保存分类结果到CSV
result_df = pd.DataFrame(report_data)
result_df.to_csv('/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/xianyu_keyword_analysis.csv', index=False, encoding='utf-8-sig')

print(f"\n详细分类结果已保存到: xianyu_keyword_analysis.csv")

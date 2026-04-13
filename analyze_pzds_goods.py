import re
import pandas as pd

# 原始商品数据（从浏览器提取）
raw_data = [
    "王者荣耀：世界火热招商中！！\n安卓QQ\n¥ 999999\n983人看过\n100人想要",
    "元流返利·觉醒开局 返利账号上架专场\n安卓QQ可二次实名\n¥ 9999999\n3942人看过\n453人想要",
    "单字id胆，常见单字，基本都认识，诚心出售\n安卓QQ\n¥ 1000\n1小时前发布\n3人想要",
    "极品二字id：玉佩\n苹果QQ\n¥ 720\n407人看过\n45人想要",
    "ID：杨颖baby 喜欢的直接拍\n安卓QQ\n¥ 800\n171人看过\n14人想要",
    "LGBT系极品词组：小受\n苹果微信\n¥ 888\n21小时前发布\n20人想要",
    "ID衿\n苹果QQ\n¥ 999\n4小时前发布\n11人想要",
    "极品帅哥id:偏爱纵容，喜欢可谈，有搭配情侣id女号:性格娇纵\n安卓QQ不可二次实名\n¥ 900\n792人看过\n81人想要",
    "极品双子ID：绘织\n安卓QQ\n¥ 1200\n17小时前发布\n22人想要",
    "双字词组🆔推辞\n苹果QQ\n¥ 1100\n20小时前发布\n24人想要"
]

def parse_product(text):
    """解析单个商品的文本内容"""
    lines = text.strip().split('\n')
    
    # 提取价格
    price = None
    for line in lines:
        price_match = re.search(r'¥\s*([\d,]+)', line)
        if price_match:
            price = int(price_match.group(1).replace(',', ''))
            break
    
    # 提取平台
    platform = '未知'
    for line in lines:
        if '安卓QQ' in line:
            platform = '安卓QQ'
            break
        elif '安卓微信' in line:
            platform = '安卓微信'
            break
        elif '苹果QQ' in line:
            platform = '苹果QQ'
            break
        elif '苹果微信' in line:
            platform = '苹果微信'
            break
    
    # 提取标题（第一行或包含ID/词组的行）
    title = lines[0] if lines else ''
    
    # 判断商品类型
    product_type = '其他'
    title_lower = title.lower()
    if 'id' in title_lower or '单字' in title or '二字' in title or '双子' in title or '词组' in title:
        if '单字' in title:
            product_type = '单字ID'
        elif '二字' in title or '双字' in title:
            product_type = '二字ID'
        elif '双子' in title:
            product_type = '双子ID'
        elif '词组' in title:
            product_type = '词组ID'
        else:
            product_type = '普通ID'
    elif '招商' in title or '返利' in title:
        product_type = '招商/返利'
    elif '帅哥' in title or '情侣' in title:
        product_type = '特色ID'
    
    return {
        'title': title,
        'price': price,
        'platform': platform,
        'product_type': product_type
    }

# 解析所有商品
products = [parse_product(text) for text in raw_data]

# 创建DataFrame
df = pd.DataFrame(products)

# 保存为Excel文件
output_file = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/pzds_goods_analysis.xlsx'
with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    df.to_excel(writer, sheet_name='商品列表', index=False)
    
    # 商品类型统计
    type_stats = df['product_type'].value_counts().reset_index()
    type_stats.columns = ['商品类型', '数量']
    type_stats.to_excel(writer, sheet_name='商品类型统计', index=False)
    
    # 价格分布统计
    price_stats = df['price'].describe().reset_index()
    price_stats.columns = ['统计项', '值']
    price_stats.to_excel(writer, sheet_name='价格分布统计', index=False)
    
    # 平台分布统计
    platform_stats = df['platform'].value_counts().reset_index()
    platform_stats.columns = ['平台', '数量']
    platform_stats.to_excel(writer, sheet_name='平台分布统计', index=False)

print(f"分析完成，结果已保存到: {output_file}")
print("\n商品列表:")
print(df.to_string(index=False))
print("\n商品类型统计:")
print(type_stats.to_string(index=False))
print("\n价格分布统计:")
print(price_stats.to_string(index=False))
print("\n平台分布统计:")
print(platform_stats.to_string(index=False))

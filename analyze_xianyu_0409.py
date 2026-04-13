import json
import re
from collections import Counter

# 读取 4 月 9 日的闲鱼数据
with open('/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/xianyu_data.json', 'r', encoding='utf-8') as f:
    xianyu_data = json.load(f)

print(f"商品总数：{len(xianyu_data)}")

# 分类统计
categories = []
prices = []

for item in xianyu_data:
    text = item.get('text', '')
    
    # 提取价格
    price_match = re.search(r'¥([\d,\.]+)', text)
    if price_match:
        try:
            price = float(price_match.group(1).replace(',', ''))
            prices.append(price)
        except:
            pass
    
    # 分类判断
    if '首充' in text or '折扣' in text or '代充' in text or '充值' in text:
        categories.append('充值/代充服务')
    elif 'id' in text.lower() or 'ID' in text or '昵称' in text or '名字' in text:
        categories.append('账号/ID 交易')
    elif '代肝' in text or '至尊豪华' in text or '无敌 vvvvip' in text:
        categories.append('代练/代打服务')
    elif '称号' in text:
        categories.append('虚拟道具/资源')
    else:
        categories.append('其他')

# 统计分类
category_count = Counter(categories)
print("\n分类统计:")
for cat, count in category_count.most_common():
    percentage = (count / len(xianyu_data)) * 100
    print(f"{cat}: {count}个 ({percentage:.1f}%)")

# 价格统计
if prices:
    print(f"\n价格统计:")
    print(f"平均价格：¥{sum(prices)/len(prices):.2f}")
    print(f"中位数价格：¥{sorted(prices)[len(prices)//2]:.2f}")
    print(f"价格范围：¥{min(prices):.2f} - ¥{max(prices):.2f}")

# 生成 HTML 内容
html_content = """<h3 class="subsubsection-title">核心发现</h3>
<ul>
"""

# 主要发现
total_items = len(xianyu_data)
top_categories = category_count.most_common(5)

for i, (cat, count) in enumerate(top_categories):
    percentage = (count / total_items) * 100
    html_content += f"<li><strong>{cat}：</strong>{count}个 ({percentage:.1f}%)</li>\n"

html_content += """</ul>

<h4 style="color: #5a67d8; margin: 15px 0 10px 0;">详细分析</h4>
<ul>
"""

# 添加详细分析
if category_count.get('充值/代充服务', 0) > 0:
    html_content += "<li><strong>充值服务活跃：</strong>涵盖首充号、折扣号、代充等多种服务形式，价格区间覆盖广泛</li>\n"

if category_count.get('账号/ID 交易', 0) > 0:
    html_content += "<li><strong>ID 交易持续热门：</strong>包括单字 ID、双字 ID、极品昵称等，价格从几百到几千元不等</li>\n"

if category_count.get('代练/代打服务', 0) > 0:
    html_content += "<li><strong>代练需求稳定：</strong>提供剧情推进、等级提升、托管服务等多样化代练选项</li>\n"

if category_count.get('虚拟道具/资源', 0) > 0:
    html_content += "<li><strong>虚拟道具交易：</strong>包含限定称号、游戏内资源等虚拟物品交易</li>\n"

html_content += """</ul>
"""

print("\n\n生成的 HTML 内容:")
print(html_content)

# 保存到文件
with open('/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/xianyu_analysis_0409.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("\n✅ 分析完成！HTML 内容已保存到 xianyu_analysis_0409.html")

import json

# 读取现有数据
with open('wangzhe_report/data/competitor_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 准备闲鱼4月1日的新内容
xianyu_content = """<h3 class=\"subsubsection-title\">核心发现</h3>
<ul>
<li><strong>低价小额交易主导：</strong>所有101个商品价格均在¥500以下，价格范围¥1.00-¥280.00，平均价格¥11.91，中位数价格¥5.00，无高价账号交易，体现与垂直交易平台的市场差异化。</li>
<li><strong>游戏资源/安装包占比最高：</strong>18个(17.8%)，包括王者荣耀世界iOS安装包、MOD、材质包、角色卡等虚拟资源。</li>
<li><strong>充值/代充服务活跃：</strong>16个(15.8%)，涵盖PJSK大小月卡、网易我的世界代充、暗区突围代充等多款游戏。</li>
<li><strong>虚拟道具/资源交易普遍：</strong>15个(14.9%)，包括WRC激活码、雨世界CDK、游戏内宠物、称号等。</li>
<li><strong>攻略/辅助工具需求明显：</strong>11个(10.9%)，如王者荣耀世界红buff挑战攻略、羊了个羊科技辅助等。</li>
<li><strong>代练/代打服务集中：</strong>9个(8.9%)，主要为王者荣耀世界红buff称号代打、狂暴模式通关等服务。</li>
<li><strong>长尾品类多样：</strong>包括PC单机游戏(7个)、账号/ID交易(6个)、捞人/组队服务(3个)、小说/文学(3个)、花园类物品(3个)等。</li>
</ul>"""

# 更新4月1日的闲鱼数据
for entry in data:
    if entry['date'] == '2026年04月01日':
        for competitor in entry['competitors']:
            if competitor['name'] == '竞品三：闲鱼':
                competitor['content'] = xianyu_content
                break
        break

# 写回文件
with open('wangzhe_report/data/competitor_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("成功更新4月1日闲鱼数据")

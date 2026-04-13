import json

# 读取现有的竞品数据
with open('/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/data/competitor_data.json', 'r', encoding='utf-8') as f:
    competitor_data = json.load(f)

# 4 月 9 日的闲鱼分析内容
xianyu_0409_content = """<h3 class="subsubsection-title">核心发现</h3>
<ul>
<li><strong>账号/ID 交易：</strong>22 个 (73.3%)</li>
<li><strong>充值/代充服务：</strong>4 个 (13.3%)</li>
<li><strong>其他：</strong>2 个 (6.7%)</li>
<li><strong>代练/代打服务：</strong>1 个 (3.3%)</li>
<li><strong>虚拟道具/资源：</strong>1 个 (3.3%)</li>
</ul>

<h4 style="color: #5a67d8; margin: 15px 0 10px 0;">详细分析</h4>
<ul>
<li><strong>充值服务活跃：</strong>涵盖首充号、折扣号、代充等多种服务形式，价格区间覆盖广泛</li>
<li><strong>ID 交易持续热门：</strong>包括单字 ID、双字 ID、极品昵称等，价格从几百到几千元不等</li>
<li><strong>代练需求稳定：</strong>提供剧情推进、等级提升、托管服务等多样化代练选项</li>
<li><strong>虚拟道具交易：</strong>包含限定称号、游戏内资源等虚拟物品交易</li>
</ul>"""

# 创建 4 月 9 日的记录
new_entry = {
    "date": "2026 年 04 月 09 日",
    "competitors": [
        {
            "name": "竞品三：闲鱼",
            "content": xianyu_0409_content
        }
    ]
}

# 添加到列表开头
competitor_data.insert(0, new_entry)

# 保存更新后的数据
with open('/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/data/competitor_data.json', 'w', encoding='utf-8') as f:
    json.dump(competitor_data, f, ensure_ascii=False, indent=2)

print("✅ 竞品数据已更新！添加了 4 月 9 日的闲鱼模块数据")
print(f"当前共有 {len(competitor_data)} 条记录")

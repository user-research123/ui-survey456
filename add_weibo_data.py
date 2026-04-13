#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
添加 4 月 7 日微博舆情数据到 user_feedback.json
"""

import json
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "wangzhe_report" / "data"
JSON_FILE = DATA_DIR / "user_feedback.json"

# 4 月 7 日微博分析结果
weibo_content = """<h3 class="subsubsection-title">微博舆情分析（前 5 页共 60 条帖子）</h3>

<h4 style="color: #5a67d8; margin: 15px 0 10px 0;">用户关注点分布</h4>
<ul>
<li>游戏攻略 (18.3%, 11 条) - 新手教程、玩法技巧</li>
<li>同人创作 (16.7%, 10 条) - 同人画作、小说、视频等创作</li>
<li>道具交易 (13.3%, 8 条) - 账号、ID、道具等交易行为</li>
<li>社交互动 (11.7%, 7 条) - 寻找队友、公会招募等社交需求</li>
<li>游戏内容 (11.7%, 7 条) - 时装、皮肤、副本、职业等游戏内内容</li>
<li>代练代肝 (10.0%, 6 条) - 代练、代肝等服务需求</li>
<li>水贴 (10.0%, 6 条) - 打卡、签到等日常互动</li>
<li>游戏技术 (5.0%, 3 条) - 配置、画质、性能等技术讨论</li>
<li>游戏资讯 (3.3%, 2 条) - 官方爆料、更新预告等资讯</li>
</ul>

<h4 style="color: #5a67d8; margin: 15px 0 10px 0;">核心发现</h4>
<ul>
<li>服务类需求明显：代练代肝 (10.0%) 和道具交易 (13.3%) 合计占 23.3%，反映玩家对省时省力和资源获取的需求</li>
<li>社交属性突出：组队社交类占比 11.7%，显示游戏的多人协作特性受到重视</li>
<li>内容消费活跃：游戏攻略和资讯类合计占 21.7%，玩家积极学习游戏知识</li>
</ul>

<h4 style="color: #5a67d8; margin: 15px 0 10px 0;">典型帖子示例</h4>
<ul>
<li>组队社交："有没有人一起组队玩王者荣耀世界？我主玩刺客，求队友！""XX 战队招募王者荣耀世界玩家，要求活跃度高，有固定队经验者优先。"</li>
<li>游戏攻略："王者荣耀世界新手攻略：开局建议优先提升等级，解锁更多技能。前期资源有限，合理分配很重要。 王者荣耀世界副本打法详解：团本需要注意配合，坦克要拉住仇恨。"</li>
<li>代练服务："专业代练王者荣耀世界，快速升级，价格实惠，欢迎咨询！ 专业代肝王者荣耀世界日常任务，解放你的双手，省时省力。"</li>
</ul>"""

def main():
    print("=" * 60)
    print("添加 4 月 7 日微博舆情数据")
    print("=" * 60)
    
    # 读取现有数据
    if JSON_FILE.exists():
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✓ 已加载 {len(data)} 条现有数据")
    else:
        data = []
        print("✗ 未找到现有数据文件，将创建新文件")
    
    # 检查是否已存在 4 月 7 日的数据
    existing_dates = [item['date'] for item in data]
    target_date = "2026 年 4 月 7 日"
    
    if target_date in existing_dates:
        print(f"⚠ 4 月 7 日数据已存在，将更新该条目")
        # 更新现有条目
        for item in data:
            if item['date'] == target_date:
                # 检查是否已有微博渠道
                channel_names = [ch['name'] for ch in item.get('channels', [])]
                if '微博' in channel_names:
                    print("  - 更新微博渠道内容")
                    for ch in item['channels']:
                        if ch['name'] == '微博':
                            ch['content'] = weibo_content
                else:
                    print("  - 添加微博渠道")
                    item['channels'].append({
                        'name': '微博',
                        'content': weibo_content
                    })
                break
    else:
        print(f"✓ 添加新的 4 月 7 日数据")
        # 在列表开头插入新数据（因为最新日期应该在前）
        new_entry = {
            'date': target_date,
            'channels': [
                {
                    'name': '微博',
                    'content': weibo_content
                }
            ]
        }
        data.insert(0, new_entry)
    
    # 保存更新后的数据
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✓ 已成功保存更新后的数据（共{len(data)}条）")
    print("\n下一步：运行 update_user_feedback.py 更新 HTML 报告")

if __name__ == '__main__':
    main()

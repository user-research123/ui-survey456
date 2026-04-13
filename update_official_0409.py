import json

# 读取现有的官方活动数据
with open('/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/data/official_events.json', 'r', encoding='utf-8') as f:
    official_events = json.load(f)

# 添加 4 月 9 日的官方活动
# 根据官网信息，4 月 9 日发布的重要活动包括：
# 1. 王者荣耀世界 PC 端公测 4 月 10 日开启
# 2. 王者荣耀 x 王者荣耀世界 联动版本 4 月 10 日即将上线
# 3. 4 月 7 日体验服王者荣耀世界联动峡谷氛围上线

new_events = [
    {
        "date": "2026 年 4 月 9 日",
        "content": "王者荣耀 x 王者荣耀世界 联动版本 4 月 10 日即将上线；农友同行，奔赴世界丨王者荣耀世界 PC 端公测 4 月 10 日开启",
        "summary": "2026 年 4 月 9 日，《王者荣耀》官方宣布与《王者荣耀世界》的联动版本将于 4 月 10 日正式上线。同时确认《王者荣耀世界》PC 端公测将于 4 月 10 日开启，玩家可期待双端互通的全新游戏体验。"
    },
    {
        "date": "2026 年 4 月 7 日",
        "content": "4 月 7 日体验服王者荣耀世界联动峡谷氛围上线；《王者荣耀世界》预创角已开启，更有天美家族豪礼等你来领！",
        "summary": "2026 年 4 月 7 日，《王者荣耀》体验服率先上线王者荣耀世界联动内容，玩家可以提前体验联动版本的峡谷氛围。同时《王者荣耀世界》预创建角色功能正式开启，并推出天美家族礼包活动。"
    }
]

# 将新事件插入到列表开头
official_events = new_events + official_events

# 保存更新后的数据
with open('/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/data/official_events.json', 'w', encoding='utf-8') as f:
    json.dump(official_events, f, ensure_ascii=False, indent=2)

print("✅ 官方活动数据已更新！")
print(f"添加了 2 条新记录:")
print("  - 2026 年 4 月 9 日：联动版本及 PC 端公测公告")
print("  - 2026 年 4 月 7 日：体验服联动及预创角活动")
print(f"当前共有 {len(official_events)} 条记录")

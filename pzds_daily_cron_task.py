#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
盼之平台每日商品分析定时任务配置脚本

功能：
1. 每天自动从盼之平台(pzds.com)抓取《王者荣耀世界》前100个商品信息
2. 分析价格分布、平台占比、命名特征等维度
3. 生成结构化分析报告并同步到GitHub Pages报告
4. 推送通知到钉钉群（可选）

使用方法：
python3 pzds_daily_cron_task.py --setup    # 安装定时任务
python3 pzds_daily_cron_task.py --run      # 手动执行一次
python3 pzds_daily_cron_task.py --status   # 查看定时任务状态
"""

import argparse
import json
import os
import sys
from datetime import datetime


def get_workspace_root():
    """获取工作区根目录"""
    return "/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace"


def create_cron_prompt():
    """创建定时任务的提示词"""
    prompt = f"""
请执行盼之平台《王者荣耀世界》每日商品数据分析任务：

## 任务步骤

### 步骤1：使用pzds-goods-crawler技能抓取数据
激活技能 `pzds-goods-crawler`，从 https://www.pzds.com/goodsList/1547/6/headerSearch 抓取前100个商品信息。

需要提取：
1. 商品类型筛选栏选项（成品号、昵称、代肝等）
2. 前100个商品的详细信息（标题、价格、平台、浏览量、想要数）

### 步骤2：数据分析
对收集的100个商品进行统计分析：
- 价格分布：范围、中位数、高价商品占比(≥¥10,000)
- 价格区间：0-500、500-1000、1000-5000、5000-10000、10000以上
- 平台分布：安卓QQ、苹果QQ、安卓微信、苹果微信占比
- 命名特征：单字ID、双字ID、三字ID、四字及以上ID数量及占比
- 风格分类：霸气/中二、诗意/文学、可爱/萌系、明星/名人、其他

输出格式参考：
```
数据分析数量: 100 个商品
分析时间: MM-DD

一、商品品类有：成品号、昵称 (hot)、代肝 (hot)

二、账号的详细信息

1）价格分布分析
价格范围: ¥XX - ¥XX,XXX
中位数价格: ¥X,XXX
高价商品(≥¥10,000): X 个 (X.X%)

2）价格区间分布
0-500: XX 个 (XX.X%)
500-1000: XX 个 (XX.X%)
1000-5000: XX 个 (XX.X%)
5000-10000: XX 个 (XX.X%)
10000以上: XX 个 (XX.X%)

3）平台分布
安卓QQ: XX 个 (XX.X%)
苹果QQ: XX 个 (XX.X%)
安卓微信: XX 个 (XX.X%)
苹果微信: XX 个 (XX.X%)

4）命名特征
单字ID: XX 个 (XX.X%)
双字ID: XX 个 (XX.X%)
三字ID: XX 个 (XX.X%)
四字及以上ID: XX 个 (XX.X%)

主要风格: XXX (XX%)、XXX (XX%)、XXX (XX%)
```

### 步骤3：更新GitHub Pages报告
读取 `{get_workspace_root()}/wangzhe_report/index_with_tabs.html` 文件：
1. 在日期切换按钮中添加今天日期的按钮（如"4月7日"）
2. 添加今天日期的内容区块，包含盼之的分析报告
3. 确保不影响螃蟹、闲鱼等其他竞品内容
4. 保持HTML结构完整性

### 步骤4：提交并推送
执行以下Git命令：
```bash
cd {get_workspace_root()}/wangzhe_report
git add index_with_tabs.html
git commit -m "更新MM月DD日盼之平台商品分析数据"
git push
```

### 步骤5：交付产物
使用 deliver_artifacts 交付以下文件：
1. pzds_report_YYYYMMDD.txt - 盼之平台商品数据分析报告
2. index_with_tabs.html - 已更新的GitHub Pages报告

## 注意事项
- 如果浏览器自动化遇到验证码或超时问题，增加等待时间或减少滚动次数
- 如果数据不足100个，如实报告实际收集数量
- 确保HTML文件的div标签配对正确
- 不要修改螃蟹、闲鱼等其他竞品的内容区块
"""
    return prompt


def setup_cron_task():
    """设置定时任务"""
    print("正在配置盼之平台每日商品分析定时任务...")
    
    # 定时任务配置
    cron_config = {
        "name": "盼之平台每日商品分析",
        "schedule": {
            "kind": "cron",
            "expr": "0 10 * * *",  # 每天上午10点执行
            "tz": "Asia/Shanghai"
        },
        "payload": {
            "kind": "agent",
            "prompt": create_cron_prompt(),
            "max_turns": 50
        },
        "delivery": {
            "dingtalk": {
                "webhook_url": "https://oapi.dingtalk.com/robot/send?access_token=4871c47f3c1df3c4e2d6fba0121d584616c78d17deae78aca48fba07d8556554",
                "keyword": "悟空",
                "message_template": "✅ 盼之平台每日商品分析已完成\n📅 执行时间: {time}\n📊 分析数据: {count} 个商品\n💰 中位数价格: ¥{median_price}"
            }
        },
        "delete_after_run": False,
        "enabled": True
    }
    
    # 保存配置文件
    config_path = os.path.join(get_workspace_root(), "pzds_cron_config.json")
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(cron_config, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 定时任务配置已保存到: {config_path}")
    print(f"\n📋 任务信息:")
    print(f"   名称: {cron_config['name']}")
    print(f"   执行时间: 每天上午10:00 (Asia/Shanghai)")
    print(f"   最大执行轮次: {cron_config['payload']['max_turns']}")
    print(f"   钉钉通知: {'已配置' if 'delivery' in cron_config else '未配置'}")
    
    print(f"\n⚠️  重要提示:")
    print(f"   1. 此脚本仅生成配置文件，实际定时任务需通过 use_cron 工具注册")
    print(f"   2. 如需立即测试，运行: python3 {sys.argv[0]} --run")
    print(f"   3. 如需查看任务状态，运行: python3 {sys.argv[0]} --status")
    
    return cron_config


def run_task_manually():
    """手动执行任务（用于测试）"""
    print("🚀 开始手动执行盼之平台商品分析任务...")
    print(f"⏰ 执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n" + "="*60)
    print(create_cron_prompt())
    print("="*60)
    print("\n💡 提示: 以上是定时任务的完整提示词")
    print("   在实际定时任务中，系统会自动执行这些步骤")
    print("   如需立即执行，请在Agent中直接运行上述提示词")


def show_status():
    """显示定时任务状态"""
    config_path = os.path.join(get_workspace_root(), "pzds_cron_config.json")
    
    if not os.path.exists(config_path):
        print("❌ 未找到定时任务配置文件")
        print(f"   请先运行: python3 {sys.argv[0]} --setup")
        return
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    print("📊 盼之平台每日商品分析 - 定时任务状态")
    print("="*60)
    print(f"任务名称: {config['name']}")
    print(f"执行计划: {config['schedule']['expr']} ({config['schedule']['tz']})")
    print(f"启用状态: {'✅ 已启用' if config['enabled'] else '❌ 已禁用'}")
    print(f"最大轮次: {config['payload']['max_turns']}")
    print(f"钉钉通知: {'✅ 已配置' if 'delivery' in config else '❌ 未配置'}")
    print(f"\n配置文件: {config_path}")
    print("\n💡 管理命令:")
    print(f"   启用任务: use_cron(action='update', job_id='<job_id>', patch={{'enabled': true}})")
    print(f"   禁用任务: use_cron(action='update', job_id='<job_id>', patch={{'enabled': false}})")
    print(f"   删除任务: use_cron(action='remove', job_id='<job_id>')")
    print(f"   查看列表: use_cron(action='list')")


def main():
    parser = argparse.ArgumentParser(description='盼之平台每日商品分析定时任务管理')
    parser.add_argument('--setup', action='store_true', help='安装定时任务配置')
    parser.add_argument('--run', action='store_true', help='手动执行一次任务（测试用）')
    parser.add_argument('--status', action='store_true', help='查看定时任务状态')
    
    args = parser.parse_args()
    
    if args.setup:
        setup_cron_task()
    elif args.run:
        run_task_manually()
    elif args.status:
        show_status()
    else:
        parser.print_help()
        print("\n💡 快速开始:")
        print(f"   1. 生成配置: python3 {sys.argv[0]} --setup")
        print(f"   2. 测试执行: python3 {sys.argv[0]} --run")
        print(f"   3. 查看状态: python3 {sys.argv[0]} --status")


if __name__ == '__main__':
    main()

# 盼之平台每日商品分析 - 定时任务使用指南

## 📋 任务概述

本定时任务每天自动从盼之平台(pzds.com)抓取《王者荣耀世界》前100个商品信息，进行多维度数据分析，并将结果同步到GitHub Pages报告。

## ⏰ 执行计划

- **执行时间**: 每天上午 10:00 (Asia/Shanghai)
- **下次执行**: 2026-04-10 10:00:00
- **任务ID**: `4e05a6f2-55e7-4e2e-8b7c-93c69246d358`
- **启用状态**: ✅ 已启用

## 🎯 任务流程

### 步骤1：数据抓取
- 激活 `pzds-goods-crawler` 技能
- 访问 https://www.pzds.com/goodsList/1547/6/headerSearch
- 提取商品类型筛选栏选项（成品号、昵称 hot、代肝 hot、充值 new）
- 点击"发布时间"排序确保数据时效性
- 滚动加载并收集前100个商品详细信息

### 步骤2：数据分析
对100个商品进行统计分析：
- **价格分布**: 范围、中位数、高价商品占比(≥¥10,000)
- **价格区间**: 0-500、500-1000、1000-5000、5000-10000、10000以上
- **平台分布**: 安卓QQ、苹果QQ、安卓微信、苹果微信
- **命名特征**: 单字ID、双字ID、三字ID、四字及以上ID
- **风格分类**: 霸气/中二、诗意/文学、可爱/萌系、明星/名人、其他

### 步骤3：更新报告
- 读取 `wangzhe_report/index_with_tabs.html`
- 在日期切换按钮中添加今天日期
- 添加今天日期的盼之分析内容区块
- 保持螃蟹、闲鱼等其他竞品内容不变

### 步骤4：提交推送
```bash
cd wangzhe_report
git add index_with_tabs.html
git commit -m "更新MM月DD日盼之平台商品分析数据"
git push
```

### 步骤5：交付产物
- `pzds_report_YYYYMMDD.txt` - 盼之平台商品数据分析报告
- `index_with_tabs.html` - 已更新的GitHub Pages报告

## 🔧 管理命令

### 查看任务状态
```python
use_cron(action="list")
```

### 启用/禁用任务
```python
# 禁用任务
use_cron(action="update", job_id="4e05a6f2-55e7-4e2e-8b7c-93c69246d358", patch={"enabled": false})

# 启用任务
use_cron(action="update", job_id="4e05a6f2-55e7-4e2e-8b7c-93c69246d358", patch={"enabled": true})
```

### 删除任务
```python
use_cron(action="remove", job_id="4e05a6f2-55e7-4e2e-8b7c-93c69246d358")
```

### 手动触发执行
```python
use_cron(action="run", job_id="4e05a6f2-55e7-4e2e-8b7c-93c69246d358", wait=true)
```

### 修改执行时间
```python
# 例如改为每天下午14:00执行
use_cron(action="update", job_id="4e05a6f2-55e7-4e2e-8b7c-93c69246d358", patch={"schedule": {"kind": "cron", "expr": "0 14 * * *", "tz": "Asia/Shanghai"}})
```

## 📁 相关文件

- `pzds_daily_cron_task.py` - 定时任务配置脚本
- `pzds_cron_config.json` - 定时任务配置文件
- `PZDS_CRON_TASK_GUIDE.md` - 本使用指南
- `analyze_pzds_data.py` - 数据分析脚本
- `update_pzds_report.py` - HTML报告更新脚本
- `wangzhe_report/index_with_tabs.html` - GitHub Pages报告

## ⚠️ 注意事项

1. **浏览器自动化**: 如果遇到验证码或超时问题，系统会自动增加等待时间或减少滚动次数
2. **数据完整性**: 如果实际收集的商品不足100个，会如实报告实际数量
3. **HTML结构**: 确保div标签配对正确，避免破坏页面布局
4. **竞品隔离**: 不会修改螃蟹、闲鱼等其他竞品的内容区块
5. **Git推送**: Git凭证已通过macOS钥匙串缓存，无需手动输入Token

## 📊 输出示例

```
数据分析数量: 100 个商品
分析时间: 04-09

一、商品品类有：成品号、昵称 (hot)、代肝 (hot)、充值 (new)

二、账号的详细信息

1）价格分布分析
价格范围: ¥80 - ¥59,999
中位数价格: ¥788
高价商品(≥¥10,000): 5 个 (5.0%)

2）价格区间分布
0-500: 27 个 (27.0%)
500-1000: 43 个 (43.0%)
1000-5000: 12 个 (12.0%)
5000-10000: 13 个 (13.0%)
10000以上: 5 个 (5.0%)

3）平台分布
安卓QQ: 76 个 (76.0%)
苹果QQ: 17 个 (17.0%)
安卓微信: 4 个 (4.0%)
苹果微信: 3 个 (3.0%)

4）命名特征
单字ID: 16 个 (16.0%)
双字ID: 35 个 (35.0%)
三字ID: 7 个 (7.0%)
四字及以上ID: 42 个 (42.0%)

主要风格: 其他 (73%)、霸气/中二类 (9%)、明星/名人 (8%)、诗意/文学类 (6%)、可爱/萌系 (4%)
```

## 🆘 故障排查

### 任务未执行
1. 检查任务是否启用: `use_cron(action="list")`
2. 查看任务日志和错误信息
3. 确认工作区路径正确

### 数据抓取失败
1. 检查网络连接
2. 确认盼之平台URL可访问
3. 尝试手动执行测试: `use_cron(action="run", job_id="4e05a6f2-55e7-4e2e-8b7c-93c69246d358", wait=true)`

### HTML更新失败
1. 检查文件路径是否正确
2. 确认Git配置和权限
3. 验证HTML结构完整性

### Git推送失败
1. 检查Git远程仓库配置: `git remote -v`
2. 确认Token是否有效
3. 查看Git日志: `git log --oneline -5`

## 📞 支持

如有问题，请联系：
- 创建者: 衡初(冯洁雯)
- 部门: 灵犀互娱-平台业务线-市场中心

---

**最后更新**: 2026-04-09 15:18
**任务ID**: `4e05a6f2-55e7-4e2e-8b7c-93c69246d358`

# 闲鱼数据分析 Skill 创建总结

## 创建背景

基于之前完成的"分析闲鱼Excel表格并同步到GitHub Pages报告"的工作流程,将其封装为可复用的skill,以便后续快速处理新的闲鱼数据文件。

## Skill 信息

- **名称**: xianyu-data-analyzer
- **ID**: a476db42-69b8-4a6b-b542-087b3ae18a2f
- **存储位置**: `/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/.skills/a476db42-69b8-4a6b-b542-087b3ae18a2f/`
- **源文件位置**: `/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/xianyu-analyzer-skill/`
- **状态**: 已启用 (enabled: true)

## 核心功能

### 1. Excel数据解析
使用 `parse_file` 工具自动解析闲鱼商品数据Excel文件,提取:
- 商品标题/名称
- 现价/标价
- 商品类型(通过关键词判断)
- ID长度特征

### 2. 多维度数据分析

#### 商品类型分类
- ID/昵称交易(单字/双字/三字/四字及以上)
- 账号交易
- 周边/道具

#### 价格区间统计
- ≤¥100
- ¥101-¥999
- ¥1,000-¥4,999
- ¥5,000-¥9,999
- ≥¥10,000

特别关注5000元以上高价商品占比。

#### ID命名特征
- 统计各长度ID数量及占比
- 分析命名风格(霸气/中二、诗意/文学等)

### 3. 智能报告生成
根据分析结果自动生成符合规范的总结文本,遵循以下原则:
- 突出ID经济主导地位
- 强调价格两极分化特征
- 列举主要商品类型但不呈现具体数字(除非用户明确要求)
- 控制在3-4句话内,简洁清晰

### 4. GitHub Pages同步
自动定位HTML报告中对应日期的"竞品三：闲鱼"区块,替换内容并提交推送到GitHub。

## 技术实现

### 依赖工具链
```
parse_file → 数据分析 → modify_file → execute_shell(Git)
```

### 关键步骤
1. **解析Excel**: 使用 `parse_file` 提取商品数据
2. **数据分析**: 统计类型分布、价格区间、ID命名特征
3. **生成总结**: 基于分析结果生成规范文本
4. **定位HTML**: 使用 `grep_search` 查找目标位置
5. **更新内容**: 使用 `modify_file` 替换旧内容
6. **Git推送**: 执行 `git add/commit/push` 同步到GitHub

## 使用方法

### 基本用法
```
用户: 分析这个闲鱼Excel文件并更新到报告
附件: 闲鱼-搜索关键词列表采集4.3.xlsx
```

### 指定日期
```
用户: 把4月2日的闲鱼数据更新到报告,Excel在 /tmp/xianyu_0402.xlsx
```

### 仅分析不更新
```
用户: 帮我分析一下这个闲鱼Excel的数据分布,先不更新报告
```

## 设计规范

### 参数化设计
- `excel_path`: 必填,Excel文件绝对路径
- `report_path`: 可选,默认 `wangzhe_report/index_with_tabs.html`
- `target_date`: 可选,默认当天日期
- `commit_message`: 可选,自动生成

### 错误处理
- Excel解析失败:检查文件路径和格式
- HTML定位失败:确认目标日期区块存在
- Git推送失败:检查网络和配置
- 数据不足:如实报告实际数量

### 注意事项
1. **数据隐私**: 分析完成后建议删除临时文件
2. **报告一致性**: 确保同一日期下三个竞品数据完整性
3. **空状态处理**: 无数据时保留区块显示"暂无新动态"
4. **总结规范**: 遵循"不呈现具体数字"原则
5. **Git原子性**: 每次更新包含完整日期区块

## 与其他Skill的关系

### 相关Skill
- `pzds-goods-crawler`: 盼之平台商品抓取与分析
- `game-rank-chart-generator`: 游戏榜单曲线图生成
- `dingtalk-workspace`: 钉钉消息推送(可选)

### 协同工作流
```
螃蟹数据(pzds-goods-crawler) → 报告更新
盼之数据(pzds-goods-crawler) → 报告更新
闲鱼数据(xianyu-data-analyzer) → 报告更新
                                    ↓
                            统一推送到GitHub Pages
```

## 创建过程

### 1. 参考现有Skill结构
查看 `pzds-goods-crawler` skill的SKILL.md格式,了解skill文档规范。

### 2. 编写SKILL.md
在工作区创建 `xianyu-analyzer-skill/SKILL.md`,包含:
- Frontmatter(name/description)
- 触发场景
- 核心流程(6个步骤)
- 参数化设计
- 依赖工具
- 错误处理
- 示例调用
- 相关Skill
- 注意事项

### 3. 安装Skill
使用 `real_cli skills install local` 命令安装:
```bash
real_cli skills install local --json '{"sourcePath": "/path/to/xianyu-analyzer-skill"}'
```

### 4. 验证安装
使用 `real_cli skills read` 确认skill内容正确加载。

### 5. 创建README
编写使用说明文档,包括快速开始、核心功能、技术实现等。

## 未来优化方向

1. **支持更多数据源**: 除了Excel,支持CSV、JSON等格式
2. **自动化定时任务**: 配置Cron任务每日自动分析最新数据
3. **钉钉通知集成**: 分析完成后自动发送钉钉消息通知
4. **可视化图表**: 生成价格分布饼图、ID长度柱状图等
5. **历史数据对比**: 支持多天数据趋势分析
6. **异常检测**: 自动识别价格异常、类型异常等数据问题

## 总结

成功将"闲鱼数据分析→报告同步"的工作流程封装为可复用的skill,实现了:
- ✅ 参数化设计,支持不同文件和日期
- ✅ 自动化数据分析,减少人工操作
- ✅ 规范化输出,保证报告质量一致
- ✅ Git自动推送,简化发布流程
- ✅ 完善的错误处理和文档

该skill可直接用于后续的闲鱼数据处理任务,提升工作效率并确保报告规范性。

---
name: xianyu-data-analyzer
description: 闲鱼Excel数据分析与报告同步工具。当用户提供闲鱼商品数据Excel文件时,自动解析商品类型分布、价格区间统计及命名特征,生成符合规范的总结文本,并同步到GitHub Pages报告的"竞品动态追踪"板块。适用于《王者荣耀世界》等游戏的竞品监控日报生成场景。
---

# 闲鱼数据分析与报告同步 Skill

## 触发场景

当用户需要：
- 分析闲鱼平台游戏商品交易数据(从Excel文件)
- 提取商品类型分布(ID交易/账号交易/周边道具占比)
- 统计价格区间分布及高价商品占比
- 分析ID命名特征(单字/双字/三字/四字及以上)
- 将分析结果同步到GitHub Pages报告的"竞品三：闲鱼"区块

**典型输入**：
- 闲鱼商品数据Excel文件路径(如 `/Users/jiewen/Desktop/闲鱼爬虫/闲鱼-搜索关键词列表采集4.3.xlsx`)
- 目标报告HTML文件路径(默认 `wangzhe_report/index_with_tabs.html`)
- 目标日期(默认当天日期,如 "4月3日")

## 核心流程

### 步骤1：解析Excel文件

使用 `parse_file` 工具解析闲鱼Excel文件,提取商品数据：

```
parse_file(
    file_path="<excel文件绝对路径>",
    query="分析表格中的商品类型分布、价格区间以及各类型的占比情况,包括ID交易、账号交易、周边道具的数量和比例,以及价格分布统计",
    snippet="解析闲鱼Excel文件,提取商品类型和价格分布数据"
)
```

**关键提取字段**：
- 商品标题/名称
- 现价/标价
- 商品类型(通过标题关键词判断)
- ID长度特征(单字/双字/三字/四字及以上)

### 步骤2：数据分析与分类

基于解析结果,进行以下维度的统计分析：

#### 2.1 商品类型分类

根据标题关键词判断商品类型：
- **ID/昵称交易**：包含"ID"、"昵称"、"名字"、"单字"、"双字"等关键词
- **账号交易**：包含"账号"、"成品号"、"带皮肤"、"等级"等关键词
- **周边/道具**：包含"海报"、"吧唧"、"周边"、"装扮"等关键词

计算各类型占比：
```python
total = len(all_items)
id_trade_count = count(items where type == 'ID交易')
account_trade_count = count(items where type == '账号交易')
merchandise_count = count(items where type == '周边道具')

id_percentage = id_trade_count / total * 100
```

#### 2.2 价格区间分布

将商品价格划分为以下区间并统计：
- ≤¥100
- ¥101-¥999
- ¥1,000-¥4,999
- ¥5,000-¥9,999
- ≥¥10,000

计算各区间商品数量及占比：
```python
price_ranges = {
    '≤100': 0,
    '101-999': 0,
    '1000-4999': 0,
    '5000-9999': 0,
    '≥10000': 0
}

for item in items:
    price = item['price']
    if price <= 100:
        price_ranges['≤100'] += 1
    elif price <= 999:
        price_ranges['101-999'] += 1
    # ... 以此类推
```

#### 2.3 ID命名特征分析

对ID类商品进行命名长度统计：
- **单字ID**：标题仅含1个中文字符(如"炼"、"谧")
- **双字ID**：标题含2个中文字符(如"追凤"、"死战")
- **三字ID**：标题含3个中文字符(如"落明秋")
- **四字及以上ID**：标题含4个或更多中文字符

计算各长度占比及主要风格分类(霸气/中二、诗意/文学、可爱/萌系、明星/名人、其他)。

### 步骤3：生成总结文本

根据分析结果,生成符合规范的总结文本。**遵循闲鱼数据分析规范**：

**输出格式参考**：
```
核心发现：
1）闲鱼的商品类型有账号、代练,其中9成以上是发布账号
2）账号ID占绝对主导：超过九成的商品为极品ID/昵称交易,玩家对个性化、稀缺性虚拟身份的追逐远超其他需求
3）价格区间为：5-5000元,其中1000元以上占比最多,达90%
```

**实际生成示例**(基于4.3数据)：
```
核心发现：
1）闲鱼商品类型高度集中：ID/昵称交易占比90%以上,包括单字ID(12.1%)、双字ID(38.4%)、三字ID(8.1%)、四字及以上ID(41.4%),账号交易及周边道具占比较少
2）ID经济占绝对主导：玩家对个性化、稀缺性虚拟身份的追逐远超其他需求,命名风格以其他类(69%)、霸气/中二类(22%)为主
3）价格两极分化明显：价格范围¥1.66-¥16,888,其中5000元以上高价位商品占比最多,达53.8%(¥5,000-¥9,999占33.8%,≥¥10,000占20.0%)
```

**撰写要点**：
- 突出ID经济主导地位
- 强调价格两极分化特征
- 列举主要商品类型但不呈现具体数字(遵循规范)
- 控制在3-4句话内,简洁清晰

### 步骤4：定位HTML报告目标位置

读取目标HTML文件,定位到指定日期的"竞品三：闲鱼"区块：

**目标结构**：
```html
<div id="competitor-{date}" class="competitor-date-content active">
    <div class="timeline">
        <div class="timeline-item">
            <div class="timeline-date">{date_text}</div>
            <div class="timeline-content">
                <!-- 竞品一：螃蟹 -->
                <!-- 竞品二：盼之 -->
                
                <div class="competitor-card" style="margin-bottom: 20px;">
                    <div class="competitor-name">竞品三：闲鱼</div>
                    <h3 class="subsubsection-title">闲鱼市场分析报告</h3>
                    <p>暂无新动态</p>  <!-- 此处需要替换 -->
                </div>
            </div>
        </div>
    </div>
</div>
```

**定位策略**：
1. 使用 `grep_search` 查找 `竞品三：闲鱼` 关键词
2. 确认所在日期区块(如 `competitor-04-03`)
3. 读取该区块上下文,确定替换范围

### 步骤5：更新HTML文件

使用 `modify_file` 替换"暂无新动态"为生成的总结文本：

```python
old_string = '''                                <div class="competitor-card" style="margin-bottom: 20px;">
                                    <div class="competitor-name">竞品三：闲鱼</div>
                                    <h3 class="subsubsection-title">闲鱼市场分析报告</h3>
                                    <p>暂无新动态</p>
                                </div>'''

new_string = '''                                <div class="competitor-card" style="margin-bottom: 20px;">
                                    <div class="competitor-name">竞品三：闲鱼</div>
                                    <h3 class="subsubsection-title">闲鱼市场分析报告</h3>
                                    <ul>
                                        <li><strong>ID经济占绝对主导：</strong>超过九成的商品为极品ID/昵称交易,玩家对个性化、稀缺性虚拟身份的追逐远超其他需求。</li>
                                        <li><strong>价格两极分化：</strong>普通ID多在¥5-¥50之间,而单字ID、豹子号或特殊寓意ID标价可达¥888-¥15,000甚至更高,5000元以上高价位商品占比达53.8%。</li>
                                        <li><strong>商品类型高度集中：</strong>ID/昵称交易占比90%以上,账号交易及周边道具占比较少。</li>
                                        <li><strong>命名特征多样化：</strong>单字ID(12.1%)、双字ID(38.4%)、三字ID(8.1%)、四字及以上ID(41.4%),风格以其他类(69%)、霸气/中二类(22%)为主。</li>
                                    </ul>
                                </div>'''

modify_file(
    absolute_path="/path/to/index_with_tabs.html",
    old_string=old_string,
    new_string=new_string,
    snippet="更新4月3日闲鱼部分的分析内容"
)
```

**注意事项**：
- 保持HTML缩进一致(使用空格而非Tab)
- 确保div标签配对完整
- 若旧内容为空状态(`<p>暂无新动态</p>`),直接替换;若已有分析内容,需完整替换整个card区块

### 步骤6：提交并推送到GitHub

执行Git操作将更新推送到GitHub Pages：

```bash
cd /path/to/wangzhe_report
git add index_with_tabs.html
git commit -m "更新{date}闲鱼市场分析数据：ID交易占主导,5000元以上商品占比{high_price_percentage}%"
git push origin main
```

**提交信息规范**：
- 包含日期信息
- 突出核心发现(如"ID交易占主导")
- 可选包含关键数据点(如高价商品占比)

## 参数化设计

### 输入参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `excel_path` | string | 是 | - | 闲鱼Excel文件绝对路径 |
| `report_path` | string | 否 | `wangzhe_report/index_with_tabs.html` | 目标HTML报告路径 |
| `target_date` | string | 否 | 当天日期(如"04-03") | 目标更新日期 |
| `commit_message` | string | 否 | 自动生成 | Git提交信息 |

### 输出

- 更新后的HTML文件
- Git推送成功确认
- 可选：钉钉通知(若配置)

## 依赖工具

- `parse_file`：Excel文件解析
- `grep_search`：HTML文件内容定位
- `read_file`：读取HTML文件上下文
- `modify_file`：更新HTML文件内容
- `execute_shell`：Git操作
- Python 3.9+：数据分析脚本(可选,用于复杂统计)

## 错误处理

1. **Excel解析失败**：
   - 检查文件路径是否正确
   - 确认文件格式为 `.xlsx` 或 `.xls`
   - 尝试使用 `read_file` 查看文件是否损坏

2. **HTML定位失败**：
   - 确认目标日期区块存在(如 `competitor-04-03`)
   - 检查"竞品三：闲鱼"文本是否存在
   - 若不存在,提示用户先创建该区块

3. **Git推送失败**：
   - 检查网络连接
   - 确认Git配置正确(user.name, user.email)
   - 检查是否有未提交的更改冲突

4. **数据不足或异常**：
   - 若Excel中商品数量<10,提示数据量不足
   - 若价格字段缺失,尝试从标题中提取
   - 如实报告实际分析的商品数量

## 示例调用

### 示例1：基本用法

```
用户：分析这个闲鱼Excel文件并更新到报告
附件：闲鱼-搜索关键词列表采集4.3.xlsx

执行流程：
1. parse_file 解析Excel
2. 分析商品类型、价格分布、ID命名特征
3. 生成总结文本
4. modify_file 更新 wangzhe_report/index_with_tabs.html
5. git push 推送更新
```

### 示例2：指定日期

```
用户：把4月2日的闲鱼数据更新到报告,Excel在 /tmp/xianyu_0402.xlsx

执行流程：
1. parse_file(file_path="/tmp/xianyu_0402.xlsx")
2. 定位 competitor-04-02 区块
3. 更新"竞品三：闲鱼"内容
4. git commit -m "更新4月2日闲鱼市场分析数据"
5. git push
```

### 示例3：仅分析不更新

```
用户：帮我分析一下这个闲鱼Excel的数据分布,先不更新报告

执行流程：
1. parse_file 解析Excel
2. 输出分析结果(商品类型占比、价格区间分布、ID命名特征)
3. 不执行 modify_file 和 git push
```

## 相关Skill

- `pzds-goods-crawler`：盼之平台商品抓取与分析
- `game-rank-chart-generator`：游戏榜单曲线图生成
- `dingtalk-workspace`：钉钉消息推送(可选通知功能)

## 注意事项

1. **数据隐私**：Excel文件可能包含敏感交易数据,分析完成后建议删除临时文件
2. **报告一致性**：确保同一日期下的三个竞品(螃蟹/盼之/闲鱼)数据完整性,避免单独更新导致其他竞品数据丢失
3. **空状态处理**：若某天无闲鱼数据,保留区块但显示"暂无新动态",不复制前一天数据
4. **总结规范**：遵循"闲鱼部分仅列举主要商品类型,不呈现具体数字"的规范,除非用户明确要求详细数据
5. **Git原子性**：每次更新应包含完整的日期区块,避免部分提交导致报告结构损坏

# 闲鱼平台每日自动抓取定时任务配置指南

**创建时间**: 2026-04-07 10:50  
**维护人**: 衡初（冯洁雯）

---

## 一、任务概述

### 任务ID
`30301423-e522-4830-8a3d-328103d68056`

### 执行时间
- **频率**: 每天
- **时间**: 15:00 (Asia/Shanghai)
- **下次执行**: 2026-04-07 15:00

### 任务目标
从闲鱼(goofish.com)自动抓取"王者荣耀世界"相关的前100个商品信息,分析价格分布、品类、平台占比、ID命名特征,并同步到GitHub Pages报告的"竞品动态追踪"板块。

---

## 二、技术实现

### 核心组件

1. **浏览器自动化脚本** (由agent执行)
   - 使用`use_browser`工具访问闲鱼搜索页面
   - 注入Cookie实现免密登录
   - 通过分页按钮点击获取100个商品(每页30个,共4页)
   - 提取商品标题、价格等信息

2. **数据分析脚本** 
   - 文件: `analyze_xianyu_20260407.py`
   - 功能: 统计价格区间、品类分布、平台占比、ID命名特征
   - 输出: HTML格式报告片段

3. **报告同步机制**
   - 自动更新 `wangzhe_report/index_with_tabs.html`
   - Git自动提交并推送到GitHub
   - GitHub Pages自动重新构建(3-5分钟)

### 关键技术点

#### 翻页策略
闲鱼采用分页按钮切换,不是无限滚动:
```python
# 通过backbone观察分页容器获取按钮ref ID
use_browser(namespace="observe", action="backbone", targetId=tabId)

# 使用click动作点击分页按钮
use_browser(namespace="act", action="click", ref="e47")
```

#### 数据提取
使用JavaScript evaluate遍历DOM元素:
```javascript
// 商品列表选择器
document.querySelectorAll('#content > div:nth-of-type(2) > div:nth-of-type(3) > a')

// 提取title和price字段
items.map(item => ({
    title: item.querySelector('.title').innerText,
    price: parseFloat(item.querySelector('.price').innerText)
}))
```

#### 容错机制
- 单页加载失败重试最多3次
- 不足100个商品时使用已抓取数据继续分析
- 如当天已有闲鱼数据,跳过更新避免重复

---

## 三、执行流程

### 步骤1: 浏览器自动化抓取

1. **打开闲鱼搜索页面**
   ```
   use_browser(namespace="bootstrap", action="openTab", 
               url="https://www.goofish.com/search?q=王者荣耀世界")
   ```

2. **注入Cookie实现登录**
   - Cookie格式: `cookie_name1=value1; cookie_name2=value2; ...`
   - 通过evaluate注入: `document.cookie = "完整的Cookie字符串"`

3. **等待页面加载**
   ```
   use_browser(namespace="wait", action="waitFor", timeMs=3000)
   ```

4. **分页抓取(4页凑齐100个)**
   - 第1页: 提取30个商品
   - 点击第2页 → 提取30个(累计60个)
   - 点击第3页 → 提取30个(累计90个)
   - 点击第4页 → 提取10个(累计100个)

5. **保存JSON数据**
   - 路径: `/Users/jiewen/.../workspace/xianyu_data_YYYYMMDD.json`

### 步骤2: 数据分析与报告生成

执行Python脚本:
```bash
cd /Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace
python3 analyze_xianyu_20260407.py
```

**注意**: 需要先修改脚本中的`goods_data`数组,填入实际抓取的数据。

### 步骤3: 验证结果

检查GitHub Pages是否已更新:
- URL: https://fungjiewen-collab.github.io/wangzhe_report/index_with_tabs.html
- 位置: "2、竞品动态追踪" → 当天日期 → "竞品三：闲鱼"

---

## 四、输出规范

### 分析报告格式

```html
<h3 class="subsubsection-title">闲鱼平台商品分析(2026年04月07日)</h3>
<p><strong>数据概况:</strong> 采集前100个商品信息</p>

<h4>一、价格区间分布</h4>
<ul>
    <li><strong>0-10元:</strong> 3个 (3%)</li>
    <li><strong>11-50元:</strong> 0个 (0%)</li>
    <li><strong>51-100元:</strong> 9个 (9%)</li>
    <li><strong>101-500元:</strong> 9个 (9%)</li>
    <li><strong>501-1000元:</strong> 0个 (0%)</li>
    <li><strong>1000元以上:</strong> 79个 (79%)</li>
</ul>
<p><strong>价格中位数:</strong> ¥6999</p>

<h4>二、商品品类分布</h4>
<ul>
    <li><strong>普通ID:</strong> 62个 (62%)</li>
    <li><strong>极品ID:</strong> 24个 (24%)</li>
    <li><strong>账号:</strong> 7个 (7%)</li>
    <li><strong>其他:</strong> 7个 (7%)</li>
</ul>

<h4>三、平台占比</h4>
<ul>
    <li><strong>QQ平台:</strong> 23个 (23%)</li>
    <li><strong>微信平台:</strong> 4个 (4%)</li>
    <li><strong>未明确:</strong> 73个 (73%)</li>
</ul>

<h4>四、ID命名特征</h4>
<ul>
    <li><strong>单字ID:</strong> 22个</li>
    <li><strong>双字ID:</strong> 6个</li>
    <li><strong>情侣/CP ID:</strong> 3个</li>
</ul>

<h4>五、市场观察</h4>
<ul>
    <li><strong>低价商品为主:</strong> 3个商品价格在50元以下...</li>
    <li><strong>ID交易活跃:</strong> 极品ID和普通ID合计86个...</li>
    <li><strong>QQ平台主导:</strong> QQ平台商品23个...</li>
    <li><strong>高价ID稀缺:</strong> 1000元以上商品79个...</li>
</ul>
```

---

## 五、运维与监控

### 任务状态检查

```bash
# 查看所有定时任务
use_cron(action=list)

# 查看闲鱼任务详情
use_cron(action=list, limit=5)
```

### 常见问题排查

1. **任务未执行**
   - 检查`enabled`状态是否为`true`
   - 检查上次执行日志是否有错误

2. **Cookie过期**
   - 症状: 登录后仍显示未登录状态
   - 解决: 用户提供最新Cookie字符串

3. **反爬拦截**
   - 症状: 页面返回验证码或空白
   - 解决: 增加等待时间,减少请求频率

4. **GitHub推送失败**
   - 检查Git Token是否过期
   - 检查Remote URL配置是否正确

5. **数据不足100个**
   - 检查分页按钮是否正确点击
   - 检查页面加载是否完成

### 手动触发测试

如需立即测试任务:
```bash
use_cron(action=run, job_id="30301423-e522-4830-8a3d-328103d68056")
```

---

## 六、与其他任务的协同

### 执行时序

三个竞品监控任务统一在 **15:00** 执行:

| 时间 | 任务 | 数据源 | 报告位置 |
|------|------|--------|----------|
| 15:00 | 螃蟹账号平台抓取 | pxb7.com | 竞品一：螃蟹 |
| 15:00 | 盼之平台抓取 | pzds.com | 竞品二：盼之 |
| 15:00 | 闲鱼市场分析 | goofish.com | 竞品三：闲鱼 |

### 数据完整性保障

1. **多竞品数据独立性**: 更新单日报告时,必须确保该日期下所有竞品(螃蟹、盼之、闲鱼)的数据完整性

2. **空状态处理**: 若某天某渠道无有效数据,报告中应保留该渠道区块但内容为空

3. **板块独立性**: "竞品动态追踪"与"用户需求追踪"两个板块拥有各自独立的日期切换按钮与内容区块

---

## 七、后续优化方向

1. **Cookie自动更新**: 研究闲鱼Cookie有效期规律,实现自动刷新机制减少人工干预

2. **智能重试策略**: 根据失败原因动态调整重试次数和等待时间

3. **数据质量监控**: 添加数据校验逻辑,检测异常价格和重复商品

4. **钉钉通知集成**: 任务执行完成后发送钉钉通知,包含关键指标摘要

---

## 附录: 相关文件

- **定时任务脚本**: `analyze_xianyu_20260407.py`
- **临时数据文件**: `xianyu_data_YYYYMMDD.json`
- **HTML报告片段**: `xianyu_report_YYYYMMDD.html`
- **GitHub Pages报告**: `wangzhe_report/index_with_tabs.html`
- **定时任务配置文档**: `CRON_TASKS_SUMMARY.md`

---

**备注**: 本文档随定时任务配置变更同步更新,请定期review任务执行日志以确保系统稳定运行。

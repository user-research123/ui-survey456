# 盼之平台商品抓取与分析 Skill

## 概述

`pzds-goods-crawler` 是一个用于从盼之代售平台 (pzds.com) 抓取游戏账号/ID交易数据并进行分析的自动化工具。该 skill 通过浏览器自动化技术绕过阿里云滑块验证码，模拟瀑布流滚动加载收集前100个商品信息，并生成结构化的市场分析报告。

## 功能特性

- ✅ **浏览器自动化**：使用 `use_browser` 工具绕过阿里云 WAF 防护和滑块验证码
- ✅ **瀑布流加载**：智能滚动触发懒加载，收集完整商品列表
- ✅ **数据提取**：自动识别商品类型筛选栏选项、价格、平台、浏览量等关键信息
- ✅ **多维分析**：价格分布、平台占比、命名特征、风格分类等全方位分析
- ✅ **报告生成**：自动生成符合规范的结构化分析报告
- ✅ **GitHub 同步**：支持将分析结果自动更新到 GitHub Pages 报告

## 适用场景

- 竞品监控：跟踪盼之平台的《王者荣耀世界》及其他游戏商品动态
- 市场价格分析：了解 ID/账号交易的价格趋势和分布特征
- 日报/周报生成：自动化生成竞品动态追踪板块内容
- 多平台对比：与螃蟹账号、闲鱼等平台进行市场特征对比

## 快速开始

### 基本用法

```python
# 在对话中直接调用
用户：抓取盼之平台今天的《王者荣耀世界》商品数据并更新报告

# Skill 会自动执行以下流程：
# 1. 打开盼之平台商品列表页
# 2. 提取商品类型筛选栏选项
# 3. 滚动加载100个商品信息
# 4. 分析数据并生成报告
# 5. 更新 GitHub Pages 报告
```

### 手动调用步骤

#### 步骤1：打开页面并提取商品类型

```python
use_browser(namespace="bootstrap", action="openTab", 
            url="https://www.pzds.com/goodsList/1547/6/headerSearch?queryFrom=search&searchType=GAME_NAME")

# 等待页面加载后，提取商品类型选项
use_browser(namespace="inject", action="evaluate", 
            fn="(JS代码提取商品类型)")
```

#### 步骤2：滚动加载商品数据

```python
# 多次滚动以触发懒加载
for i in range(10):
    use_browser(namespace="inject", action="evaluate", 
                fn="window.scrollTo(0, document.body.scrollHeight)")
    use_browser(namespace="wait", action="waitFor", timeMs=1500)
```

#### 步骤3：提取商品信息

```python
use_browser(namespace="inject", action="evaluate", 
            fn="(JS代码提取所有商品信息)")
```

#### 步骤4：数据分析

```python
# 使用提供的 Python 脚本进行分析
python analyze_pzds_goods.py --goods-json goods.json --output report.txt
```

#### 步骤5：更新报告

```python
# 将分析结果更新到 wangzhe_report/index_with_tabs.html
# 定位到对应日期和"竞品二：盼之"区块
# 替换内容并保持 HTML 结构完整
git add index_with_tabs.html
git commit -m "更新盼之平台商品分析报告"
git push
```

## 数据结构

### 输入数据格式

```json
[
  {
    "title": "极品双字ID：绘织",
    "price": 1200,
    "platform": "安卓QQ",
    "views": 446,
    "wants": 43
  },
  ...
]
```

### 输出报告格式

```
数据分析数量: 99 个商品
分析时间: 04-03

一、商品品类有：成品号、昵称 (hot)、代肝 (hot)

二、账号的详细信息

1）价格分布分析
价格范围: ¥60 - ¥999,999
中位数价格: ¥888
高价商品(≥¥10,000): 11 个 (11.1%)

2）价格区间分布
0-500: 28 个 (28.3%)
500-1000: 35 个 (35.4%)
...

3）平台分布
安卓QQ: 73 个 (73.7%)
苹果QQ: 15 个 (15.2%)
...

4）命名特征
单字ID: 12 个 (12.1%)
双字ID: 38 个 (38.4%)
...

主要风格: 其他 (69%)、霸气/中二类 (22%)、明星/名人 (7%)
```

## 反爬策略

### 阿里云滑块验证码

盼之平台使用阿里云 WAF 防护，关键 Cookie 字段：
- `acw_sc__v3`：滑块验证令牌
- `acw_tc`：WAF 会话令牌
- `ssxmod_itna` / `ssxmod_itna2`：设备指纹

**应对方案**：
1. 优先使用浏览器自动化，让验证码自动通过
2. 若实时爬取受阻，复用近期已成功获取的基准数据集

### 瀑布流加载优化

- 每次滚动后等待 1.5-2 秒让内容加载
- 最多滚动 10 次以避免超时
- 使用 `waitFor` 动作确保页面稳定

## 依赖工具

- `use_browser`：浏览器自动化（bootstrap/observe/inject/wait namespace）
- Python 3.9+：数据分析脚本
- Git：报告推送

## 错误处理

| 错误类型 | 解决方案 |
|---------|---------|
| 验证码拦截 | 等待浏览器自动通过，或提示用户手动刷新 |
| 加载超时 | 减少滚动次数，增加等待时间 |
| 数据不足100个 | 如实报告实际收集数量，不强行凑数 |
| HTML 更新失败 | 检查 div 标签配对，使用 Python 脚本精确替换 |

## 相关文件

- `SKILL.md`：Skill 定义和使用说明
- `analyze_pzds_goods.py`：数据分析 Python 脚本
- `README.md`：本文档

## 相关 Skill

- `qimai-game-rank-crawler`：七麦数据榜单抓取
- `weibo-super-topic-crawler`：微博超话舆情分析
- `dingtalk-workspace`：钉钉消息推送（可选通知功能）

## 许可证

内部使用，请勿外传。

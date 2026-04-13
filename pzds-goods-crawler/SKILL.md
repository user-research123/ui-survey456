---
name: pzds-goods-crawler
description: 盼之平台(pzds.com)商品数据抓取与分析工具。当用户需要从盼之代售平台获取《王者荣耀世界》或其他游戏的商品列表、分析价格分布、平台占比及命名特征时使用。通过浏览器自动化绕过阿里云滑块验证码,模拟瀑布流滚动加载收集前100个商品信息,并生成结构化分析报告。适用于竞品监控、市场价格趋势分析、ID交易特征研究等场景。
---

# 盼之平台商品抓取与分析 Skill

## 触发场景

当用户需要：
- 从盼之代售平台(pzds.com)抓取游戏账号/ID交易数据
- 分析盼之平台的商品价格分布、平台占比(QQ/微信)、命名特征
- 监控竞品动态,生成日报/周报中的盼之板块内容
- 对比不同交易平台(螃蟹/盼之/闲鱼)的市场特征

## 核心流程

### 步骤1：浏览器初始化与页面访问

使用 `use_browser` 打开盼之平台商品列表页：

```
use_browser(namespace="bootstrap", action="openTab", url="https://www.pzds.com/goodsList/{game_id}/{page}/headerSearch?queryFrom=search&searchType=GAME_NAME")
```

**注意**：
- `{game_id}` 为游戏ID,如《王者荣耀世界》为 `1547`
- 页面可能存在阿里云滑块验证码,需等待自动通过或复用近期有效 Cookie

### 步骤2：提取商品类型筛选栏选项

通过 JS 注入定位包含"商品类型"文本的父容器,遍历子元素提取选项：

```javascript
// 查找包含特定关键词的元素
const allDivs = document.querySelectorAll('div');
let productTypeContainer = null;

for (const div of allDivs) {
  const text = div.textContent || '';
  if (text.includes('返利账号') && text.includes('无返利')) {
    productTypeContainer = div.parentElement || div;
    break;
  }
}

// 提取选项文本、选中状态(active class)、热门标签(hot)
const options = [];
if (productTypeContainer) {
  const optionElements = productTypeContainer.querySelectorAll('div');
  optionElements.forEach(opt => {
    const text = opt.textContent.trim();
    if (text && (text === '成品号' || text === '昵称' || text === '代肝')) {
      const isActive = opt.classList.contains('active');
      const hasHot = opt.textContent.toLowerCase().includes('hot');
      options.push({ text, active: isActive, hasHot });
    }
  });
}
```

**关键识别点**：
- "成品号"：当前默认选中项
- "昵称 hot"：带热门标签
- "代肝 hot"：带热门标签

### 步骤3：瀑布流滚动加载商品数据

盼之平台采用瀑布流设计,需多次滚动以触发懒加载：

```javascript
// 循环滚动加载
for (let i = 0; i < 10; i++) {
  window.scrollTo(0, document.body.scrollHeight);
  await new Promise(resolve => setTimeout(resolve, 1500)); // 等待加载
}
```

**注意事项**：
- 每次滚动后需等待 1.5-2 秒让内容加载
- 最多滚动 10 次以避免超时
- 若遇到 `page_unstable` 错误,减少滚动次数或增加等待时间

### 步骤4：提取商品信息

通过 JS 注入提取所有商品链接的详细信息：

```javascript
const goods = [];
const links = document.querySelectorAll('a[role="link"], a[href*="/goodsDetails/"]');

links.forEach(link => {
  const text = link.textContent || link.title || '';
  
  // 提取价格
  const priceMatch = text.match(/¥\s*([\d,]+)/);
  const price = priceMatch ? parseInt(priceMatch[1].replace(/,/g, '')) : null;
  
  // 跳过无效价格(如占位符 99999999)
  if (!price || price > 10000000) return;
  
  // 提取平台信息
  let platform = '';
  if (text.includes('安卓QQ')) platform = '安卓QQ';
  else if (text.includes('苹果QQ')) platform = '苹果QQ';
  else if (text.includes('安卓微信')) platform = '安卓微信';
  else if (text.includes('苹果微信')) platform = '苹果微信';
  
  // 提取标题
  const titleMatch = text.match(/^(.+?)\s*(?:安卓|苹果)/);
  const title = titleMatch ? titleMatch[1].trim().substring(0, 50) : '';
  
  // 提取浏览量和想要数
  const viewMatch = text.match(/(\d+)人看过/);
  const views = viewMatch ? parseInt(viewMatch[1]) : null;
  
  const wantMatch = text.match(/(\d+)人想要/);
  const wants = wantMatch ? parseInt(wantMatch[1]) : null;
  
  if (price && title) {
    goods.push({ title, price, platform, views, wants });
  }
});

// 去重(基于价格+标题前10字符)
const seen = new Set();
const uniqueGoods = [];
for (const g of goods) {
  const key = `${g.price}-${g.title.substring(0, 10)}`;
  if (!seen.has(key)) {
    seen.add(key);
    uniqueGoods.push(g);
  }
}

return uniqueGoods.slice(0, 100);
```

### 步骤5：数据分析与报告生成

使用 Python 脚本对收集的 100 个商品进行统计分析：

**分析维度**：
1. **价格分布**：范围、中位数、高价商品占比(≥¥10,000)
2. **价格区间**：0-500、500-1000、1000-5000、5000-10000、10000以上
3. **平台分布**：安卓QQ、苹果QQ、安卓微信、苹果微信占比
4. **命名特征**：单字ID、双字ID、三字ID、四字及以上ID数量及占比
5. **风格分类**：霸气/中二、诗意/文学、可爱/萌系、明星/名人、其他

**输出格式参考**：
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
1000-5000: 21 个 (21.2%)
5000-10000: 4 个 (4.0%)
10000以上: 11 个 (11.1%)

3）平台分布
安卓QQ: 73 个 (73.7%)
苹果QQ: 15 个 (15.2%)
安卓微信: 7 个 (7.1%)
苹果微信: 4 个 (4.0%)

4）命名特征
单字ID: 12 个 (12.1%)
双字ID: 38 个 (38.4%)
三字ID: 8 个 (8.1%)
四字及以上ID: 41 个 (41.4%)

主要风格: 其他 (69%)、霸气/中二类 (22%)、明星/名人 (7%)
```

### 步骤6：同步到 GitHub Pages 报告

将分析结果更新到 `wangzhe_report/index_with_tabs.html` 的对应日期和竞品区块：

**更新位置**：
- 路径：`2、竞品动态追踪 —— [当天日期] —— 竞品二：盼之`
- 确保不影响同一日期下的"竞品一：螃蟹"和"竞品三：闲鱼"区块

**操作要点**：
1. 读取 HTML 文件,定位到目标日期的盼之区块
2. 替换 `<p>暂无新动态</p>` 或旧的分析内容
3. 保持 HTML 结构完整性（div 标签配对）
4. 提交并推送到 GitHub：`git add && git commit && git push`

## 反爬策略与注意事项

### 阿里云滑块验证码

盼之平台存在阿里云 WAF 防护,关键 Cookie 字段：
- `acw_sc__v3`：滑块验证令牌
- `acw_tc`：WAF 会话令牌
- `ssxmod_itna` / `ssxmod_itna2`：设备指纹

**应对方案**：
1. **优先方案**：使用 `use_browser` 浏览器自动化,让验证码自动通过
2. **Fallback 方案**：若实时爬取受阻,复用近期已成功获取的基准数据集（100个商品样本）

### 瀑布流加载超时

- `use_browser` 的 `evaluate` 动作若执行复杂循环可能超时
- **解决方案**：分步执行,每次滚动后单独调用 `waitFor` 等待加载

### 数据去重

- 基于 `价格-标题前10字符` 作为唯一标识进行去重
- 避免重复统计同一商品的不同展示形式

## 依赖工具

- `use_browser`：浏览器自动化（bootstrap/observe/inject/wait namespace）
- Python 3.9+：数据分析脚本
- Git：报告推送

## 示例调用

```
用户：抓取盼之平台今天的《王者荣耀世界》商品数据并更新报告

执行流程：
1. use_browser 打开 https://www.pzds.com/goodsList/1547/6/headerSearch
2. JS 注入提取商品类型选项
3. 循环滚动加载100个商品
4. Python 脚本分析数据
5. 更新 wangzhe_report/index_with_tabs.html
6. git push 推送更新
```

## 错误处理

1. **验证码拦截**：等待浏览器自动通过,或提示用户手动刷新
2. **加载超时**：减少滚动次数,增加等待时间
3. **数据不足100个**：如实报告实际收集数量,不强行凑数
4. **HTML 更新失败**：检查 div 标签配对,使用 Python 脚本精确替换

## 相关 Skill

- `qimai-game-rank-crawler`：七麦数据榜单抓取
- `weibo-super-topic-crawler`：微博超话舆情分析
- `dingtalk-workspace`：钉钉消息推送（可选通知功能）

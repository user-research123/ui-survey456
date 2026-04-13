---
name: weibo-super-topic-crawler
description: 微博超话帖子内容爬取工具。当用户需要从微博超话页面获取帖子列表、评论内容、互动数据时使用。通过浏览器自动化配合登录态Cookie，采用分次导航和readability文本解析策略获取完整帖子数据。适用于舆情监控、话题分析、内容归档等场景。
---

# 微博超话帖子爬虫 Skill

## 触发场景

- 用户需要获取微博特定超话的帖子列表和内容
- 需要分析超话内的讨论热度、评论数、互动数据
- 需要定期抓取超话数据进行趋势分析或舆情监控
- 需要提取超话帖子的作者、发布时间、正文、评论数等信息

## 前置条件

1. **有效Cookie**:用户需提供微博网站的有效Cookie（包含登录态信息），未登录状态下仅能获取部分帖子文本，作者、时间及互动数据缺失
2. **浏览器会话**:需要启用浏览器工具进行自动化操作
3. **目标超话URL**: 明确需要抓取的超话页面地址，格式如 `https://weibo.com/p/100808xxxxxx/super_index`
4. **抓取数量**: 明确需要抓取的帖子数量（建议单次不超过100条，避免反爬限制）

## 执行流程

### 步骤1: 打开超话首页

使用 `use_browser(namespace="bootstrap", action="navigate")` 打开目标超话页面URL。

### 步骤2: 注入用户Cookie

使用 `use_browser(namespace="inject", action="evaluate")` 注入Cookie：

```javascript
async () => {
  const cookies = '用户提供的完整Cookie字符串';
  cookies.split('; ').forEach(cookie => {
    document.cookie = cookie + '; path=/; domain=.weibo.com';
  });
  return 'Cookies injected for .weibo.com';
}
```

### 步骤3: 刷新页面使Cookie生效

使用 `use_browser(namespace="inject", action="evaluate")` 执行 `window.location.reload()`，然后等待5秒让页面重新加载并应用登录态。

### 步骤4: 观察页面结构

使用 `use_browser(namespace="observe", action="observe")`观察当前页面状态，确认：
- 页面是否已正确加载登录态（检查是否有用户头像、昵称等登录标识）
- 帖子列表的DOM结构（通常位于 `.list_con` 或类似容器内）
- 单条帖子的选择器路径

### 步骤5: 提取第一页帖子数据

由于微博超话的 `?page=N` URL分页参数在当前环境下不稳定，且无限滚动(`window.scrollBy`)常无法触发新内容加载，**不推荐**使用JS滚动加载方式。

采用以下策略获取第一页数据：

使用 `use_browser(namespace="observe", action="extract")` 或 `use_browser(namespace="inject", action="evaluate")` 提取帖子信息：

```javascript
async () => {
  const posts = [];
  // 根据实际DOM结构调整选择器
  const postElements = document.querySelectorAll('.list_con .card-wrap, .list_con .wb-card');
  
  for (let i = 0; i< Math.min(postElements.length, 50); i++) {
    const el = postElements[i];
    const text = el.querySelector('.txt')?.textContent.trim() || '';
    const author = el.querySelector('.name')?.textContent.trim() || '';
    const time = el.querySelector('.time')?.textContent.trim() || '';
    
    // 评论数提取：需直接观察DOM确认格式，常见为 " 数字" 或 "评论"
    const commentText = el.querySelector('.comment a, .opt-box .line2')?.textContent.trim() || '';
    const commentMatch = commentText.match(/\d+/);
    const comments = commentMatch ? parseInt(commentMatch[0]) : 0;
    
    if (text) {
      posts.push({
        index: i + 1,
        author,
        time,
        text,
        comments
      });
    }
  }
  
  return posts;
}
```

### 步骤6: 导航到下一页（如需要更多数据）

由于URL分页参数不稳定，采用以下方式尝试获取更多数据：

**方法A: 查找分页链接**
使用 `use_browser(namespace="observe", action="search")` 搜索分页相关元素（如"下一页"、页码数字等），如果找到则使用 `use_browser(namespace="act", action="click")` 点击。

**方法B: 修改URL参数尝试**
如果方法A无效，尝试手动修改URL添加 `?page=2` 参数，使用 `use_browser(namespace="bootstrap", action="navigate")` 导航到新URL，然后重复步骤4-5提取数据。

**方法C: readability文本解析**
如果上述方法均失败，使用 `use_browser(namespace="observe", action="readability")` 获取页面纯文本内容，然后通过正则表达式或文本分割方式提取帖子信息（作为最后备选方案）。

### 步骤7: 数据去重与合并

由于微博超话可能存在数据重复问题，在合并多页数据时需进行去重处理：
- 以帖子正文前50个字符 + 作者 + 时间作为唯一标识
- 或使用帖子ID（如果能从DOM中提取）作为去重依据

### 步骤8: 保存数据

根据用户需求选择合适的交付格式：

**CSV格式**（推荐用于Excel查看）：
使用Python脚本生成CSV文件，**必须添加UTF-8 BOM**以确保Excel兼容，避免中文乱码：

```python
import csv

with open('weibo_posts.csv', 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    writer.writerow(['排名', '作者', '发布时间', '正文', '评论数'])
    for post in posts:
        writer.writerow([post['index'], post['author'], post['time'], post['text'], post['comments']])
```

**JSON格式**（推荐用于程序处理）：
使用 `create_file` 保存为JSON文件，路径建议为工作区根目录，文件名格式: `weibo_{超话名称}_posts.json`。

**Excel格式**（推荐用于正式交付）：
使用Python的openpyxl库生成Excel文件，按字段分列，便于后续分析。

## 数据结构

输出的数据包含以下字段：

```json
{
  "index": "帖子序号（整数）",
  "author": "作者昵称（字符串）",
  "time": "发布时间（字符串，如'3分钟前'、'今天 14:30'）",
  "text": "帖子正文内容（字符串）",
  "comments": "评论数（整数）"
}
```

## 注意事项

1. **登录态必要性**: 未登录状态下仅能获取部分帖子文本，作者、时间及互动数据缺失；完整数据必须登录后配合浏览器自动化获取

2. **分页机制限制**: 
   - URL参数 `?page=N` 在非登录或非标准接口下可能失效或返回异常数据
   - 无限滚动(`window.scrollBy`)常无法触发新内容加载
   - 最终采用分次导航配合 `readability` 文本解析的方式获取数据

3. **评论数提取陷阱**: 评论数DOM结构易误读，需通过浏览器直接观察确认" 数字"或"评论"格式，避免依赖初始extract schema

4. **数据量限制**: 建议单次抓取不超过100条帖子，避免触发反爬机制；如需更多数据，可分多次执行并合并结果

5. **Cookie有效期**: Cookie可能过期，如遇到加载失败或数据不全，需用户提供最新Cookie

6. **反爬机制**: 微博有较强的反爬策略，避免短时间内频繁请求；建议在两次抓取之间间隔至少5分钟

7. **DOM结构变化**: 微博前端可能更新，导致选择器失效；如提取失败需重新观察页面结构并调整选择器

8. **编码兼容性**: CSV文件必须添加UTF-8 BOM（使用 `utf-8-sig` 编码）以确保Excel正确显示中文

## 常见问题

- **页面显示未登录状态**: 检查Cookie是否有效，或刷新页面重新加载；确保Cookie包含完整的登录态信息

- **只能获取少量帖子**: 微博超话默认可能只显示前几条，需尝试分页或滚动；如仍无法加载更多，可能是该超话本身帖子较少或触发反爬

- **评论数提取为0或错误值**: DOM结构可能变化，需使用 `use_browser(namespace="observe", action="observe")` 重新观察评论数的实际HTML结构

- **分页导航失败**: `?page=N` 参数可能不生效，尝试查找页面内的"下一页"按钮或使用 `readability` 解析文本

- **数据重复**: 多页抓取时可能出现重复帖子，需在合并时进行去重处理

- **中文乱码**: CSV文件在Excel中打开乱码，确保使用 `utf-8-sig` 编码（带BOM的UTF-8）

## 示例调用

**示例1: 基础抓取**

用户请求: "帮我抓取微博'洛克王国世界交易'超话的前30个帖子"

执行步骤:
1. 打开超话页面 → 注入Cookie → 刷新 → 观察页面结构
2. 提取第一页帖子数据（约45条）
3. 筛选前30条，保存为CSV和JSON文件
4. 交付文件给用户

**示例2: 深度抓取**

用户请求: "帮我抓取微博'洛克王国世界交易'超话的前80个帖子，包含评论数"

执行步骤:
1. 打开超话第1页 → 注入Cookie → 刷新 → 提取约45条帖子
2. 导航到第2页（尝试 `?page=2` 或点击分页链接）→ 提取约28条帖子
3. 合并两页数据，去重后得到73条有效帖子
4. 核实评论数DOM结构，修正可能的误读
5. 保存为CSV（带BOM）、JSON和Excel格式
6. 交付文件给用户

**示例3: 定期监控**

用户请求: "每天帮我抓取这个超话的最新50条帖子，记录趋势"

执行步骤:
1. 创建定时任务，每天固定时间执行
2. 打开超话页面 → 注入Cookie → 提取最新50条帖子
3. 保存为带日期戳的文件（如 `weibo_posts_2026-03-25.csv`）
4. 可选：对比历史数据，生成趋势分析报告

## 技术要点总结

1. **核心策略**: 分次导航 + readability文本解析，而非依赖JS滚动加载
2. **关键工具**: `use_browser` 的 `navigate`、`observe`、`inject`、`act` 动作组合使用
3. **数据验证**: 评论数等关键字段需直接观察DOM确认，避免schema误判
4. **交付规范**: CSV加BOM、JSON结构化、Excel分Sheet，根据用户需求选择
5. **反爬应对**: 控制抓取频率、使用有效Cookie、避免单次请求过多数据

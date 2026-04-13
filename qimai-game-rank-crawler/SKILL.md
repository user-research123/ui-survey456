---
name: qimai-game-rank-crawler
description:七麦数据游戏榜单爬取工具。当用户需要从七麦数据(Qimai.cn)获取iOS游戏榜单数据(免费榜/畅销榜)时使用。通过浏览器自动化配合有效Cookie,模拟瀑布流滚动加载完整榜单数据(最多200条),并结构化保存为JSON文件。适用于游戏市场分析、竞品追踪、榜单趋势研究等场景。
---

#七麦数据游戏榜单爬取 Skill

##触发场景

-用户需要获取七麦数据(Qimai.cn)的iOS游戏榜单数据
-需要获取免费榜或畅销榜的完整排名(前200名)
-需要分析游戏市场趋势、竞品排名、开发者分布
-需要定期抓取榜单数据进行对比分析

##前置条件

1. **有效Cookie**:用户需提供七麦数据网站的有效Cookie(包含登录态和权限信息)
2. **浏览器会话**:需要启用浏览器工具进行自动化操作
3. **目标榜单类型**:明确需要抓取免费榜(free)或畅销榜(grossing)
4. **筛选条件**:地区(默认中国cn)、设备(默认iPhone)、子分类(默认全部游戏6014)

##执行流程

###步骤1:打开目标榜单页面

根据用户指定的榜单类型,导航到对应URL:

- **免费榜**: `https://www.qimai.cn/rank/index/brand/free/country/cn/genre/6014/device/iphone`
- **畅销榜**: `https://www.qimai.cn/rank/index/brand/grossing/country/cn/genre/6014/device/iphone`

使用 `use_browser(namespace="bootstrap", action="navigate")`打开页面。

###步骤2:注入用户Cookie

使用 `use_browser(namespace="inject", action="evaluate")`注入Cookie:

```javascript
async () => {
  const cookies = '用户提供的完整Cookie字符串';
  cookies.split('; ').forEach(cookie => {
    document.cookie = cookie + '; path=/; domain=.qimai.cn';
  });
  return 'Cookies injected for .qimai.cn';
}
```

###步骤3:刷新页面使Cookie生效

使用 `use_browser(namespace="inject", action="evaluate")`执行 `window.location.reload()`,然后等待5秒让页面重新加载。

###步骤4:验证数据加载状态

使用 `use_browser(namespace="observe", action="observe")`观察页面,确认筛选条件正确(游戏榜/免费或畅销/全部游戏/中国/目标日期)。

###步骤5:滚动加载完整数据

七麦数据采用瀑布流懒加载机制,需持续滚动才能加载完整200条数据。使用 `use_browser(namespace="inject", action="evaluate")`执行滚动脚本:

```javascript
async () => {
  let maxScroll =0;
  const targetCount =200;
  let attempts =0;
  const maxAttempts =15;
  
  while (attempts< maxAttempts) {
    const currentCount = document.querySelectorAll('table tbody tr').length;
    if (currentCount >= targetCount) break;
    
    window.scrollTo(0, document.body.scrollHeight);
    await new Promise(resolve => setTimeout(resolve,2000));
    
    const newCount = document.querySelectorAll('table tbody tr').length;
    if (newCount === currentCount) {
      attempts++;
    } else {
      attempts =0;
    }
    maxScroll = document.body.scrollHeight;
  }
  
  const finalCount = document.querySelectorAll('table tbody tr').length;
  return `Loaded ${finalCount} items after scrolling`;
}
```

###步骤6:提取游戏数据

使用 `use_browser(namespace="inject", action="evaluate")`提取DOM中的游戏信息:

```javascript
async () => {
  const rows = document.querySelectorAll('table tbody tr');
  const games = [];
  
  for (let i =0; i< Math.min(rows.length,200); i++) {
    const cells = rows[i].querySelectorAll('td');
    if (cells.length >=2) {
      const rank = cells[0]?.textContent.trim();
      const fullText = cells[1]?.textContent || '';
      const lines = fullText.split('\n').map(s => s.trim()).filter(Boolean);
      const name = lines[0] || '';
      const developer = lines.length >1 ? lines[lines.length -1] : '';
      
      games.push({ rank, name, developer });
    }
  }
  
  return games;
}
```

###步骤7:保存数据为JSON

使用 `create_file`将提取的游戏数据保存为JSON文件,路径建议为工作区根目录,文件名格式: `qimai_{榜单类型}_rank.json`。

###步骤8:切换到另一个榜单(如需要)

如果用户需要同时获取免费榜和畅销榜,重复步骤1-7,只需修改URL中的 `brand`参数:
-免费榜: `brand/free`
-畅销榜: `brand/grossing`

##数据结构

输出的JSON文件包含数组,每个元素为:

```json
{
  "rank": "排名(字符串)",
  "name": "游戏名称",
  "developer": "开发者/发行商名称"
}
```

##注意事项

1. **Cookie有效性**: Cookie过期会导致无法加载数据,需用户提供最新Cookie
2. **日期问题**:页面默认显示当天日期,如显示"暂无榜单数据",可能是Cookie权限不足或日期选择器未正确加载
3. **滚动等待时间**:瀑布流加载需要2秒间隔,总耗时约30-40秒获取200条数据
4. **数据完整性**:如滚动后数据不足200条,可能是该榜单实际条目数不足或加载失败
5. **反爬机制**:七麦数据可能有频率限制,避免短时间内多次请求
6. **字段提取**: DOM结构可能随网站更新变化,如提取失败需重新分析单元格索引

##常见问题

- **页面显示"暂无榜单数据"**:检查Cookie是否有效,或刷新页面重新加载
- **数据提取为空**: DOM结构可能变化,需重新观察页面表格结构
- **滚动无法加载更多**:可能已达到榜单上限或触发反爬,检查网络请求状态
- **Cookie注入失败**:确保Cookie字符串格式正确,使用 `; `分隔而非 `;`

##示例调用

用户请求: "帮我抓取七麦数据今天中国区iPhone游戏的免费榜和畅销榜前200名"

执行步骤:
1.打开免费榜页面 →注入Cookie →刷新 →滚动加载200条 →提取数据 →保存为 `qimai_free_rank.json`
2.打开畅销榜页面 →注入Cookie →刷新 →滚动加载200条 →提取数据 →保存为 `qimai_grossing_rank.json`
3.交付两个JSON文件给用户

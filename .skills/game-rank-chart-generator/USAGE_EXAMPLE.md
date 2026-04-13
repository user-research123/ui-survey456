# 使用示例

## 场景1: 从CSV数据生成曲线图

**用户输入:**
```
我有云·王者荣耀世界的榜单数据CSV，帮我生成曲线图
```

**执行流程:**
1. 读取CSV文件（如`云·王者荣耀世界_排行数据_20260327_20260402.csv`）
2. 解析数据，过滤空排名值
3. 调用game-rank-chart-generator skill
4. 生成HTML文件并交付

**输出:** `云·王者荣耀世界_游戏榜单曲线图.html`

---

## 场景2: 更新现有报告中的曲线图

**用户输入:**
```
把最新的榜单数据更新到报告中
```

**执行流程:**
1. 读取新数据CSV/JSON
2. 调用skill生成新的曲线图HTML
3. 读取目标报告HTML（如`wangzhe_report/index_with_tabs.html`）
4. 定位总结部分下方的curve chart section
5. 替换旧图表代码
6. 提交git并推送到GitHub Pages

**输出:** 更新后的报告已推送到 https://fungjiewen-collab.github.io/wangzhe_report/index_with_tabs.html

---

## 场景3: 自定义榜单类型

**用户输入:**
```
生成畅销榜曲线图
```

**执行流程:**
1. 读取数据
2. 修改标题为"游戏(畅销)榜单曲线图"
3. 图例文字改为"游戏(畅销)"
4. 其他逻辑相同，生成HTML

**输出:** `云·王者荣耀世界_游戏畅销榜曲线图.html`

---

## 数据格式要求

### CSV格式示例
```csv
time,game_rank
2026-03-27 00:00,
2026-03-27 01:00,
...
2026-03-28 05:00,95
2026-03-28 08:00,93
2026-03-30 13:00,3
2026-04-02 10:32,4
```

### JSON格式示例
```json
[
  {"time": "2026-03-27 00点00分", "game": ""},
  {"time": "2026-03-28 05点00分", "game": "95"},
  {"time": "2026-03-30 13点00分", "game": "3"},
  {"time": "2026-04-02 10点32分", "game": "4"}
]
```

**注意:**
- 空字符串表示该时间点无排名数据，会被过滤
- 时间格式支持 `YYYY-MM-DD HH:MM` 或 `YYYY-MM-DD HH点MM分`
- 排名数值必须为整数

---

## 生成的图表特性

✅ Y轴排名正序（0在最上方，数值越大越靠下）  
✅ X轴显示月日格式（如03-28），避免堆叠  
✅ 图表高度350px紧凑设计  
✅ 悬停tooltip显示完整时间和排名  
✅ 底部标注"数据来源：七麦数据"  
✅ 完全离线可用（无外部CDN依赖）  
✅ 响应式resize自动重绘  
✅ 纯SVG实现，无需ECharts/D3.js等库  

---

## 嵌入到其他HTML报告

如果需要将生成的曲线图嵌入到现有HTML报告中，只需复制以下三部分:

1. **CSS样式**（从`<style>`标签中提取相关类）
2. **HTML结构**（container + h1 + p.subtitle + legend + #chart-container + p.data-source）
3. **JavaScript代码**（rawData数组 + createChart函数 + resize监听）

参考`wangzhe_report/index_with_tabs.html`中的实现方式。

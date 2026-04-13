---
name: game-rank-chart-generator
description: 游戏榜单曲线图生成器。基于七麦数据或其他来源的游戏榜单排名数据，生成符合规范的离线可用SVG曲线图HTML文件。适用于《王者荣耀世界》等游戏的免费榜/畅销榜排名趋势可视化，支持Y轴排名正序、X轴月日简化格式、悬停tooltip交互，完全离线可用无需外部依赖。
---

# Game Rank Chart Generator (游戏榜单曲线图生成器)

## Purpose
基于七麦数据或其他来源的游戏榜单排名数据，生成符合规范的离线可用SVG曲线图HTML文件。适用于《王者荣耀世界》等游戏的免费榜/畅销榜排名趋势可视化。

## When to Use
- 用户提供游戏榜单CSV/JSON数据（包含时间戳和排名数值）
- 需要生成Y轴排名正序（0在最上方）、X轴简化为月日格式的紧凑曲线图
- 要求图表完全离线可用、无需外部依赖
- 需要嵌入到HTML报告中的场景

## Input Requirements
**必需数据格式：**
```csv
time,game_rank
2026-03-27 00:00,
2026-03-28 05:00,95
2026-03-28 08:00,93
...
```

或JSON格式：
```json
[
  {"time": "2026-03-27 00点00分", "game": ""},
  {"time": "2026-03-28 05点00分", "game": "95"},
  ...
]
```

**数据规范：**
- 时间格式支持：`YYYY-MM-DD HH:MM` 或 `YYYY-MM-DD HH点MM分`
- 排名为空字符串表示无数据，需过滤
- 排名数值为整数，越小表示排名越靠前

## Output Specifications

### 视觉标准
1. **尺寸与布局**
   - 容器高度：350px（紧凑设计）
   - 宽度：自适应父容器（max-width: 1200px）
   - 内边距：上下左右各20px
   - 图表区域padding：top 40px, right 60px, bottom 80px, left 80px

2. **坐标轴规范**
   - Y轴：排名正序排列（0在最上方，数值越大越靠下）
   - Y轴刻度：每10名一个刻度，标签格式"X名"
   - X轴：仅显示月日格式（如"03-28"），下方附加时间（如"05:00"）
   - X轴标签间隔：根据数据点数量自动计算，约8个标签均匀分布

3. **曲线样式**
   - 线条颜色：#91CC75（绿色系）
   - 线宽：2.5px
   - 连接方式：round圆角连接
   - 数据点：半径4px的圆形，填充#91CC75，白色描边2px

4. **交互功能**
   - 悬停tooltip：黑色半透明背景，白色文字
   - 显示内容：完整时间 + "排名：第X名"
   - tooltip位置：跟随鼠标，偏移(10, -30)

5. **辅助元素**
   - 标题：居中，字号默认，颜色#333
   - 副标题：数据统计周期，居中，字号14px，颜色#666
   - 图例：居中显示，色块20x3px，标签"游戏(免费)"或"游戏(畅销)"
   - 数据来源：底部居中，字号12px，颜色#999，固定文本"数据来源：七麦数据"

### 技术实现
- **纯SVG实现**：不使用任何外部库（如ECharts、D3.js）
- **响应式**：监听window resize事件，自动重绘
- **网格线**：浅灰色#e0e0e0，线宽1px
- **字体**：系统默认字体栈 `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, ...`

## Execution Steps

### Step 1: 数据预处理
```python
# 读取CSV或JSON数据
# 过滤空排名值
# 转换时间格式：'2026-03-28 05点00分' → '2026-03-28 05:00'
# 提取月日：'2026-03-28' → '03-28'
# 确保排名为整数类型
```

### Step 2: 计算图表参数
```javascript
const width = container.clientWidth;
const height = 350; // 固定高度
const padding = { top: 40, right: 60, bottom: 80, left: 80 };
const chartWidth = width - padding.left - padding.right;
const chartHeight = height - padding.top - padding.bottom;

// Y轴范围
const maxRank = Math.max(...gameRanks);
const yMax = Math.ceil(maxRank / 10) * 10; // 向上取整到10的倍数
```

### Step 3: 生成SVG结构
按以下顺序构建SVG元素：
1. 网格线组（gridGroup）：水平线 + Y轴标签
2. X轴标签组（xAxisGroup）：月日+时间双行显示
3. 曲线路径（path）：使用M/L命令连接数据点
4. 数据点圆圈（circle）：每个有效数据点对应一个圆

### Step 4: 添加交互
为每个circle绑定mouseenter/mouseleave/mousemove事件，控制tooltip显示/隐藏/定位

### Step 5: 输出完整HTML
生成独立HTML文件，包含：
- `<style>`：所有CSS样式内联
- `<body>`：container + h1标题 + p副标题 + legend + #chart-container + p数据来源
- `<script>`：rawData数组 + createChart函数 + resize监听

## Template Code Structure

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{游戏名称} - {榜单类型}榜单曲线图</title>
    <style>
        /* 完整CSS样式，见下方Template CSS */
    </style>
</head>
<body>
    <div class="container">
        <h1>{游戏名称} - {榜单类型}榜单曲线图</h1>
        <p class="subtitle">数据统计周期：{起始日期} 至 {结束日期}</p>
        
        <div class="legend">
            <div class="legend-item">
                <div class="legend-color" style="background-color: #91CC75;"></div>
                <span>{榜单类型}</span>
            </div>
        </div>
        
        <div id="chart-container">
            <div class="tooltip" id="tooltip"></div>
        </div>
        
        <p class="data-source">数据来源：七麦数据</p>
    </div>

    <script>
        const rawData = [/* 原始数据数组 */];
        
        // 数据预处理
        const times = [];
        const gameRanks = [];
        rawData.forEach(item => {
            if (item.game && item.game !== "") {
                const timeStr = item.time.replace('点', ':').replace('分', '');
                times.push(timeStr);
                gameRanks.push(parseInt(item.game));
            }
        });

        function createChart() {
            // SVG绘制逻辑，见下方Template JS
        }

        createChart();
        window.addEventListener('resize', () => {
            const container = document.getElementById('chart-container');
            container.innerHTML = '<div class="tooltip" id="tooltip"></div>';
            createChart();
        });
    </script>
</body>
</html>
```

## Template CSS

```css
body {
    margin: 0;
    padding: 20px;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    background-color: #f5f5f5;
}
.container {
    max-width: 1200px;
    margin: 0 auto;
    background-color: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
h1 {
    text-align: center;
    color: #333;
    margin-bottom: 10px;
}
.subtitle {
    text-align: center;
    color: #666;
    margin-bottom: 20px;
    font-size: 14px;
}
#chart-container {
    width: 100%;
    height: 350px;
    position: relative;
}
svg {
    width: 100%;
    height: 100%;
}
.tooltip {
    position: absolute;
    background: rgba(0, 0, 0, 0.8);
    color: white;
    padding: 8px 12px;
    border-radius: 4px;
    font-size: 12px;
    pointer-events: none;
    display: none;
    z-index: 1000;
}
.legend {
    display: flex;
    justify-content: center;
    gap: 30px;
    margin-bottom: 15px;
}
.legend-item {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 14px;
}
.legend-color {
    width: 20px;
    height: 3px;
}
.data-source {
    text-align: center;
    color: #999;
    font-size: 12px;
    margin-top: 15px;
}
```

## Template JavaScript (核心绘制逻辑)

```javascript
function createChart() {
    const container = document.getElementById('chart-container');
    const width = container.clientWidth;
    const height = container.clientHeight;
    const padding = { top: 40, right: 60, bottom: 80, left: 80 };
    const chartWidth = width - padding.left - padding.right;
    const chartHeight = height - padding.top - padding.bottom;

    const minRank = 0;
    const maxRank = Math.max(...gameRanks);
    const yMax = Math.ceil(maxRank / 10) * 10;

    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('viewBox', `0 0 ${width} ${height}`);
    svg.style.width = '100%';
    svg.style.height = '100%';

    // 绘制网格线和Y轴标签
    const gridGroup = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    for (let i = 0; i <= yMax; i += 10) {
        const y = padding.top + (i / yMax) * chartHeight;
        
        const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
        line.setAttribute('x1', padding.left);
        line.setAttribute('y1', y);
        line.setAttribute('x2', width - padding.right);
        line.setAttribute('y2', y);
        line.setAttribute('stroke', '#e0e0e0');
        line.setAttribute('stroke-width', '1');
        gridGroup.appendChild(line);

        const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        text.setAttribute('x', padding.left - 10);
        text.setAttribute('y', y + 4);
        text.setAttribute('text-anchor', 'end');
        text.setAttribute('font-size', '12');
        text.setAttribute('fill', '#666');
        text.textContent = i + '名';
        gridGroup.appendChild(text);
    }
    svg.appendChild(gridGroup);

    // 绘制X轴标签（月日+时间）
    const xAxisGroup = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    const labelInterval = Math.ceil(times.length / 8);
    for (let i = 0; i < times.length; i += labelInterval) {
        const x = padding.left + (i / (times.length - 1)) * chartWidth;
        const timeParts = times[i].split(' ');
        const datePart = timeParts[0];
        const timePart = timeParts[1] || '';
        
        const dateComponents = datePart.split('-');
        const monthDay = dateComponents[1] + '-' + dateComponents[2];
        
        const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        text.setAttribute('x', x);
        text.setAttribute('y', height - padding.bottom + 20);
        text.setAttribute('text-anchor', 'middle');
        text.setAttribute('font-size', '11');
        text.setAttribute('fill', '#666');
        text.textContent = monthDay + '\n' + timePart;
        xAxisGroup.appendChild(text);
    }
    svg.appendChild(xAxisGroup);

    // 绘制曲线路径
    const pathGroup = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    let pathData = '';
    
    gameRanks.forEach((rank, index) => {
        const x = padding.left + (index / (gameRanks.length - 1)) * chartWidth;
        const y = padding.top + (rank / yMax) * chartHeight;
        
        if (index === 0) {
            pathData += `M ${x} ${y}`;
        } else {
            pathData += ` L ${x} ${y}`;
        }
    });

    const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    path.setAttribute('d', pathData);
    path.setAttribute('fill', 'none');
    path.setAttribute('stroke', '#91CC75');
    path.setAttribute('stroke-width', '2.5');
    path.setAttribute('stroke-linejoin', 'round');
    path.setAttribute('stroke-linecap', 'round');
    pathGroup.appendChild(path);

    // 绘制数据点并绑定交互
    gameRanks.forEach((rank, index) => {
        const x = padding.left + (index / (gameRanks.length - 1)) * chartWidth;
        const y = padding.top + (rank / yMax) * chartHeight;
        
        const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        circle.setAttribute('cx', x);
        circle.setAttribute('cy', y);
        circle.setAttribute('r', '4');
        circle.setAttribute('fill', '#91CC75');
        circle.setAttribute('stroke', 'white');
        circle.setAttribute('stroke-width', '2');
        circle.style.cursor = 'pointer';
        
        circle.addEventListener('mouseenter', (e) => {
            const tooltip = document.getElementById('tooltip');
            tooltip.innerHTML = `<strong>${times[index]}</strong><br/>排名：第${rank}名`;
            tooltip.style.display = 'block';
            tooltip.style.left = (e.pageX + 10) + 'px';
            tooltip.style.top = (e.pageY - 30) + 'px';
        });
        
        circle.addEventListener('mouseleave', () => {
            const tooltip = document.getElementById('tooltip');
            tooltip.style.display = 'none';
        });
        
        circle.addEventListener('mousemove', (e) => {
            const tooltip = document.getElementById('tooltip');
            tooltip.style.left = (e.pageX + 10) + 'px';
            tooltip.style.top = (e.pageY - 30) + 'px';
        });
        
        pathGroup.appendChild(circle);
    });

    svg.appendChild(pathGroup);
    container.appendChild(svg);
}
```

## Usage Examples

### Example 1: 从CSV生成曲线图
用户：我有云·王者荣耀世界的榜单数据CSV，帮我生成曲线图
你：读取CSV → 解析数据 → 调用本skill生成HTML文件 → deliver_artifacts交付

### Example 2: 更新现有报告
用户：把最新的榜单数据更新到报告中
你：读取新数据 → 生成新的曲线图HTML → 读取目标报告HTML → 替换curve chart section → 提交git推送

### Example 3: 自定义榜单类型
用户：生成畅销榜曲线图
你：修改标题为"游戏(畅销)榜单曲线图"，图例文字改为"游戏(畅销)"，其他逻辑相同

## Quality Checklist
- [ ] Y轴排名正序（0在最上方）
- [ ] X轴显示月日格式（如03-28）
- [ ] 图表高度350px
- [ ] 悬停tooltip正常工作
- [ ] 底部标注"数据来源：七麦数据"
- [ ] 完全离线可用（无外部CDN依赖）
- [ ] 响应式resize正常
- [ ] 空数据点已过滤
- [ ] 颜色使用#91CC75

## Notes
- 本skill生成的HTML可直接嵌入到其他HTML报告中（如wangzhe_report/index_with_tabs.html）
- 如需嵌入，只需复制`<style>`中的相关CSS、HTML结构和`<script>`中的JS代码
- 数据预处理时务必过滤空字符串排名，避免NaN错误
- Y轴最大值向上取整到10的倍数，保证刻度整齐
- X轴标签间隔动态计算，避免重叠

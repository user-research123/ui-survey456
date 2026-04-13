# 盼之平台商品抓取 Skill 使用示例

## 示例1：基础数据抓取与分析

**用户请求**：
```
帮我抓取盼之平台今天的《王者荣耀世界》商品数据，分析价格分布和平台占比
```

**执行流程**：

1. **激活 Skill**
   ```python
   use_skill(skill_name="pzds-goods-crawler", purpose="用户需要抓取盼之平台的王者荣耀世界商品数据进行分析")
   ```

2. **打开页面**
   ```python
   use_browser(namespace="bootstrap", action="openTab", 
               url="https://www.pzds.com/goodsList/1547/6/headerSearch?queryFrom=search&searchType=GAME_NAME")
   ```

3. **提取商品类型选项**
   ```python
   use_browser(namespace="inject", action="evaluate", 
               fn="(JS代码提取商品类型)")
   # 返回: ["成品号", "昵称 hot", "代肝 hot"]
   ```

4. **滚动加载商品**
   ```python
   for i in range(8):
       use_browser(namespace="inject", action="evaluate", 
                   fn="window.scrollTo(0, document.body.scrollHeight)")
       use_browser(namespace="wait", action="waitFor", timeMs=1500)
   ```

5. **提取商品信息**
   ```python
   use_browser(namespace="inject", action="evaluate", 
               fn="(JS代码提取100个商品信息)")
   # 保存到 goods.json
   ```

6. **数据分析**
   ```python
   python analyze_pzds_goods.py --goods-json goods.json --output report.txt
   ```

7. **输出结果**
   ```
   数据分析数量: 99 个商品
   分析时间: 04-03
   
   一、商品品类有：成品号、昵称 (hot)、代肝 (hot)
   
   二、账号的详细信息
   
   1）价格分布分析
   价格范围: ¥60 - ¥999,999
   中位数价格: ¥888
   高价商品(≥¥10,000): 11 个 (11.1%)
   ...
   ```

---

## 示例2：更新 GitHub Pages 报告

**用户请求**：
```
将盼之平台的最新分析数据同步到日报中
```

**执行流程**：

1. **执行示例1的数据抓取与分析**

2. **读取目标 HTML 文件**
   ```python
   read_file(absolute_path="/workspace/wangzhe_report/index_with_tabs.html", 
             start_line=475, end_line=540)
   ```

3. **定位并替换内容**
   - 找到 `<!-- 4月3日内容 -->` 区块
   - 定位到 `<div class="competitor-name">竞品二：盼之</div>`
   - 替换 `<p>暂无新动态</p>` 为新的分析报告

4. **保持 HTML 结构完整**
   ```python
   # 确保 div 标签配对正确
   modify_file(absolute_path="/workspace/wangzhe_report/index_with_tabs.html",
               old_string="<p>暂无新动态</p>",
               new_string="<p><strong>数据分析数量:</strong> 99 个商品</p>...")
   ```

5. **提交并推送**
   ```bash
   cd /workspace/wangzhe_report
   git add index_with_tabs.html
   git commit -m "更新4月3日盼之平台商品分析报告"
   git push
   ```

---

## 示例3：多竞品对比分析

**用户请求**：
```
对比盼之、螃蟹、闲鱼三个平台的《王者荣耀世界》ID交易特征
```

**执行流程**：

1. **分别抓取三个平台数据**
   - 盼之：使用 `pzds-goods-crawler` skill
   - 螃蟹：使用现有爬虫脚本
   - 闲鱼：使用浏览器自动化

2. **生成对比表格**
   ```markdown
   | 维度 | 盼之 | 螃蟹 | 闲鱼 |
   |------|------|------|------|
   | 中位数价格 | ¥888 | ¥888 | ¥500 |
   | QQ平台占比 | 88.9% | 83.0% | N/A |
   | 双字ID占比 | 38.4% | 48.2% | 45.0% |
   | 高价商品占比 | 11.1% | 9.8% | 5.0% |
   ```

3. **生成总结**
   ```
   竞品对比总结：
   - 盼之与螃蟹价格水平接近，中位数均为¥888
   - 盼之QQ平台占比更高（88.9% vs 83.0%）
   - 螃蟹双字ID更受欢迎（48.2% vs 38.4%）
   - 闲鱼整体价格偏低，但极品ID溢价明显
   ```

---

## 示例4：定时任务配置

**用户请求**：
```
设置每天下午3点自动抓取盼之平台数据并更新报告
```

**执行流程**：

1. **创建定时任务**
   ```python
   use_cron(action="add", 
            name="盼之平台每日数据抓取",
            schedule={"kind": "cron", "expr": "0 15 * * *"},
            prompt="使用 pzds-goods-crawler skill 抓取盼之平台《王者荣耀世界》商品数据，分析后更新到 wangzhe_report/index_with_tabs.html 的今日竞品动态板块，并推送到GitHub")
   ```

2. **验证任务**
   ```python
   use_cron(action="list")
   # 确认任务已创建，下次执行时间为明天15:00
   ```

3. **手动测试**
   ```python
   use_cron(action="run", job_id="<task_id>", wait=True)
   # 立即执行一次，验证流程是否正常
   ```

---

## 常见问题与解决方案

### Q1: 遇到阿里云滑块验证码怎么办？

**A**: Skill 已内置浏览器自动化方案，通常能自动通过验证码。若失败：
- 等待 30 秒让验证码自动刷新
- 或提示用户手动在浏览器中通过验证
- Fallback：复用近期已成功获取的基准数据集

### Q2: 滚动加载超时如何处理？

**A**: 
- 减少滚动次数（从 10 次降到 6-8 次）
- 增加每次滚动后的等待时间（从 1500ms 增加到 2000-3000ms）
- 分步执行，避免单次 JS 注入过于复杂

### Q3: 数据不足 100 个怎么办？

**A**: 
- 如实报告实际收集数量
- 检查是否滚动次数不够，尝试增加滚动
- 若确实只有这么多商品，说明市场活跃度低，这也是有价值的信息

### Q4: HTML 更新后格式错乱？

**A**: 
- 检查 div 标签是否正确配对
- 使用 Python 脚本进行精确替换，避免手动编辑
- 先备份原文件，更新后验证 HTML 结构

### Q5: 如何自定义分析维度？

**A**: 
- 修改 `analyze_pzds_goods.py` 脚本中的分析逻辑
- 添加新的统计维度（如浏览量分布、想要数分布等）
- 调整输出格式以符合需求

---

## 最佳实践

1. **数据缓存**：将每次抓取的商品数据保存为 JSON 文件，便于后续分析和回溯
2. **错误重试**：若某次抓取失败，自动重试 2-3 次
3. **增量更新**：若只需更新部分数据，可只抓取新增商品
4. **日志记录**：记录每次抓取的时间、商品数量、异常信息等
5. **定期清理**：删除超过 30 天的临时数据文件

---

## 进阶用法

### 结合钉钉通知

```python
# 抓取完成后发送钉钉通知
use_channel(content=f"""
【盼之平台日报】
- 抓取时间: {datetime.now()}
- 商品数量: {total_count} 个
- 中位数价格: ¥{median_price}
- 查看详情: https://fungjiewen-collab.github.io/wangzhe_report/index_with_tabs.html
""")
```

### 生成可视化图表

```python
# 使用 matplotlib 生成价格分布柱状图
import matplotlib.pyplot as plt

plt.bar(price_ranges.keys(), price_ranges.values())
plt.title('盼之平台商品价格区间分布')
plt.savefig('price_distribution.png')
```

### 多游戏支持

```python
# 修改 URL 中的 game_id 即可切换游戏
game_ids = {
    "王者荣耀世界": 1547,
    "其他游戏": xxx
}

url = f"https://www.pzds.com/goodsList/{game_id}/6/headerSearch..."
```

---

## 反馈与支持

如有问题或建议，请联系技能维护者或通过内部渠道反馈。

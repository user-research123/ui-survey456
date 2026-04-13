# Auto Research搜索策略和知识缺口追踪

## 搜索策略概述

Auto Research 采用多层次、迭代式的搜索策略，确保信息的全面性和准确性。核心原则：

1. **并行化**：多个 Task 子代理同时搜索不同子问题
2. **迭代式**：基于知识缺口进行多轮补充搜索
3. **智能降级**：WebFetch 失败时自动切换浏览器自动化
4. **质量优先**：注重来源权威性和信息相关性

## 搜索流程

```
┌─────────────────┐
│  接收子问题      │
└────────┬────────┘
         ↓
┌─────────────────┐
│ 第一轮:广泛搜索  │ ← 收集5-10个相关来源
└────────┬────────┘
         ↓
┌─────────────────┐
│ 抓取页面内容     │ ← WebFetch → 浏览器自动化
└────────┬────────┘
         ↓
┌─────────────────┐
│ 提取关键信息     │ ← LLM 信息抽取
└────────┬────────┘
         ↓
┌─────────────────┐
│ 识别知识缺口     │ ← 检查维度覆盖度
└────────┬────────┘
         ↓
    有缺口？
   ╱        ╲
 是          否
  ↓           ↓
┌─────┐   ┌──────────┐
│第二轮│   │ 完成搜索  │
│定向搜│   └──────────┘
│索   │
└──┬──┘
   ↓
┌──────────┐
│完成搜索  │
└──────────┘
```

## 第一轮搜索：广泛收集

### 目标

- 收集 5-10 个相关来源
- 覆盖不同类型的资源
-建立对主题的初步理解

### 搜索关键词生成

#### 基础关键词

从子问题中提取核心术语：

```python
def extract_keywords(question: str) -> List[str]:
    """从问题中提取关键词"""
    
    # 示例： "KV Cache 在推理集群中的通信模式是什么？"
    # 提取：["KV Cache", "推理集群", "通信模式"]
    
    keywords = []
    
    # 1. 专有名词
    keywords.extend(extract_proper_nouns(question))
    
    # 2. 技术术语
    keywords.extend(extract_technical_terms(question))
    
    # 3. 核心概念
    keywords.extend(extract_core_concepts(question))
    
    return keywords
```

#### 关键词扩展

基于基础关键词生成变体：

**同义词扩展**：
- "KV Cache" → "Key-Value Cache", "键值缓存"
- "通信模式" → "communication pattern", "数据传输方式"

**上下位词扩展**：
- 上位词："缓存技术", "分布式系统"
- 下位词："PagedAttention", "vLLM KV Cache"

**相关词扩展**：
- "推理优化", "显存管理", "注意力机制"

#### 搜索查询组合

生成多种搜索查询：

```python
queries = [
    # 精确匹配
    '"KV Cache" "通信模式"',
    
    # 宽泛搜索
    'KV Cache 推理集群',
    
    # 问题导向
    'KV Cache 如何通信',
    
    # 对比型
    'KV Cache 通信模式 对比',
    
    # 最佳实践
    'KV Cache 通信 最佳实践',
    
    # 英文搜索
    'KV Cache communication pattern inference cluster'
]
```

### 搜索引擎选择

#### 优先级1: 通用搜索引擎

- **Bing**: 中文内容丰富，API 稳定
- **Google**: 全球范围最广，学术资源丰富
- **百度**: 中文本土内容，但质量参差不齐

#### 优先级2: 专业搜索引擎

- **GitHub Search**: 代码实现、开源项目
- **arXiv**: 学术论文
- **Stack Overflow**: 技术问题解答
- **知乎**: 中文技术讨论

####优先级3: 垂直领域搜索

根据主题选择：
- 技术类：Dev.to, Medium, InfoQ
- 学术类：PubMed, IEEE Xplore, ACM Digital Library
- 商业类：Crunchbase, Gartner, Forrester

### 结果筛选

#### 相关性评分

对每个搜索结果计算相关性评分（0-1）：

```python
def calculate_relevance(result: dict, question: str) -> float:
    """计算搜索结果的相关性评分"""
    
    score = 0.0
    
    # 1. 标题匹配度（权重 0.4）
    title_score = jaccard_similarity(result['title'], question)
    score += 0.4 * title_score
    
    # 2. 摘要匹配度（权重 0.3）
    snippet_score = keyword_overlap(result['snippet'], question)
    score += 0.3 * snippet_score
    
    # 3. 来源权威性（权重 0.2）
    authority_score = get_source_authority(result['url'])
    score += 0.2 * authority_score
    
    # 4. 时效性（权重 0.1）
    recency_score = calculate_recency(result['date'])
    score += 0.1 * recency_score
    
    return min(score, 1.0)
```

#### 筛选标准

- **保留**：相关性 ≥ 0.6
- **优先**：相关性 ≥ 0.8 + 权威来源
- **剔除**：相关性 < 0.4 或明显不相关

#### 去重策略

- URL 去重：相同 URL 只保留一次
- 内容去重：相似度 > 90% 的内容只保留质量最高的
- 来源去重：同一域名最多保留 3 个结果

## 页面内容抓取

### 策略1: WebFetch（优先）

使用 URL 前缀转换服务快速获取结构化 Markdown。

#### 服务列表

按优先级尝试：

1. **markdown.new**
   ```
   https://markdown.new/<target_url>
   ```
   - 优点：速度快，格式好
   - 缺点：部分网站不支持

2. **defuddle.md**
   ```
   https://defuddle.md/<target_url>
   ```
   - 优点：智能提取正文
   - 缺点：偶尔提取不完整

3. **r.jina.ai**
   ```
   https://r.jina.ai/<target_url>
   ```
   - 优点：支持广泛，稳定性好
   - 缺点：格式相对简单

#### 使用示例

```python
def fetch_with_webfetch(url: str) -> Optional[dict]:
    """使用 WebFetch 服务抓取页面"""
    
    services = [
        "https://markdown.new/{}",
        "https://defuddle.md/{}",
        "https://r.jina.ai/{}"
    ]
    
    for service in services:
        try:
            target_url = service.format(url)
            response = requests.get(target_url, timeout=10)
            
            if response.status_code == 200:
                content = response.text
                
                # 检查是否为有效内容
                if is_valid_content(content):
                    return {
                        "content": content,
                        "method": "webfetch",
                        "service": service.split('/')[2],
                        "success": True
                    }
        
        except Exception as e:
            print(f"[WARN] {service} 失败: {e}")
            continue
    
    return None
```

#### 成功指标

- HTTP 状态码 200
- 返回内容长度 > 500字符
- 包含合理的文本内容（非错误页面）

### 策略2: 浏览器自动化（降级）

当 WebFetch 全部失败时，自动切换为浏览器自动化。

#### 适用场景

- 动态渲染页面（SPA、React、Vue）
- 需要登录的页面
- 反爬严格的网站
- 瀑布流加载的内容

#### 实现步骤

```python
def fetch_with_browser(url: str) -> Optional[dict]:
    """使用浏览器自动化抓取页面"""
    
    # Step 1: 打开页面
    use_browser(namespace="bootstrap", action="openTab", url=url)
    
    # Step 2: 等待页面加载
    use_browser(namespace="wait", action="waitFor", timeMs=3000)
    
    # Step 3: 处理滚动加载（如需要）
    if is_infinite_scroll(url):
        scroll_and_wait()
    
    # Step 4: 提取正文内容
    result = use_browser(namespace="observe", action="readability")
    
    # Step 5: 关闭标签页
    use_browser(namespace="bootstrap", action="closeTab")
    
    if result and result.get('content'):
        return {
            "content": result['content'],
            "title": result.get('title', ''),
            "method": "browser_automation",
            "success": True
        }
    
    return None
```

#### 滚动加载处理

对于瀑布流页面，模拟滚动触发新内容加载：

```python
def scroll_and_wait(max_scrolls: int = 10):
    """模拟滚动加载"""
    
    for i in range(max_scrolls):
        # 滚动到页面底部
        use_browser(
            namespace="inject",
            action="evaluate",
            fn="() => window.scrollBy(0, window.innerHeight)"
        )
        
        # 等待新内容加载
        use_browser(namespace="wait", action="waitFor", timeMs=2000)
        
        # 检查是否有新内容
        new_content = check_for_new_content()
        
        if not new_content:
            # 没有新内容，停止滚动
            break
```

#### Readability 提取

使用浏览器内置的 readability 功能提取正文：

```python
result = use_browser(namespace="observe", action="readability")

# 返回结构
{
    "title": "页面标题",
    "content": "正文内容（HTML或纯文本）",
    "excerpt": "摘要",
    "byline": "作者",
    "dir": "文本方向"
}
```

### 策略选择逻辑

```python
def fetch_page_content(url: str) -> Optional[dict]:
    """智能选择抓取策略"""
    
    # 策略1: 尝试 WebFetch
    result = fetch_with_webfetch(url)
    
    if result and result['success']:
        return result
    
    # 策略2: 降级为浏览器自动化
    print(f"[INFO] WebFetch 失败，降级为浏览器自动化: {url}")
    result = fetch_with_browser(url)
    
    if result and result['success']:
        return result
    
    # 策略3: 全部失败
    print(f"[ERROR] 页面抓取失败: {url}")
    return None
```

## 信息提取

### 提取目标

从页面内容中提取：

1. **关键要点**（key_points）：3-5 个核心观点
2. **支撑证据**（evidence）：具体的数据、案例、引用
3. **元数据**（metadata）：作者、发布时间、来源类型

### 提取方法

#### 使用 LLM提取

```python
def extract_key_information(content: str, question: str) -> dict:
    """使用 LLM 从内容中提取关键信息"""
    
    prompt = f"""
请从以下内容中提取与问题相关的信息。

问题：{question}

内容：
{content[:5000]}  # 限制长度避免超出上下文

请提取：
1. 关键要点（3-5个）
2. 支撑证据（具体数据、案例、引用）
3.与问题的相关性评分（0-1）

以 JSON 格式返回：
{{
    "key_points": ["要点1", "要点2", ...],
    "evidence": [
        {{"text": "证据文本", "type": "data/case/quote"}},
        ...
    ],
    "relevance_score":0.85,
    "source_type": "official_doc/paper/blog/report"
}}
"""
    
    # 调用 LLM
    response = call_llm(prompt)
    
    return parse_json(response)
```

#### 提取质量检查

```python
def validate_extraction(extracted: dict) -> bool:
    """验证提取质量"""
    
    # 检查关键要点数量
    if len(extracted.get('key_points', [])) < 2:
        return False
    
    # 检查相关性评分
    if extracted.get('relevance_score', 0) < 0.5:
        return False
    
    # 检查是否有支撑证据
    if len(extracted.get('evidence', [])) == 0:
        return False
    
    return True
```

## 知识缺口识别

### 检查维度

#### 1. 内容维度覆盖度

检查是否覆盖了必要的信息维度：

```python
REQUIRED_DIMENSIONS = {
    "definition": ["定义", "原理", "概念", "是什么"],
    "application": ["应用", "场景", "案例", "实例"],
    "advantages": ["优点", "优势", "好处", "价值"],
    "disadvantages": ["缺点", "劣势", "局限", "问题"],
    "comparison": ["对比", "比较", "vs", "优劣"],
    "best_practice": ["最佳实践", "建议", "推荐", "方案"],
    "data": ["数据", "统计", "百分比", "数字"]
}

def check_dimension_coverage(collected_info: List[dict]) -> Dict[str, bool]:
    """检查各维度的覆盖情况"""
    
    coverage = {dim: False for dim in REQUIRED_DIMENSIONS.keys()}
    
    for info in collected_info:
        text = ' '.join(info.get('key_points', []))
        text += ' '.join([ev['text'] for ev in info.get('evidence', [])])
        
        for dim, keywords in REQUIRED_DIMENSIONS.items():
            if any(kw in text for kw in keywords):
                coverage[dim] = True
    
    return coverage
```

#### 2.来源多样性

检查来源的类型和数量：

```python
def check_source_diversity(collected_info: List[dict]) -> dict:
    """检查来源多样性"""
    
    source_types = {}
    unique_domains = set()
    
    for info in collected_info:
        url = info.get('source_url', '')
        domain = extract_domain(url)
        unique_domains.add(domain)
        
        source_type = info.get('source_type', 'unknown')
        source_types[source_type] = source_types.get(source_type, 0) + 1
    
    return {
        "unique_sources": len(unique_domains),
        "source_type_distribution": source_types,
        "is_diverse": len(unique_domains) >= 3
    }
```

#### 3. 数据支撑度

检查是否有量化数据支撑：

```python
def check_data_support(collected_info: List[dict]) -> dict:
    """检查数据支撑情况"""
    
    data_points = []
    
    for info in collected_info:
        for evidence in info.get('evidence', []):
            if evidence.get('type') == 'data':
                data_points.append(evidence['text'])
    
    return {
        "data_count": len(data_points),
        "has_sufficient_data": len(data_points) >= 3,
        "data_points": data_points
    }
```

###缺口识别算法

```python
def identify_knowledge_gaps(
    question: str,
    collected_info: List[dict]
) -> List[str]:
    """识别知识缺口"""
    
    gaps = []
    
    # 检查1: 维度覆盖度
    coverage = check_dimension_coverage(collected_info)
    missing_dims = [dim for dim, covered in coverage.items() if not covered]
    
    for dim in missing_dims:
        gaps.append(f"缺少'{dim}'维度的信息")
    
    # 检查2: 来源多样性
    diversity = check_source_diversity(collected_info)
    if not diversity['is_diverse']:
        gaps.append(
            f"来源不足（当前{diversity['unique_sources']}个，"
            f"建议至少3个不同来源）"
        )
    
    # 检查3: 数据支撑
    data_support = check_data_support(collected_info)
    if not data_support['has_sufficient_data']:
        gaps.append(
            f"缺少量化数据支撑（当前{data_support['data_count']}个，"
            f"建议至少3个数据点）"
        )
    
    # 检查4: 信息饱和度
    if len(collected_info) < 3:
        gaps.append(
            f"信息来源太少（当前{len(collected_info)}个，"
            f"建议至少5个）"
        )
    
    return gaps
```

### 缺口优先级排序

对识别出的缺口进行优先级排序：

```python
def prioritize_gaps(gaps: List[str]) -> List[dict]:
    """对知识缺口进行优先级排序"""
    
    priority_map = {
        "definition": 1,      # 定义缺失 - 最高优先级
        "data": 2,            # 数据缺失 - 高优先级
        "application": 3,     # 应用缺失 -中优先级
        "comparison": 4,      # 对比缺失 - 中优先级
        "best_practice": 5,   # 最佳实践缺失 - 低优先级
        "source_diversity": 6 # 来源多样性 - 低优先级
    }
    
    prioritized = []
    
    for gap in gaps:
        # 确定缺口类型
        gap_type = determine_gap_type(gap)
        priority = priority_map.get(gap_type,99)
        
        prioritized.append({
            "gap": gap,
            "type": gap_type,
            "priority": priority
        })
    
    # 按优先级排序
    prioritized.sort(key=lambda x: x['priority'])
    
    return prioritized
```

## 第二轮搜索：定向补充

### 搜索策略调整

基于知识缺口调整搜索策略：

#### 缺口类型 → 搜索策略映射

```python
GAP_STRATEGY_MAP = {
    "definition": {
        "keywords": ["定义", "原理", "是什么", "concept", "definition"],
        "sources": ["官方文档", "维基百科", "教科书"],
        "query_template": "{topic} 定义原理"
    },
    "data": {
        "keywords": ["数据", "统计", "报告", "study", "statistics"],
        "sources": ["行业报告", "研究论文", "数据分析"],
        "query_template": "{topic} 数据 统计 报告"
    },
    "application": {
        "keywords": ["案例", "应用", "实例", "case study", "example"],
        "sources": ["技术博客", "案例分析", "实践分享"],
        "query_template": "{topic} 应用案例实战"
    },
    "comparison": {
        "keywords": ["对比", "比较", "vs", "comparison", "vs"],
        "sources": ["对比文章", "评测", "选型指南"],
        "query_template": "{topic} vs 对比优劣"
    },
    "best_practice": {
        "keywords": ["最佳实践", "建议", "推荐", "best practice", "guide"],
        "sources": ["官方指南", "最佳实践", "教程"],
        "query_template": "{topic} 最佳实践 建议"
    }
}
```

### 生成针对性查询

```python
def generate_targeted_queries(
    topic: str,
    gaps: List[dict]
) -> List[str]:
    """基于知识缺口生成针对性搜索查询"""
    
    queries = []
    
    for gap in gaps:
        gap_type = gap['type']
        strategy = GAP_STRATEGY_MAP.get(gap_type)
        
        if strategy:
            query = strategy['query_template'].format(topic=topic)
            queries.append(query)
            
            # 添加英文查询
            if strategy.get('keywords'):
                english_query = f"{topic} {' '.join(strategy['keywords'][:2])}"
                queries.append(english_query)
    
    return queries
```

### 迭代终止条件

避免无限循环，设置终止条件：

```python
def should_continue_search(
    iteration: int,
    gaps: List[str],
    collected_info: List[dict]
) -> bool:
    """判断是否继续搜索"""
    
    # 条件1: 达到最大迭代次数
    if iteration >= 2:
        return False
    
    # 条件2: 没有剩余缺口
    if len(gaps) == 0:
        return False
    
    # 条件3: 信息已足够饱和
    if len(collected_info) >= 10:
        return False
    
    # 条件4: 剩余缺口都是低优先级
    high_priority_gaps = [g for g in gaps if get_gap_priority(g)<= 3]
    if len(high_priority_gaps) == 0:
        return False
    
    return True
```

## 搜索质量控制

### 来源权威性评估

```python
AUTHORITY_SCORES = {
    # 官方文档
    "docs.python.org": 1.0,
    "developer.mozilla.org": 1.0,
    "kubernetes.io/docs": 1.0,
    
    # 学术论文
    "arxiv.org": 0.95,
    "ieee.org": 0.95,
    "acm.org": 0.95,
    
    # 知名媒体
    "infoq.com": 0.85,
    "medium.com": 0.75,
    "zhihu.com": 0.70,
    
    # 技术博客
    "dev.to": 0.80,
    "blog.cloudflare.com": 0.90,
    
    # 默认
    "default": 0.60
}

def get_source_authority(url: str) -> float:
    """获取来源权威性评分"""
    
    domain = extract_domain(url)
    
    for known_domain, score in AUTHORITY_SCORES.items():
        if known_domain in domain:
            return score
    
    return AUTHORITY_SCORES["default"]
```

### 时效性评估

```python
def calculate_recency(date_str: str) -> float:
    """计算内容的时效性评分"""
    
    if not date_str:
        return 0.5  # 未知时间，中等评分
    
    try:
        pub_date = parse_date(date_str)
        days_old = (datetime.now() - pub_date).days
        
        if days_old <= 30:
            return 1.0  # 最近1个月
        elif days_old <= 90:
            return 0.9  # 最近3个月
        elif days_old <= 180:
            return 0.8  # 最近6个月
        elif days_old <= 365:
            return 0.7  # 最近1年
        elif days_old <= 730:
            return 0.5  # 最近2年
        else:
            return 0.3  # 超过2年
    
    except:
        return 0.5  # 解析失败，中等评分
```

### 交叉验证

对关键信息进行交叉验证：

```python
def cross_validate_facts(collected_info: List[dict]) -> dict:
    """交叉验证书实"""
    
    facts = {}
    
    # 收集所有事实陈述
    for info in collected_info:
        for point in info.get('key_points', []):
            # 简化事实（取前20个字符作为key）
            fact_key = point[:20]
            
            if fact_key not in facts:
                facts[fact_key] = {
                    "statement": point,
                    "sources": [],
                    "consistency": True
                }
            
            facts[fact_key]["sources"].append(info['source_url'])
    
    # 检查一致性
    validated_facts = []
    contradictory_facts = []
    
    for fact_key, fact_data in facts.items():
        if len(fact_data["sources"]) >= 2:
            #多个来源一致，高置信度
            validated_facts.append({
                "fact": fact_data["statement"],
                "confidence": "high",
                "source_count": len(fact_data["sources"])
            })
        elif len(fact_data["sources"]) == 1:
            # 单一来源，中置信度
            validated_facts.append({
                "fact": fact_data["statement"],
                "confidence": "medium",
                "source_count": 1
            })
    
    return {
        "validated_facts": validated_facts,
        "contradictory_facts": contradictory_facts,
        "total_facts": len(facts)
    }
```

## 搜索日志和调试

### 日志记录

记录每次搜索的详细信息：

```python
def log_search_activity(activity: dict):
    """记录搜索活动"""
    
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "question": activity.get('question'),
        "queries": activity.get('queries'),
        "results_count": activity.get('results_count'),
        "sources": activity.get('sources'),
        "knowledge_gaps": activity.get('knowledge_gaps'),
        "iteration": activity.get('iteration'),
        "duration_seconds": activity.get('duration')
    }
    
    # 保存到日志文件
    save_to_log(log_entry)
```

### 性能监控

监控搜索性能指标：

```python
SEARCH_METRICS = {
    "total_searches": 0,
    "successful_fetches": 0,
    "failed_fetches": 0,
    "avg_relevance_score": 0.0,
    "avg_duration_seconds": 0.0,
    "webfetch_success_rate": 0.0,
    "browser_fallback_rate": 0.0
}

def update_metrics(metric_name: str, value: float):
    """更新搜索指标"""
    
    if metric_name in SEARCH_METRICS:
        # 更新累计值和计数
        old_value = SEARCH_METRICS[metric_name]
        SEARCH_METRICS[metric_name] = (old_value + value) / 2
```

### 调试工具

提供调试工具帮助排查问题：

```python
def debug_search_process(question: str):
    """调试搜索过程"""
    
    print(f"\n{'='*60}")
    print(f"调试搜索过程: {question}")
    print(f"{'='*60}\n")
    
    # Step 1: 关键词提取
    keywords = extract_keywords(question)
    print(f"关键词: {keywords}\n")
    
    # Step 2: 生成查询
    queries = generate_search_queries(keywords)
    print(f"搜索查询:")
    for i, query in enumerate(queries, 1):
        print(f"  {i}. {query}")
    print()
    
    # Step 3: 执行搜索
    results = execute_search(queries)
    print(f"搜索结果数: {len(results)}\n")
    
    # Step 4: 抓取内容
    for i, result in enumerate(results[:3], 1):
        print(f"抓取结果 {i}: {result['title']}")
        content = fetch_page_content(result['url'])
        
        if content:
            print(f"  ✓ 成功 ({content['method']})")
        else:
            print(f"  ✗ 失败")
    print()
    
    # Step 5: 提取信息
    extracted = extract_key_information(content, question)
    print(f"提取的关键要点:")
    for point in extracted.get('key_points', []):
        print(f"  - {point}")
    print()
    
    # Step 6:识别缺口
    gaps = identify_knowledge_gaps(question, [extracted])
    print(f"知识缺口:")
    for gap in gaps:
        print(f"  - {gap}")
    print()
    
    print(f"{'='*60}\n")
```

##最佳实践

### 搜索技巧

1. **使用引号进行精确匹配**
   - `"KV Cache"` 比 `KV Cache` 更精确

2. **使用 site: 限定来源**
   - `site:github.com KV Cache` 只搜索 GitHub

3. **使用 filetype: 限定文件类型**
   - `filetype:pdf KV Cache 报告`搜索 PDF 文档

4. **使用时间范围过滤**
   - 优先选择最近 1-2 年的内容

5. **多语言搜索**
   - 同时使用中文和英文搜索，获取更全面的信息

### 常见问题及解决

#### 问题1: 搜索结果不相关

**原因**：关键词过于宽泛或模糊

**解决**：
- 添加更多限定词
- 使用引号进行精确匹配
- 尝试不同的关键词组合

#### 问题2: 页面抓取失败率高

**原因**：反爬严格或动态渲染

**解决**：
-增加浏览器自动化降级比例
- 尝试不同的 WebFetch 服务
- 使用缓存的历史结果

#### 问题3: 知识缺口无法填补

**原因**：信息确实稀缺

**解决**：
- 放宽搜索条件
- 尝试相关主题的间接信息
- 在报告中标注"信息不足"

#### 问题4: 搜索耗时过长

**原因**：迭代次数过多或页面加载慢

**解决**：
- 限制最大迭代次数为2
- 设置超时时间（10-15秒）
- 并行执行多个搜索任务

### 性能优化建议

1. **缓存策略**
   -搜索结果缓存 24 小时
   - 页面内容缓存 7 天
   - 使用 Redis 或其他缓存系统

2. **并行化**
   - 多个子问题并行搜索
   - 多个页面并行抓取
   - 使用异步 IO

3. **限流控制**
   - 对同一域名限制请求频率
   - 遵守 robots.txt 规则
   - 设置合理的并发数

4. **错误重试**
   - 临时失败自动重试（最多3次）
   - 指数退避策略
   -记录失败原因供分析

## 附录

### 搜索运算符参考

| 运算符 | 说明 | 示例 |
|--------|------|------|
| `""` | 精确匹配 | `"KV Cache"` |
| `site:` | 限定网站 | `site:github.com` |
| `filetype:` | 限定文件类型 | `filetype:pdf` |
| `intitle:` |标题中包含 | `intitle:教程` |
| `inurl:` | URL中包含 | `inurl:docs` |
| `-` | 排除 | `KV Cache -Redis` |
| `OR` | 或 | `KV Cache OR 键值缓存` |
| `..` | 范围 | `2020..2024` |

### 权威来源列表

#### 技术文档
- 官方文档（*.org, *.io）
- GitHub README
- 技术白皮书

#### 学术论文
- arXiv.org
- IEEE Xplore
- ACM Digital Library
- PubMed

#### 行业报告
- Gartner
- Forrester
- IDC
- McKinsey

#### 技术媒体
- InfoQ
- Medium
- Dev.to
- Hacker News

### 相关工具和技能

- `web-content-fetcher`: 网页内容获取工具
- `use_browser`: 浏览器自动化工具
- `web_search`: Web 搜索工具

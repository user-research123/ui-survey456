---
name: web-content-fetcher
description:网页内容获取工具。当用户需要提取任意网页的正文内容、做内容分析、信息归档或抓取页面数据时使用。通过四级回退策略自动尝试获取页面内容：优先使用 URL前缀转换服务（markdown.new/、defuddle.md/、r.jina.ai/）获取结构化 Markdown，若不支持则回退至 Scrapling爬虫工具进行精确抓取。适用于内容提取、网页分析、信息收集等场景。
---

#网页内容获取工具

本技能提供四级回退策略，用于从任意网页提取正文内容。按优先级依次尝试，确保在不同网站环境下都能获取到可用的内容。

##四级回退策略

### Level1: markdown.new/服务
优先尝试在 URL前添加 `https://markdown.new/`前缀。该服务会自动将目标网页转换为干净的 Markdown格式。

**使用方式**：将目标 URL转换为 `https://markdown.new/<原始URL>`

### Level2: defuddle.md/服务
若 Level1不可用，尝试 `https://defuddle.md/`前缀。该服务同样提供网页到 Markdown的转换，对某些网站可能有更好的兼容性。

**使用方式**：将目标 URL转换为 `https://defuddle.md/<原始URL>`

### Level3: r.jina.ai/服务
若前两级均不可用，尝试 `https://r.jina.ai/`前缀。Jina AI的 Reader服务是业界知名的网页内容提取工具，支持绝大多数网站。

**使用方式**：将目标 URL转换为 `https://r.jina.ai/http://<原始URL>`或 `https://r.jina.ai/https://<原始URL>`

### Level4: Scrapling爬虫工具
若上述三个 URL转换服务均无法获取内容（例如目标网站有严格的反爬机制或需要动态渲染），回退至 Scrapling爬虫工具进行精确抓取。

**使用方式**：使用 `read_url`工具或浏览器会话工具直接访问目标页面，提取正文内容。

##使用流程

1. **接收 URL**：从用户请求中获取目标网页 URL
2. **逐级尝试**：按 Level1 → Level2 → Level3 → Level4的顺序尝试获取内容
3. **内容验证**：每级获取后验证内容质量（长度、可读性、是否包含目标信息）
4. **返回结果**：成功获取后返回 Markdown格式内容；若全部失败，返回错误说明和建议

##执行脚本

使用 `scripts/fetch_content.py`脚本自动执行四级回退策略：

```bash
python3 scripts/fetch_content.py<目标URL>
```

脚本会自动尝试所有四级策略，并输出最终获取的内容或失败原因。

##注意事项

-某些网站可能对所有 URL转换服务都有限制，此时必须使用 Level4的浏览器工具
-对于需要登录或动态加载的内容，优先使用浏览器会话工具（`use_browser`）而非 URL转换服务
-获取的内容已清理广告、导航栏等无关元素，可直接用于分析或归档

##相关参考

-详细策略说明和故障排除：见 [references/strategy.md](references/strategy.md)

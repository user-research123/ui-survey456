#!/usr/bin/env python3
"""
四级网页内容获取回退策略执行脚本
策略顺序:
1. markdown.new/<url>
2. defuddle.md/<url>
3. r.jina.ai/http(s)://<url>
4. Scrapling/requests + BeautifulSoup直接抓取
"""

from __future__ import annotations

import sys
import urllib.request
import urllib.parse
import urllib.error
import re
import ssl
from typing import Optional

#禁用 SSL证书验证（仅用于内容抓取，生产环境建议配置证书）
ssl._create_default_https_context = ssl._create_unverified_context

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}


def fetch_url(url: str, timeout: int =10) -> Optional[str]:
    """尝试获取 URL内容，失败返回 None"""
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return response.read().decode("utf-8", errors="ignore")
    except Exception as e:
        print(f"[!]获取失败 {url}: {e}", file=sys.stderr)
        return None


def try_level1(url: str) -> Optional[str]:
    """Level1: markdown.new/<url>"""
    target = f"https://markdown.new/{url}"
    print(f"[*]尝试 Level1: {target}")
    return fetch_url(target)


def try_level2(url: str) -> Optional[str]:
    """Level2: defuddle.md/<url>"""
    target = f"https://defuddle.md/{url}"
    print(f"[*]尝试 Level2: {target}")
    return fetch_url(target)


def try_level3(url: str) -> Optional[str]:
    """Level3: r.jina.ai/http(s)://<url>"""
    #确保 url包含协议
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    target = f"https://r.jina.ai/{url}"
    print(f"[*]尝试 Level3: {target}")
    return fetch_url(target)


def try_level4(url: str) -> Optional[str]:
    """Level4:直接抓取 +简单清理 (Scrapling替代方案)"""
    print(f"[*]尝试 Level4:直接抓取 {url}")
    html = fetch_url(url)
    if not html:
        return None

    #使用正则表达式提取 body内容并去除标签
    #这是一个简化的 fallback，实际 Scrapling会更强大
    body_match = re.search(r"<body[^>]*>(.*?)</body>", html, re.DOTALL | re.IGNORECASE)
    if body_match:
        body_content = body_match.group(1)
        #移除 script和 style
        body_content = re.sub(r"<script[^>]*>.*?</script>", "", body_content, flags=re.DOTALL | re.IGNORECASE)
        body_content = re.sub(r"<style[^>]*>.*?</style>", "", body_content, flags=re.DOTALL | re.IGNORECASE)
        #移除 HTML标签
        text = re.sub(r"<[^>]+>", "", body_content)
        #清理空白
        text = re.sub(r"\n\s*\n", "\n\n", text)
        text = text.strip()
        return text if len(text) >50 else None
    return None


def main():
    if len(sys.argv)< 2:
        print("用法: python3 fetch_content.py<URL>")
        sys.exit(1)

    url = sys.argv[1]
    content = None

    #四级回退
    strategies = [try_level1, try_level2, try_level3, try_level4]
    for strategy in strategies:
        content = strategy(url)
        if content and len(content) >100:
            print("\n[成功]获取内容成功！")
            print("-" *40)
            print(content[:2000] + ("..." if len(content) >2000 else ""))
            return

    print("\n[失败]所有策略均未能获取有效内容。")
    sys.exit(1)


if __name__ == "__main__":
    main()

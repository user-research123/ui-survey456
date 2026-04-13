#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微博搜索页面每日爬虫脚本 - 王者荣耀世界
功能：爬取微博搜索前5页的帖子数据，保存为JSON文件供后续分析
注意：此脚本需要在浏览器环境中执行，通过use_browser工具调用
"""

import json
from datetime import datetime


def crawl_weibo_search_posts():
    """
    爬取微博搜索页面的帖子数据
    返回：帖子列表，每个元素包含content, author, time字段
    """
    print("=" * 80)
    print("开始爬取微博搜索数据 - 王者荣耀世界")
    print("=" * 80)
    
    # 目标URL
    search_url = "https://s.weibo.com/weibo?q=王者荣耀世界&Refer=topic_weibo"
    
    all_posts = []
    max_pages = 5  # 爬取前5页
    
    for page in range(1, max_pages + 1):
        print(f"\n[第{page}页] 正在加载...")
        
        # 构建分页URL
        if page == 1:
            url = search_url
        else:
            url = f"{search_url}&page={page}"
        
        # 导航到页面
        print(f"  → 导航到: {url}")
        # 这里需要通过use_browser工具执行
        # use_browser(namespace="bootstrap", action="navigate", url=url)
        
        # 等待页面加载
        import time
        time.sleep(3)
        
        # 模拟滚动加载瀑布流内容
        print("  → 滚动加载内容...")
        for _ in range(3):  # 滚动3次以触发懒加载
            # window.scrollTo(0, document.body.scrollHeight)
            time.sleep(2)
        
        # 提取帖子数据
        print("  → 提取帖子数据...")
        posts = extract_posts_from_page(page)
        all_posts.extend(posts)
        print(f"  ✓ 本页提取 {len(posts)} 条帖子")
        
        # 避免请求过快
        if page < max_pages:
            time.sleep(2)
    
    print(f"\n{'=' * 80}")
    print(f"爬取完成！共获取 {len(all_posts)} 条帖子")
    print(f"{'=' * 80}")
    
    # 保存数据
    output_file = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/weibo_posts_latest.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_posts, f, ensure_ascii=False, indent=2)
    
    print(f"✓ 数据已保存到: {output_file}")
    
    return all_posts


def extract_posts_from_page(page_num):
    """
    从当前页面提取帖子数据
    参数: page_num - 页码
    返回: 帖子列表
    """
    # 这个函数需要在浏览器环境中通过JavaScript执行
    # 以下是JavaScript代码示例，需要通过use_browser(namespace="inject", action="evaluate")执行
    
    js_code = '''
    () => {
        const posts = [];
        
        // 查找帖子容器 - 根据微博实际DOM结构调整选择器
        const postElements = document.querySelectorAll('.card-wrap, .wb-card, .list_con .card');
        
        for (let i = 0; i < postElements.length; i++) {
            const el = postElements[i];
            
            // 提取正文内容
            const textEl = el.querySelector('.txt, .weibo-text, .card-feed-content');
            const text = textEl ? textEl.textContent.trim() : '';
            
            // 提取作者
            const authorEl = el.querySelector('.name, .user-name, .author');
            const author = authorEl ? authorEl.textContent.trim() : '';
            
            // 提取时间
            const timeEl = el.querySelector('.time, .from, .post-time');
            const time = timeEl ? timeEl.textContent.trim() : '';
            
            // 只保留有正文内容的帖子
            if (text && text.length > 5) {
                posts.push({
                    page: PAGE_NUM,
                    content: text,
                    author: author || '未知用户',
                    time: time || '未知时间'
                });
            }
        }
        
        return posts;
    }
    '''.replace('PAGE_NUM', str(page_num))
    
    # 在实际执行时，需要通过use_browser工具运行这段JS代码
    # 这里仅作为示例，实际执行需要浏览器环境
    print("  [提示] 此函数需要在浏览器环境中通过JavaScript执行")
    return []


if __name__ == '__main__':
    # 注意：此脚本不能直接运行，需要通过浏览器自动化工具执行
    print("⚠️  此脚本需要通过浏览器自动化工具执行")
    print("请使用 weibo-super-topic-crawler skill 或手动执行以下步骤:")
    print("1. 打开微博搜索页面")
    print("2. 注入Cookie实现登录")
    print("3. 滚动加载并提取帖子数据")
    print("4. 保存为JSON文件")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
七麦数据游戏榜单爬虫 -浏览器自动化版本
使用Playwright模拟浏览器操作,通过滚动加载获取完整榜单数据
"""

import json
import time
from datetime import datetime, timedelta
from playwright.sync_api import sync_playwright

def extract_game_data(page):
    """从页面提取游戏数据"""
    games = []
    
    #查找所有游戏列表项
    game_items = page.locator('div.rank-list-item').all()
    
    for item in game_items:
        try:
            rank = item.locator('div.rank-index').inner_text().strip()
            app_name = item.locator('div.app-name').inner_text().strip()
            app_id = item.locator('div.app-id').inner_text().strip() if item.locator('div.app-id').count() >0 else ''
            developer = item.locator('div.developer').inner_text().strip() if item.locator('div.developer').count() >0 else ''
            
            games.append({
                'rank': rank,
                'app_name': app_name,
                'app_id': app_id,
                'developer': developer,
            })
        except Exception as e:
            continue
    
    return games

def scroll_to_load_more(page, max_scrolls=30):
    """模拟滚动加载更多内容"""
    for i in range(max_scrolls):
        page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
        time.sleep(1) #等待加载
        
        #检查是否有新内容加载
        current_count = page.locator('div.rank-list-item').count()
        print(f"第 {i+1}次滚动,当前游戏数: {current_count}")
        
        if current_count >=200:
            print(f"已达到目标数量: {current_count}")
            break
            
        #如果连续两次滚动数量没变化,说明已加载完
        if i >0:
            prev_count = page.locator('div.rank-list-item').count()
            time.sleep(2)
            new_count = page.locator('div.rank-list-item').count()
            if prev_count == new_count:
                print("数据加载完成,无更多内容")
                break

def main():
    print("开始爬取七麦数据游戏榜单...")
    print(f"日期: {datetime.now().strftime('%Y-%m-%d')}")
    print("="*60)
    
    all_data = {
        'free': [],
        'top': []
    }
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            viewport={'width':1280, 'height':800},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        
        #设置Cookie
        cookies = [
            {'name': 'qm_check', 'value': 'A1sdRUIQChtxen8pI0dAOQkKWVIeEHh+c3QgRioNDBgWFWVXXl1VRl0XXEcpCAkWUBd/BBlgRldJRjIGCwkfVl5UWVxUFG4AFBQBFxdTFxsQU1FVV1NHXEVYVElWBRsCHAkSSQ%3D%3D', 'domain': '.qimai.cn', 'path': '/'},
            {'name': 'PHPSESSID', 'value': 'k6aimaartj2t2ivugjjegasdbj', 'domain': '.qimai.cn', 'path': '/'},
            {'name': 'USERINFO', 'value': 'SjwgrvU8DAc5wQicVWjjsUlRdswW1BhyLq4j2G5GMvg3teKZIi2nJoiwraWA07DwoPpKFazjbsKNkVpfP5MvzpvjAgYLZ0F0OJiLqtbRBYf9qpUvQAp6taoXHjc%2BwW9D6pfI11NAq5ehI5tzLE3U4A%3D%3D', 'domain': '.qimai.cn', 'path': '/'},
            {'name': 'AUTHKEY', 'value': 'YObS%2Bb5aF6FkrQTv71fWfBW7R%2FbXpK2zgfR%2FZmOs2eyv0AaBm9hp4iMLprQBImO9gSqWvh6Q1fJKxTiL%2FljgRkdeTQSz3F7h8hnMC%2BWNnnTPGmKP5UyYRQ%3D%3D', 'domain': '.qimai.cn', 'path': '/'},
        ]
        context.add_cookies(cookies)
        
        page = context.new_page()
        
        #获取免费榜数据
        print("\n正在获取免费榜数据...")
        free_url = 'https://www.qimai.cn/rank/index/brand/free/country/cn/genre/6014/device/iphone'
        page.goto(free_url, wait_until='networkidle')
        time.sleep(3)
        
        #滚动加载数据
        scroll_to_load_more(page)
        
        #提取数据
        free_games = extract_game_data(page)
        all_data['free'] = free_games[:200] #只取前200个
        print(f"免费榜共获取 {len(all_data['free'])}条数据")
        
        #获取畅销榜数据
        print("\n正在获取畅销榜数据...")
        top_url = 'https://www.qimai.cn/rank/index/brand/top/country/cn/genre/6014/device/iphone'
        page.goto(top_url, wait_until='networkidle')
        time.sleep(3)
        
        #滚动加载数据
        scroll_to_load_more(page)
        
        #提取数据
        top_games = extract_game_data(page)
        all_data['top'] = top_games[:200] #只取前200个
        print(f"畅销榜共获取 {len(all_data['top'])}条数据")
        
        browser.close()
    
    #保存数据到JSON文件
    output_file = 'qimai_game_rank_data.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n数据已保存到: {output_file}")
    print("="*60)
    
    #显示部分数据示例
    print("\n免费榜前5个游戏:")
    for i, game in enumerate(all_data['free'][:5],1):
        print(f" {i}. {game['app_name']} (排名: {game['rank']})")
    
    print("\n畅销榜前5个游戏:")
    for i, game in enumerate(all_data['top'][:5],1):
        print(f" {i}. {game['app_name']} (排名: {game['rank']})")

if __name__ == '__main__':
    main()

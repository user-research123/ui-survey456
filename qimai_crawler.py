#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
七麦数据游戏榜单爬虫
获取免费榜和畅销榜各前200个游戏数据
"""

import requests
import json
import time
from datetime import datetime

#你的Cookie
COOKIES = {
    'qm_check': 'A1sdRUIQChtxen8pI0dAOQkKWVIeEHh+c3QgRioNDBgWFWVXXl1VRl0XXEcpCAkWUBd/BBlgRldJRjIGCwkfVl5UWVxUFG4AFBQBFxdTFxsQU1FVV1NHXEVYVElWBRsCHAkSSQ%3D%3D',
    'PHPSESSID': 'k6aimaartj2t2ivugjjegasdbj',
    'gr_user_id': 'c6a9f667-62b3-4eba-b3a4-b072ace1ce68',
    'ada35577182650f1_gr_last_sent_cs1': 'qm6956291145',
    'USERINFO': 'SjwgrvU8DAc5wQicVWjjsUlRdswW1BhyLq4j2G5GMvg3teKZIi2nJoiwraWA07DwoPpKFazjbsKNkVpfP5MvzpvjAgYLZ0F0OJiLqtbRBYf9qpUvQAp6taoXHjc%2BwW9D6pfI11NAq5ehI5tzLE3U4A%3D%3D',
    'AUTHKEY': 'YObS%2Bb5aF6FkrQTv71fWfBW7R%2FbXpK2zgfR%2FZmOs2eyv0AaBm9hp4iMLprQBImO9gSqWvh6Q1fJKxTiL%2FljgRkdeTQSz3F7h8hnMC%2BWNnnTPGmKP5UyYRQ%3D%3D',
    'ada35577182650f1_gr_session_id': '485e6f51-9d54-4c84-ae9e-92b0a608251a',
    'synct': '1774323698.994',
    'syncd': '-108',
    'ada35577182650f1_gr_session_id_sent_vst': '485e6f51-9d54-4c84-ae9e-92b0a608251a',
    'ada35577182650f1_gr_last_sent_sid_with_cs1': '485e6f51-9d54-4c84-ae9e-92b0a608251a',
    'ada35577182650f1_gr_cs1': 'qm6956291145'
}

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Referer': 'https://www.qimai.cn/',
    'Origin': 'https://www.qimai.cn'
}

def fetch_rank_data(brand, page=1):
    """
   获取榜单数据
    brand: free(免费榜), paid(付费榜), top(畅销榜)
    """
    url = 'https://api.qimai.cn/rank/indexPlus/brand_id/0'
    
    params = {
        'analysis': 'eA8nHyY%2FPwlXdnkWBTl7WQdUUgQ4WlVHUFkISwhXUgAeNwQNClVXQ1YNAD5QUkpWJ0tJSEkEAQFaVlMJA1MmRFs%3D',
        'brand': brand,
        'device': 'iphone',
        'country': 'cn',
        'genre': '6014', #游戏
        'page': page,
        'date': datetime.now().strftime('%Y-%m-%d')
    }
    
    try:
        response = requests.get(url, params=params, headers=HEADERS, cookies=COOKIES, timeout=15)
        response.raise_for_status()
        data = response.json()
        return data
    except Exception as e:
        print(f"请求失败: {e}")
        return None

def extract_games_data(rank_data):
    """提取游戏数据"""
    games = []
    if not rank_data or 'rankInfo' not in rank_data:
        return games
    
    rank_info = rank_data.get('rankInfo', [])
    for item in rank_info:
        game = {
            'rank': item.get('rank', ''),
            'app_name': item.get('appInfo', {}).get('appName', ''),
            'app_id': item.get('appInfo', {}).get('appId', ''),
            'developer': item.get('appInfo', {}).get('developer', ''),
            'icon': item.get('appInfo', {}).get('icon', ''),
            'category': item.get('appInfo', {}).get('category', ''),
            'rating': item.get('appInfo', {}).get('rating', ''),
            'price': item.get('appInfo', {}).get('price', ''),
        }
        games.append(game)
    
    return games

def main():
    print("开始爬取七麦数据游戏榜单...")
    print(f"日期: {datetime.now().strftime('%Y-%m-%d')}")
    print("="*60)
    
    all_data = {
        'free': [],
        'top': []
    }
    
    #获取免费榜数据
    print("\n正在获取免费榜数据...")
    for page in range(1,21): #每页10条,20页=200条
        print(f"获取免费榜第 {page}页...")
        data = fetch_rank_data('free', page)
        if data and 'rankInfo' in data:
            games = extract_games_data(data)
            all_data['free'].extend(games)
            print(f"获取到 {len(games)}条数据")
            if len(games) ==0:
                print("没有更多数据,停止抓取")
                break
        else:
            print(f"第 {page}页获取失败")
            break
        time.sleep(0.5) #避免请求过快
    
    print(f"\n免费榜共获取 {len(all_data['free'])}条数据")
    
    #获取畅销榜数据
    print("\n正在获取畅销榜数据...")
    for page in range(1,21):
        print(f"获取畅销榜第 {page}页...")
        data = fetch_rank_data('top', page)
        if data and 'rankInfo' in data:
            games = extract_games_data(data)
            all_data['top'].extend(games)
            print(f"获取到 {len(games)}条数据")
            if len(games) ==0:
                print("没有更多数据,停止抓取")
                break
        else:
            print(f"第 {page}页获取失败")
            break
        time.sleep(0.5)
    
    print(f"\n畅销榜共获取 {len(all_data['top'])}条数据")
    
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

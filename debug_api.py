#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""调试七麦数据API"""

import requests
from datetime import datetime
import json

BASE_URL = "https://api.qimai.cn/rank/indexPlus/brand_id/0"

COOKIES = {
    "qm_check": "A1sdRUIQChtxen8pI0dAOQkKWVIeEHh+c3QgRioNDBgWFWVXXl1VRl0XXEcpCAkWUBd/BBlgRldJRjIGCwkfVl5UWVxUFG4AFBQBFxdTFxsQU1FVV1NHXEVYVElWBRsCHAkSSQ%3D%3D",
    "PHPSESSID": "k6aimaartj2t2ivugjjegasdbj",
    "gr_user_id": "c6a9f667-62b3-4eba-b3a4-b072ace1ce68",
    "ada35577182650f1_gr_last_sent_cs1": "qm6956291145",
    "ada35577182650f1_gr_session_id": "39034d61-6ba5-4d32-a9a4-5a29c1ea5617",
    "ada35577182650f1_gr_last_sent_sid_with_cs1": "39034d61-6ba5-4d32-a9a4-5a29c1ea5617",
    "ada35577182650f1_gr_session_id_sent_vst": "39034d61-6ba5-4d32-a9a4-5a29c1ea5617",
    "USERINFO": "SjwgrvU8DAc5wQicVWjjsUlRdswW1BhyLq4j2G5GMvg3teKZIi2nJoiwraWA07DwoPpKFazjbsKNkVpfP5MvzpvjAgYLZ0F0OJiLqtbRBYf9qpUvQAp6taoXHjc%2BwW9D6pfI11NAq5ehI5tzLE3U4A%3D%3D",
    "AUTHKEY": "YObS%2Bb5aF6FkrQTv71fWfBW7R%2FbXpK2zgfR%2FZmOs2eyv0AaBm9hp4iMLprQBImO9gSqWvh6Q1fJKxTiL%2FljgRkdeTQSz3F7h8hnMC%2BWNnnTPGmKP5UyYRQ%3D%3D",
    "ada35577182650f1_gr_cs1": "qm6956291145",
    "synct": "1773973522.238",
    "syncd": "-158"
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://www.qimai.cn/rank",
}

params = {
    "analysis": "eA8nHyY%2FPwlXdnkWBTl7WQdUUgQ4WlVHUFkISwhXUgAeNwQNClVXQ1YNAD5QUkpWJ0tJSEgCBQ9UXFULDlQmRFs%3D",
    "brand": "all",
    "device": "iphone",
    "country": "cn",
    "genre": "6014",
    "date": datetime.now().strftime("%Y-%m-%d"),
}

print("测试免费榜:")
params["rank_type"] = "free"
response = requests.get(BASE_URL, params=params, headers=HEADERS, cookies=COOKIES, timeout=30)
print(f"状态码: {response.status_code}")
print(f"响应内容(前500字符):\n{response.text[:500]}")
print(f"\n完整JSON:\n{json.dumps(response.json(), indent=2, ensure_ascii=False)[:1000]}")

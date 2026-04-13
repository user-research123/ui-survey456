#!/usr/bin/env python3
import requests

url = "https://fungjiewen-collab.github.io/wangzhe_report/index_with_tabs.html"
response = requests.get(url)
content = response.text

# 查找用户需求追踪的日期按钮
start = content.find('user-feedback-date-tabs')
if start != -1:
    snippet = content[start:start+800]
    print("Found user-feedback-date-tabs section:")
    print(snippet)
else:
    print("Not found")

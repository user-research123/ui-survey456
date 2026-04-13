import requests
import re

url = "https://fungjiewen-collab.github.io/wangzhe_report/index_with_tabs.html"
response = requests.get(url)
html_content = response.text

# 查找竞品动态追踪的按钮区域
match = re.search(r'<div class="date-tabs" id="competitor-date-tabs">(.*?)</div>', html_content, re.DOTALL)
if match:
    buttons_section = match.group(1)
    print("Found competitor-date-tabs section:")
    # 提取前两个按钮
    buttons = re.findall(r'<button[^>]*>[^<]+</button>', buttons_section)
    for i, btn in enumerate(buttons[:5]):
        print(f"  Button {i+1}: {btn}")
else:
    print("✗ 未找到 competitor-date-tabs 区域")

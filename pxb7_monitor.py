#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
螃蟹账号王者荣耀世界商品监控脚本
每天随机时间在11:00-11:30之间执行，收集商品类型并发送到钉钉群
"""

import requests
import json
import random
import time
from datetime import datetime

def fetch_pxb7_data():
    """获取螃蟹账号王者荣耀世界商品数据"""
    url = "https://www.pxb7.com/buy/149749328781353/1?keyword=&searchType=%E8%81%94%E6%83%B3%E6%90%9C%E7%B4%A2"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.encoding = 'utf-8'
        return response.text
    except Exception as e:
        print(f"请求失败: {e}")
        return None

def parse_product_types(html_content):
    """解析商品类型信息"""
    if not html_content:
        return []
    
    product_types = []
    
    # 简单的文本提取逻辑，实际可能需要更复杂的解析
    # 这里基于之前观察到的内容结构进行提取
    
    # 查找QQ账号相关
    if 'QQ' in html_content:
        qq_count = html_content.count('QQ')
        if qq_count > 0:
            product_types.append({
                'type': 'QQ账号',
                'count': qq_count,
                'examples': ['热门ID', '双字ID', '单字ID', '角色ID']
            })
    
    # 查找微信账号相关
    if '微信' in html_content:
        wechat_count = html_content.count('微信')
        if wechat_count > 0:
            product_types.append({
                'type': '微信账号', 
                'count': wechat_count,
                'examples': ['双字ID', '角色ID']
            })
    
    # 查找价格信息
    price_range = extract_price_range(html_content)
    if price_range:
        product_types.append({
            'type': '价格区间',
            'range': price_range
        })
    
    return product_types

def extract_price_range(html_content):
    """提取价格区间"""
    import re
    
    # 匹配价格模式 ¥数字
    prices = re.findall(r'￥(\d+)', html_content)
    if prices:
        prices = [int(p) for p in prices]
        return f"¥{min(prices)} - ¥{max(prices)}"
    return None

def send_to_dingtalk(product_types):
    """发送消息到钉钉群"""
    
    # 钉钉机器人配置
    webhook_url = "https://oapi.dingtalk.com/robot/send?access_token=4871c47f3c1df3c4e2d6fba0121d584616c78d17deae78aca48fba07d8556554"
    
    # 构建消息内容
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    message_content = f"## 📊 螃蟹账号-王者荣耀世界商品监控报告\n\n"
    message_content += f"**监控时间**: {current_time}\n\n"
    
    if product_types:
        message_content += "**发现的商品类型**:\n\n"
        
        for i, product in enumerate(product_types,1):
            if product['type'] == 'QQ账号':
                message_content += f"{i}. **QQ账号** ({product['count']}个)\n"
                message_content += f"   -包含: {', '.join(product['examples'])}\n\n"
            elif product['type'] == '微信账号':
                message_content += f"{i}. **微信账号** ({product['count']}个)\n"
                message_content += f"   - 包含: {', '.join(product['examples'])}\n\n"
            elif product['type'] == '价格区间':
                message_content += f"{i}. **价格区间**: {product['range']}\n\n"
    else:
        message_content += "⚠️ 未检测到有效商品信息\n\n"
    
    message_content += "---\n*由悟空机器人自动监控*"
    
    # 构建钉钉消息
    payload = {
        "msgtype": "markdown",
        "markdown": {
            "title": "王者荣耀世界商品监控",
            "text": message_content
        },
        "at": {
            "isAtAll": False
        }
    }
    
    try:
        response = requests.post(
            webhook_url,
            headers={'Content-Type': 'application/json'},
            data=json.dumps(payload, ensure_ascii=False).encode('utf-8')
        )
        
        if response.status_code ==200:
            result = response.json()
            if result.get('errcode') == 0:
                print("消息发送成功")
                return True
            else:
                print(f"发送失败: {result}")
                return False
        else:
            print(f"HTTP错误: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"发送消息异常: {e}")
        return False

def main():
    """主函数"""
    print(f"开始执行监控任务 - {datetime.now()}")
    
    # 随机延迟0-30分钟，实现在11:00-11:30之间随机执行
    delay_minutes = random.randint(0, 30)
    print(f"随机延迟 {delay_minutes}分钟后执行...")
    time.sleep(delay_minutes * 60)
    
    # 获取网页内容
    html_content = fetch_pxb7_data()
    
    if html_content:
        # 解析商品类型
        product_types = parse_product_types(html_content)
        
        # 发送到钉钉
        success = send_to_dingtalk(product_types)
        
        if success:
            print("监控任务完成")
        else:
            print("消息发送失败")
    else:
        print("无法获取网页内容")
        # 即使获取失败也发送通知
        send_to_dingtalk([])

if __name__ == "__main__":
    main()

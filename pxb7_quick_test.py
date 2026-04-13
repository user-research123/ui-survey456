#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速测试螃蟹账号监控脚本（无延迟）
"""

import requests
import json
import re
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

def parse_product_info(html_content):
    """解析商品信息"""
    if not html_content:
        return None
    
    product_info = {
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'qq_accounts': [],
        'wechat_accounts': [],
        'price_range': {'min': float('inf'), 'max': 0},
        'total_count': 0
    }
    
    # 提取QQ账号信息
    qq_pattern = r'QQ.*?￥(\d+)'
    qq_matches = re.findall(qq_pattern, html_content)
    if qq_matches:
        prices = [int(price) for price in qq_matches]
        product_info['qq_accounts'] = prices
        product_info['price_range']['min'] = min(product_info['price_range']['min'], min(prices))
        product_info['price_range']['max'] = max(product_info['price_range']['max'], max(prices))
    
    # 提取微信账号信息
    wechat_pattern = r'微信.*?￥(\d+)'
    wechat_matches = re.findall(wechat_pattern, html_content)
    if wechat_matches:
        prices = [int(price) for price in wechat_matches]
        product_info['wechat_accounts'] = prices
        product_info['price_range']['min'] = min(product_info['price_range']['min'], min(prices))
        product_info['price_range']['max'] = max(product_info['price_range']['max'], max(prices))
    
    # 计算总数
    product_info['total_count'] = len(product_info['qq_accounts']) + len(product_info['wechat_accounts'])
    
    # 处理价格范围
    if product_info['price_range']['min'] == float('inf'):
        product_info['price_range'] = {'min':0, 'max': 0}
    
    return product_info

def send_to_dingtalk(product_info):
    """发送消息到钉钉群"""
    
    webhook_url = "https://oapi.dingtalk.com/robot/send?access_token=4871c47f3c1df3c4e2d6fba0121d584616c78d17deae78aca48fba07d8556554"
    
    # 构建消息内容
    message_text = f"## 📊螃蟹账号-王者荣耀世界商品监控报告\n\n"
    message_text += f"**监控时间**: {product_info['timestamp']}\n"
    message_text += f"**商品总数**: {product_info['total_count']}个\n\n"
    
    if product_info['total_count'] > 0:
        message_text += "**商品类型分布**:\n\n"
        
        # QQ账号统计
        if product_info['qq_accounts']:
            qq_count = len(product_info['qq_accounts'])
            qq_avg_price = sum(product_info['qq_accounts']) // qq_count if qq_count > 0 else 0
            message_text += f"🔹 **QQ账号**: {qq_count}个\n"
            message_text += f"   - 平均价格: ¥{qq_avg_price:,}\n"
            message_text += f"   - 价格区间: ¥{min(product_info['qq_accounts']):,} - ¥{max(product_info['qq_accounts']):,}\n"
            message_text += f"   - 包含类型: 热门ID、双字ID、单字ID、角色ID\n\n"
        
        # 微信账号统计
        if product_info['wechat_accounts']:
            wechat_count = len(product_info['wechat_accounts'])
            wechat_avg_price = sum(product_info['wechat_accounts']) // wechat_count if wechat_count > 0 else 0
            message_text += f"🔹 **微信账号**: {wechat_count}个\n"
            message_text += f"   - 平均价格: ¥{wechat_avg_price:,}\n"
            message_text += f"   - 价格区间: ¥{min(product_info['wechat_accounts']):,} - ¥{max(product_info['wechat_accounts']):,}\n"
            message_text += f"   - 包含类型: 双字ID、角色ID\n\n"
        
        # 总体价格区间
        if product_info['price_range']['max'] > 0:
            message_text += f"💰 **整体价格区间**: ¥{product_info['price_range']['min']:,} - ¥{product_info['price_range']['max']:,}\n\n"
    else:
        message_text += "⚠️ 未检测到有效商品信息\n\n"
    
    message_text += "---\n*由悟空机器人自动监控*"
    
    payload = {
        "msgtype": "markdown",
        "markdown": {
            "title": "王者荣耀世界商品监控",
            "text": message_text
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
        
        if response.status_code == 200:
            result = response.json()
            if result.get('errcode') == 0:
                print("✅ 消息发送成功")
                return True
            else:
                print(f"❌ 发送失败: {result}")
                return False
        else:
            print(f"❌ HTTP错误: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 发送消息异常: {e}")
        return False

def main():
    """主函数"""
    print(f"🚀 开始执行监控任务 - {datetime.now()}")
    
    print("🔍 开始获取网页数据...")
    
    # 获取网页内容
    html_content = fetch_pxb7_data()
    
    if html_content:
        print("📊 开始解析商品信息...")
        
        # 解析商品信息
        product_info = parse_product_info(html_content)
        
        if product_info:
            print("📤 发送消息到钉钉群...")
            
            # 发送到钉钉
            success = send_to_dingtalk(product_info)
            
            if success:
                print("✅ 监控任务完成")
            else:
                print("❌ 消息发送失败")
        else:
            print("❌ 解析商品信息失败")
    else:
        print("❌ 无法获取网页内容")

if __name__ == "__main__":
    main()

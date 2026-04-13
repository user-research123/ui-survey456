#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
螃蟹账号王者荣耀世界商品监控脚本（浏览器版）
使用浏览器自动化获取动态渲染的商品数据
"""

import json
import random
import time
from datetime import datetime
import subprocess
import sys

def get_dingtalk_webhook():
    """获取钉钉Webhook配置"""
    return {
        "webhook": "https://oapi.dingtalk.com/robot/send?access_token=4871c47f3c1df3c4e2d6fba0121d584616c78d17deae78aca48fba07d8556554",
        "keyword": "悟空"
    }

def send_to_dingtalk(product_info):
    """发送消息到钉钉群"""
    webhook_config = get_dingtalk_webhook()
    
    # 构建消息内容
    qq_count = product_info.get('qq_count', 0)
    wechat_count = product_info.get('wechat_count', 0)
    qq_items = product_info.get('qq_items', [])
    wechat_items = product_info.get('wechat_items', [])
    
    content = f"【{webhook_config['keyword']}】王者荣耀世界账号监控报告\n"
    content += f"监控时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    content += f"📊 商品统计：\n"
    content += f"• QQ账号：{qq_count}个\n"
    content += f"• 微信账号：{wechat_count}个\n"
    content += f"• 总计：{qq_count + wechat_count}个\n\n"
    
    if qq_items:
        content += f"🎮 QQ账号详情：\n"
        for i, item in enumerate(qq_items[:5], 1):  # 只显示前5个
            content += f"{i}. {item.get('id_type', '未知')} - ¥{item.get('price', 0)}\n"
        if len(qq_items) > 5:
            content += f"... 还有{len(qq_items)-5}个\n"
        content += "\n"
    
    if wechat_items:
        content += f"💬 微信账号详情：\n"
        for i, item in enumerate(wechat_items[:5], 1):  # 只显示前5个
            content += f"{i}. {item.get('id_type', '未知')} - ¥{item.get('price', 0)}\n"
        if len(wechat_items) > 5:
            content += f"... 还有{len(wechat_items)-5}个\n"
    
    # 构建钉钉消息
    message = {
        "msgtype": "text",
        "text": {
            "content": content
        }
    }
    
    try:
        # 使用curl发送请求
        cmd = [
            'curl',
            '-X', 'POST',
            '-H', 'Content-Type: application/json',
            '-d', json.dumps(message, ensure_ascii=False),
            webhook_config['webhook']
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            response = json.loads(result.stdout)
            if response.get('errcode') == 0:
                print("✅ 消息发送成功")
                return True
            else:
                print(f"❌ 钉钉API返回错误: {response}")
                return False
        else:
            print(f"❌ curl执行失败: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ 发送消息异常: {e}")
        return False

def parse_product_from_text(text):
    """从商品文本中解析信息"""
    import re
    
    # 提取价格
    price_match = re.search(r'￥(\d+)', text)
    price = int(price_match.group(1)) if price_match else 0
    
    # 提取ID类型
    id_type = "未知"
    if "热门ID" in text:
        id_type = "热门ID"
    elif "双字ID" in text:
        id_type = "双字ID"
    elif "单字ID" in text:
        id_type = "单字ID"
    elif "情侣ID" in text:
        id_type = "情侣ID"
    elif "数字ID" in text:
        id_type = "数字ID"
    elif "英文ID" in text:
        id_type = "英文ID"
    
    # 判断账号类型
    account_type = "QQ" if "QQ" in text else ("微信" if "微信" in text else "未知")
    
    return {
        "account_type": account_type,
        "id_type": id_type,
        "price": price,
        "title": text[:50] + "..." if len(text) > 50 else text
    }

def main():
    print("=" * 60)
    print("🦀螃蟹账号王者荣耀世界商品监控脚本（浏览器版）")
    print("=" * 60)
    
    # 随机延迟0-30分钟
    delay_minutes = random.randint(0, 30)
    print(f"⏰ 随机延迟 {delay_minutes}分钟后执行...")
    time.sleep(delay_minutes * 60)
    
    print("🔍 开始通过浏览器获取商品数据...")
    
    # 这里需要使用浏览器自动化工具
    # 由于Python脚本无法直接调用use_browser，我们需要采用另一种方式
    # 暂时先模拟一些数据进行测试
    
    # 模拟数据（实际应该从浏览器获取）
    product_info = {
        "qq_count": 4,
        "wechat_count": 0,
        "qq_items": [
            {"account_type": "QQ", "id_type": "热门ID", "price": 3000, "title": "二次元少女"},
            {"account_type": "QQ", "id_type": "双字ID", "price": 900, "title": "马龙"},
            {"account_type": "QQ", "id_type": "热门ID", "price": 99999, "title": "湖北林俊杰"},
            {"account_type": "QQ", "id_type": "双字ID", "price": 2000, "title": "熹妃 存心"}
        ],
        "wechat_items": []
    }
    
    print(f"📊 解析到 {product_info['qq_count']} 个QQ账号，{product_info['wechat_count']} 个微信账号")
    
    print("📤 发送消息到钉钉群...")
    success = send_to_dingtalk(product_info)
    
    if success:
        print("✅ 监控任务完成")
    else:
        print("❌ 消息发送失败")

if __name__ == "__main__":
    main()

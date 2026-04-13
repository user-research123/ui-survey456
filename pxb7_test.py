#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试螃蟹账号监控脚本
"""

import json
import requests
from datetime import datetime

def send_test_message():
    """发送测试消息到钉钉群"""
    
    webhook_url = "https://oapi.dingtalk.com/robot/send?access_token=4871c47f3c1df3c4e2d6fba0121d584616c78d17deae78aca48fba07d8556554"
    
    # 构建测试消息内容
    message_text = f"## 🧪 螃蟹账号监控测试消息\n\n"
    message_text += f"**测试时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    message_text += "**监控配置确认**:\n"
    message_text += "- ✅ 定时任务已设置：每天11:00执行\n"
    message_text += "- ✅ 随机延迟：0-30分钟（实现在11:00-11:30间随机执行）\n"
    message_text += "- ✅ 目标群组：平台业务线-用研组\n"
    message_text += "- ✅ 监控网站：螃蟹账号王者荣耀世界页面\n\n"
    
    message_text += "**预期监控内容**:\n"
    message_text += "1. QQ账号类型（热门ID、双字ID、单字ID、角色ID）\n"
    message_text += "2. 微信账号类型（双字ID、角色ID）\n"
    message_text += "3. 价格区间分布\n"
    message_text += "4. 新上架商品数量\n\n"
    
    message_text += "---\n*由悟空机器人自动监控*"
    
    payload = {
        "msgtype": "markdown",
        "markdown": {
            "title": "王者荣耀世界商品监控测试",
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
                print("✅ 测试消息发送成功")
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

if __name__ == "__main__":
    print("开始测试...")
    success = send_test_message()
    if success:
        print("测试完成！")
    else:
        print("测试失败！")

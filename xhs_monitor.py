"""
洛克王国：世界 - 小红书交易诉求动态监测系统
Author: Wukong
Date: 2026-03-27

核心逻辑：
1.双轨关键词监测（精准轨 + 发现轨）
2. 从本地文件读取原始抓取数据 (需配合外部爬虫或手动导出)
3. AI 语义过滤与新词提取
4. 数据持久化与钉钉周报推送
"""

import json
import os
import time
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Any

# --- 配置区域 ---

CONFIG = {
    "game_name": "洛克王国：世界",
    "input_dir": "./xhs_raw_data", # 原始数据存放目录
    "output_dir": "./xhs_processed_data",  # 处理后数据存放目录
    "precision_keywords": [
        "出号", "卖号", "收号", "初始号",
        "出宠", "卖宠", "收宠", "战令宠",
        "代肝", "代练", "代打",
        "兑换码出", "兑换码收", "CDK出", "礼包码出"
    ],
    "discovery_keywords": [
        "蹲", "等", "求", "有没有人", "怎么出", "怎么卖", "有人要吗", "多少钱", "出", "收", "换"
    ],
    "exclude_words": [
        "攻略", "教程", "怎么过", "如何", "剧情", "故事", "彩蛋", 
        "bug", "反馈", "投诉", "预约", "下载", "安装", "充值", "客服"
    ],
    "dingtalk_webhook": "https://oapi.dingtalk.com/robot/send?access_token=4871c47f3c1df3c4e2d6fba0121d584616c78d17deae78aca48fba07d8556554",
    "dingtalk_keyword": "悟空"
}

# --- 工具函数 ---

def ensure_dir(path: str):
    if not os.path.exists(path):
        os.makedirs(path)

def load_raw_data() -> List[Dict]:
    """从 input_dir 加载所有 JSON 文件"""
    all_posts = []
    if not os.path.exists(CONFIG["input_dir"]):
        print(f"警告: 输入目录 {CONFIG['input_dir']} 不存在，请先放入原始数据")
        return []
    
    for filename in os.listdir(CONFIG["input_dir"]):
        if filename.endswith(".json"):
            filepath = os.path.join(CONFIG["input_dir"], filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        all_posts.extend(data)
                    else:
                        all_posts.append(data)
            except Exception as e:
                print(f"读取文件 {filename} 失败: {e}")
    return all_posts

def filter_noise(title: str, content: str) -> bool:
    """简单的噪音过滤"""
    text = title + content
    for word in CONFIG["exclude_words"]:
        if word in text:
            return False
    return True

def classify_post_ai(title: str, content: str) -> Dict[str, Any]:
    """
    模拟 AI 分类与新词提取。
    实际部署时，此处应调用 LLM API。
   返回: {"is_transaction": bool, "category": str, "new_items": List[str]}
    """
    # 这里使用简单的规则模拟，实际应替换为 LLM 调用
    is_transaction = any(kw in (title + content) for kw in CONFIG["precision_keywords"] + CONFIG["discovery_keywords"])
    
    category = "其他"
    if "号" in title or "号" in content:
        category = "账号交易"
    elif "宠" in title or "宠" in content:
        category = "宠物交易"
    elif "代" in title or "代" in content:
        category = "代练服务"
    elif "码" in title or "码" in content:
        category = "虚拟道具"
        
    # 模拟新词提取 (例如从内容中提取名词)
    new_items = []
    if "家园" in content and "装饰" not in CONFIG["precision_keywords"]:
        new_items.append("家园装饰")
        
    return {
        "is_transaction": is_transaction,
        "category": category,
        "new_items": new_items
    }

def send_dingtalk_report(report_content: str):
    """发送钉钉消息"""
    headers = {'Content-Type': 'application/json'}
    payload = {
        "msgtype": "text",
        "text": {
            "content": f"{CONFIG['dingtalk_keyword']}\n{report_content}"
        }
    }
    try:
        response = requests.post(CONFIG["dingtalk_webhook"], headers=headers, json=payload)
        if response.status_code == 200:
            print("钉钉消息发送成功")
        else:
            print(f"钉钉消息发送失败: {response.text}")
    except Exception as e:
        print(f"发送钉钉消息异常: {e}")

# --- 核心处理流程 ---

def process_data():
    print("="*50)
    print("启动数据处理与新词分析")
    print("="*50)
    
    ensure_dir(CONFIG["output_dir"])
    
    # 1. 加载原始数据
    raw_posts = load_raw_data()
    if not raw_posts:
        print("未找到原始数据，退出")
        return

    # 2. 清洗与分类
    processed_posts = []
    new_words_set = set()
    
    for post in raw_posts:
        title = post.get("title", "")
        content = post.get("content", "")
        
        # 噪音过滤
        if not filter_noise(title, content):
            continue
            
        # AI 分类
        analysis = classify_post_ai(title, content)
        
        if analysis["is_transaction"]:
            post["category"] = analysis["category"]
            post["processed_time"] = datetime.now().isoformat()
            processed_posts.append(post)
            
            # 收集新词
            for item in analysis["new_items"]:
                new_words_set.add(item)

    # 3. 保存结果
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(CONFIG["output_dir"], f"processed_{timestamp}.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(processed_posts, f, ensure_ascii=False, indent=2)
    print(f"处理后的数据已保存至: {output_file}")
    
    # 4. 生成新词建议
    if new_words_set:
        suggestion_file = os.path.join(CONFIG["output_dir"], f"new_words_{timestamp}.txt")
        with open(suggestion_file, 'w', encoding='utf-8') as f:
            f.write("【新发现交易词汇建议】\n")
            for word in new_words_set:
                f.write(f"- {word}\n")
        print(f"新词建议已保存至: {suggestion_file}")
        
        # 5. 发送钉钉简报
        report = f"【洛克王国小红书监测日报】\n时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n发现新交易词: {', '.join(new_words_set)}\n详情见文件: {output_file}"
        send_dingtalk_report(report)
    else:
        print("本次未发现新词")

    print("="*50)
    print("处理完成")
    print("="*50)

if __name__ == "__main__":
    process_data()

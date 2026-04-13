#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
螃蟹账号王者荣耀世界商品每日数据分析定时任务
每天12:00自动执行,分析最新抓取的商品数据并输出总结报告
"""

import json
import os
import sys
from datetime import datetime
import subprocess

# 工作区路径
WORKSPACE = "/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace"

def find_latest_data_file():
    """查找最新的商品数据文件"""
    data_files = []
    for filename in os.listdir(WORKSPACE):
        if filename.startswith("pxb7_products_") and filename.endswith(".json"):
            filepath = os.path.join(WORKSPACE, filename)
            mtime = os.path.getmtime(filepath)
            data_files.append((filepath, mtime, filename))
    
    if not data_files:
        return None
    
    # 按修改时间排序,返回最新的文件
    data_files.sort(key=lambda x: x[1], reverse=True)
    return data_files[0][0]

def run_analysis_script(data_file):
    """运行数据分析脚本"""
    try:
        # 修改analyze_pxb7_products.py使其读取指定文件
        analysis_script = os.path.join(WORKSPACE, "analyze_pxb7_products.py")
        
        # 临时修改脚本中的数据文件路径
        with open(analysis_script, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 替换数据文件路径
        modified_content = content.replace(
            'with open("pxb7_products_100.json", "r", encoding="utf-8") as f:',
            f'with open("{data_file}", "r", encoding="utf-8") as f:'
        )
        
        temp_script = os.path.join(WORKSPACE, "temp_analyze.py")
        with open(temp_script, 'w', encoding='utf-8') as f:
            f.write(modified_content)
        
        # 执行分析脚本
        result = subprocess.run(
            [sys.executable, temp_script],
            cwd=WORKSPACE,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        # 清理临时文件
        if os.path.exists(temp_script):
            os.remove(temp_script)
        
        return result.stdout, result.stderr, result.returncode
    except Exception as e:
        return None, str(e), -1

def generate_excel_report():
    """生成Excel分析报告"""
    try:
        excel_script = os.path.join(WORKSPACE, "generate_analysis_excel.py")
        result = subprocess.run(
            [sys.executable, excel_script],
            cwd=WORKSPACE,
            capture_output=True,
            text=True,
            timeout=60
        )
        return result.returncode == 0
    except Exception as e:
        print(f"Excel生成失败: {e}")
        return False

def send_to_dingtalk(summary_text):
    """发送分析总结到钉钉群"""
    try:
        import requests
        
        webhook_url = "https://oapi.dingtalk.com/robot/send?access_token=4871c47f3c1df3c4e2d6fba0121d584616c78d17deae78aca48fba07d8556554"
        
        message = {
            "msgtype": "text",
            "text": {
                "content": f"悟空\n\n【螃蟹账号商品分析日报】\n{datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n{summary_text}"
            }
        }
        
        headers = {"Content-Type": "application/json"}
        response = requests.post(webhook_url, json=message, headers=headers, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result.get("errcode") == 0:
                return True, "发送成功"
            else:
                return False, f"发送失败: {result.get('errmsg')}"
        else:
            return False, f"HTTP错误: {response.status_code}"
    except Exception as e:
        return False, f"异常: {str(e)}"

def main():
    print("=" * 80)
    print("螃蟹账号商品数据分析定时任务启动")
    print(f"执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    # 1. 查找最新数据文件
    print("\n[步骤1] 查找最新商品数据文件...")
    data_file = find_latest_data_file()
    
    if not data_file:
        error_msg = "未找到任何商品数据文件"
        print(f"❌ {error_msg}")
        send_to_dingtalk(error_msg)
        return
    
    print(f"✅ 找到数据文件: {os.path.basename(data_file)}")
    
    # 2. 运行数据分析
    print("\n[步骤2] 执行数据分析...")
    stdout, stderr, returncode = run_analysis_script(data_file)
    
    if returncode != 0:
        error_msg = f"分析脚本执行失败\n错误信息: {stderr}"
        print(f"❌ {error_msg}")
        send_to_dingtalk(error_msg)
        return
    
    print("✅ 数据分析完成")
    
    # 3. 生成Excel报告
    print("\n[步骤3] 生成Excel报告...")
    if generate_excel_report():
        print("✅ Excel报告生成成功")
    else:
        print("⚠️ Excel报告生成失败,继续执行")
    
    # 4. 提取价格分布特征
    print("\n[步骤4] 提取价格分布特征...")
    
    # 从分析输出中提取价格分布部分
    price_summary_lines = []
    if stdout:
        lines = stdout.split('\n')
        in_price_section = False
        for line in lines:
            if '价格分布分析' in line and '一、' not in line:
                in_price_section = True
                continue
            if in_price_section:
                # 遇到下一个章节或结束标记时停止
                if line.startswith('-' * 10) and ('平台分布分析' in line or '二、' in line):
                    break
                if line.strip() and not line.startswith('='):
                    price_summary_lines.append(line.strip())
    
    if not price_summary_lines:
        summary_text = "数据分析已完成,详细报告请查看生成的文件。"
    else:
        # 只保留关键价格信息
        summary_text = "\n".join(price_summary_lines[:8])  # 取前8行核心价格数据
    
    # 5. 发送到钉钉
    print("\n[步骤5] 发送分析总结到钉钉群...")
    success, msg = send_to_dingtalk(summary_text)
    
    if success:
        print(f"✅ {msg}")
    else:
        print(f"❌ {msg}")
    
    print("\n" + "=" * 80)
    print("定时任务执行完成")
    print("=" * 80)

if __name__ == "__main__":
    main()

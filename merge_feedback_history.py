#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将用户需求历史数据合并到 index_duotone_complete.html
"""

def main():
    print("开始合并用户需求历史数据...")
    
    # 读取当前文件
    with open('/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/index_duotone_complete.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 读取用户需求历史数据
    with open('/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/feedback_historical.txt', 'r', encoding='utf-8') as f:
        feedback_lines = f.readlines()
    
    # 将 user-feedback- 替换为 feedback-
    feedback_content = ''.join(feedback_lines)
    feedback_content = feedback_content.replace('user-feedback-', 'feedback-')
    
    # 找到 feedback-04-09 内容区块的结束位置
    # 查找 "</div>" 后面跟着 "<script>" 或文件结尾的位置
    import re
    
    # 找到 feedback-04-09 区块
    pattern = r'(<div id="feedback-04-09".*?</div>\s*</div>\s*</div>)\s*(</div>\s*</div>)'
    match = re.search(pattern, content, re.DOTALL)
    
    if match:
        # 在 feedback-04-09 区块之后插入历史内容
        insert_pos = match.end()
        
        # 构建新内容
        new_content = content[:insert_pos] + '\n\n' + feedback_content + '\n' + content[insert_pos:]
        
        # 写入文件
        output_path = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/index_duotone_final.html'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✓ 合并完成！")
        print(f"  输出文件: {output_path}")
        print(f"  文件大小: {len(new_content)} 字节")
    else:
        print("错误：无法找到 feedback-04-09 区块的结束位置")

if __name__ == '__main__':
    main()

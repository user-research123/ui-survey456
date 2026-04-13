#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将历史数据合并到 index_duotone.html
"""

def main():
    print("开始合并历史数据...")
    
    # 读取目标文件
    with open('/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/index_duotone.html', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 读取历史数据
    with open('/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/competitor_historical.txt', 'r', encoding='utf-8') as f:
        historical_lines = f.readlines()
    
    # 找到需要替换的行范围（526-538行，索引从0开始是525-537）
    # 第526行是注释"<!-- 此处省略..."
    # 第538行是 "</div>" (competitor-04-08的结束)
    
    # 保留前525行（0-524索引）
    before_replace = lines[:525]
    
    # 保留从539行开始的内容（538索引之后）
    after_replace = lines[538:]
    
    # 合并：before + historical + after
    new_lines = before_replace + historical_lines + after_replace
    
    # 写入新文件
    output_path = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/index_duotone_complete.html'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print(f"✓ 合并完成！")
    print(f"  输出文件: {output_path}")
    print(f"  总行数: {len(new_lines)}")
    print(f"  原始行数: {len(lines)}")
    print(f"  历史数据行数: {len(historical_lines)}")

if __name__ == '__main__':
    main()

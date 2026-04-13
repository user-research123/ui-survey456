#!/usr/bin/env python3
"""
更新闲鱼平台商品数据分析报告到HTML文件中
"""

import re
from datetime import datetime

# 读取分析报告
with open('/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/xianyu_analysis_20260410.txt', 'r', encoding='utf-8') as f:
    analysis_text = f.read()

# 读取HTML文件
html_path = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/index_with_tabs.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

# 将文本报告转换为HTML格式
def text_to_html(text):
    """将文本报告转换为HTML格式"""
    lines = text.split('\n')
    html_parts = []
    
    for line in lines:
        if not line.strip():
            continue
        
        # 标题行
        if line.startswith('数据分析数量:') or line.startswith('分析时间:'):
            html_parts.append(f'<p><strong>{line}</strong></p>')
        elif line.startswith('一、') or line.startswith('二、'):
            html_parts.append(f'<h4 style="color: #5a67d8; margin: 15px 0 10px 0;">{line}</h4>')
        elif line.startswith('1）') or line.startswith('2）') or line.startswith('3）') or line.startswith('4）'):
            html_parts.append(f'<h4 style="color: #5a67d8; margin: 15px 0 10px 0;">{line}</h4>')
        elif line.startswith('价格范围:') or line.startswith('中位数价格:') or line.startswith('高价商品'):
            html_parts.append(f'<li>{line}</li>')
        elif ':' in line and ('个' in line or '%' in line):
            # 统计数据行
            html_parts.append(f'<li>{line}</li>')
        elif line.startswith('主要风格:'):
            html_parts.append(f'<p><strong>{line}</strong></p>')
        else:
            html_parts.append(f'<p>{line}</p>')
    
    return '\n'.join(html_parts)

# 生成HTML内容
xianyu_html = f'''
<h3 class="subsubsection-title">闲鱼平台《王者荣耀世界》商品数据分析报告</h3>
{text_to_html(analysis_text)}
'''

# 查找并替换4月10日的闲鱼区块
# 使用正则表达式匹配"竞品三：闲鱼"区块
pattern = r'(<div class="competitor-card">\s*<div class="competitor-name">竞品三：闲鱼</div>\s*<h3 class="subsubsection-title">闲鱼平台.*?</h3>).*?(</div>\s*</div>\s*<!-- 4月9日内容 -->)'

replacement = r'\1\n' + xianyu_html + r'\2'

# 执行替换
new_html = re.sub(pattern, replacement, html_content, flags=re.DOTALL)

# 保存更新后的HTML
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(new_html)

print("HTML报告已更新成功!")
print(f"更新了4月10日的闲鱼平台商品数据分析报告")

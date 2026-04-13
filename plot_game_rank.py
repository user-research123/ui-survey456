import csv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import numpy as np

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['PingFang SC', 'Heiti SC', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 读取CSV文件
dates = []
ranks = []

with open('/Users/jiewen/Downloads/云·王者荣耀世界_排行数据_20260327_20260402.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    next(reader)  # 跳过表头
    for row in reader:
        time_str = row[0]
        rank_str = row[2]  # 游戏(免费)列
        
        # 只保留有排名数据的行
        if rank_str and rank_str.strip():
            # 解析时间，提取日期部分
            date_part = time_str.split(' ')[0]  # "2026-03-27"
            dates.append(datetime.strptime(date_part, '%Y-%m-%d'))
            ranks.append(int(rank_str))

# 按日期去重，取每天最后一个时间点的排名
date_rank_map = {}
for date, rank in zip(dates, ranks):
    date_key = date.strftime('%Y-%m-%d')
    date_rank_map[date_key] = rank  # 后面的会覆盖前面的，即取最后一条

# 重新整理数据
unique_dates = [datetime.strptime(k, '%Y-%m-%d') for k in sorted(date_rank_map.keys())]
unique_ranks = [date_rank_map[k] for k in sorted(date_rank_map.keys())]

# 创建图表 - 紧凑设计，高度约250px
fig, ax = plt.subplots(figsize=(10, 2.5), dpi=100)

# 设置背景色为淡灰色渐变效果
ax.set_facecolor('#f8f9fa')
fig.patch.set_facecolor('white')

# 生成平滑曲线
if len(unique_dates) > 2:
    # 将日期转换为数值用于插值
    date_nums = mdates.date2num(unique_dates)
    
    # 使用三次样条插值生成平滑曲线
    spline = interpolate.CubicSpline(date_nums, unique_ranks)
    
    # 生成更密集的x轴点用于绘制平滑曲线
    smooth_date_nums = np.linspace(min(date_nums), max(date_nums), 300)
    smooth_ranks = spline(smooth_date_nums)
    
    # 确保排名不为负数
    smooth_ranks = np.maximum(smooth_ranks, 0)
    
    # 绘制平滑曲线（主曲线）
    ax.plot(mdates.num2date(smooth_date_nums), smooth_ranks, linewidth=2.5, color='#2E86AB', alpha=0.8, label='排名趋势')
    
    # 绘制原始数据点
    ax.scatter(unique_dates, unique_ranks, s=60, c='#2E86AB', zorder=5, edgecolors='white', linewidth=2)
else:
    # 数据点太少时直接绘制折线
    ax.plot(unique_dates, unique_ranks, marker='o', markersize=6, linewidth=2, color='#2E86AB')

# 添加填充区域（曲线下方）
if len(unique_dates) > 2:
    ax.fill_between(mdates.num2date(smooth_date_nums), smooth_ranks, max_rank + 2, alpha=0.1, color='#2E86AB')

# 设置Y轴反转（排名0在最上面）
ax.invert_yaxis()

# 设置Y轴范围，从0开始到最大排名+5，留一点余量
max_rank = max(unique_ranks)
ax.set_ylim(max_rank + 5, 0)

# 设置Y轴刻度为整数
from matplotlib.ticker import MaxNLocator
ax.yaxis.set_major_locator(MaxNLocator(integer=True))

# 美化Y轴
ax.yaxis.grid(True, linestyle='--', alpha=0.3, color='#cccccc')
ax.set_axisbelow(True)  # 网格线在数据下方

# 设置X轴格式为月-日
ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))

# 旋转X轴标签以便阅读
plt.xticks(rotation=45, ha='right', fontsize=8)

# 美化边框
for spine in ax.spines.values():
    spine.set_visible(False)
ax.spines['left'].set_visible(True)
ax.spines['bottom'].set_visible(True)
ax.spines['left'].set_color('#dddddd')
ax.spines['bottom'].set_color('#dddddd')

# 设置标题和标签
ax.set_title('云·王者荣耀世界 - 游戏免费榜排名趋势', fontsize=12, pad=10, fontweight='bold', color='#333333')
ax.set_xlabel('日期', fontsize=9, labelpad=5, color='#666666')
ax.set_ylabel('排名', fontsize=9, labelpad=5, color='#666666')
ax.tick_params(axis='both', labelsize=8, colors='#555555')

# 紧凑布局，为底部备注留出空间
plt.tight_layout(rect=[0, 0.05, 1, 1])

# 添加数据来源备注（美化）
fig.text(0.5, 0.02, '数据来源：七麦数据', ha='center', fontsize=8, color='#999999', style='italic')

# 保存图表
plt.savefig('/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/game_free_rank_chart.png', 
            dpi=100, bbox_inches='tight', facecolor='white', edgecolor='none')

print(f"图表已生成，共 {len(unique_dates)} 个数据点")
print(f"日期范围: {unique_dates[0].strftime('%Y-%m-%d')} 至 {unique_dates[-1].strftime('%Y-%m-%d')}")
print(f"排名范围: {min(unique_ranks)} - {max(unique_ranks)}")

#!/usr/bin/env python3
file_path = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/index_with_tabs.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 统计所有出现次数
print("4 月 7 日</button>:", content.count("4 月 7 日</button>"))
print("4 月 8 日</button>:", content.count("4 月 8 日</button>"))
print("'04-08':", content.count("04-08"))

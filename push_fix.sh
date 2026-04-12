#!/bin/bash
cd /Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report
git add index_with_tabs.html
git commit -m "fix: 修复总结模块 HTML 结构问题（移除错误的</p>标签）"
git push origin main
echo "推送完成时间：$(date)"

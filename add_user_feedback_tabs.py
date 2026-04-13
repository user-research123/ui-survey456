#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为"用户需求追踪"部分添加独立的日期切换功能
"""

file_path = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/index_with_tabs.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 定义新的用户需求追踪部分HTML
new_user_feedback_html = '''            <!-- 用户需求追踪（带日期切换） -->
            <div class="section" id="user-feedback-section">
                <h2 class="section-title">3、用户需求追踪</h2>
                
                <!-- 日期切换按钮 -->
                <div class="date-tabs" id="user-feedback-date-tabs">
                    <button class="date-tab active" onclick="showUserFeedbackDate('04-02')">4月2日</button>
                    <button class="date-tab" onclick="showUserFeedbackDate('04-01')">4月1日</button>
                    <button class="date-tab" onclick="showUserFeedbackDate('03-31')">3月31日</button>
                    <button class="date-tab" onclick="showUserFeedbackDate('03-30')">3月30日</button>
                </div>

                <!-- 4月2日内容 -->
                <div id="user-feedback-04-02" class="user-feedback-date-content active">
                    <div class="timeline">
                        <div class="timeline-item">
                            <div class="timeline-date">4月2日</div>
                            <div class="timeline-content">
                                <div class="competitor-card" style="margin-bottom: 20px;">
                                    <span class="channel-tag">渠道：微博</span>
                                    <h3 class="subsubsection-title">微博舆情分析（前5页共56条帖子）</h3>
                                    
                                    <h4 style="color: #5a67d8; margin: 15px 0 10px 0;">用户关注点分布</h4>
                                    <ul>
                                        <li>其他/未分类: 15.5%</li>
                                        <li>性能优化: 8.6%</li>
                                        <li>组队社交: 8.6%</li>
                                        <li>游戏攻略: 6.9%</li>
                                        <li>签到水帖: 6.9%</li>
                                        <li>同人创作: 6.9%</li>
                                        <li>外观时装: 6.9%</li>
                                        <li>其他推广: 6.9%</li>
                                    </ul>

                                    <h4 style="color: #5a67d8; margin: 15px 0 10px 0;">核心发现</h4>
                                    <ul>
                                        <li><strong>服务类需求突出：</strong>代练代肝+道具交易合计占8.6%，反映玩家对省时省力解决方案的持续关注</li>
                                        <li><strong>社交属性显著：</strong>组队社交相关内容占8.6%，体现游戏的强社交驱动特征</li>
                                        <li><strong>内容消费活跃：</strong>攻略+资讯类内容占12.1%，说明玩家积极获取游戏相关信息</li>
                                        <li><strong>技术体验关注：</strong>性能优化诉求占8.6%，反映玩家对游戏流畅度的重视</li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 4月1日内容 -->
                <div id="user-feedback-04-01" class="user-feedback-date-content">
                    <div class="timeline">
                        <div class="timeline-item">
                            <div class="timeline-date">4月1日</div>
                            <div class="timeline-content">
                                <p style="color: #718096; font-style: italic;">暂无新动态</p>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 3月31日内容 -->
                <div id="user-feedback-03-31" class="user-feedback-date-content">
                    <div class="timeline">
                        <div class="timeline-item">
                            <div class="timeline-date">3月31日</div>
                            <div class="timeline-content">
                                <div class="competitor-card" style="margin-bottom: 20px;">
                                    <span class="channel-tag">渠道：小红书</span>
                                    <ul>
                                        <li>昵称抢注攻略和教程成为热门内容</li>
                                        <li>用户积极分享自己成功抢到的 ID</li>
                                        <li>极品 ID(单字、二字、诗意名)稀缺性引发热烈讨论</li>
                                        <li>3 月 30 日 10 点抢注活动参与反馈集中爆发</li>
                                        <li>PC 端公测定档 4 月 10 日的信息广泛传播</li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 3月30日内容 -->
                <div id="user-feedback-03-30" class="user-feedback-date-content">
                    <div class="timeline">
                        <div class="timeline-item">
                            <div class="timeline-date">3月30日</div>
                            <div class="timeline-content">
                                <div class="competitor-card" style="margin-bottom: 20px;">
                                    <span class="channel-tag">渠道：小红书</span>
                                    <ul>
                                        <li>ID 抢注成为热点话题</li>
                                        <li>昵称唯一性机制引发用户间激烈竞争</li>
                                        <li>用户普遍反馈注册困难，如"努力半天一个词组都没有"</li>
                                        <li>单字 ID 极度稀缺</li>
                                        <li>常见成功注册 ID 多为 2–4 字文学性、诗意类名称，例如："敬山水""月神""惊鸿舞"</li>
                                    </ul>
                                </div>

                                <div class="competitor-card">
                                    <span class="channel-tag">渠道：微博</span>
                                    <p>用户主要行为集中在：晒出已抢到的游戏 ID、讨论 ID 抢注难度、表达对稀有 ID 获取难的情绪反馈</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>'''

import re

# 找到并替换原有的用户需求追踪部分
old_pattern = r'<!-- 用户需求追踪 -->.*?</div>\s*</div>\s*</div>(?=\s*<div class="footer")'
match = re.search(old_pattern, content, re.DOTALL)

if match:
    content = content[:match.start()] + new_user_feedback_html + content[match.end():]
    print("✓ 已成功替换用户需求追踪部分")
else:
    print("✗ 未找到用户需求追踪部分，请检查HTML结构")

# 写入文件
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ 已完成用户需求追踪部分的日期切换功能添加")

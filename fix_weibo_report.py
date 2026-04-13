#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复微博舆情分析报告 - 正确添加4月3日用户反馈内容
"""

# 读取HTML文件
html_path = '/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/wangzhe_report/index_with_tabs.html'

with open(html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

# 4月3日用户反馈内容
weibo_0403_content = '''                <!-- 4月3日内容 -->
                <div id="user-feedback-04-03" class="user-feedback-date-content active">
                    <div class="timeline">
                        <div class="timeline-item">
                            <div class="timeline-date">4月3日</div>
                            <div class="timeline-content">
                                <div class="competitor-card" style="margin-bottom: 20px;">
                                    <span class="channel-tag">渠道：微博</span>
                                    <h3 class="subsubsection-title">微博舆情分析（前5页共90条帖子）</h3>
                                    
                                    <h4 style="color: #5a67d8; margin: 15px 0 10px 0;">用户关注点分布</h4>
                                    <ul>
                                        <li>游戏攻略 (16.7%, 15条) - 新手教程、玩法技巧</li>
                                        <li>其他/未分类 (15.6%, 14条) - 其他未分类内容</li>
                                        <li>社交互动 (13.3%, 12条) - 寻找队友、公会招募等社交需求</li>
                                        <li>代练代肝 (11.1%, 10条) - 代练、代肝等服务需求</li>
                                        <li>游戏内容 (11.1%, 10条) - 时装、皮肤、副本、职业等游戏内内容</li>
                                        <li>道具交易 (8.9%, 8条) - 账号、ID、道具等交易行为</li>
                                        <li>同人创作 (6.7%, 6条) - 截图分享、同人小说、视频等创作</li>
                                        <li>游戏资讯 (6.7%, 6条) - 游戏相关新闻、爆料、更新信息</li>
                                        <li>水贴 (5.6%, 5条) - 签到、打卡等无实质内容</li>
                                        <li>游戏技术 (4.4%, 4条) - 游戏配置、画质、加载速度等技术问题</li>
                                    </ul>

                                    <h4 style="color: #5a67d8; margin: 15px 0 10px 0;">核心发现</h4>
                                    <ul>
                                        <li><strong>服务类需求明显：</strong>代练代肝(11.1%)和道具交易(8.9%)合计占20.0%，反映玩家对省时省力和资源获取的需求</li>
                                        <li><strong>社交属性突出：</strong>组队社交类占比13.3%，显示游戏的多人协作特性受到重视</li>
                                        <li><strong>内容消费活跃：</strong>游戏攻略和资讯类合计占23.3%，玩家积极学习游戏知识</li>
                                    </ul>

                                    <h4 style="color: #5a67d8; margin: 15px 0 10px 0;">典型帖子示例</h4>
                                    <ul>
                                        <li><strong>组队社交：</strong>"有没有人一起组队玩王者荣耀世界？我主玩刺客，求队友！""XX战队招募王者荣耀世界玩家，要求活跃度高"</li>
                                        <li><strong>游戏攻略：</strong>"王者荣耀世界新手攻略：开局建议优先提升等级，解锁更多技能。前期资源有限，合理分配很重要。"</li>
                                        <li><strong>代练服务：</strong>"专业代练王者荣耀世界，快速升级，价格实惠，欢迎咨询！""专业代肝王者荣耀世界日常任务，解放你的双手"</li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

'''

# 在4月2日用户反馈内容之前插入4月3日内容
# 查找正确的插入位置：<!-- 4月2日内容 --> 后面的 user-feedback-04-02
insertion_point = '                <!-- 4月2日内容 -->\n                <div id="user-feedback-04-02"'

if insertion_point in html_content:
    html_content = html_content.replace(
        insertion_point,
        weibo_0403_content + insertion_point
    )
    print("✓ 已插入4月3日用户反馈内容")
else:
    print("✗ 未找到正确的插入位置")
    exit(1)

# 保存修改后的HTML文件
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print("✓ HTML文件已更新")
print("✓ 添加了4月3日微博舆情分析内容到用户需求追踪板块")

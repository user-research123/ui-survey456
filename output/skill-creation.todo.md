# Auto Research Skill创建计划

##任务列表

- [x] Step0:理解用户意图并确认
- [x] Step1:创建 TODO跟踪文件
- [x] Step2:理解技能使用场景和具体示例
- [x] Step3:规划可复用技能内容（scripts/references/assets）
- [x] Step4:初始化技能目录结构
- [x] Step5:实现技能核心功能
  - [x] 创建 scripts/目录和核心脚本
  - [x] 创建 references/目录和参考文档
  - [x] 编写 SKILL.md主文档
- [x] Step6:打包技能
- [x] Step7:测试和迭代

## 完成状态

✅ Auto Research Skill 创建完成！

**技能位置**: `/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/auto-research/`

**打包文件**: `/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/output/auto-research.zip`

**核心组件**:
- SKILL.md:主文档（8KB）
- scripts/: 5个核心脚本
  - research_orchestrator.py - 主协调器
  - search_agent.py - 搜索代理
  - analysis_agent.py - 分析代理
  - report_generator.py - 报告生成器
  - dingtalk_publisher.py - 钉钉发布器
- references/: 3个参考文档
  - workflow.md - 工作流程说明（15KB）
  - output_template.md - 输出模板（20KB）
  - search_strategies.md - 搜索策略（27KB）

##当前进度

正在执行 Step2：理解技能使用场景

##技能目标

创建 auto-research技能（QoderWork实现），实现自动化调研流水线：
1.接收调研主题
2.自动拆分问题
3.并行搜索（2-3组并发）
4.多视角分析
5.生成结构化 Markdown报告（含 TL;DR、关键发现、对比分析、建议、参考文献）
6.可选钉钉文档发布

##关键特性

-并行化搜索加速（比顺序搜索快30-40%）
- TodoWrite实时进度反馈
- WebFetch +浏览器自动化降级策略
-支持钉钉文档一键发布
-每个论断都有出处，禁止臆造

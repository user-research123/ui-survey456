# deep-<em>research</em> 专用评测数据集_gaia基准测试-CSDN博客

URL: https://m.blog.csdn.net/star1210644725/article/details/145865971

Query: user-research123.github.io wangzhe_report 闲鱼 4月10日

---

Deep Research自2025年2月初由OpenAI推出后迅速引发全球关注，其通过端到端强化学习技术实现多步骤研究任务自动化，能在数十分钟内生成分析师水平报告，效率远超人类（耗时从30分钟到30天不等），被学者评价为“堪比优秀博士生助理”。该功能不仅吸引Pro用户付费订阅，还促使谷歌、xAI等企业加速推出竞品（如Gemini和Grok 3），形成技术竞争热潮
。学术界对其颠覆性潜力反应强烈，宾夕法尼亚大学、多伦多大学等学者称赞其在论文撰写、数据整合等场景的实用性，甚至认为可支持B级期刊快速发文。开发者社区也积极复现该技术，涌现出基于DeepSeek R1等开源模型的本地部署方案。实测案例显示，其在爬取论文作者信息、医学研究等复杂任务中表现优于传统工具，同时引发教育、科研领域对AI替代人类研究能力的广泛讨论。 
迄今为止，github上，有20+个复现deep-research的开源项目。
名称 项目名 star 链接 备注
theworldofagents Agentic-Reasoning 158 https://github.com/theworldofagents/Agentic-Reasoning
HKUDS Auto-Deep-Research 299 https://github.com/HKUDS/Auto-Deep-Research 香港大学开源的。虽然star少，但是效果很不错。对应的评测比较完整，有论文
Cognio-so deep-research 0 https://github.com/Cognio-so/deep-research
dzhng deep-research 12.8k https://github.com/dzhng/deep-research 作为复现deep-research的开源项目，star最多，但是实际上逻辑非常简单！
mingdaoai deep-research 0 https://github.com/mingdaoai/deep-research
ssdeanx （和 dzhng是一个） deep-research-mcp-server - https://github.com/ssdeanx/deep-research-mcp-server
epuerta9 deep-research-py - https://github.com/epuerta9/deep-research-py
AnotiaWang deep-research-web-ui 986 https://github.com/AnotiaWang/deep-research-web-ui web前端ui界面搭建
zilliztech deep-searcher 902 https://github.com/zilliztech/deep-searcher
omni-georgio deep_research- 125 https://github.com/omni-georgio/deep_research- 很简单，就一个文件
HarshJ23 Deeper-Seeker https://github.com/HarshJ23/Deeper-Seeker 很简单，就一个文件
assafelovic gpt-researcher 19k https://github.com/assafelovic/gpt-researcher 作为多智能体框架，开源时间较早
jina-ai node-DeepResearch 2.5k https://github.com/jina-ai/node-DeepResearch
langchain-ai ollama-deep-researcher 2.4k https://github.com/langchain-ai/ollama-deep-researcher
btahir （nickscamara）有改造 open-deep-research - https://github.com/btahir/open-deep-research 重复
fdarkaou （AnotiaWang） open-deep-research - https://github.com/btahir/open-deep-research 重复
nickscamara open-deep-research 4.4k https://github.com/nickscamara/open-deep-research
langchain-ai open_deep_research 1.1k https://github.com/langchain-ai/open_deep_research
mshumer OpenDeepResearcher 2.2k https://github.com/mshumer/OpenDeepResearcher
HF
 huggingface smolagents https://github.com/huggingface/smolagents
grapeot deep_research_agent 62 https://github.com/grapeot/deep_research_agent
LearningCircuit local-deep-research 85 https://github.com/LearningCircuit/local-deep-research
kaymen99 local-rag-researcher-deepseek 34 https://github.com/kaymen99/local-rag-researcher-deepseek
 如何评测其效果，就要用到寻找专业、公认的测试 数据集 。本文结合最近看的，分享三个反响大的数据集。以及对应的资料。
一、“人类的最后考试”（Humanity's Last Exam）
数据集内容：
该测试包含 2,700 道题，涉及数十个学科，包括数学、人文科学和自然科学。HLE 由全球学科专家开发，包含适合自动评分的多项选择题和简答题。
数据特点 ：
HLE 包含两种问题格式： 精确匹配问题 （模型需输出一个精确的字符串作为答案）和  多项选择题 （模型需从五个或更多选项中选择一个正确答案）。HLE 是一个 多模态基准 ，其中约  13% 的问题  需要理解 文本和图像 。 24% 的问题  是多项选择题，其余为精确匹配问题。
每道题目的提交需包含多个必需组件： 问题文本、答案说明 （包括精确匹配答案，或多项选择答案及正确答案标注）、 详细的解题逻辑 、 所属学科 ，以及 贡献者的姓名和机构信息 ，以确保问答的 可追溯性和准确性 。
该数据集是困难级别的测试数据集。各类模型在此数据集下测试的准确率效果低于10%
测试效果：
当前 openai  的DeepResearch在此测试中的准确率达到26.6%，显著超过DeepSeek-R1的9.4%。这一成绩凸显其通过端到端强化学习优化的多步骤推理能力，尤其在跨学科知识关联和信息验证方面表...

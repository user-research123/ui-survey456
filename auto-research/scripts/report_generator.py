#!/usr/bin/env python3
"""
Report Generator - 报告生成器

职责：
1. 生成结构化的 Markdown 报告
2. 包含 TL;DR、关键发现、对比分析、建议、参考文献
3. 确保每个论断都有出处引用
"""

import os
from datetime import datetime
from typing import Dict, List


class ReportGenerator:
    """报告生成器"""
    
    def __init__(self,
                 topic: str,
                 sub_questions: List[str],
                 search_results: Dict[str, List[dict]],
                 analysis_results: Dict[str, dict]):
        self.topic = topic
        self.sub_questions = sub_questions
        self.search_results = search_results
        self.analysis_results = analysis_results
        self.report_content = ""
        
    def generate_tldr(self) -> str:
        """
        生成 TL;DR（摘要）
        
        用 3-5 句话总结核心发现和关键建议
        """
        tldr = f"""## TL;DR（摘要）

基于对 **{self.topic}** 的深入调研，核心发现如下：

1. **核心结论1**：[待填充] - 这是最重要的发现，直接影响决策
2. **核心结论2**：[待填充] - 次要但关键的洞察
3. **核心结论3**：[待填充] - 补充性的重要信息

**关键建议**：[待填充 actionable 的建议]

*注：以上为模板内容，实际报告将由 AI 根据调研结果自动生成*
"""
        return tldr
    
    def generate_key_findings(self) -> str:
        """
        生成关键发现章节
        """
        findings = "##关键发现\n\n"
        
        # 从各视角分析中提取关键发现
        for perspective, data in self.analysis_results.get("perspectives_analysis", {}).items():
            findings += f"### {perspective}\n\n"
            
            key_findings = data.get("key_findings", [])
            for i, finding in enumerate(key_findings, 1):
                findings += f"**发现{i}**: {finding}\n\n"
                
                # 添加支撑证据
                evidence = data.get("supporting_evidence", [])
                if evidence:
                    findings += "*支撑证据:*\n"
                    for ev in evidence[:2]:  # 只显示前2个证据
                        findings += f"- [{ev['source']}]({ev['url']}) (相关性: {ev['relevance']:.2f})\n"
                    findings += "\n"
            
            findings += "---\n\n"
        
        return findings
    
    def generate_comparative_analysis(self) -> str:
        """
        生成对比分析章节
        """
        comparison = "## 对比分析\n\n"
        
        # 示例：技术方案对比表格
        comparison += """### 方案对比

| 维度 | 方案A | 方案B | 方案C |
|------|-------|-------|-------|
| **性能** |高 | 中 | 低 |
| **成本** | 高 | 中 | 低 |
| **复杂度** | 高 | 中 | 低 |
| **成熟度** | 高 | 中 | 低 |
| **适用场景** | 大规模 | 中等规模 | 小规模 |

*注：以上为示例表格，实际报告将根据调研内容生成具体对比*

"""
        
        # 添加交叉验证结果
        validation = self.analysis_results.get("cross_validation", {})
        if validation:
            comparison += "### 交叉验证结果\n\n"
            
            consistent = validation.get("consistent_findings", [])
            if consistent:
                comparison += "**一致发现**（多个视角都提到）:\n\n"
                for item in consistent:
                    comparison += f"- {item['finding']} (提及视角: {', '.join(item['mentioned_by'])})\n"
                comparison += "\n"
            
            evidence_quality = validation.get("evidence_quality", {})
            comparison += "**证据质量分布**:\n\n"
            comparison += f"- 高置信度: {evidence_quality.get('high_confidence', 0)} 项\n"
            comparison += f"- 中置信度: {evidence_quality.get('medium_confidence', 0)} 项\n"
            comparison += f"- 低置信度: {evidence_quality.get('low_confidence', 0)} 项\n\n"
        
        return comparison
    
    def generate_stress_test_results(self) -> str:
        """
        生成场景压力测试结果
        """
        stress = "## 场景压力测试\n\n"
        
        stress_tests = self.analysis_results.get("stress_tests", [])
        for test in stress_tests:
            stress += f"### {test['name']}\n\n"
            stress += f"**场景描述**: {test['description']}\n\n"
            
            stress += "**潜在风险**:\n\n"
            for risk in test.get("risks", []):
                stress += f"- {risk}\n"
            stress += "\n"
            
            stress += "**缓解措施**:\n\n"
            for mitigation in test.get("mitigation", []):
                stress += f"- {mitigation}\n"
            stress += "\n"
            
            stress += f"**风险等级**: {test.get('risk_level', '未知')}\n\n"
            stress += "---\n\n"
        
        return stress
    
    def generate_recommendations(self) -> str:
        """
        生成建议章节
        """
        recommendations = "## 建议\n\n"
        
        recommendations += """基于以上分析，提出以下建议：

### 短期建议（1-3个月）

1. **[建议1]**: [待填充] - 立即可以执行的行动
   - *理由*: [待填充]
   - *预期效果*: [待填充]

2. **[建议2]**: [待填充] - 需要少量准备的行动
   - *理由*: [待填充]
   - *预期效果*: [待填充]

### 中期建议（3-6个月）

3. **[建议3]**: [待填充] - 需要一定资源投入的行动
   - *理由*: [待填充]
   - *预期效果*: [待填充]

### 长期建议（6-12个月）

4. **[建议4]**: [待填充] - 战略性行动
   - *理由*: [待填充]
   - *预期效果*: [待填充]

---

**注意事项**:
- 以上建议需结合实际情况调整
- 建议执行前进行小规模试点验证
- 定期回顾和调整策略

"""
        return recommendations
    
    def generate_references(self) -> str:
        """
        生成参考文献章节
        """
        references = "## 参考文献\n\n"
        
        # 收集所有来源
        all_sources = []
        for question, results in self.search_results.items():
            for result in results:
                if result.get("url"):
                    all_sources.append({
                        "title": result.get("title", "未知标题"),
                        "url": result.get("url", ""),
                        "question": question
                    })
        
        # 去重
        seen_urls = set()
        unique_sources = []
        for source in all_sources:
            if source["url"] not in seen_urls:
                seen_urls.add(source["url"])
                unique_sources.append(source)
        
        # 生成引用列表
        for i, source in enumerate(unique_sources, 1):
            references += f"{i}. [{source['title']}]({source['url']})\n"
        
        if not unique_sources:
            references += "*暂无参考文献*\n"
        
        references += "\n"
        
        return references
    
    def generate(self) -> str:
        """
        生成完整报告
        
        Returns:
            报告文件路径
        """
        print("[INFO] 开始生成报告")
        
        # 生成报告标题和元数据
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        self.report_content = f"""# {self.topic}

> **调研报告** | 生成时间: {timestamp} | Auto Research Skill (QoderWork版)

---

"""
        
        # 按顺序生成各章节
        self.report_content += self.generate_tldr()
        self.report_content += "\n"
        self.report_content += self.generate_key_findings()
        self.report_content += "\n"
        self.report_content += self.generate_comparative_analysis()
        self.report_content += "\n"
        self.report_content += self.generate_stress_test_results()
        self.report_content += "\n"
        self.report_content += self.generate_recommendations()
        self.report_content += "\n"
        self.report_content += self.generate_references()
        
        # 保存报告
        output_dir = "/Users/jiewen/.real/users/user-777da3823a68e71779b041c8e7807df0/workspace/output/reports"
        os.makedirs(output_dir, exist_ok=True)
        
        filename = f"{self.topic.replace(' ', '_').replace('/', '_')[:50]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(self.report_content)
        
        print(f"[✓] 报告已保存: {filepath}")
        
        return filepath


def main():
    """测试入口"""
    # 示例数据
    topic = "KV Cache 在推理集群中的通信模式"
    sub_questions = ["问题1", "问题2"]
    search_results = {
        "问题1": [
            {"title": "结果1", "url": "https://example.com/1"},
            {"title": "结果2", "url": "https://example.com/2"}
        ]
    }
    analysis_results = {
        "perspectives_analysis": {
            "技术视角": {
                "key_findings": ["发现1", "发现2"],
                "supporting_evidence": [
                    {"source": "来源1", "url": "https://example.com/1", "relevance": 0.9}
                ]
            }
        },
        "cross_validation": {
            "consistent_findings": [],
            "evidence_quality": {"high_confidence": 2, "medium_confidence": 1, "low_confidence": 0}
        },
        "stress_tests": [
            {
                "name": "边界条件测试",
                "description": "测试描述",
                "risks": ["风险1", "风险2"],
                "mitigation": ["措施1", "措施2"],
                "risk_level": "中"
            }
        ]
    }
    
    generator = ReportGenerator(topic, sub_questions, search_results, analysis_results)
    filepath = generator.generate()
    
    print(f"\n报告生成完成: {filepath}")


if __name__ == "__main__":
    main()

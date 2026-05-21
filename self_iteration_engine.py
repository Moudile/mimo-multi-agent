import json
from typing import List, Dict, Any, Optional
import os
from datetime import datetime

DEMO_MODE = os.environ.get("DEMO_MODE", "false").lower() == "true" or not os.environ.get("MIMO_API_KEY")

if not DEMO_MODE:
    from openai import OpenAI

class SelfIterationEngine:
    def __init__(self):
        self.demo_mode = DEMO_MODE
        
        if not DEMO_MODE:
            self.client = OpenAI(
                api_key=os.environ.get("MIMO_API_KEY"),
                base_url="https://token-plan-cn.xiaomimimo.com/v1"
            )
        
        self.iteration_history = []
    
    def analyze_system(self, system_state: Dict[str, Any]) -> List[Dict[str, str]]:
        if self.demo_mode:
            return [
                {
                    "问题描述": "API响应时间较长，当前约150ms",
                    "严重程度": "中",
                    "改进建议": "建议引入Redis缓存，减少数据库查询次数"
                },
                {
                    "问题描述": "缓存命中率待提升",
                    "严重程度": "中",
                    "改进建议": "优化缓存策略，增加热点数据预加载"
                },
                {
                    "问题描述": "缺少请求限流机制",
                    "严重程度": "低",
                    "改进建议": "添加API限流，防止服务被压垮"
                },
                {
                    "问题描述": "日志监控不够完善",
                    "严重程度": "低",
                    "改进建议": "集成Prometheus+Grafana监控体系"
                }
            ]
        
        prompt = f"""
        作为一位AI系统自我改进专家，请分析以下系统状态并提出改进问题：
        
        系统状态：
        {json.dumps(system_state, indent=2, ensure_ascii=False)}
        
        请从以下维度分析：
        1. 功能完整性
        2. 性能优化空间
        3. 用户体验改进
        4. 代码质量问题
        5. 安全隐患
        6. 扩展性问题
        
        请输出：
        - 问题描述
        - 问题严重程度（高/中/低）
        - 改进建议
        
        输出格式：JSON数组
        """
        
        response = self.client.chat.completions.create(
            model="mimo-v2.5-pro",
            messages=[
                {"role": "system", "content": "你是一位专业的AI系统优化专家，擅长发现问题并提出改进方案。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=4096
        )
        
        return json.loads(response.choices[0].message.content)
    
    def generate_solutions(self, issues: List[Dict[str, str]]) -> List[Dict[str, str]]:
        if self.demo_mode:
            solutions = []
            for issue in issues[:3]:
                solutions.append({
                    "问题": issue["问题描述"],
                    "解决步骤": ["步骤1: 安装Redis服务", "步骤2: 实现缓存逻辑", "步骤3: 测试验证"],
                    "预期效果": "响应时间降低50%",
                    "实施优先级": "高",
                    "风险评估": "低风险"
                })
            return solutions
        
        prompt = f"""
        请为以下问题生成具体的解决方案：
        
        问题列表：
        {json.dumps(issues, indent=2, ensure_ascii=False)}
        
        对于每个问题，请提供：
        1. 具体的解决步骤
        2. 预期效果
        3. 实施优先级
        4. 风险评估
        
        输出格式：JSON数组
        """
        
        response = self.client.chat.completions.create(
            model="mimo-v2.5-pro",
            messages=[
                {"role": "system", "content": "你是一位经验丰富的技术解决方案专家。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=4096
        )
        
        return json.loads(response.choices[0].message.content)
    
    def validate_solution(self, solution: Dict[str, str], system_state: Dict[str, Any]) -> Dict[str, Any]:
        if self.demo_mode:
            return {
                "feasibility": "high",
                "难度": "中等",
                "收益": "高",
                "风险": "低",
                "建议": "方案可行，可以实施"
            }
        
        prompt = f"""
        请评估以下解决方案的可行性：
        
        解决方案：
        {json.dumps(solution, indent=2, ensure_ascii=False)}
        
        当前系统状态：
        {json.dumps(system_state, indent=2, ensure_ascii=False)}
        
        请评估：
        1. 技术可行性
        2. 实施难度
        3. 预期收益
        4. 潜在风险
        5. 建议调整
        
        输出格式：JSON
        """
        
        response = self.client.chat.completions.create(
            model="mimo-v2.5-pro",
            messages=[
                {"role": "system", "content": "你是一位专业的技术评估专家。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2048
        )
        
        return json.loads(response.choices[0].message.content)
    
    def run_iteration(self, system_state: Dict[str, Any]) -> Dict[str, Any]:
        issues = self.analyze_system(system_state)
        solutions = self.generate_solutions(issues)
        
        validated_solutions = []
        for solution in solutions:
            validation = self.validate_solution(solution, system_state)
            if validation.get("feasibility", "low") in ["high", "medium"]:
                validated_solutions.append({**solution, "validation": validation})
        
        iteration_result = {
            "timestamp": datetime.now().isoformat(),
            "issues_found": len(issues),
            "solutions_generated": len(solutions),
            "solutions_validated": len(validated_solutions),
            "issues": issues,
            "solutions": validated_solutions,
            "demo_mode": self.demo_mode
        }
        
        self.iteration_history.append(iteration_result)
        return iteration_result
    
    def get_iteration_history(self) -> List[Dict[str, Any]]:
        return self.iteration_history
    
    def suggest_next_question(self, context: str) -> str:
        if self.demo_mode:
            return "如何进一步优化系统的并发处理能力，以支持更高的用户访问量？"
        
        prompt = f"""
        基于以下上下文，提出一个能够帮助改进系统的关键问题：
        
        上下文：{context}
        
        请提出一个有深度、有挑战性的问题，能够揭示潜在问题或发现改进机会。
        """
        
        response = self.client.chat.completions.create(
            model="mimo-v2.5-pro",
            messages=[
                {"role": "system", "content": "你是一位擅长提出深刻问题的AI研究员，能够通过提问推动系统进化。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1024
        )
        
        return response.choices[0].message.content
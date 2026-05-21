import json
from typing import List, Dict, Any
from openai import OpenAI
import os

class AgentNegotiationEngine:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.environ.get("MIMO_API_KEY"),
            base_url="https://token-plan-cn.xiaomimimo.com/v1"
        )
    
    def negotiate(self, agent_results: Dict[str, str], conflict_areas: List[str]) -> str:
        prompt = f"""
        作为Agent协商专家，请协调以下Agent的输出结果：
        
        Agent结果：
        {json.dumps(agent_results, indent=2)}
        
        潜在冲突点：
        {chr(10).join(conflict_areas)}
        
        请：
        1. 识别各Agent输出之间的潜在冲突
        2. 协调解决冲突，生成统一方案
        3. 提供协调过程的说明
        
        输出格式：JSON，包含 negotiation_result 和 explanation 字段
        """
        
        response = self.client.chat.completions.create(
            model="mimo-v2.5-pro",
            messages=[
                {"role": "system", "content": "你是一位经验丰富的技术协调专家，擅长解决多团队协作中的冲突。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=4096
        )
        
        return response.choices[0].message.content
    
    def validate_consistency(self, agent_results: Dict[str, str]) -> Dict[str, Any]:
        prompt = f"""
        请检查以下Agent输出的一致性：
        
        {json.dumps(agent_results, indent=2)}
        
        检查维度：
        1. 技术栈一致性
        2. API设计一致性
        3. 数据模型一致性
        4. 架构风格一致性
        
        输出格式：JSON，包含 consistency_score (0-100) 和 issues 列表
        """
        
        response = self.client.chat.completions.create(
            model="mimo-v2.5-pro",
            messages=[
                {"role": "system", "content": "你是一位专业的系统一致性检查专家。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2048
        )
        
        return json.loads(response.choices[0].message.content)
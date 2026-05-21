import json
from typing import Dict, Any, List
from openai import OpenAI
import os

class FeedbackSystem:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.environ.get("MIMO_API_KEY"),
            base_url="https://token-plan-cn.xiaomimimo.com/v1"
        )
        self.feedback_history = []
    
    def collect_feedback(self, task_id: str, user_feedback: str, rating: int) -> None:
        feedback = {
            "task_id": task_id,
            "feedback": user_feedback,
            "rating": rating,
            "timestamp": self._get_timestamp()
        }
        self.feedback_history.append(feedback)
    
    def analyze_feedback(self) -> Dict[str, Any]:
        if not self.feedback_history:
            return {"insights": "暂无反馈数据"}
        
        feedback_text = "\n".join([
            f"评分: {f['rating']}/5 - 反馈: {f['feedback']}"
            for f in self.feedback_history
        ])
        
        prompt = f"""
        请分析以下用户反馈并提供改进建议：
        
        反馈记录：
        {feedback_text}
        
        请输出：
        1. 主要优点
        2. 主要问题
        3. 具体改进建议
        4. 优先级排序
        
        输出格式：JSON
        """
        
        response = self.client.chat.completions.create(
            model="mimo-v2.5-pro",
            messages=[
                {"role": "system", "content": "你是一位专业的用户体验分析专家。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=4096
        )
        
        return json.loads(response.choices[0].message.content)
    
    def apply_improvements(self, agent_type: str, improvements: List[str]) -> str:
        prompt = f"""
        请根据以下改进建议优化{agent_type} Agent的行为：
        
        改进建议：
        {chr(10).join(improvements)}
        
        请输出优化后的Agent指令（系统提示词）。
        """
        
        response = self.client.chat.completions.create(
            model="mimo-v2.5-pro",
            messages=[
                {"role": "system", "content": "你是一位AI系统优化专家。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=4096
        )
        
        return response.choices[0].message.content
    
    def _get_timestamp(self):
        from datetime import datetime
        return datetime.now().isoformat()
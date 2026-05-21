import os
from openai import OpenAI
from typing import List, Dict, Any

class MimoCodeAssistant:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.environ.get("MIMO_API_KEY"),
            base_url="https://token-plan-cn.xiaomimimo.com/v1"
        )
    
    def analyze_requirement(self, requirement: str) -> Dict[str, Any]:
        prompt = f"""
        作为资深技术架构师，请分析以下需求并输出结构化技术方案：
        
        需求描述：{requirement}
        
        请输出：
        1. 技术栈选型建议（前端/后端/数据库）
        2. 核心架构设计（模块划分/数据流）
        3. API接口设计（RESTful规范）
        4. 关键实现要点
        5. 潜在风险和解决方案
        
        输出格式：JSON
        """
        
        response = self.client.chat.completions.create(
            model="mimo-v2.5-pro",
            messages=[
                {"role": "system", "content": "你是小米MiMo驱动的智能代码助手，擅长技术架构设计和代码生成。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=4096
        )
        
        return response.choices[0].message.content
    
    def generate_code(self, task_description: str, language: str = "python") -> str:
        prompt = f"""
        作为高级{language}开发者，请根据以下任务描述生成高质量代码：
        
        任务：{task_description}
        
        要求：
        1. 代码符合行业最佳实践
        2. 包含完整的类型注解
        3. 添加必要的错误处理
        4. 生成对应的单元测试
        5. 提供清晰的代码注释
        
        输出格式：代码块 + 简要说明
        """
        
        response = self.client.chat.completions.create(
            model="mimo-v2.5-pro",
            messages=[
                {"role": "system", "content": f"你是精通{language}的代码专家，输出代码必须可直接运行。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=8192
        )
        
        return response.choices[0].message.content
    
    def generate_documentation(self, code: str, project_name: str) -> str:
        prompt = f"""
        作为技术文档工程师，请为以下代码生成专业文档：
        
        项目名称：{project_name}
        
        代码内容：
        {code}
        
        请输出：
        1. 功能概述
        2. API接口说明
        3. 使用示例
        4. 配置说明
        5. 部署指南
        
        输出格式：Markdown
        """
        
        response = self.client.chat.completions.create(
            model="mimo-v2.5-pro",
            messages=[
                {"role": "system", "content": "你是专业技术文档撰写专家，输出清晰、专业的技术文档。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=4096
        )
        
        return response.choices[0].message.content

if __name__ == "__main__":
    assistant = MimoCodeAssistant()
    
    requirement = "开发一个AI驱动的代码审查工具，支持代码质量检测、安全漏洞扫描、性能优化建议"
    
    print("=== 需求分析 ===")
    analysis = assistant.analyze_requirement(requirement)
    print(analysis)
    
    print("\n=== 代码生成 ===")
    code = assistant.generate_code("实现代码质量检测模块，包含代码复杂度分析和重复代码检测")
    print(code)
    
    print("\n=== 文档生成 ===")
    doc = assistant.generate_documentation(code, "AI代码审查工具")
    print(doc)
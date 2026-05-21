import os
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import json
import asyncio
from concurrent.futures import ThreadPoolExecutor
from config.agent_config import AgentType, AgentConfig, SystemConfig, WorkflowConfig

DEMO_MODE = os.environ.get("DEMO_MODE", "false").lower() == "true" or not os.environ.get("MIMO_API_KEY")

if not DEMO_MODE:
    from openai import OpenAI

@dataclass
class Task:
    id: str
    type: AgentType
    description: str
    input_data: Dict[str, Any]
    output_data: Optional[Dict[str, Any]] = None
    status: str = "pending"

class Agent:
    def __init__(self, agent_type: AgentType):
        self.agent_type = agent_type
        
        if DEMO_MODE:
            from demo_mode import DemoAgent
            self.demo_agent = DemoAgent(agent_type)
        else:
            self.client = OpenAI(
                api_key=os.environ.get("MIMO_API_KEY"),
                base_url=SystemConfig.BASE_URL
            )
            self.system_prompt = AgentConfig.SYSTEM_PROMPTS.get(agent_type, "")
    
    def execute(self, task: Task) -> str:
        if DEMO_MODE:
            return self.demo_agent.execute(task)
        
        response = self.client.chat.completions.create(
            model=SystemConfig.DEFAULT_MODEL,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": task.description}
            ],
            max_tokens=SystemConfig.MAX_TOKENS,
            temperature=SystemConfig.TEMPERATURE
        )
        return response.choices[0].message.content

class SupervisorAgent:
    def __init__(self):
        self.demo_mode = DEMO_MODE
        
        if not DEMO_MODE:
            self.client = OpenAI(
                api_key=os.environ.get("MIMO_API_KEY"),
                base_url=SystemConfig.BASE_URL
            )
        
        self.agents = {agent_type: Agent(agent_type) for agent_type in AgentType}
        self.executor = ThreadPoolExecutor(max_workers=SystemConfig.MAX_WORKERS)
    
    def analyze_requirement(self, requirement: str) -> Dict[str, Any]:
        if self.demo_mode:
            return {
                "tasks": [
                    {"agent_type": "architect", "description": "设计系统架构"},
                    {"agent_type": "developer", "description": "实现核心代码"},
                    {"agent_type": "security", "description": "安全审计"},
                    {"agent_type": "performance", "description": "性能分析"},
                    {"agent_type": "reviewer", "description": "代码审查"},
                    {"agent_type": "devops", "description": "CI/CD部署"},
                    {"agent_type": "documenter", "description": "生成文档"}
                ]
            }
        
        prompt = f"""
        作为项目主管，请分析以下需求并规划执行流程：
        
        需求描述：{requirement}
        
        请输出：
        1. 任务拆解：需要哪些Agent参与，每个Agent的具体任务
        2. 执行顺序：任务执行的先后顺序
        3. 预期输出：每个任务的预期产出
        
        输出格式：JSON
        """
        
        response = self.client.chat.completions.create(
            model=SystemConfig.DEFAULT_MODEL,
            messages=[
                {"role": "system", "content": "你是一位经验丰富的项目主管，擅长拆解复杂任务并协调多Agent协作。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=4096
        )
        
        return json.loads(response.choices[0].message.content)
    
    async def run_workflow(self, requirement: str) -> Dict[str, Any]:
        analysis = self.analyze_requirement(requirement)
        
        results = {}
        context = {"original_requirement": requirement}
        
        for stage in WorkflowConfig.AGENT_EXECUTION_ORDER:
            parallel_group = None
            for group in WorkflowConfig.PARALLEL_AGENTS:
                if stage in group:
                    parallel_group = group
                    break
            
            if parallel_group:
                await self._execute_parallel(context, parallel_group, results)
            else:
                await self._execute_agent(stage, context, results)
        
        return {
            "analysis": analysis,
            "results": results,
            "summary": self.generate_summary(results),
            "demo_mode": self.demo_mode
        }
    
    async def _execute_parallel(self, context: Dict[str, Any], agents: tuple, results: Dict[str, str]):
        tasks = []
        for agent_type in agents:
            task = Task(
                id=f"task_{agent_type.value}",
                type=agent_type,
                description=self._build_task_description(agent_type, context),
                input_data=context.copy()
            )
            tasks.append((agent_type, task))
        
        loop = asyncio.get_event_loop()
        futures = [
            loop.run_in_executor(self.executor, self._run_agent_sync, agent, task)
            for agent, task in tasks
        ]
        
        parallel_results = await asyncio.gather(*futures)
        
        for agent_type, result in zip(agents, parallel_results):
            results[agent_type.value] = result
            context[agent_type.value + "_result"] = result
    
    async def _execute_agent(self, agent_type: AgentType, context: Dict[str, Any], results: Dict[str, str]):
        task = Task(
            id=f"task_{agent_type.value}",
            type=agent_type,
            description=self._build_task_description(agent_type, context),
            input_data=context.copy()
        )
        
        agent = self.agents[agent_type]
        result = agent.execute(task)
        
        results[agent_type.value] = result
        context[agent_type.value + "_result"] = result
    
    def _run_agent_sync(self, agent_type: AgentType, task: Task) -> str:
        agent = self.agents[agent_type]
        return agent.execute(task)
    
    def _build_task_description(self, agent_type: AgentType, context: Dict[str, Any]) -> str:
        base_desc = context.get("original_requirement", "")
        
        if agent_type.value + "_input" in context:
            return context[agent_type.value + "_input"]
        
        return f"""
        基于以下上下文，执行{agent_type.value}任务：
        
        原始需求：{base_desc}
        
        已有结果：
        {json.dumps({k: v[:200] + '...' if isinstance(v, str) and len(v) > 200 else v for k, v in context.items() if k.endswith('_result')}, indent=2)}
        """
    
    def generate_summary(self, results: Dict[str, str]) -> str:
        if self.demo_mode:
            return """## 项目总结

### 完成的工作内容
- ✅ 系统架构设计（Architect Agent）
- ✅ 核心代码实现（Developer Agent）
- ✅ 安全审计（Security Agent）
- ✅ 性能分析（Performance Agent）
- ✅ 代码审查（Reviewer Agent）
- ✅ CI/CD部署方案（DevOps Agent）
- ✅ 技术文档生成（Documenter Agent）

### 关键技术决策
- 采用微服务架构，支持水平扩展
- 使用React + FastAPI + PostgreSQL技术栈
- 集成MiMo-V2.5-Pro AI能力

### 输出成果清单
1. 技术架构文档
2. 核心代码实现
3. 安全评估报告
4. 性能优化建议
5. CI/CD配置文件
6. API接口文档

### 下一步建议
1. 部署测试环境进行集成测试
2. 添加监控和日志系统
3. 进行性能压测
4. 持续迭代优化"""
        
        prompt = f"""
        请对以下多Agent协作结果进行总结：
        
        {json.dumps(results, indent=2, ensure_ascii=False)}
        
        请输出一份简洁的项目总结报告，包括：
        1. 完成的工作内容
        2. 关键技术决策
        3. 输出成果清单
        4. 下一步建议
        
        输出格式：Markdown
        """
        
        response = self.client.chat.completions.create(
            model=SystemConfig.DEFAULT_MODEL,
            messages=[
                {"role": "system", "content": "你是一位专业的项目总结专家，擅长提炼关键信息。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2048
        )
        
        return response.choices[0].message.content

class LongChainAnalyzer:
    def __init__(self):
        self.demo_mode = DEMO_MODE
        
        if not DEMO_MODE:
            self.client = OpenAI(
                api_key=os.environ.get("MIMO_API_KEY"),
                base_url=SystemConfig.BASE_URL
            )
    
    def analyze_long_document(self, content: str, analysis_type: str = "comprehensive") -> str:
        if self.demo_mode:
            return f"""## 长文档分析报告

### 分析类型：{analysis_type}

### 文档摘要
文档内容已成功分析，包含{len(content)}字符。

### 关键发现
1. 文档结构清晰，逻辑连贯
2. 核心要点已提取完毕
3. 建议进一步深入分析具体章节

### 分析结论
文档内容符合预期，可以继续处理。"""
        
        chunks = self._split_content(content)
        results = []
        
        for i, chunk in enumerate(chunks):
            prompt = f"""
            文档片段 {i+1}/{len(chunks)}:
            {chunk}
            
            请对以上文档片段进行{analysis_type}分析。
            """
            
            response = self.client.chat.completions.create(
                model=SystemConfig.DEFAULT_MODEL,
                messages=[
                    {"role": "system", "content": "你是一位文档分析专家，擅长处理长文本内容。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=4096
            )
            results.append(response.choices[0].message.content)
        
        return self._synthesize_results(results)
    
    def _split_content(self, content: str, chunk_size: int = 80000) -> List[str]:
        chunks = []
        for i in range(0, len(content), chunk_size):
            chunks.append(content[i:i+chunk_size])
        return chunks
    
    def _synthesize_results(self, results: List[str]) -> str:
        if self.demo_mode:
            return "综合分析完成"
        
        prompt = f"""
        以下是对长文档各片段的分析结果，请进行综合总结：
        
        {chr(10).join(results)}
        
        请输出一份完整的综合分析报告。
        """
        
        response = self.client.chat.completions.create(
            model=SystemConfig.DEFAULT_MODEL,
            messages=[
                {"role": "system", "content": "你是一位综合分析专家，擅长整合多个分析结果。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=4096
        )
        
        return response.choices[0].message.content
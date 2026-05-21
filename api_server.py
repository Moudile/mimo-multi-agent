from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from multi_agent_system import SupervisorAgent, LongChainAnalyzer
from agent_negotiation import AgentNegotiationEngine
from feedback_system import FeedbackSystem
from cache_system import SmartCache, TaskQueue
from utils.logger import WorkflowLogger
from self_iteration_engine import SelfIterationEngine
from learning_assistant import LearningAssistant
from config.system_config import SystemConfig
import asyncio
import json
import uuid

app = FastAPI(title="MiMo多Agent智能代码助手 API", version="4.0")

app.mount("/static", StaticFiles(directory="static"), name="static")

assistant = SupervisorAgent()
long_chain_analyzer = LongChainAnalyzer()
negotiation_engine = AgentNegotiationEngine()
feedback_system = FeedbackSystem()
cache = SmartCache(max_size=SystemConfig.CACHE_MAX_SIZE, ttl_hours=SystemConfig.CACHE_TTL_HOURS)
task_queue = TaskQueue(max_workers=SystemConfig.MAX_WORKERS)
logger = WorkflowLogger()
self_iteration = SelfIterationEngine()
learning_assistant = LearningAssistant()

class RequirementRequest(BaseModel):
    requirement: str

class LongChainRequest(BaseModel):
    content: str
    analysis_type: str = "comprehensive"

class FeedbackRequest(BaseModel):
    task_id: str
    feedback: str
    rating: int

class NegotiationRequest(BaseModel):
    agent_results: dict
    conflict_areas: list

class SelfIterationRequest(BaseModel):
    system_state: dict

class LearningRequest(BaseModel):
    topic: str
    skill_level: str = "beginner"

class QuestionRequest(BaseModel):
    question: str
    context: str = ""

@app.get("/", summary="首页")
async def index():
    return FileResponse("static/index.html")

@app.post("/api/analyze", summary="需求分析")
async def analyze_requirement(request: RequirementRequest):
    try:
        result = await asyncio.to_thread(
            assistant.analyze_requirement, 
            request.requirement
        )
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/run-workflow", summary="启动多Agent工作流")
async def run_workflow(request: RequirementRequest):
    task_id = str(uuid.uuid4())
    
    try:
        cached_result = cache.get(request.requirement, SystemConfig.DEFAULT_MODEL)
        if cached_result:
            return {"success": True, "data": cached_result, "task_id": task_id, "cached": True}
        
        logger.log_workflow_start(task_id, request.requirement)
        
        result = await asyncio.to_thread(
            assistant.run_workflow, 
            request.requirement
        )
        
        cache.set(request.requirement, SystemConfig.DEFAULT_MODEL, result)
        logger.log_workflow_complete(task_id, success=True)
        
        return {"success": True, "data": result, "task_id": task_id, "cached": False}
    except Exception as e:
        logger.log_workflow_complete(task_id, success=False, error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/long-chain", summary="长链文档分析")
async def long_chain_analysis(request: LongChainRequest):
    try:
        result = await asyncio.to_thread(
            long_chain_analyzer.analyze_long_document,
            request.content,
            request.analysis_type
        )
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/negotiate", summary="Agent协商")
async def negotiate(request: NegotiationRequest):
    try:
        result = await asyncio.to_thread(
            negotiation_engine.negotiate,
            request.agent_results,
            request.conflict_areas
        )
        return {"success": True, "data": json.loads(result)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/validate-consistency", summary="一致性检查")
async def validate_consistency(request: NegotiationRequest):
    try:
        result = await asyncio.to_thread(
            negotiation_engine.validate_consistency,
            request.agent_results
        )
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/feedback", summary="提交反馈")
async def submit_feedback(request: FeedbackRequest):
    try:
        feedback_system.collect_feedback(
            request.task_id,
            request.feedback,
            request.rating
        )
        return {"success": True, "message": "反馈已提交"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/feedback-analysis", summary="反馈分析")
async def get_feedback_analysis():
    try:
        result = feedback_system.analyze_feedback()
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/self-iterate", summary="自迭代分析")
async def self_iterate(request: SelfIterationRequest):
    try:
        result = await asyncio.to_thread(
            self_iteration.run_iteration,
            request.system_state
        )
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/self-iteration-history", summary="自迭代历史")
async def get_self_iteration_history():
    try:
        result = self_iteration.get_iteration_history()
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/suggest-question", summary="提出关键问题")
async def suggest_question(request: QuestionRequest):
    try:
        result = await asyncio.to_thread(
            self_iteration.suggest_next_question,
            request.context
        )
        return {"success": True, "data": {"question": result}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate-tutorial", summary="生成教程")
async def generate_tutorial(request: LearningRequest):
    try:
        result = await asyncio.to_thread(
            learning_assistant.generate_tutorial,
            request.topic,
            request.skill_level
        )
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/explain-concept", summary="解释概念")
async def explain_concept(request: LearningRequest):
    try:
        result = await asyncio.to_thread(
            learning_assistant.explain_concept,
            request.topic,
            request.skill_level
        )
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/suggest-project", summary="推荐项目")
async def suggest_project(request: LearningRequest):
    try:
        result = await asyncio.to_thread(
            learning_assistant.suggest_project,
            request.skill_level
        )
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/answer-question", summary="回答问题")
async def answer_question(request: QuestionRequest):
    try:
        result = await asyncio.to_thread(
            learning_assistant.answer_question,
            request.question,
            request.context
        )
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate-cheatsheet", summary="生成速查表")
async def generate_cheatsheet(request: LearningRequest):
    try:
        result = await asyncio.to_thread(
            learning_assistant.generate_cheat_sheet,
            request.topic
        )
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stats", summary="系统统计")
async def get_stats():
    return {
        "success": True,
        "data": {
            "cache": cache.get_stats(),
            "task_queue": task_queue.get_status(),
            "feedback_count": len(feedback_system.feedback_history),
            "iteration_count": len(self_iteration.get_iteration_history()),
            "config": {
                "max_workers": SystemConfig.MAX_WORKERS,
                "max_tokens": SystemConfig.MAX_TOKENS,
                "model": SystemConfig.DEFAULT_MODEL
            }
        }
    }

@app.get("/api/log-report", summary="获取日志报告")
async def get_log_report():
    return {"success": True, "data": logger.get_task_report()}

@app.get("/health", summary="健康检查")
async def health_check():
    return {
        "status": "healthy", 
        "model": SystemConfig.DEFAULT_MODEL, 
        "features": [
            "多Agent协作", 
            "长链推理", 
            "Agent协商",
            "智能缓存",
            "用户反馈",
            "并行执行",
            "日志监控",
            "自迭代修复",
            "学习助手"
        ],
        "version": "4.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
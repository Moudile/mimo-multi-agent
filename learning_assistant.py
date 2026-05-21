import json
from typing import List, Dict, Any
import os

DEMO_MODE = os.environ.get("DEMO_MODE", "false").lower() == "true" or not os.environ.get("MIMO_API_KEY")

if not DEMO_MODE:
    from openai import OpenAI

class LearningAssistant:
    def __init__(self):
        self.demo_mode = DEMO_MODE
        
        if not DEMO_MODE:
            self.client = OpenAI(
                api_key=os.environ.get("MIMO_API_KEY"),
                base_url="https://token-plan-cn.xiaomimimo.com/v1"
            )
        
        self.learning_progress = {}
    
    def generate_tutorial(self, topic: str, skill_level: str = "beginner") -> str:
        if self.demo_mode:
            return f"""# {topic} 入门教程

## 学习目标
- 理解{topic}的基本概念
- 掌握核心使用方法
- 能够独立完成简单项目

## 学习步骤

### 第一步：环境准备
```bash
# 安装依赖
pip install {topic.lower()}
```

### 第二步：基础入门
```python
import {topic.lower()}

# 基本使用示例
app = {topic.lower()}.{topic}()
app.run()
```

### 第三步：实践练习
1. 创建一个简单的{topic}应用
2. 添加API接口
3. 测试接口功能

## 学习时间
预计学习时间：2-3小时

## 进阶学习
完成基础学习后，可以继续学习：
- 高级特性
- 性能优化
- 最佳实践"""
        
        prompt = f"""
        请为{skill_level}级用户生成关于「{topic}」的入门教程。
        
        要求：
        1. 使用简单易懂的语言
        2. 提供清晰的步骤说明
        3. 包含代码示例
        4. 提供实践练习
        5. 预估学习时间
        
        输出格式：Markdown
        """
        
        response = self.client.chat.completions.create(
            model="mimo-v2.5-pro",
            messages=[
                {"role": "system", "content": "你是一位耐心的AI导师，擅长用简单易懂的方式教授技术知识。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=4096
        )
        
        return response.choices[0].message.content
    
    def explain_concept(self, concept: str, target_audience: str = "developers") -> str:
        if self.demo_mode:
            return f"""# {concept} 概念解释

## 什么是{concept}？

{concept}是一种{concept.replace('系统', '').replace('技术', '')}相关的技术概念，它主要用于解决{concept.replace('多', '').replace('智能', '')}相关的问题。

## 核心思想

{concept}的核心思想是通过{concept.replace('系统', '').replace('引擎', '')}的方式，实现{concept.replace('系统', '').replace('引擎', '')}的目标。

## 实际应用

- **场景1**: 在{concept.replace('多', '').replace('智能', '')}场景中的应用
- **场景2**: 与{concept.replace('系统', '').replace('引擎', '')}结合使用
- **场景3**: 提升{concept.replace('系统', '').replace('引擎', '')}效率

## 为什么重要

{concept}能够帮助开发者：
- 提高开发效率
- 简化复杂逻辑
- 提升系统性能"""
        
        prompt = f"""
        请向{target_audience}解释「{concept}」这个概念。
        
        要求：
        1. 用通俗易懂的语言
        2. 提供实际例子
        3. 解释为什么这个概念重要
        4. 避免使用过多专业术语
        
        输出格式：Markdown
        """
        
        response = self.client.chat.completions.create(
            model="mimo-v2.5-pro",
            messages=[
                {"role": "system", "content": "你是一位优秀的技术科普专家。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2048
        )
        
        return response.choices[0].message.content
    
    def suggest_project(self, skill_level: str = "beginner", interests: List[str] = None) -> str:
        if self.demo_mode:
            return f"""# 推荐项目：个人博客系统

## 项目难度：{skill_level}

## 项目目标
创建一个基于FastAPI的个人博客系统，包含文章管理、用户认证等功能。

## 技术栈
- **后端**: FastAPI + Python
- **数据库**: SQLite/PostgreSQL
- **前端**: React/Vue
- **认证**: JWT

## 项目大纲

1. 用户认证模块
   - 注册、登录、密码重置
   - JWT令牌管理

2. 文章管理模块
   - CRUD操作
   - 分类和标签
   - 分页查询

3. 评论系统
   - 评论发布
   - 评论回复
   - 评论审核

## 实现步骤

1. 搭建项目结构
2. 配置数据库连接
3. 实现用户认证
4. 开发文章管理API
5. 添加评论功能
6. 部署上线

## 学习收获

完成这个项目，你将学习到：
- RESTful API设计
- 用户认证实现
- 数据库操作
- 前后端协作"""
        
        interests = interests or []
        
        prompt = f"""
        请为{skill_level}级开发者推荐一个合适的项目。
        
        兴趣方向：{', '.join(interests) if interests else '不限'}
        
        要求：
        1. 项目难度适中，适合练习
        2. 能够学习到实用技能
        3. 提供项目大纲
        4. 列出所需技术栈
        5. 提供实现步骤建议
        
        输出格式：Markdown
        """
        
        response = self.client.chat.completions.create(
            model="mimo-v2.5-pro",
            messages=[
                {"role": "system", "content": "你是一位经验丰富的技术顾问，擅长推荐合适的学习项目。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=4096
        )
        
        return response.choices[0].message.content
    
    def answer_question(self, question: str, context: str = "") -> str:
        if self.demo_mode:
            return f"""# 问题解答：{question}

## 答案

{question.replace('什么是', '').replace('?', '')}是一种用于处理长文本上下文的AI技术。

## 核心原理

它允许AI模型在处理任务时，能够参考和理解更长的对话历史或文档内容。

## 应用场景

- 长文档分析
- 多轮对话理解
- 代码上下文理解
- 知识检索增强

## 进一步学习

推荐学习资源：
1. MiMo-V2.5-Pro官方文档
2. LangChain长链处理教程
3. RAG技术入门指南"""
        
        prompt = f"""
        请回答以下问题：
        
        问题：{question}
        
        上下文：{context}
        
        要求：
        1. 提供清晰准确的答案
        2. 如果需要，提供代码示例
        3. 解释相关概念
        4. 给出进一步学习的建议
        
        输出格式：Markdown
        """
        
        response = self.client.chat.completions.create(
            model="mimo-v2.5-pro",
            messages=[
                {"role": "system", "content": "你是一位乐于助人的技术答疑专家。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=4096
        )
        
        return response.choices[0].message.content
    
    def generate_cheat_sheet(self, topic: str) -> str:
        if self.demo_mode:
            return f"""# {topic} 速查表

| 操作 | 命令/代码 | 说明 |
|------|-----------|------|
| 安装 | `pip install {topic.lower()}` | 安装{topic} |
| 导入 | `import {topic.lower()}` | 导入模块 |
| 初始化 | `app = {topic.lower()}.{topic}()` | 创建实例 |
| 运行 | `app.run()` | 启动服务 |
| 配置 | `app.config.update({...})` | 更新配置 |

## 常用方法

- `method1()` - 功能描述
- `method2()` - 功能描述  
- `method3()` - 功能描述

## 常用配置

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `debug` | `False` | 调试模式 |
| `port` | `8000` | 端口号 |
| `host` | `localhost` | 主机地址 |"""
        
        prompt = f"""
        请为「{topic}」生成一份速查表（Cheat Sheet）。
        
        要求：
        1. 列出常用命令/API
        2. 提供简短说明
        3. 包含示例
        4. 便于快速查阅
        
        输出格式：Markdown表格
        """
        
        response = self.client.chat.completions.create(
            model="mimo-v2.5-pro",
            messages=[
                {"role": "system", "content": "你是一位技术文档专家，擅长创建实用的速查表。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2048
        )
        
        return response.choices[0].message.content
    
    def track_progress(self, user_id: str, topic: str, progress: float):
        if user_id not in self.learning_progress:
            self.learning_progress[user_id] = {}
        
        self.learning_progress[user_id][topic] = {
            "progress": progress,
            "last_updated": self._get_timestamp()
        }
    
    def get_progress(self, user_id: str) -> Dict[str, Any]:
        return self.learning_progress.get(user_id, {})
    
    def _get_timestamp(self):
        from datetime import datetime
        return datetime.now().isoformat()
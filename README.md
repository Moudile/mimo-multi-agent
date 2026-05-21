# MiMo多Agent智能代码助手

基于小米MiMo-V2.5-Pro构建的多Agent协作系统，支持长链推理、自迭代修复和低门槛学习。

## ✨ 功能特性

- **多Agent协作**：7个专业Agent分工协作，覆盖架构设计、代码实现、安全审计、性能优化、代码审查、DevOps部署、文档生成
- **长链推理**：支持100万Token超长上下文，处理完整项目架构
- **自迭代修复**：自动分析系统状态，提出改进问题，生成解决方案并验证可行性
- **学习助手**：提供教程生成、概念解释、项目推荐、问题解答、速查表生成等学习支持
- **并行执行**：支持多个Agent并行执行，提升效率
- **智能缓存**：基于请求的智能缓存机制，减少重复计算
- **用户反馈**：收集用户反馈并自动分析改进方向
- **在线演示**：提供美观的Web界面进行交互演示

## 🚀 快速开始

### 环境要求

- Python >= 3.10
- 小米MiMo API Key

### 安装依赖

```bash
pip install -r requirements.txt
```

### 配置环境变量

```bash
export MIMO_API_KEY=your_api_key_here
```

### 启动服务

```bash
python api_server.py
```

访问 http://localhost:8000 查看在线演示

## 📁 项目结构

```
mimo-multi-agent/
├── config/
│   ├── agent_config.py      # Agent类型和系统提示词配置
│   └── system_config.py     # 系统级配置参数
├── utils/
│   └── logger.py            # 工作流日志和监控
├── multi_agent_system.py    # 多Agent协作核心模块
├── agent_negotiation.py     # Agent协商引擎
├── feedback_system.py       # 用户反馈系统
├── cache_system.py          # 智能缓存和任务队列
├── self_iteration_engine.py # 自迭代修复引擎
├── learning_assistant.py    # 学习助手
├── api_server.py            # FastAPI服务端
├── static/
│   └── index.html           # 前端演示页面
└── README.md                # 项目文档
```

## 🛠️ 技术栈

| 分类 | 技术 |
|------|------|
| 语言 | Python 3.10+ |
| 框架 | FastAPI |
| AI模型 | MiMo-V2.5-Pro |
| 前端 | HTML5 + TailwindCSS |
| 并发 | asyncio + ThreadPoolExecutor |

## 🧠 Agent团队

| Agent | 职责 |
|-------|------|
| **Architect Agent** | 系统架构设计与技术方案规划 |
| **Developer Agent** | 高质量代码实现与测试编写 |
| **Security Agent** | 安全审计与漏洞检测 |
| **Performance Agent** | 性能分析与优化建议 |
| **Reviewer Agent** | 代码审查与质量保证 |
| **DevOps Agent** | CI/CD设计与部署指南 |
| **Documenter Agent** | 技术文档撰写与API说明 |

## 🔄 自迭代修复引擎

### 功能概述

参考PUAskill的自我进化理念，系统能够：

1. **自我分析**：从功能完整性、性能优化、用户体验、代码质量、安全隐患、扩展性等维度分析系统状态
2. **问题发现**：自动识别系统存在的问题并分级（高/中/低）
3. **方案生成**：为每个问题生成具体的解决方案
4. **方案验证**：评估解决方案的技术可行性、实施难度和预期收益
5. **持续进化**：记录迭代历史，支持持续改进

### 工作流程

```
系统状态 → 分析问题 → 生成方案 → 验证方案 → 记录迭代 → 持续改进
```

## 📚 学习助手

### 功能特性

| 功能 | 说明 |
|------|------|
| **教程生成** | 根据主题和技能级别生成入门教程 |
| **概念解释** | 用通俗易懂的语言解释技术概念 |
| **项目推荐** | 根据技能水平推荐合适的练习项目 |
| **问题解答** | 提供技术问题的详细解答和代码示例 |
| **速查表** | 生成常用命令和API的速查表 |

## 📊 工作流程

```
需求输入 → 架构设计 → 代码实现 → 安全审计 → 性能优化 → 代码审查 → DevOps部署 → 文档生成
                                              ↖           ↗
                                          并行执行
```

## 📝 API接口

### 核心功能

| 接口 | 方法 | 功能 |
|------|------|------|
| `/api/analyze` | POST | 需求分析 |
| `/api/run-workflow` | POST | 启动多Agent工作流 |
| `/api/long-chain` | POST | 长链文档分析 |

### 自迭代功能

| 接口 | 方法 | 功能 |
|------|------|------|
| `/api/self-iterate` | POST | 执行自迭代分析 |
| `/api/self-iteration-history` | GET | 获取迭代历史 |
| `/api/suggest-question` | POST | 提出关键问题 |

### 学习功能

| 接口 | 方法 | 功能 |
|------|------|------|
| `/api/generate-tutorial` | POST | 生成教程 |
| `/api/explain-concept` | POST | 解释概念 |
| `/api/suggest-project` | POST | 推荐项目 |
| `/api/answer-question` | POST | 回答问题 |
| `/api/generate-cheatsheet` | POST | 生成速查表 |

### 辅助功能

| 接口 | 方法 | 功能 |
|------|------|------|
| `/api/negotiate` | POST | Agent协商 |
| `/api/validate-consistency` | POST | 一致性检查 |
| `/api/feedback` | POST | 提交反馈 |
| `/api/feedback-analysis` | GET | 反馈分析 |
| `/api/stats` | GET | 系统统计 |
| `/api/log-report` | GET | 日志报告 |
| `/health` | GET | 健康检查 |

## 📊 性能指标

| 指标 | 数值 |
|------|------|
| 支持最大Token数 | 100万 |
| 并行Agent数 | 4 |
| 缓存容量 | 1000条 |
| 缓存有效期 | 24小时 |

## 🌟 技术亮点

1. **长链推理**：利用MiMo-V2.5-Pro的100万Token上下文能力
2. **多Agent协作**：专业Agent分工协作，提升输出质量
3. **自迭代修复**：参考PUAskill理念，系统能够自我分析、发现问题、生成解决方案
4. **低门槛学习**：提供友好的学习助手，降低上手难度
5. **并行执行**：Security和Performance Agent可并行执行
6. **智能缓存**：减少重复计算，提升响应速度

## 📄 许可证

MIT License
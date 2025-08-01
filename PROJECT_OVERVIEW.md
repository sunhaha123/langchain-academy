# LangChain Academy 项目完整文档

## 🎯 项目概述

LangChain Academy 是一套专注于 **LangGraph 生态系统基础概念** 的模块化学习课程。该项目从基础设置开始，逐步深入到高级主题，帮助开发者掌握构建智能代理和多代理应用程序的核心技能。

### 📚 核心特色

- **渐进式学习路径**: 从基础概念到生产部署的完整学习链路
- **理论与实践结合**: 每个模块都包含 Jupyter notebook (理论学习) 和 studio (实践项目)
- **可视化调试**: 内置 LangGraph Studio 支持，提供图执行的可视化调试
- **生产就绪**: 包含完整的部署和生产环境配置

## 🏗️ 项目结构

```
langchain-academy/
├── README.md                    # 项目说明和安装指南
├── requirements.txt            # 全局依赖包
├── module-0/                   # 基础设置
│   └── basics.ipynb           # LangChain 基础和环境配置
├── module-1/                   # LangGraph 入门
│   ├── simple-graph.ipynb     # 简单图结构
│   ├── chain.ipynb           # 链式图
│   ├── router.ipynb          # 路由图
│   ├── agent.ipynb           # 基础代理
│   ├── agent-memory.ipynb    # 记忆代理
│   ├── deployment.ipynb      # 部署相关
│   └── studio/               # 实践项目
├── module-2/                   # 状态管理和内存
│   ├── state-schema.ipynb     # 状态模式定义
│   ├── state-reducers.ipynb  # 状态约减器
│   ├── multiple-schemas.ipynb # 多状态模式
│   ├── trim-filter-messages.ipynb # 消息处理
│   ├── chatbot-*.ipynb       # 聊天机器人系列
│   └── studio/               # 实践项目
├── module-3/                   # 人机交互循环
│   ├── breakpoints.ipynb      # 断点功能
│   ├── dynamic-breakpoints.ipynb # 动态断点
│   ├── edit-state-human-feedback.ipynb # 状态编辑
│   ├── streaming-interruption.ipynb # 流式中断
│   ├── time-travel.ipynb     # 时间旅行调试
│   └── studio/               # 实践项目
├── module-4/                   # 并行处理和子图
│   ├── map-reduce.ipynb       # Map-Reduce 模式
│   ├── parallelization.ipynb # 并行处理
│   ├── sub-graph.ipynb       # 子图构建
│   ├── research-assistant.ipynb # 研究助手应用
│   └── studio/               # 实践项目
├── module-5/                   # 长期记忆系统
│   ├── memory_store.ipynb     # 记忆存储
│   ├── memoryschema_*.ipynb  # 记忆模式系列
│   ├── memory_agent.ipynb    # 记忆代理
│   └── studio/               # 实践项目
└── module-6/                   # 生产部署
    ├── assistant.ipynb        # 助手管理
    ├── creating.ipynb         # 助手创建
    ├── connecting.ipynb       # 连接管理
    ├── double-texting.ipynb   # 双重文本处理
    └── deployment/            # 生产部署配置
```

## 📖 学习路径

### 🎯 学习目标递进

| 模块 | 主题 | 核心概念 | 技能水平 |
|------|------|----------|----------|
| **Module-0** | 基础设置 | Chat Models, API 配置 | 初学者 |
| **Module-1** | LangGraph 入门 | StateGraph, 节点边, 记忆 | 入门 |
| **Module-2** | 状态管理 | 状态模式, 约减器, 消息处理 | 初级 |
| **Module-3** | 人机交互 | 断点, 调试, 状态编辑 | 中级 |
| **Module-4** | 并行处理 | Map-Reduce, 子图, 复合应用 | 中高级 |
| **Module-5** | 长期记忆 | 语义存储, 用户档案, 智能记忆 | 高级 |
| **Module-6** | 生产部署 | 助手系统, 版本控制, 容器化 | 专家级 |

### 🛤️ 推荐学习顺序

1. **环境准备阶段** (Module-0)
   - 配置开发环境和 API 密钥
   - 理解 LangChain 基础组件

2. **核心概念掌握** (Module-1-2)
   - 学习 LangGraph 的图构建模式
   - 掌握状态管理和记忆机制

3. **高级功能应用** (Module-3-4)
   - 实现人机交互和调试控制
   - 构建复杂的并行处理应用

4. **企业级应用** (Module-5-6)
   - 实现长期记忆和智能存储
   - 掌握生产环境部署

## 🔧 技术栈

### 核心依赖
```txt
langgraph                    # 核心图框架
langgraph-prebuilt         # 预构建组件
langgraph-sdk              # SDK 工具
langgraph-checkpoint-sqlite # SQLite 检查点存储
langsmith                  # 追踪和监控
langchain-community        # 社区组件
langchain-core             # 核心功能
langchain-openai           # OpenAI 集成
tavily-python              # 网络搜索
wikipedia                  # 维基百科工具
trustcall                  # JSON 模式验证
langgraph-cli[inmem]       # CLI 工具
```

### 开发工具
- **LangGraph Studio**: 可视化图调试和监控
- **LangSmith**: 应用追踪和性能分析
- **Jupyter Notebook**: 交互式学习环境

## 🚀 快速开始

### 1. 环境准备

```bash
# 克隆项目
git clone https://github.com/langchain-ai/langchain-academy.git
cd langchain-academy

# 创建虚拟环境
python3 -m venv lc-academy-env
source lc-academy-env/bin/activate  # Linux/Mac
# lc-academy-env\Scripts\activate   # Windows

# 安装依赖
pip install -r requirements.txt
```

### 2. API 配置

```bash
# OpenAI API (必需)
export OPENAI_API_KEY="your-openai-api-key"

# LangSmith (推荐，用于追踪)
export LANGCHAIN_API_KEY="your-langsmith-api-key"
export LANGCHAIN_TRACING_V2=true

# Tavily Search (Module-4 需要)
export TAVILY_API_KEY="your-tavily-api-key"
```

### 3. 启动学习

```bash
# 启动 Jupyter Notebook
jupyter notebook

# 或使用 LangGraph Studio (在 studio 子目录中)
cd module-1/studio
langgraph dev
```

## 🎯 核心项目展示

### 1. Module-1: 记忆代理 (Memory Agent)
```python
# 基础代理 vs 记忆代理
basic_agent.invoke({"messages": [HumanMessage("Hello")]})
memory_agent.invoke(
    {"messages": [HumanMessage("Hello")]}, 
    config={"configurable": {"thread_id": "conversation-1"}}
)
```

### 2. Module-4: 研究助手 (Research Assistant)
- **多代理协作**: AI 分析师团队并行工作
- **动态规划**: 根据用户需求生成专门的研究团队
- **深度访谈**: 每个分析师与专家 AI 进行详细对话
- **报告合成**: 将多个研究结果合成为统一报告

### 3. Module-5: task_mAIstro
- **智能记忆**: 自动决定何时保存重要信息
- **用户档案**: 维护用户偏好和行为模式
- **待办管理**: 智能任务创建和跟踪
- **程序性记忆**: 学习用户的工作流程

### 4. Module-6: 生产部署
- **助手版本控制**: 支持助手的创建、更新和回滚
- **配置管理**: 灵活的配置系统支持多环境部署
- **容器化**: Docker 和 docker-compose 支持
- **API 服务**: 完整的 REST API 和 WebSocket 支持

## 🔍 高级特性

### 状态管理模式
```python
# 三种状态定义方式
# 1. TypedDict (简单)
class SimpleState(TypedDict):
    messages: list[BaseMessage]

# 2. Dataclass (结构化)
@dataclass
class DataclassState:
    messages: list[BaseMessage]

# 3. Pydantic (验证)
class PydanticState(BaseModel):
    messages: list[BaseMessage]
```

### 人机交互控制
```python
# 断点控制
graph = builder.compile(
    checkpointer=memory,
    interrupt_before=["human_node"]  # 在人工节点前暂停
)

# 动态断点
graph.update_state(
    config, 
    values={"feedback": "Please revise the answer"}
)
```

### 并行处理模式
```python
# Map-Reduce 模式
def map_step(state):
    return [process_item(item) for item in state["items"]]

def reduce_step(results):
    return {"final_result": combine(results)}
```

## 📊 学习成果

完成本课程后，您将掌握：

### 🎯 核心技能
- ✅ LangGraph 图结构设计和实现
- ✅ 智能代理的构建和部署
- ✅ 状态管理和记忆系统设计
- ✅ 人机交互和调试技术
- ✅ 并行处理和复合应用开发
- ✅ 生产环境部署和维护

### 🚀 实际应用能力
- ✅ 构建对话式 AI 应用
- ✅ 设计多代理协作系统
- ✅ 实现智能研究和分析工具
- ✅ 开发带记忆的个人助手
- ✅ 部署企业级 AI 应用

### 🔧 技术栈精通
- ✅ LangChain/LangGraph 生态系统
- ✅ OpenAI API 和其他 LLM 集成
- ✅ 向量数据库和语义搜索
- ✅ 容器化和云端部署
- ✅ AI 应用监控和调试

## 🔗 相关资源

### 官方文档
- [LangGraph 官方文档](https://langchain-ai.github.io/langgraph/)
- [LangChain 文档](https://python.langchain.com/)
- [LangSmith 文档](https://docs.smith.langchain.com/)

### 社区资源
- [LangChain GitHub](https://github.com/langchain-ai/langchain)
- [LangGraph Studio 指南](https://langchain-ai.github.io/langgraph/concepts/langgraph_studio/)
- [LangChain Academy 官网](https://academy.langchain.com/)

---

## 📝 使用建议

### 学习策略
1. **按序进行**: 严格按照 Module-0 到 Module-6 的顺序学习
2. **理论实践结合**: 每个 notebook 学习后立即在 studio 中实践
3. **动手实验**: 修改示例代码，尝试不同的参数和配置
4. **项目驱动**: 结合自己的实际需求构建应用

### 调试技巧
1. **使用 LangGraph Studio**: 可视化图执行过程
2. **启用 LangSmith 追踪**: 监控 LLM 调用和性能
3. **设置断点**: 在关键节点暂停检查状态
4. **日志记录**: 增加详细的日志输出

### 最佳实践
1. **代码版本控制**: 使用 Git 管理实验和改进
2. **环境隔离**: 为不同模块使用独立的虚拟环境
3. **API 密钥安全**: 使用环境变量管理敏感信息
4. **性能优化**: 关注内存使用和响应时间

---

🎉 **开始您的 LangGraph 学习之旅吧！** 从 Module-0 开始，逐步掌握构建智能代理应用的核心技能。
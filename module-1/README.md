# LangGraph Memory Agent 项目完整指南

## 🎯 项目概述

这是一个基于 **LangGraph** 构建的智能代理项目，展示了如何实现带记忆功能的对话AI系统。项目包含两种代理：
- **basic_agent**: 基础代理，无记忆功能
- **memory_agent**: 带记忆的代理，支持多轮对话上下文

## 🏗️ 项目结构

```
module-1/
├── agent_graphs.py          # 主要的图定义文件 
├── langgraph.json          # LangGraph配置文件
├── agent-memory.ipynb      # 学习教程notebook
├── test_api.py             # API测试脚本
├── README.md               # 项目说明
└── studio/                 # Studio相关文件
    ├── agent.py
    ├── router.py
    └── simple.py
```

## 🚀 启动方式

### 方式一：开发模式 (推荐)

```bash
# 1. 进入项目目录
cd /home/echo/workspace/langchain-academy/module-1

# 2. 启动开发服务器
/home/echo/miniconda3/envs/agent/bin/langgraph dev --port 3000

# 3. 访问服务
# - 🚀 API服务器: http://127.0.0.1:3000
# - 🎨 Studio UI: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:3000  
# - 📚 API文档: http://127.0.0.1:3000/docs
```

### 方式二：直接Python调用

```python
from agent_graphs import basic_agent, memory_agent
from langchain_core.messages import HumanMessage

# 基础代理使用
messages = [HumanMessage(content="计算 10 + 5")]
result = basic_agent.invoke({"messages": messages})
print(result['messages'][-1].content)

# 记忆代理使用 (需要thread_id)
config = {"configurable": {"thread_id": "my_conversation"}}
result = memory_agent.invoke({"messages": messages}, config)
print(result['messages'][-1].content)
```

### 方式三：生产部署

```bash
# 构建Docker镜像
langgraph build

# 生产环境启动
langgraph up
```

## 📡 API 使用方式

### 1. 创建Assistant

```bash
curl -X POST http://127.0.0.1:3000/assistants \
  -H "Content-Type: application/json" \
  -d '{"graph_id": "memory_agent"}'
```

### 2. 创建Thread

```bash
curl -X POST http://127.0.0.1:3000/threads \
  -H "Content-Type: application/json" -d '{}'
```

### 3. 发送消息

```bash
curl -X POST http://127.0.0.1:3000/threads/{thread_id}/runs \
  -H "Content-Type: application/json" \
  -d '{
    "assistant_id": "{assistant_id}",
    "input": {
      "messages": [
        {"role": "human", "content": "计算 15 + 25"}
      ]
    }
  }'
```

### 4. 查看结果

```bash
curl http://127.0.0.1:3000/threads/{thread_id}/runs/{run_id}
```

## 🔧 LangGraph Dev 原理解析

### 架构对比

| 特性 | LangGraph Dev | FastAPI | 说明 |
|------|---------------|---------|------|
| **架构模式** | Graph-based API | REST/HTTP API | 专注于状态图执行 |
| **状态管理** | 内置Checkpointer | 需要外部存储 | 自动处理状态持久化 |
| **并发模型** | Actor-based | ASGI协程 | Actor模式管理并发 |
| **调试工具** | 可视化Studio | Swagger UI | 图执行可视化 |
| **热重载** | 图定义重载 | Python代码重载 | 重载图结构 |

### 启动流程

```bash
langgraph dev
│
├── 解析 langgraph.json 配置
├── 安装依赖包 (dependencies)  
├── 导入图定义 (graphs)
├── 设置环境变量 (env)
│
├── 启动API服务器 (基于FastAPI)
│   ├── 端口: 3000 (可配置)
│   ├── 路由: /assistants, /threads, /runs
│   └── 中间件: CORS, 认证, 日志
│
├── 启动文件监控 (热重载)
│   ├── 监控: *.py, *.json
│   └── 回调: 重新加载图定义
│
├── 连接Studio前端
│   ├── WebSocket: 实时通信
│   ├── 代理: 本地请求转发  
│   └── 调试: 断点和状态同步
│
└── 可选: 自动打开浏览器
```

## 🧠 记忆管理机制

### 1. 状态持久化

LangGraph使用 **Checkpointer** 机制自动保存图的执行状态：

```python
# 开发模式: 内存存储
memory = MemorySaver()
graph = builder.compile(checkpointer=memory)

# 生产模式: 自动持久化
graph = builder.compile()  # API服务器自动处理
```

### 2. Thread概念

- **Thread**: 独立的对话会话，包含完整的消息历史
- **Thread ID**: 唯一标识符，用于区分不同的对话
- **State**: 每个Thread维护独立的状态

### 3. 消息累积

```python
class MessagesState(TypedDict):
    messages: Annotated[list[BaseMessage], add]  # add作为reducer
```

新消息会**追加**到现有消息列表，形成完整对话历史。

## 🛠️ 开发调试

### 1. LangGraph Studio

- **可视化图结构**: 实时查看节点和边
- **状态检查**: 每个步骤的状态变化
- **断点调试**: 暂停执行检查中间状态
- **时间旅行**: 回滚到历史状态

### 2. 日志监控

```bash
# 启用详细日志
langgraph dev --server-log-level DEBUG

# 监控worker状态
# 服务器会定期输出worker和队列统计信息
```

### 3. 热重载

修改 `agent_graphs.py` 文件后自动重新加载，无需重启服务器。

## 🔍 故障排查

### 常见问题

1. **"langgraph: 未找到命令"**
   ```bash
   # 安装CLI工具
   pip install langgraph-cli
   
   # 或使用完整路径
   /path/to/env/bin/langgraph dev
   ```

2. **"自定义checkpointer错误"**
   ```python
   # 错误: 在图定义中使用了MemorySaver
   def create_graph():
       builder = StateGraph(MessagesState)
       # ... 添加节点和边
       return builder.compile(checkpointer=MemorySaver())  # ❌
   
   # 正确: 让API服务器处理持久化
   def create_graph():
       builder = StateGraph(MessagesState)
       # ... 添加节点和边  
       return builder.compile()  # ✅
   ```

3. **端口占用**
   ```bash
   # 更换端口
   langgraph dev --port 8000
   
   # 或杀死占用进程
   lsof -ti:3000 | xargs kill -9
   ```

## 🎯 最佳实践

### 1. 开发环境

```bash
# 开发时使用详细日志和调试
langgraph dev --debug-port 5678 --server-log-level DEBUG
```

### 2. 生产部署

```bash
# 构建生产镜像
langgraph build

# 使用环境变量配置
export POSTGRES_URI="postgresql://..."
langgraph up
```

### 3. 记忆管理

对于长对话，考虑实现消息裁剪或摘要机制：

```python
from langchain_core.messages.utils import trim_messages

def trim_hook(state):
    return {"messages": trim_messages(
        state["messages"], 
        max_tokens=1000,
        strategy="last"
    )}
```

## 📊 性能监控

- **队列统计**: 监控运行中和等待中的任务数量
- **Worker状态**: 跟踪可用和活跃的worker数量  
- **内存使用**: 关注内存中的状态数据大小
- **响应时间**: 监控端到端的请求处理时间

## 🔗 相关资源

- [LangGraph 官方文档](https://langchain-ai.github.io/langgraph/)
- [LangGraph Studio 指南](https://langchain-ai.github.io/langgraph/concepts/langgraph_studio/)
- [LangSmith 追踪](https://docs.smith.langchain.com/)
- [LangChain Academy](https://academy.langchain.com/)

---

🎉 **恭喜！** 你现在已经完全理解了LangGraph的工作原理和使用方式！
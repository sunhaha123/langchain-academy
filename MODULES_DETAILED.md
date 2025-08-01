# LangChain Academy 模块详细文档

## 📚 模块详细分析

### Module-0: 基础设置 (Basics)

#### 🎯 学习目标
- 掌握 LangChain 和 OpenAI API 的基础配置
- 理解 Chat Models 的核心概念
- 学习消息类型的使用方法
- 配置 Tavily 搜索工具

#### 📁 文件结构
```
module-0/
└── basics.ipynb          # 基础概念和配置教程
```

#### 🔧 核心技术要点
```python
# Chat Model 初始化
from langchain_openai import ChatOpenAI

# 支持代理配置
proxy_url = os.getenv("PROXY")  
llm = ChatOpenAI(
    model="gpt-4o",  # 或 gpt-3.5-turbo
    openai_proxy=proxy_url if proxy_url else None
)

# 消息类型使用
from langchain_core.messages import HumanMessage, AIMessage
messages = [HumanMessage(content="Hello, world!")]
response = llm.invoke(messages)
```

#### 📋 学习检查清单
- [ ] 成功配置 OpenAI API 密钥
- [ ] 理解 HumanMessage 和 AIMessage 的差异
- [ ] 掌握 Chat Model 的基本调用方式
- [ ] 配置 Tavily 搜索工具 (为 Module-4 做准备)

---

### Module-1: LangGraph 入门 (Introduction to LangGraph)

#### 🎯 学习目标
- 掌握 StateGraph 的构建和执行
- 理解节点(Node)和边(Edge)的概念
- 学习条件边(Conditional Edge)的使用
- 实现基础代理和记忆代理

#### 📁 文件结构
```
module-1/
├── simple-graph.ipynb     # 最简单的3节点图示例
├── chain.ipynb           # 链式图结构
├── router.ipynb          # 路由图实现
├── agent.ipynb           # 基础代理构建
├── agent-memory.ipynb    # 带记忆的代理
├── deployment.ipynb      # 部署相关
├── agent_graphs.py       # 主要的图定义文件
├── langgraph.json        # LangGraph配置文件
└── studio/               # Studio实践项目
    ├── agent.py          # React代理实现
    ├── router.py         # 路由逻辑
    └── simple.py         # 简单图示例
```

#### 🔧 核心技术要点

##### 1. 状态定义
```python
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add

class MessagesState(TypedDict):
    messages: Annotated[list[BaseMessage], add]  # add作为reducer
```

##### 2. 图构建模式
```python
from langgraph.graph import StateGraph

# 创建图构建器
builder = StateGraph(MessagesState)

# 添加节点
builder.add_node("assistant", assistant_node)
builder.add_node("tools", tool_node)

# 添加边
builder.add_edge("__start__", "assistant")
builder.add_conditional_edges(
    "assistant",
    should_continue,  # 条件函数
    {
        "tools": "tools",
        "__end__": "__end__"
    }
)

# 编译图
graph = builder.compile()
```

##### 3. 记忆机制
```python
from langgraph.checkpoint.memory import MemorySaver

# 添加记忆功能
memory = MemorySaver()
graph_with_memory = builder.compile(checkpointer=memory)

# 使用时指定线程ID
config = {"configurable": {"thread_id": "conversation-1"}}
result = graph_with_memory.invoke(input_data, config)
```

#### 📊 实践项目

##### React 代理 (studio/agent.py)
```python
# 工具定义
def add(a: int, b: int) -> int:
    """Add two integers."""
    return a + b

def multiply(a: int, b: int) -> int:
    """Multiply two integers."""
    return a * b

def divide(a: int, b: int) -> float:
    """Divide two integers."""
    return a / b

tools = [add, multiply, divide]

# 代理节点
def assistant(state: MessagesState):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

def should_continue(state: MessagesState) -> Literal["tools", "__end__"]:
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        return "tools"
    return "__end__"
```

#### 📋 学习检查清单
- [ ] 理解 StateGraph 的基本结构
- [ ] 掌握节点和边的添加方法
- [ ] 实现条件边的逻辑判断
- [ ] 成功构建带工具的 React 代理
- [ ] 实现记忆功能并测试多轮对话
- [ ] 使用 LangGraph Studio 可视化图执行

---

### Module-2: 状态管理和内存 (State Management & Memory)

#### 🎯 学习目标
- 掌握不同的状态定义方式
- 理解状态约减器(Reducer)的作用
- 学习消息修剪和过滤技术
- 实现外部记忆存储

#### 📁 文件结构
```
module-2/
├── state-schema.ipynb             # 状态模式定义方法
├── state-reducers.ipynb          # 状态约减器使用
├── multiple-schemas.ipynb        # 多状态模式管理
├── trim-filter-messages.ipynb   # 消息修剪和过滤
├── chatbot-summarization.ipynb  # 聊天机器人摘要
├── chatbot-external-memory.ipynb # 外部记忆存储
├── state_db/
│   └── example.db               # SQLite示例数据库
└── studio/
    ├── chatbot.py               # 完整聊天机器人实现
    ├── langgraph.json
    └── requirements.txt
```

#### 🔧 核心技术要点

##### 1. 三种状态定义方式
```python
# 方式1: TypedDict (简单快速)
from typing import TypedDict
class TypedDictState(TypedDict):
    messages: list[BaseMessage]
    user_info: str

# 方式2: Dataclass (结构化)
from dataclasses import dataclass
@dataclass
class DataclassState:
    messages: list[BaseMessage]
    user_info: str = ""

# 方式3: Pydantic (类型验证)
from pydantic import BaseModel, Field
class PydanticState(BaseModel):
    messages: list[BaseMessage] = Field(default_factory=list)
    user_info: str = Field(default="", description="用户信息")
```

##### 2. 状态约减器
```python
from typing import Annotated
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add

def add_messages(left: list, right: list) -> list:
    """自定义消息添加逻辑"""
    return left + right

class MessagesState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    
# 内置约减器
from langgraph.graph.message import add
messages: Annotated[list[BaseMessage], add]  # 默认追加
```

##### 3. 消息修剪策略
```python
from langchain_core.messages.utils import trim_messages

def trim_messages_node(state: MessagesState):
    """修剪消息以控制上下文长度"""
    trimmed = trim_messages(
        state["messages"],
        max_tokens=1000,           # 最大token数
        strategy="last",           # 保留最新的消息
        token_counter=len,         # token计数函数
        include_system=True,       # 保留系统消息
    )
    return {"messages": trimmed}
```

##### 4. 外部记忆存储
```python
import sqlite3
from datetime import datetime

class ExternalMemory:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY,
                user_id TEXT,
                content TEXT,
                timestamp DATETIME,
                memory_type TEXT
            )
        """)
        conn.commit()
        conn.close()
    
    def save_memory(self, user_id: str, content: str, memory_type: str = "conversation"):
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            "INSERT INTO memories (user_id, content, timestamp, memory_type) VALUES (?, ?, ?, ?)",
            (user_id, content, datetime.now(), memory_type)
        )
        conn.commit()
        conn.close()
```

#### 📊 实践项目示例

##### 带摘要的聊天机器人
```python
def summarize_conversation(state: MessagesState):
    """对长对话进行摘要"""
    messages = state["messages"]
    if len(messages) > 10:  # 超过10条消息时触发摘要
        conversation_text = "\n".join([m.content for m in messages])
        summary_prompt = f"请总结以下对话的要点:\n{conversation_text}"
        summary = llm.invoke([AIMessage(content=summary_prompt)])
        
        # 保留系统消息和摘要，清除历史
        return {
            "messages": [
                messages[0],  # 系统消息
                AIMessage(content=f"对话摘要: {summary.content}")
            ]
        }
    return {"messages": messages}
```

#### 📋 学习检查清单
- [ ] 理解三种状态定义方式的优缺点
- [ ] 掌握自定义状态约减器的实现
- [ ] 实现消息修剪和过滤逻辑
- [ ] 构建带摘要功能的聊天机器人
- [ ] 集成外部数据库进行记忆存储
- [ ] 测试不同状态模式的性能差异

---

### Module-3: 人机交互循环 (Human-in-the-Loop)

#### 🎯 学习目标
- 掌握断点(Breakpoint)的设置和使用
- 实现动态断点控制
- 学习状态编辑和人工反馈
- 理解流式处理中断机制
- 掌握时间旅行(Time Travel)调试

#### 📁 文件结构
```
module-3/
├── breakpoints.ipynb              # 基础断点功能
├── dynamic-breakpoints.ipynb     # 动态断点实现
├── edit-state-human-feedback.ipynb # 状态编辑和人工反馈
├── streaming-interruption.ipynb  # 流式处理中断
├── time-travel.ipynb            # 时间旅行调试
└── studio/
    ├── agent.py                 # 支持断点的代理
    ├── dynamic_breakpoints.py   # 动态断点控制
    ├── langgraph.json
    └── requirements.txt
```

#### 🔧 核心技术要点

##### 1. 基础断点设置
```python
from langgraph.checkpoint.memory import MemorySaver

# 在特定节点前设置断点
graph = builder.compile(
    checkpointer=MemorySaver(),
    interrupt_before=["human_feedback"],  # 在人工反馈节点前暂停
    interrupt_after=["critical_decision"] # 在关键决策节点后暂停
)

# 执行到断点
config = {"configurable": {"thread_id": "conversation-1"}}
result = graph.invoke(input_data, config)

# 恢复执行
result = graph.invoke(None, config)  # 传入None继续执行
```

##### 2. 动态断点控制
```python
def should_interrupt(state: MessagesState) -> bool:
    """动态判断是否需要中断"""
    last_message = state["messages"][-1]
    
    # 检查是否需要人工审核
    if "sensitive" in last_message.content.lower():
        return True
    
    # 检查置信度
    if hasattr(last_message, 'confidence') and last_message.confidence < 0.7:
        return True
    
    return False

def conditional_interrupt_node(state: MessagesState):
    """条件中断节点"""
    if should_interrupt(state):
        # 返回特殊状态指示需要中断
        return {"needs_human_review": True, "messages": state["messages"]}
    return {"messages": state["messages"]}
```

##### 3. 状态编辑和人工反馈
```python
# 获取当前状态
current_state = graph.get_state(config)
print(f"当前状态: {current_state.values}")

# 编辑状态
new_state = {
    "messages": current_state.values["messages"] + [
        HumanMessage(content="人工修正: 请重新生成更准确的回答")
    ]
}

# 更新状态
graph.update_state(config, new_state)

# 继续执行
result = graph.invoke(None, config)
```

##### 4. 流式处理中断
```python
def streaming_with_interrupt(graph, input_data, config):
    """支持中断的流式处理"""
    for chunk in graph.stream(input_data, config):
        # 检查是否需要中断
        if should_interrupt_streaming(chunk):
            print("检测到需要人工干预，暂停流式处理...")
            break
        
        # 处理数据块
        yield chunk
        
        # 检查用户输入
        if user_requested_stop():
            print("用户请求停止，中断处理...")
            break

def user_requested_stop():
    """检查用户是否请求停止 (简化示例)"""
    # 实际实现中可能检查文件、数据库或消息队列
    return False
```

##### 5. 时间旅行调试
```python
# 获取状态历史
state_history = graph.get_state_history(config)

print("状态历史:")
for i, state_snapshot in enumerate(state_history):
    print(f"步骤 {i}: {state_snapshot.config}")
    print(f"值: {state_snapshot.values}")
    print(f"下一步: {state_snapshot.next}")
    print("---")

# 回滚到特定状态
target_config = list(state_history)[2].config  # 回滚到第3个状态
graph.update_state(target_config, values=None)  # 回滚操作

# 从回滚点继续执行
result = graph.invoke(None, target_config)
```

#### 📊 实践项目示例

##### 智能客服代理 (支持人工介入)
```python
class CustomerServiceAgent:
    def __init__(self):
        self.graph = self.build_graph()
    
    def build_graph(self):
        builder = StateGraph(MessagesState)
        
        # 添加节点
        builder.add_node("analyze_query", self.analyze_query)
        builder.add_node("auto_respond", self.auto_respond)
        builder.add_node("human_handoff", self.human_handoff)
        builder.add_node("quality_check", self.quality_check)
        
        # 添加边和条件边
        builder.add_edge("__start__", "analyze_query")
        builder.add_conditional_edges(
            "analyze_query",
            self.should_handoff_to_human,
            {
                "human": "human_handoff",
                "auto": "auto_respond"
            }
        )
        builder.add_edge("auto_respond", "quality_check")
        builder.add_conditional_edges(
            "quality_check",
            self.quality_check_passed,
            {
                "pass": "__end__",
                "review": "human_handoff"
            }
        )
        
        return builder.compile(
            checkpointer=MemorySaver(),
            interrupt_before=["human_handoff"]  # 人工介入前暂停
        )
    
    def should_handoff_to_human(self, state: MessagesState):
        """判断是否需要人工介入"""
        query = state["messages"][-1].content
        
        # 复杂查询检测
        if len(query.split()) > 50:
            return "human"
        
        # 情感分析 - 检测负面情绪
        if any(word in query.lower() for word in ["angry", "frustrated", "complaint"]):
            return "human"
        
        # 技术问题检测
        if any(word in query.lower() for word in ["bug", "error", "not working"]):
            return "human"
        
        return "auto"
```

#### 📋 学习检查清单
- [ ] 掌握基础断点的设置和恢复
- [ ] 实现动态断点逻辑
- [ ] 学会状态编辑和更新操作
- [ ] 构建支持人工介入的工作流
- [ ] 实现流式处理的中断机制
- [ ] 掌握时间旅行调试技术
- [ ] 测试复杂的人机交互场景

---

### Module-4: 并行处理和子图 (Parallelization & Sub-graphs)

#### 🎯 学习目标
- 掌握 Map-Reduce 设计模式
- 实现任务并行化处理
- 学习子图的构建和管理
- 构建复杂的研究助手应用

#### 📁 文件结构
```
module-4/
├── map-reduce.ipynb           # Map-Reduce模式实现
├── parallelization.ipynb     # 并行处理技术
├── sub-graph.ipynb          # 子图构建和管理
├── research-assistant.ipynb # 研究助手综合应用
└── studio/
    ├── map_reduce.py         # Map-Reduce实现
    ├── parallelization.py    # 并行处理逻辑
    ├── sub_graphs.py         # 子图定义
    ├── research_assistant.py # 完整研究助手
    ├── langgraph.json
    └── requirements.txt
```

#### 🔧 核心技术要点

##### 1. Map-Reduce 模式
```python
from functools import reduce
from concurrent.futures import ThreadPoolExecutor

class MapReduceState(TypedDict):
    inputs: list[str]           # 输入数据列表
    mapped_results: list[dict]  # Map阶段结果
    final_result: dict          # Reduce阶段结果

def map_step(state: MapReduceState):
    """Map阶段：并行处理每个输入"""
    inputs = state["inputs"]
    
    def process_single_input(input_item):
        # 对单个输入进行处理
        return {
            "input": input_item,
            "processed": llm.invoke([HumanMessage(content=f"分析: {input_item}")]).content,
            "timestamp": datetime.now().isoformat()
        }
    
    # 并行处理
    with ThreadPoolExecutor(max_workers=4) as executor:
        mapped_results = list(executor.map(process_single_input, inputs))
    
    return {"mapped_results": mapped_results}

def reduce_step(state: MapReduceState):
    """Reduce阶段：合并所有结果"""
    results = state["mapped_results"]
    
    # 合并所有分析结果
    combined_analysis = "\n".join([r["processed"] for r in results])
    
    # 生成最终总结
    summary_prompt = f"请总结以下分析结果:\n{combined_analysis}"
    final_summary = llm.invoke([HumanMessage(content=summary_prompt)]).content
    
    return {
        "final_result": {
            "summary": final_summary,
            "individual_results": results,
            "total_processed": len(results)
        }
    }
```

##### 2. 并行节点执行
```python
from langgraph.graph import StateGraph

def build_parallel_graph():
    builder = StateGraph(MapReduceState)
    
    # 添加节点
    builder.add_node("input_preparation", prepare_inputs)
    builder.add_node("map_process", map_step)
    builder.add_node("reduce_process", reduce_step)
    
    # 串行执行
    builder.add_edge("__start__", "input_preparation")
    builder.add_edge("input_preparation", "map_process")
    builder.add_edge("map_process", "reduce_process")
    builder.add_edge("reduce_process", "__end__")
    
    return builder.compile()

# 使用并行处理工具
from langgraph.prebuilt import ToolNode
from concurrent.futures import as_completed

def parallel_tool_execution(state: MessagesState):
    """并行执行多个工具"""
    tools_to_execute = state.get("pending_tools", [])
    
    results = []
    with ThreadPoolExecutor(max_workers=3) as executor:
        # 提交所有工具执行任务
        future_to_tool = {
            executor.submit(execute_tool, tool): tool 
            for tool in tools_to_execute
        }
        
        # 收集结果
        for future in as_completed(future_to_tool):
            tool = future_to_tool[future]
            try:
                result = future.result()
                results.append({"tool": tool, "result": result})
            except Exception as exc:
                results.append({"tool": tool, "error": str(exc)})
    
    return {"tool_results": results}
```

##### 3. 子图构建和组合
```python
def build_analysis_subgraph():
    """构建分析子图"""
    sub_builder = StateGraph(AnalysisState)
    
    sub_builder.add_node("data_extraction", extract_data)
    sub_builder.add_node("data_analysis", analyze_data)
    sub_builder.add_node("result_formatting", format_results)
    
    sub_builder.add_edge("__start__", "data_extraction")
    sub_builder.add_edge("data_extraction", "data_analysis")
    sub_builder.add_edge("data_analysis", "result_formatting")
    sub_builder.add_edge("result_formatting", "__end__")
    
    return sub_builder.compile()

def build_main_graph():
    """构建主图，集成多个子图"""
    main_builder = StateGraph(MainState)
    
    # 创建子图实例
    analysis_subgraph = build_analysis_subgraph()
    
    # 添加子图作为节点
    main_builder.add_node("analysis", analysis_subgraph)
    main_builder.add_node("preprocessing", preprocess_data)
    main_builder.add_node("postprocessing", postprocess_results)
    
    main_builder.add_edge("__start__", "preprocessing")
    main_builder.add_edge("preprocessing", "analysis")
    main_builder.add_edge("analysis", "postprocessing")
    main_builder.add_edge("postprocessing", "__end__")
    
    return main_builder.compile()
```

##### 4. 研究助手应用架构
```python
class ResearchAssistant:
    """多代理研究助手系统"""
    
    def __init__(self):
        self.graph = self.build_research_graph()
    
    def build_research_graph(self):
        builder = StateGraph(ResearchState)
        
        # 研究规划阶段
        builder.add_node("plan_research", self.plan_research)
        builder.add_node("create_analysts", self.create_analysts)
        
        # 并行研究阶段
        builder.add_node("conduct_interviews", self.conduct_interviews)
        builder.add_node("gather_information", self.gather_information)
        
        # 结果合成阶段
        builder.add_node("synthesize_findings", self.synthesize_findings)
        builder.add_node("generate_report", self.generate_report)
        
        # 连接节点
        builder.add_edge("__start__", "plan_research")
        builder.add_edge("plan_research", "create_analysts")
        
        # 并行执行研究任务
        builder.add_edge("create_analysts", "conduct_interviews")
        builder.add_edge("create_analysts", "gather_information")
        
        # 等待并行任务完成后合成结果
        builder.add_edge(["conduct_interviews", "gather_information"], "synthesize_findings")
        builder.add_edge("synthesize_findings", "generate_report")
        builder.add_edge("generate_report", "__end__")
        
        return builder.compile()
    
    def create_analysts(self, state: ResearchState):
        """创建AI分析师团队"""
        research_topic = state["research_topic"]
        
        # 分解研究主题为子主题
        subtopics_prompt = f"""
        将研究主题 "{research_topic}" 分解为3-5个具体的子主题，
        每个子主题需要一个专门的分析师来研究。
        """
        
        subtopics_response = llm.invoke([HumanMessage(content=subtopics_prompt)])
        subtopics = self.parse_subtopics(subtopics_response.content)
        
        # 为每个子主题创建专门的分析师
        analysts = []
        for subtopic in subtopics:
            analyst = {
                "id": f"analyst_{len(analysts)}",
                "specialization": subtopic,
                "instructions": f"你是专门研究 {subtopic} 的AI分析师...",
                "tools": ["web_search", "document_analysis", "data_extraction"]
            }
            analysts.append(analyst)
        
        return {"analysts": analysts, "subtopics": subtopics}
    
    def conduct_interviews(self, state: ResearchState):
        """并行进行专家访谈"""
        analysts = state["analysts"]
        
        def interview_expert(analyst):
            """单个分析师进行专家访谈"""
            interview_prompt = f"""
            作为 {analyst['specialization']} 的专业分析师，
            请就这个主题进行深入的专家级分析...
            """
            
            expert_response = llm.invoke([HumanMessage(content=interview_prompt)])
            
            return {
                "analyst_id": analyst["id"],
                "specialization": analyst["specialization"],
                "interview_result": expert_response.content,
                "confidence_score": 0.85  # 模拟置信度评分
            }
        
        # 并行执行所有访谈
        with ThreadPoolExecutor(max_workers=len(analysts)) as executor:
            interview_results = list(executor.map(interview_expert, analysts))
        
        return {"interview_results": interview_results}
```

#### 📊 核心应用：智能研究助手

##### 功能特性
1. **动态团队生成**: 根据研究主题自动生成AI分析师团队
2. **并行信息收集**: 多个分析师同时进行研究
3. **专家级访谈**: 每个分析师与专家AI进行深度对话
4. **智能合成**: 将多个研究结果合成为统一报告
5. **可定制输出**: 支持多种报告格式和详细程度

##### 使用示例
```python
# 启动研究助手
research_topic = "人工智能在医疗诊断中的应用现状和未来趋势"
config = {"configurable": {"thread_id": "research_session_1"}}

result = research_assistant.invoke({
    "research_topic": research_topic,
    "output_format": "detailed_report",
    "required_sections": ["current_state", "challenges", "opportunities", "future_trends"]
}, config)

print(result["final_report"])
```

#### 📋 学习检查清单
- [ ] 理解 Map-Reduce 模式的原理和应用
- [ ] 实现任务的并行化处理
- [ ] 掌握子图的构建和组合技术
- [ ] 构建完整的研究助手应用
- [ ] 测试并行处理的性能优势
- [ ] 优化多代理协作的效率
- [ ] 处理并发执行中的错误和异常

---

### Module-5: 长期记忆系统 (Long-term Memory)

#### 🎯 学习目标
- 实现语义记忆存储和检索
- 掌握用户档案(Profile)管理
- 学习记忆集合(Collection)的使用
- 构建具有长期记忆的智能代理

#### 📁 文件结构
```
module-5/
├── memory_store.ipynb              # 记忆存储基础
├── memoryschema_profile.ipynb     # 用户档案记忆模式
├── memoryschema_collection.ipynb  # 集合记忆模式
├── memory_agent.ipynb             # 记忆代理实现
└── studio/
    ├── memory_store.py             # 记忆存储实现
    ├── memoryschema_profile.py     # 档案模式定义
    ├── memoryschema_collection.py  # 集合模式定义
    ├── memory_agent.py             # 完整记忆代理
    ├── configuration.py            # 配置管理
    ├── langgraph.json
    └── requirements.txt
```

#### 🔧 核心技术要点

##### 1. 记忆存储基础架构
```python
from langchain_core.memory import BaseMemory
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
import json
from datetime import datetime
from typing import Dict, List, Any

class SemanticMemoryStore:
    """语义记忆存储系统"""
    
    def __init__(self, embedding_model="text-embedding-ada-002"):
        self.embeddings = OpenAIEmbeddings(model=embedding_model)
        self.vector_store = None
        self.metadata_store = {}  # 存储记忆的元数据
        
    def initialize_store(self, memory_documents: List[str] = None):
        """初始化向量存储"""
        if memory_documents:
            self.vector_store = FAISS.from_texts(
                memory_documents, 
                self.embeddings
            )
        else:
            # 创建空的向量存储
            self.vector_store = FAISS.from_texts(
                ["初始化文档"], 
                self.embeddings
            )
    
    def save_memory(self, content: str, memory_type: str, metadata: Dict[str, Any] = None):
        """保存记忆到向量存储"""
        memory_id = f"memory_{datetime.now().timestamp()}"
        
        # 保存到向量存储
        self.vector_store.add_texts(
            [content],
            metadatas=[{
                "memory_id": memory_id,
                "memory_type": memory_type,
                "timestamp": datetime.now().isoformat(),
                **(metadata or {})
            }]
        )
        
        # 保存详细元数据
        self.metadata_store[memory_id] = {
            "content": content,
            "memory_type": memory_type,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        
        return memory_id
    
    def retrieve_memories(self, query: str, k: int = 5, memory_type: str = None):
        """检索相关记忆"""
        # 语义搜索
        results = self.vector_store.similarity_search_with_score(query, k=k)
        
        # 过滤记忆类型
        if memory_type:
            results = [
                (doc, score) for doc, score in results
                if doc.metadata.get("memory_type") == memory_type
            ]
        
        return results
```

##### 2. 用户档案记忆模式
```python
from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from enum import Enum

class ProfileMemoryType(str, Enum):
    PREFERENCE = "preference"      # 用户偏好
    BEHAVIOR = "behavior"         # 行为模式
    BACKGROUND = "background"     # 背景信息
    SKILL = "skill"              # 技能和专长
    GOAL = "goal"                # 目标和意图

class UserProfile(BaseModel):
    """用户档案数据模型"""
    user_id: str = Field(description="用户唯一标识")
    name: Optional[str] = Field(default=None, description="用户姓名")
    preferences: Dict[str, Any] = Field(default_factory=dict, description="用户偏好")
    skills: List[str] = Field(default_factory=list, description="用户技能")
    goals: List[str] = Field(default_factory=list, description="用户目标")
    behavior_patterns: Dict[str, Any] = Field(default_factory=dict, description="行为模式")
    background_info: Dict[str, Any] = Field(default_factory=dict, description="背景信息")
    last_updated: str = Field(default_factory=lambda: datetime.now().isoformat())

class ProfileMemoryManager:
    """用户档案记忆管理器"""
    
    def __init__(self, memory_store: SemanticMemoryStore):
        self.memory_store = memory_store
        self.profiles: Dict[str, UserProfile] = {}
    
    def update_profile(self, user_id: str, update_data: Dict[str, Any], 
                      memory_type: ProfileMemoryType):
        """更新用户档案"""
        if user_id not in self.profiles:
            self.profiles[user_id] = UserProfile(user_id=user_id)
        
        profile = self.profiles[user_id]
        
        # 根据记忆类型更新不同字段
        if memory_type == ProfileMemoryType.PREFERENCE:
            profile.preferences.update(update_data)
        elif memory_type == ProfileMemoryType.SKILL:
            new_skills = update_data.get("skills", [])
            profile.skills.extend([s for s in new_skills if s not in profile.skills])
        elif memory_type == ProfileMemoryType.GOAL:
            new_goals = update_data.get("goals", [])
            profile.goals.extend([g for g in new_goals if g not in profile.goals])
        elif memory_type == ProfileMemoryType.BEHAVIOR:
            profile.behavior_patterns.update(update_data)
        elif memory_type == ProfileMemoryType.BACKGROUND:
            profile.background_info.update(update_data)
        
        profile.last_updated = datetime.now().isoformat()
        
        # 保存到记忆存储
        memory_content = f"用户 {user_id} 的 {memory_type.value} 信息: {json.dumps(update_data, ensure_ascii=False)}"
        self.memory_store.save_memory(
            content=memory_content,
            memory_type=f"profile_{memory_type.value}",
            metadata={
                "user_id": user_id,
                "profile_field": memory_type.value
            }
        )
    
    def get_profile(self, user_id: str) -> Optional[UserProfile]:
        """获取用户档案"""
        return self.profiles.get(user_id)
    
    def get_relevant_profile_info(self, user_id: str, context: str) -> Dict[str, Any]:
        """根据上下文获取相关的档案信息"""
        # 检索相关记忆
        memories = self.memory_store.retrieve_memories(
            query=context,
            k=5,
            memory_type=f"profile_"
        )
        
        # 过滤当前用户的记忆
        user_memories = [
            (doc, score) for doc, score in memories
            if doc.metadata.get("user_id") == user_id
        ]
        
        relevant_info = {
            "preferences": {},
            "skills": [],
            "goals": [],
            "behavior_patterns": {},
            "background_info": {}
        }
        
        for doc, score in user_memories:
            if score < 0.8:  # 相似度阈值
                profile_field = doc.metadata.get("profile_field")
                if profile_field in relevant_info:
                    # 解析记忆内容并添加到相关信息中
                    try:
                        content_data = json.loads(doc.page_content.split(": ", 1)[1])
                        if isinstance(relevant_info[profile_field], dict):
                            relevant_info[profile_field].update(content_data)
                        elif isinstance(relevant_info[profile_field], list):
                            relevant_info[profile_field].extend(content_data.get(profile_field, []))
                    except:
                        pass
        
        return relevant_info
```

##### 3. 集合记忆模式
```python
class CollectionMemoryManager:
    """集合记忆管理器 - 管理相关记忆的集合"""
    
    def __init__(self, memory_store: SemanticMemoryStore):
        self.memory_store = memory_store
        self.collections: Dict[str, Dict[str, Any]] = {}
    
    def create_collection(self, collection_id: str, description: str, 
                         tags: List[str] = None) -> str:
        """创建记忆集合"""
        self.collections[collection_id] = {
            "description": description,
            "tags": tags or [],
            "memory_ids": [],
            "created_at": datetime.now().isoformat(),
            "last_accessed": datetime.now().isoformat()
        }
        
        # 将集合信息保存到记忆存储
        collection_content = f"记忆集合: {description}"
        memory_id = self.memory_store.save_memory(
            content=collection_content,
            memory_type="collection_meta",
            metadata={
                "collection_id": collection_id,
                "tags": tags or []
            }
        )
        
        return collection_id
    
    def add_to_collection(self, collection_id: str, content: str, 
                         content_type: str = "general"):
        """向集合添加记忆"""
        if collection_id not in self.collections:
            raise ValueError(f"集合 {collection_id} 不存在")
        
        # 保存记忆并关联到集合
        memory_id = self.memory_store.save_memory(
            content=content,
            memory_type=f"collection_item_{content_type}",
            metadata={
                "collection_id": collection_id,
                "content_type": content_type
            }
        )
        
        # 更新集合
        self.collections[collection_id]["memory_ids"].append(memory_id)
        self.collections[collection_id]["last_accessed"] = datetime.now().isoformat()
        
        return memory_id
    
    def query_collection(self, collection_id: str, query: str, k: int = 5):
        """查询集合中的相关记忆"""
        if collection_id not in self.collections:
            return []
        
        # 检索集合中的记忆
        all_memories = self.memory_store.retrieve_memories(query, k=k*2)
        
        # 过滤属于指定集合的记忆
        collection_memories = [
            (doc, score) for doc, score in all_memories
            if doc.metadata.get("collection_id") == collection_id
        ]
        
        # 更新访问时间
        self.collections[collection_id]["last_accessed"] = datetime.now().isoformat()
        
        return collection_memories[:k]
    
    def get_collection_summary(self, collection_id: str) -> Dict[str, Any]:
        """获取集合摘要"""
        if collection_id not in self.collections:
            return {}
        
        collection = self.collections[collection_id]
        
        # 获取集合中的所有记忆
        memories = self.query_collection(collection_id, collection["description"], k=20)
        
        # 生成摘要
        if memories:
            memory_contents = [doc.page_content for doc, _ in memories]
            summary_prompt = f"""
            请总结以下记忆集合的主要内容:
            集合描述: {collection['description']}
            记忆内容: {' | '.join(memory_contents[:10])}  # 限制长度
            """
            
            summary = llm.invoke([HumanMessage(content=summary_prompt)]).content
        else:
            summary = "集合中暂无记忆内容"
        
        return {
            "collection_id": collection_id,
            "description": collection["description"],
            "memory_count": len(collection["memory_ids"]),
            "tags": collection["tags"],
            "summary": summary,
            "created_at": collection["created_at"],
            "last_accessed": collection["last_accessed"]
        }
```

##### 4. 智能记忆代理
```python
from trustcall import create_tool

class MemoryAgent:
    """具有长期记忆能力的智能代理"""
    
    def __init__(self):
        self.memory_store = SemanticMemoryStore()
        self.profile_manager = ProfileMemoryManager(self.memory_store)
        self.collection_manager = CollectionMemoryManager(self.memory_store)
        self.graph = self.build_memory_graph()
        
        # 初始化记忆存储
        self.memory_store.initialize_store()
    
    def build_memory_graph(self):
        """构建带记忆功能的图"""
        
        # 定义记忆工具
        @create_tool
        def save_user_preference(preference_type: str, preference_value: str, user_id: str = "default") -> str:
            """保存用户偏好信息"""
            self.profile_manager.update_profile(
                user_id, 
                {preference_type: preference_value},
                ProfileMemoryType.PREFERENCE
            )
            return f"已保存用户偏好: {preference_type} = {preference_value}"
        
        @create_tool
        def recall_memories(query: str, user_id: str = "default") -> str:
            """回忆相关记忆"""
            memories = self.memory_store.retrieve_memories(query, k=3)
            if memories:
                recalled = [f"记忆 {i+1}: {doc.page_content}" for i, (doc, score) in enumerate(memories)]
                return "\\n".join(recalled)
            return "未找到相关记忆"
        
        @create_tool
        def create_memory_collection(name: str, description: str) -> str:
            """创建记忆集合"""
            collection_id = self.collection_manager.create_collection(name, description)
            return f"已创建记忆集合: {collection_id}"
        
        tools = [save_user_preference, recall_memories, create_memory_collection]
        
        # 构建图
        builder = StateGraph(MessagesState)
        
        builder.add_node("memory_assistant", self.memory_assistant_node)
        builder.add_node("tools", ToolNode(tools))
        builder.add_node("memory_decision", self.memory_decision_node)
        
        builder.add_edge("__start__", "memory_assistant")
        builder.add_conditional_edges(
            "memory_assistant",
            self.should_use_tools,
            {
                "tools": "tools",
                "memory": "memory_decision",
                "end": "__end__"
            }
        )
        builder.add_edge("tools", "memory_decision")
        builder.add_edge("memory_decision", "__end__")
        
        return builder.compile(checkpointer=MemorySaver())
    
    def memory_assistant_node(self, state: MessagesState):
        """记忆助手节点"""
        messages = state["messages"]
        last_message = messages[-1]
        
        # 检索相关记忆来增强回答
        relevant_memories = self.memory_store.retrieve_memories(
            last_message.content, k=3
        )
        
        # 构建包含记忆上下文的系统消息
        memory_context = ""
        if relevant_memories:
            memory_context = "\\n".join([
                f"相关记忆: {doc.page_content}" 
                for doc, score in relevant_memories[:2]
            ])
        
        system_message = SystemMessage(content=f"""
        你是一个具有长期记忆能力的智能助手。
        
        当前相关记忆:
        {memory_context}
        
        请基于这些记忆和当前对话来回答用户的问题。
        如果需要保存新的记忆或偏好，请使用适当的工具。
        """)
        
        # 调用LLM
        response = llm_with_tools.invoke([system_message] + messages)
        return {"messages": [response]}
    
    def memory_decision_node(self, state: MessagesState):
        """记忆决策节点 - 决定是否需要保存记忆"""
        messages = state["messages"]
        last_response = messages[-1]
        
        # 分析对话内容，决定是否保存记忆
        should_save = self.should_save_memory(messages)
        
        if should_save:
            # 提取关键信息并保存
            key_info = self.extract_key_information(messages)
            for info in key_info:
                self.memory_store.save_memory(
                    content=info["content"],
                    memory_type=info["type"],
                    metadata={"user_id": "default", "conversation_turn": len(messages)}
                )
        
        return {"messages": messages}
    
    def should_save_memory(self, messages: List[BaseMessage]) -> bool:
        """判断是否应该保存记忆"""
        recent_messages = messages[-3:]  # 分析最近3条消息
        
        # 检查是否包含重要信息的关键词
        important_keywords = [
            "我喜欢", "我不喜欢", "我的目标", "我的工作", 
            "记住", "重要", "下次", "以后"
        ]
        
        for message in recent_messages:
            if any(keyword in message.content for keyword in important_keywords):
                return True
        
        return False
    
    def extract_key_information(self, messages: List[BaseMessage]) -> List[Dict[str, str]]:
        """从对话中提取关键信息"""
        recent_conversation = "\\n".join([m.content for m in messages[-5:]])
        
        extraction_prompt = f"""
        从以下对话中提取需要记住的关键信息:
        {recent_conversation}
        
        请返回JSON格式的关键信息列表，每个信息包含content和type字段。
        type可以是: preference, fact, goal, skill, background
        """
        
        try:
            response = llm.invoke([HumanMessage(content=extraction_prompt)])
            # 这里应该使用更robust的JSON解析
            key_info = json.loads(response.content)
            return key_info if isinstance(key_info, list) else []
        except:
            return []
```

#### 📊 核心应用：task_mAIstro

task_mAIstro 是一个具有长期记忆能力的个人任务管理助手：

##### 主要特性
1. **智能记忆决策**: 自动判断什么信息值得长期保存
2. **用户偏好学习**: 学习用户的工作习惯和偏好
3. **程序性记忆**: 记住用户创建待办事项的模式
4. **上下文感知**: 基于历史交互提供个性化建议

##### 使用示例
```python
# 创建记忆代理实例
memory_agent = MemoryAgent()

# 用户交互
config = {"configurable": {"thread_id": "user_session_1"}}

# 第一次交互 - 学习用户偏好
result1 = memory_agent.invoke({
    "messages": [HumanMessage(content="我喜欢在早上完成重要任务，下午处理邮件")]
}, config)

# 后续交互 - 基于记忆提供建议
result2 = memory_agent.invoke({
    "messages": [HumanMessage(content="帮我安排明天的任务")]
}, config)
```

#### 📋 学习检查清单
- [ ] 理解语义记忆存储的原理和实现
- [ ] 掌握用户档案的结构化存储
- [ ] 实现记忆集合的管理和查询
- [ ] 构建智能记忆决策逻辑
- [ ] 集成向量数据库进行语义搜索
- [ ] 测试长期记忆的准确性和效率
- [ ] 实现记忆的更新和过期机制

---

### Module-6: 生产部署 (Production Deployment)

#### 🎯 学习目标
- 掌握助手(Assistants)的创建和管理
- 学习配置版本控制
- 实现生产环境部署
- 处理双重文本和连接管理

#### 📁 文件结构
```
module-6/
├── assistant.ipynb            # 助手管理基础
├── creating.ipynb            # 助手创建流程
├── connecting.ipynb          # 连接管理
├── double-texting.ipynb      # 双重文本处理
└── deployment/               # 生产部署配置
    ├── task_maistro.py       # 生产级应用
    ├── configuration.py      # 配置管理
    ├── docker-compose-example.yml # Docker部署
    ├── langgraph.json        # 部署配置
    └── requirements.txt      # 生产依赖
```

#### 🔧 核心技术要点

##### 1. 助手系统架构
```python
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from enum import Enum
import uuid
from datetime import datetime

class AssistantConfig(BaseModel):
    """助手配置模型"""
    assistant_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str = Field(description="助手名称")
    description: str = Field(description="助手描述")
    graph_id: str = Field(description="关联的图ID")
    version: str = Field(default="v1.0.0", description="版本号")
    config: Dict[str, Any] = Field(default_factory=dict, description="配置参数")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="元数据")
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    is_active: bool = Field(default=True, description="是否激活")

class AssistantManager:
    """助手管理器"""
    
    def __init__(self):
        self.assistants: Dict[str, AssistantConfig] = {}
        self.graph_registry: Dict[str, Any] = {}
    
    def register_graph(self, graph_id: str, graph_instance: Any, 
                      description: str = ""):
        """注册图实例"""
        self.graph_registry[graph_id] = {
            "instance": graph_instance,
            "description": description,
            "registered_at": datetime.now().isoformat()
        }
    
    def create_assistant(self, name: str, graph_id: str, 
                        config: Dict[str, Any] = None) -> AssistantConfig:
        """创建新助手"""
        if graph_id not in self.graph_registry:
            raise ValueError(f"图 {graph_id} 未注册")
        
        assistant_config = AssistantConfig(
            name=name,
            description=f"基于 {graph_id} 的智能助手",
            graph_id=graph_id,
            config=config or {}
        )
        
        self.assistants[assistant_config.assistant_id] = assistant_config
        return assistant_config
    
    def update_assistant(self, assistant_id: str, 
                        updates: Dict[str, Any]) -> AssistantConfig:
        """更新助手配置"""
        if assistant_id not in self.assistants:
            raise ValueError(f"助手 {assistant_id} 不存在")
        
        assistant = self.assistants[assistant_id]
        
        # 更新字段
        for key, value in updates.items():
            if hasattr(assistant, key):
                setattr(assistant, key, value)
        
        assistant.updated_at = datetime.now().isoformat()
        return assistant
    
    def get_assistant(self, assistant_id: str) -> Optional[AssistantConfig]:
        """获取助手配置"""
        return self.assistants.get(assistant_id)
    
    def list_assistants(self, active_only: bool = True) -> List[AssistantConfig]:
        """列出所有助手"""
        assistants = list(self.assistants.values())
        if active_only:
            assistants = [a for a in assistants if a.is_active]
        return assistants
    
    def invoke_assistant(self, assistant_id: str, input_data: Dict[str, Any], 
                        config: Dict[str, Any] = None) -> Any:
        """调用助手执行任务"""
        assistant = self.get_assistant(assistant_id)
        if not assistant or not assistant.is_active:
            raise ValueError(f"助手 {assistant_id} 不存在或未激活")
        
        # 获取图实例
        graph_info = self.graph_registry[assistant.graph_id]
        graph = graph_info["instance"]
        
        # 合并配置
        execution_config = {**(config or {}), **assistant.config}
        
        # 执行图
        return graph.invoke(input_data, execution_config)
```

##### 2. 配置版本控制
```python
class ConfigurationManager:
    """配置版本控制管理器"""
    
    def __init__(self):
        self.config_history: Dict[str, List[Dict[str, Any]]] = {}
        self.current_configs: Dict[str, Dict[str, Any]] = {}
    
    def set_config(self, config_key: str, config_value: Dict[str, Any], 
                   version: str = None):
        """设置配置并保存历史版本"""
        if version is None:
            version = f"v{len(self.config_history.get(config_key, []))+1}.0.0"
        
        # 保存历史版本
        if config_key not in self.config_history:
            self.config_history[config_key] = []
        
        self.config_history[config_key].append({
            "version": version,
            "config": config_value.copy(),
            "timestamp": datetime.now().isoformat()
        })
        
        # 更新当前配置
        self.current_configs[config_key] = config_value
    
    def get_config(self, config_key: str, version: str = None) -> Dict[str, Any]:
        """获取配置（指定版本或当前版本）"""
        if version is None:
            return self.current_configs.get(config_key, {})
        
        # 查找指定版本
        history = self.config_history.get(config_key, [])
        for config_entry in history:
            if config_entry["version"] == version:
                return config_entry["config"]
        
        raise ValueError(f"未找到配置 {config_key} 的版本 {version}")
    
    def rollback_config(self, config_key: str, target_version: str):
        """回滚配置到指定版本"""
        target_config = self.get_config(config_key, target_version)
        self.current_configs[config_key] = target_config.copy()
        
        # 记录回滚操作
        rollback_entry = {
            "version": f"rollback_to_{target_version}",
            "config": target_config.copy(),
            "timestamp": datetime.now().isoformat(),
            "rollback_from": self.config_history[config_key][-1]["version"]
        }
        self.config_history[config_key].append(rollback_entry)
    
    def list_versions(self, config_key: str) -> List[Dict[str, str]]:
        """列出配置的所有版本"""
        history = self.config_history.get(config_key, [])
        return [
            {
                "version": entry["version"],
                "timestamp": entry["timestamp"],
                "is_rollback": "rollback_to_" in entry["version"]
            }
            for entry in history
        ]
```

##### 3. 生产部署配置
```python
# docker-compose-example.yml 配置
docker_compose_config = """
version: '3.8'

services:
  langgraph-api:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - LANGCHAIN_API_KEY=${LANGCHAIN_API_KEY}
      - LANGCHAIN_TRACING_V2=true
      - POSTGRES_URI=postgresql://user:password@postgres:5432/langgraph
    depends_on:
      - postgres
      - redis
    volumes:
      - ./data:/app/data
    restart: unless-stopped
    
  postgres:
    image: postgres:15
    environment:
      - POSTGRES_DB=langgraph
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    restart: unless-stopped
    
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped
    
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - langgraph-api
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
"""

# 生产环境配置类
class ProductionConfig:
    """生产环境配置"""
    
    def __init__(self):
        self.load_config()
    
    def load_config(self):
        """加载生产配置"""
        self.database_url = os.getenv("POSTGRES_URI", "sqlite:///production.db")
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        self.api_host = os.getenv("API_HOST", "0.0.0.0")
        self.api_port = int(os.getenv("API_PORT", "8000"))
        self.worker_count = int(os.getenv("WORKER_COUNT", "4"))
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.enable_cors = os.getenv("ENABLE_CORS", "true").lower() == "true"
        self.cors_origins = os.getenv("CORS_ORIGINS", "*").split(",")
        
        # 安全配置
        self.api_key_required = os.getenv("API_KEY_REQUIRED", "false").lower() == "true"
        self.allowed_api_keys = os.getenv("ALLOWED_API_KEYS", "").split(",")
        
        # 性能配置
        self.request_timeout = int(os.getenv("REQUEST_TIMEOUT", "300"))
        self.max_request_size = int(os.getenv("MAX_REQUEST_SIZE", "10485760"))  # 10MB
        
        # 监控配置
        self.enable_metrics = os.getenv("ENABLE_METRICS", "true").lower() == "true"
        self.metrics_port = int(os.getenv("METRICS_PORT", "9090"))
```

##### 4. 双重文本处理和连接管理
```python
from asyncio import Queue, Event
from typing import AsyncGenerator
import asyncio

class ConnectionManager:
    """连接管理器 - 处理WebSocket连接和双重文本"""
    
    def __init__(self):
        self.active_connections: Dict[str, Dict[str, Any]] = {}
        self.message_queues: Dict[str, Queue] = {}
        self.processing_locks: Dict[str, Event] = {}
    
    async def connect(self, connection_id: str, websocket = None):
        """建立连接"""
        self.active_connections[connection_id] = {
            "websocket": websocket,
            "connected_at": datetime.now().isoformat(),
            "last_activity": datetime.now().isoformat(),
            "message_count": 0
        }
        self.message_queues[connection_id] = Queue()
        self.processing_locks[connection_id] = Event()
        self.processing_locks[connection_id].set()  # 初始状态为可处理
    
    async def disconnect(self, connection_id: str):
        """断开连接"""
        if connection_id in self.active_connections:
            del self.active_connections[connection_id]
        if connection_id in self.message_queues:
            del self.message_queues[connection_id]
        if connection_id in self.processing_locks:
            del self.processing_locks[connection_id]
    
    async def handle_message(self, connection_id: str, message: str) -> bool:
        """处理消息 - 防止双重文本"""
        if connection_id not in self.active_connections:
            return False
        
        # 检查是否正在处理消息
        processing_lock = self.processing_locks[connection_id]
        if not processing_lock.is_set():
            # 正在处理中，这是双重文本
            await self.send_response(connection_id, {
                "type": "warning",
                "message": "正在处理您的消息，请稍候..."
            })
            return False
        
        # 设置处理锁
        processing_lock.clear()
        
        try:
            # 添加到消息队列
            await self.message_queues[connection_id].put({
                "message": message,
                "timestamp": datetime.now().isoformat(),
                "message_id": str(uuid.uuid4())
            })
            
            # 更新连接信息
            self.active_connections[connection_id]["last_activity"] = datetime.now().isoformat()
            self.active_connections[connection_id]["message_count"] += 1
            
            return True
            
        finally:
            # 释放处理锁
            processing_lock.set()
    
    async def process_message_queue(self, connection_id: str, assistant_manager: AssistantManager):
        """处理消息队列"""
        if connection_id not in self.message_queues:
            return
        
        queue = self.message_queues[connection_id]
        
        while not queue.empty():
            try:
                message_data = await queue.get()
                
                # 处理消息
                await self.send_response(connection_id, {
                    "type": "processing",
                    "message": "正在处理您的消息..."
                })
                
                # 这里调用助手处理消息
                # response = await assistant_manager.invoke_assistant(...)
                
                await self.send_response(connection_id, {
                    "type": "response",
                    "message": "处理完成的回答...",
                    "message_id": message_data["message_id"]
                })
                
            except Exception as e:
                await self.send_response(connection_id, {
                    "type": "error",
                    "message": f"处理消息时出错: {str(e)}"
                })
    
    async def send_response(self, connection_id: str, response: Dict[str, Any]):
        """发送响应"""
        if connection_id not in self.active_connections:
            return
        
        connection = self.active_connections[connection_id]
        websocket = connection.get("websocket")
        
        if websocket:
            try:
                await websocket.send_json(response)
            except Exception as e:
                print(f"发送响应失败: {e}")
                # 连接可能已断开，清理连接
                await self.disconnect(connection_id)

class DoubleTextingHandler:
    """双重文本处理器"""
    
    def __init__(self, debounce_time: float = 1.0):
        self.debounce_time = debounce_time
        self.pending_messages: Dict[str, Dict[str, Any]] = {}
        self.timers: Dict[str, asyncio.Task] = {}
    
    async def handle_input(self, user_id: str, message: str, 
                          callback: callable) -> bool:
        """处理用户输入，防止双重发送"""
        # 取消之前的定时器
        if user_id in self.timers:
            self.timers[user_id].cancel()
        
        # 更新待处理消息
        self.pending_messages[user_id] = {
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "callback": callback
        }
        
        # 设置新的定时器
        self.timers[user_id] = asyncio.create_task(
            self._process_after_delay(user_id)
        )
        
        return True
    
    async def _process_after_delay(self, user_id: str):
        """延迟处理消息"""
        await asyncio.sleep(self.debounce_time)
        
        if user_id in self.pending_messages:
            message_data = self.pending_messages[user_id]
            callback = message_data["callback"]
            
            try:
                await callback(message_data["message"])
            except Exception as e:
                print(f"处理消息时出错: {e}")
            finally:
                # 清理
                if user_id in self.pending_messages:
                    del self.pending_messages[user_id]
                if user_id in self.timers:
                    del self.timers[user_id]
```

#### 📊 生产级应用：task_mAIstro

##### 完整的生产部署示例
```python
# 生产级 task_mAIstro 应用
class ProductionTaskMaistro:
    """生产级任务管理助手"""
    
    def __init__(self, config: ProductionConfig):
        self.config = config
        self.assistant_manager = AssistantManager()
        self.connection_manager = ConnectionManager()
        self.double_texting_handler = DoubleTextingHandler()
        self.config_manager = ConfigurationManager()
        
        # 初始化核心组件
        self.setup_assistants()
        self.setup_monitoring()
    
    def setup_assistants(self):
        """设置助手"""
        # 注册任务管理图
        task_graph = self.build_task_management_graph()
        self.assistant_manager.register_graph(
            "task_manager", 
            task_graph, 
            "智能任务管理助手"
        )
        
        # 创建默认助手
        self.assistant_manager.create_assistant(
            name="task_mAIstro",
            graph_id="task_manager",
            config={
                "memory_enabled": True,
                "learning_enabled": True,
                "max_context_length": 4000
            }
        )
    
    def setup_monitoring(self):
        """设置监控"""
        if self.config.enable_metrics:
            # 设置 Prometheus 指标
            # 设置日志记录
            # 设置健康检查
            pass
    
    async def start_server(self):
        """启动生产服务器"""
        from fastapi import FastAPI, WebSocket
        from fastapi.middleware.cors import CORSMiddleware
        
        app = FastAPI(title="task_mAIstro API", version="1.0.0")
        
        # 添加 CORS 中间件
        if self.config.enable_cors:
            app.add_middleware(
                CORSMiddleware,
                allow_origins=self.config.cors_origins,
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )
        
        # API 路由
        @app.post("/assistants/{assistant_id}/invoke")
        async def invoke_assistant(assistant_id: str, request: Dict[str, Any]):
            return self.assistant_manager.invoke_assistant(assistant_id, request)
        
        @app.websocket("/ws/{connection_id}")
        async def websocket_endpoint(websocket: WebSocket, connection_id: str):
            await websocket.accept()
            await self.connection_manager.connect(connection_id, websocket)
            
            try:
                while True:
                    message = await websocket.receive_text()
                    await self.connection_manager.handle_message(connection_id, message)
                    await self.connection_manager.process_message_queue(
                        connection_id, self.assistant_manager
                    )
            except Exception as e:
                print(f"WebSocket 错误: {e}")
            finally:
                await self.connection_manager.disconnect(connection_id)
        
        # 启动服务器
        import uvicorn
        await uvicorn.run(
            app,
            host=self.config.api_host,
            port=self.config.api_port,
            workers=self.config.worker_count
        )
```

#### 📋 学习检查清单
- [ ] 理解助手系统的架构和管理
- [ ] 掌握配置版本控制的实现
- [ ] 学会 Docker 容器化部署
- [ ] 实现 WebSocket 连接管理
- [ ] 处理双重文本和消息防重
- [ ] 配置生产环境的监控和日志
- [ ] 测试高并发场景下的性能
- [ ] 实现健康检查和故障恢复

---

## 🎯 学习成果总结

通过完成所有模块的学习，您将获得：

### 核心技能
- ✅ 从零开始构建 LangGraph 应用
- ✅ 实现复杂的多代理协作系统
- ✅ 掌握状态管理和长期记忆
- ✅ 构建生产级智能应用

### 实际项目经验
- ✅ 对话式 AI 应用开发
- ✅ 研究助手系统构建  
- ✅ 个人任务管理助手
- ✅ 企业级部署和维护

### 技术栈精通
- ✅ LangChain/LangGraph 生态系统
- ✅ 向量数据库和语义搜索
- ✅ 容器化和微服务架构
- ✅ AI 应用监控和调试

准备好开始您的 LangGraph 学习之旅了吗？从 Module-0 开始，一步步掌握构建智能代理应用的核心技能！
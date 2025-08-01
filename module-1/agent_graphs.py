"""
LangGraph Studio 图定义文件
将 agent-memory.ipynb 中的图导出为可导入的 Python 模块
"""

import os
from dotenv import load_dotenv
load_dotenv()

# 导入必需的库
from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState, START, StateGraph
from langgraph.prebuilt import tools_condition, ToolNode
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import SystemMessage

# 获取代理
proxy = os.environ.get("PROXY")

# 定义工具
def multiply(a: int, b: int) -> int:
    """Multiply a and b.

    Args:
        a: first int
        b: second int
    """
    return a * b

def add(a: int, b: int) -> int:
    """Adds a and b.

    Args:
        a: first int
        b: second int
    """
    return a + b

def divide(a: int, b: int) -> float:
    """Divide a and b.

    Args:
        a: first int
        b: second int
    """
    return a / b

# 工具列表
tools = [add, multiply, divide]

# 创建 LLM
llm = ChatOpenAI(model="gpt-4o", openai_proxy=f"http://{proxy}" if proxy else None)
llm_with_tools = llm.bind_tools(tools)

# 系统消息
sys_msg = SystemMessage(content="You are a helpful assistant tasked with performing arithmetic on a set of inputs.")

# 助手节点
def assistant(state: MessagesState):
    return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]}

# 创建基础图（无记忆）
def create_basic_graph():
    """创建基础的 React 图（无记忆）"""
    builder = StateGraph(MessagesState)
    
    # 添加节点
    builder.add_node("assistant", assistant)
    builder.add_node("tools", ToolNode(tools))
    
    # 添加边
    builder.add_edge(START, "assistant")
    builder.add_conditional_edges(
        "assistant",
        tools_condition,
    )
    builder.add_edge("tools", "assistant")
    
    return builder.compile()

# 创建带记忆的图 (LangGraph API服务器会自动提供持久化)
def create_memory_graph():
    """创建带记忆的 React 图 - API服务器自动处理持久化"""
    builder = StateGraph(MessagesState)
    
    # 添加节点
    builder.add_node("assistant", assistant)
    builder.add_node("tools", ToolNode(tools))
    
    # 添加边
    builder.add_edge(START, "assistant")
    builder.add_conditional_edges(
        "assistant",
        tools_condition,
    )
    builder.add_edge("tools", "assistant")
    
    # 不使用自定义checkpointer - API服务器会自动处理持久化
    return builder.compile()

# 导出的图对象（Studio 会导入这些）
react_graph = create_basic_graph()
react_graph_memory = create_memory_graph()

# 为了 Studio 的兼容性，也可以直接赋值
basic_agent = react_graph
memory_agent = react_graph_memory

if __name__ == "__main__":
    # 测试脚本
    print("🧪 测试图定义...")
    
    # 测试基础图
    from langchain_core.messages import HumanMessage
    messages = [HumanMessage(content="Add 2 and 3.")]
    result = basic_agent.invoke({"messages": messages})
    print(f"基础图测试: {result['messages'][-1].content}")
    
    # 测试记忆图 (本地测试需要添加checkpointer)
    from langgraph.checkpoint.memory import MemorySaver
    local_memory_graph = create_memory_graph()
    local_memory_graph_with_checkpointer = StateGraph(MessagesState)
    local_memory_graph_with_checkpointer.add_node("assistant", assistant)
    local_memory_graph_with_checkpointer.add_node("tools", ToolNode(tools))
    local_memory_graph_with_checkpointer.add_edge(START, "assistant")
    local_memory_graph_with_checkpointer.add_conditional_edges("assistant", tools_condition)
    local_memory_graph_with_checkpointer.add_edge("tools", "assistant")
    local_memory_compiled = local_memory_graph_with_checkpointer.compile(checkpointer=MemorySaver())
    
    config = {"configurable": {"thread_id": "test"}}
    result = local_memory_compiled.invoke({"messages": messages}, config)
    print(f"记忆图测试: {result['messages'][-1].content}")
    
    print("✅ 图定义正常工作！")

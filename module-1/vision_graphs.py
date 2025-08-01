"""
支持图片输入的LangGraph图定义
演示如何创建能处理文本和图片的多模态Agent
"""

import os
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState, START, StateGraph
from langchain_core.messages import SystemMessage

# 获取代理配置
proxy = os.environ.get("PROXY")

# 创建支持视觉的LLM
vision_llm = ChatOpenAI(
    model="gpt-4o",  # gpt-4o支持视觉功能
    openai_proxy=f"http://{proxy}" if proxy else None
)

def vision_assistant(state: MessagesState):
    """
    支持文本和图片的多模态助手
    可以分析图片内容，描述图片，回答关于图片的问题
    """
    sys_msg = SystemMessage(content="""你是一个多模态AI助手，具有以下能力：

1. **图片分析**: 详细分析和描述图片内容，包括：
   - 识别图片中的物体、人物、场景
   - 读取图片中的文字内容
   - 分析图片的颜色、构图、风格
   - 回答关于图片的具体问题

2. **数学计算**: 进行各种数学运算和解题

3. **对话交流**: 进行自然的对话，回答各种问题

4. **综合分析**: 结合图片和文字进行综合分析

请根据用户的输入（文字和/或图片）提供准确、详细的回答。""")
    
    messages = [sys_msg] + state["messages"]
    response = vision_llm.invoke(messages)
    return {"messages": [response]}

def create_vision_graph():
    """创建支持视觉的图"""
    builder = StateGraph(MessagesState)
    builder.add_node("vision_assistant", vision_assistant)
    builder.add_edge(START, "vision_assistant")
    return builder.compile()

# 导出的图对象
vision_agent = create_vision_graph()

# 创建一个带记忆的视觉助手 (API服务器会自动处理持久化)
def create_vision_memory_graph():
    """创建带记忆的视觉助手"""
    builder = StateGraph(MessagesState)
    builder.add_node("vision_assistant", vision_assistant)
    builder.add_edge(START, "vision_assistant")
    return builder.compile()

vision_memory_agent = create_vision_memory_graph()

if __name__ == "__main__":
    # 测试脚本
    print("🔍 测试视觉图定义...")
    
    from langchain_core.messages import HumanMessage
    
    # 测试纯文本消息
    text_message = HumanMessage(content="你好！请介绍一下你的功能。")
    result = vision_agent.invoke({"messages": [text_message]})
    print(f"文本测试: {result['messages'][-1].content[:100]}...")
    
    # 注意：图片测试需要实际的图片base64数据
    # 这里只是展示消息格式
    print("\n📷 图片消息格式示例:")
    image_message_example = HumanMessage(content=[
        {"type": "text", "text": "这张图片里有什么？"},
        {
            "type": "image_url",
            "image_url": {
                "url": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQ..."  # 实际使用时需要真实的base64数据
            }
        }
    ])
    print("消息类型: HumanMessage")
    print("内容: 文本 + 图片URL")
    
    print("\n✅ 视觉图定义创建完成！")
    print("📝 要在Studio中使用：")
    print("1. 更新 langgraph.json 配置")
    print("2. 重启 langgraph dev 服务")
    print("3. 在Studio中选择 vision_agent")
    print("4. 尝试上传图片或拖拽图片到输入框")
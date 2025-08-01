# 🖼️ LangGraph Studio 图片输入功能分析

## 📋 当前项目状态

### ❌ **当前项目不支持图片输入**

**原因分析：**
1. **模型配置**: 使用的是 `gpt-4o`，虽然支持视觉，但没有配置图片处理
2. **消息类型**: 只处理文本消息 (`HumanMessage` with text content)
3. **工具限制**: 只有数学计算工具 (add, multiply, divide)
4. **系统提示**: 专门针对数学运算设计

### 🔍 **Studio界面图片支持情况**

**LangGraph Studio理论上支持图片**，但需要满足以下条件：
- 图定义支持多模态消息
- 使用支持视觉的LLM (如 gpt-4o, claude-3-sonnet)
- 正确的消息格式配置

## 🚀 如何添加图片支持

### 方法1: 创建支持图片的新图

```python
# vision_agent.py
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState, START, StateGraph

# 使用支持视觉的模型
vision_llm = ChatOpenAI(
    model="gpt-4o",  # 确保是支持视觉的模型
    openai_proxy=f"http://{proxy}" if proxy else None
)

def vision_assistant(state: MessagesState):
    """支持图片和文本的助手"""
    return {"messages": [vision_llm.invoke(state["messages"])]}

# 构建支持图片的图
def create_vision_graph():
    builder = StateGraph(MessagesState)
    builder.add_node("vision_assistant", vision_assistant)
    builder.add_edge(START, "vision_assistant")
    return builder.compile()

# 导出图
vision_agent = create_vision_graph()
```

### 方法2: 修改现有图支持多模态

```python
# 在 agent_graphs.py 中添加
def image_analyze_tool(image_description: str) -> str:
    """分析图片内容的工具"""
    return f"图片分析结果: {image_description}"

# 添加到工具列表
tools_with_vision = [add, multiply, divide, image_analyze_tool]

# 修改系统消息
vision_sys_msg = SystemMessage(content="""
你是一个多功能助手，可以：
1. 进行数学计算 (使用工具)
2. 分析图片内容
3. 回答各种问题
""")
```

## 🎨 Studio中的图片输入方式

### **如果图支持图片，Studio界面会提供：**

#### 1. **拖拽上传**
```
┌─────────────────────────────────────┐
│  💬 消息输入区域                     │
│  ┌─────────────────────────────────┐ │
│  │ 输入消息或拖拽图片到这里...      │ │
│  └─────────────────────────────────┘ │
│  📎 [附件] 📷 [图片] 🎤 [语音]      │
└─────────────────────────────────────┘
```

#### 2. **点击上传按钮**
- 点击 📷 图片按钮
- 选择本地图片文件
- 支持常见格式: PNG, JPG, GIF, WebP

#### 3. **复制粘贴**
- 直接粘贴剪贴板中的图片
- 从其他应用拖拽图片

## 🔧 实现图片支持的完整方案

### 步骤1: 创建支持图片的新图文件

```python
# vision_graphs.py
import os
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState, START, StateGraph
from langchain_core.messages import SystemMessage

proxy = os.environ.get("PROXY")

# 支持视觉的LLM
vision_llm = ChatOpenAI(
    model="gpt-4o",
    openai_proxy=f"http://{proxy}" if proxy else None
)

def vision_assistant(state: MessagesState):
    """处理文本和图片的助手"""
    sys_msg = SystemMessage(content="""
    你是一个多模态AI助手，可以：
    1. 分析图片内容，描述图片中的物体、场景、文字等
    2. 回答关于图片的问题
    3. 进行数学计算
    4. 进行对话交流
    """)
    
    messages = [sys_msg] + state["messages"]
    response = vision_llm.invoke(messages)
    return {"messages": [response]}

# 构建图
def create_vision_graph():
    builder = StateGraph(MessagesState)
    builder.add_node("vision_assistant", vision_assistant)
    builder.add_edge(START, "vision_assistant")
    return builder.compile()

# 导出图
vision_agent = create_vision_graph()
```

### 步骤2: 更新langgraph.json配置

```json
{
  "dependencies": ["."],
  "graphs": {
    "memory_agent": "./agent_graphs.py:memory_agent",
    "basic_agent": "./agent_graphs.py:basic_agent",
    "vision_agent": "./vision_graphs.py:vision_agent"
  },
  "env": ".env"
}
```

### 步骤3: 重启服务器

```bash
# 重启LangGraph开发服务器以加载新图
langgraph dev --port 3000
```

### 步骤4: 在Studio中测试

1. 访问 Studio
2. 选择新的 "vision_agent"
3. 尝试上传图片或拖拽图片到输入区域

## 💡 图片输入的消息格式

### LangChain中的图片消息格式：

```python
from langchain_core.messages import HumanMessage

# 文本 + 图片消息
message = HumanMessage(content=[
    {"type": "text", "text": "这张图片里有什么？"},
    {
        "type": "image_url",
        "image_url": {
            "url": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQ..."
        }
    }
])
```

### API请求格式：

```json
{
  "input": {
    "messages": [
      {
        "role": "human",
        "content": [
          {"type": "text", "text": "分析这张图片"},
          {
            "type": "image_url", 
            "image_url": {"url": "data:image/jpeg;base64,..."}
          }
        ]
      }
    ]
  }
}
```

## 🎯 总结

### **当前状态：**
- ❌ 现有的 memory_agent 和 basic_agent **不支持图片**
- ✅ 可以通过添加新图来支持图片输入
- ✅ Studio界面**支持**图片上传功能

### **要启用图片功能需要：**
1. 创建支持视觉的新图定义
2. 使用多模态LLM (gpt-4o已支持)
3. 更新配置文件
4. 重启服务器

### **Studio中的图片输入方式：**
- 📷 点击图片按钮上传
- 🖱️ 拖拽图片到输入框
- 📋 复制粘贴图片

**要测试图片功能，需要先创建支持视觉的图定义！**
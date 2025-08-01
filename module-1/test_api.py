#!/usr/bin/env python3
"""
测试LangGraph API的功能
"""
import requests
import json
import time

# API基础URL
BASE_URL = "http://127.0.0.1:3000"

def test_langgraph_api():
    """测试LangGraph API的完整流程"""
    
    print("🚀 开始测试LangGraph API...")
    
    # 1. 创建assistant
    print("\n1️⃣ 创建memory_agent assistant...")
    assistant_response = requests.post(
        f"{BASE_URL}/assistants",
        json={"graph_id": "memory_agent"}
    )
    assistant_data = assistant_response.json()
    assistant_id = assistant_data["assistant_id"]
    print(f"✅ Assistant创建成功: {assistant_id}")
    
    # 2. 创建thread
    print("\n2️⃣ 创建对话线程...")
    thread_response = requests.post(f"{BASE_URL}/threads", json={})
    thread_data = thread_response.json()
    thread_id = thread_data["thread_id"]
    print(f"✅ Thread创建成功: {thread_id}")
    
    # 3. 发送第一条消息
    print("\n3️⃣ 发送第一条消息: '计算 15 + 25'")
    run_response = requests.post(
        f"{BASE_URL}/threads/{thread_id}/runs",
        json={
            "assistant_id": assistant_id,
            "input": {"messages": [{"role": "human", "content": "计算 15 + 25"}]}
        }
    )
    run_data = run_response.json()
    run_id = run_data["run_id"]
    print(f"✅ 运行启动: {run_id}")
    
    # 4. 等待运行完成并获取结果
    print("⏳ 等待运行完成...")
    while True:
        time.sleep(1)
        status_response = requests.get(f"{BASE_URL}/threads/{thread_id}/runs/{run_id}")
        status_data = status_response.json()
        
        if status_data["status"] == "success":
            print("✅ 运行完成!")
            print(f"🔍 响应结构: {json.dumps(status_data, indent=2)[:500]}...")
            # 获取thread状态来看消息
            thread_state = requests.get(f"{BASE_URL}/threads/{thread_id}/state")
            state_data = thread_state.json()
            
            if "values" in state_data and "messages" in state_data["values"]:
                for message in state_data["values"]["messages"][-2:]:  # 显示最后2条消息
                    if message["type"] == "ai" and not message.get("tool_calls"):
                        print(f"🤖 Assistant: {message['content']}")
            break
        elif status_data["status"] == "error":
            print(f"❌ 运行失败: {status_data}")
            break
    
    # 5. 发送第二条消息测试记忆
    print("\n4️⃣ 发送第二条消息: '现在乘以 2'")
    run2_response = requests.post(
        f"{BASE_URL}/threads/{thread_id}/runs",
        json={
            "assistant_id": assistant_id,
            "input": {"messages": [{"role": "human", "content": "现在乘以 2"}]}
        }
    )
    run2_data = run2_response.json()
    run2_id = run2_data["run_id"]
    
    # 6. 等待第二次运行完成
    print("⏳ 等待第二次运行完成...")
    while True:
        time.sleep(1)
        status2_response = requests.get(f"{BASE_URL}/threads/{thread_id}/runs/{run2_id}")
        status2_data = status2_response.json()
        
        if status2_data["status"] == "success":
            print("✅ 第二次运行完成!")
            # 获取thread状态来看所有消息
            thread_state2 = requests.get(f"{BASE_URL}/threads/{thread_id}/state")
            state_data2 = thread_state2.json()
            
            if "values" in state_data2 and "messages" in state_data2["values"]:
                print("📝 完整对话历史:")
                for message in state_data2["values"]["messages"]:
                    if message["type"] == "human":
                        print(f"👤 Human: {message['content']}")
                    elif message["type"] == "ai" and not message.get("tool_calls"):
                        print(f"🤖 Assistant: {message['content']}")
            break
        elif status2_data["status"] == "error":
            print(f"❌ 第二次运行失败: {status2_data}")
            break
    
    # 7. 检查thread状态
    print("\n5️⃣ 检查线程最终状态...")
    final_state = requests.get(f"{BASE_URL}/threads/{thread_id}/state")
    final_data = final_state.json()
    message_count = len(final_data["values"]["messages"])
    print(f"📊 线程中总消息数: {message_count}")
    print("✅ 记忆功能正常工作!")
    
    print("\n🎉 LangGraph API测试完成!")
    return True

if __name__ == "__main__":
    try:
        test_langgraph_api()
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
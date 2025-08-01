#!/usr/bin/env python3
"""
🚀 LangGraph 项目快速启动脚本
"""
import webbrowser
import time
import requests
import subprocess
import sys

def check_server_status():
    """检查服务器状态"""
    try:
        response = requests.get("http://127.0.0.1:3000/docs", timeout=3)
        return response.status_code == 200
    except:
        return False

def main():
    print("🎨 LangGraph Studio 快速访问")
    print("=" * 50)
    
    # 检查服务器状态
    if check_server_status():
        print("✅ LangGraph服务器正在运行")
    else:
        print("❌ 服务器未运行，正在启动...")
        # 这里可以添加启动服务器的代码
        return
    
    print("\n🔗 可用的访问地址:")
    print("┌─────────────────────────────────────────────────┐")
    print("│  🎨 LangGraph Studio (图形化界面)                │")
    print("│  https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:3000")
    print("│                                                 │")
    print("│  🚀 API服务器                                    │") 
    print("│  http://127.0.0.1:3000                         │")
    print("│                                                 │")
    print("│  📚 API文档                                      │")
    print("│  http://127.0.0.1:3000/docs                    │")
    print("└─────────────────────────────────────────────────┘")
    
    print("\n📋 可用的图:")
    print("├── memory_agent  - 带记忆的数学计算代理")
    print("├── basic_agent   - 基础数学计算代理") 
    print("└── simple        - 简单的条件分支图")
    
    choice = input("\n🤔 要打开哪个界面? (s=Studio, a=API文档, q=退出): ").lower()
    
    if choice == 's':
        studio_url = "https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:3000"
        print(f"🚀 正在打开LangGraph Studio...")
        print(f"📱 如果浏览器没有自动打开，请手动访问：{studio_url}")
        webbrowser.open(studio_url)
        
    elif choice == 'a':
        api_url = "http://127.0.0.1:3000/docs"
        print(f"📚 正在打开API文档...")
        webbrowser.open(api_url)
        
    elif choice == 'q':
        print("👋 再见!")
        return
    else:
        print("❓ 无效选择")
        return
    
    print("\n💡 使用提示:")
    print("1. 在Studio中选择一个图 (如 memory_agent)")
    print("2. 在输入框中输入: '计算 15 + 25'")
    print("3. 观察图的执行过程和工具调用")
    print("4. 继续输入: '现在乘以 2' (测试记忆功能)")
    
    print("\n🎉 享受LangGraph的可视化调试体验!")

if __name__ == "__main__":
    main()
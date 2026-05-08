from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_community.tools import DuckDuckGoSearchRun
from core.state import SquadState
import os

# Initialize the Gemini Engine and the Search Tool
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=os.environ.get("GOOGLE_API_KEY"))
search_tool = DuckDuckGoSearchRun()

def pm_node(state: SquadState):
    """The Product Manager researches the request and creates a technical spec."""
    print("🧠 [PM Agent]: Analyzing request...")
    
    # Get the user's request
    user_request = state["messages"][-1].content
    
    # ==========================================
    # 🌐 Autonomous Research Phase
    # ==========================================
    print(f"🌐 [PM Agent]: Searching the web for the latest context on: '{user_request}'")
    try:
        # The PM automatically searches the internet based on the user's prompt
        search_results = search_tool.invoke(user_request)
        print("✅ [PM Agent]: Research complete. Drafting technical specifications...")
    except Exception as e:
        print(f"⚠️ [PM Agent]: Search failed ({e}), proceeding with internal knowledge.")
        search_results = "No recent internet data available."
    
    system_instruction = """You are the Lead Product Manager of an elite AI software squad.
    Your job is to read the user's feature request, review the provided Internet Research, and write a clear, step-by-step technical implementation plan for the Senior Coder.
    
    RULES:
    1. DO NOT write actual Python or JavaScript code.
    2. Define the file names to be created or modified.
    3. Define the exact logic the Coder needs to implement.
    4. Use the Internet Research to ensure your plan uses the most up-to-date best practices."""
    
    # Pass the Request AND the live Internet Data to Gemini
    messages = [
        SystemMessage(content=system_instruction),
        HumanMessage(content=f"User Request: {user_request}\n\nLive Internet Research:\n{search_results}")
    ]
    
    # Generate the technical plan
    response = llm.invoke(messages)
    
    return {
        "messages": [response],
        "next_agent": "coder"
    }
import requests  # ✅ FIX 2: Added this import
from langchain_core.messages import HumanMessage
from core.state import SquadState  # ✅ FIX 1: Removed trailing comma
from langchain_google_genai import ChatGoogleGenerativeAI

from core.state import SquadState
import os
import re # We need Regex to parse the markdown

# Initialize the Gemini Engine
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=os.environ.get("GOOGLE_API_KEY"))

def coder_node(state: SquadState):
    # 1. Grab the last 3-5 messages (includes the PM spec AND previous QA failures)
    # This gives the Coder "Memory" of what went wrong!
    full_context = "\n".join([str(m.content) for m in state["messages"][-5:]])
    
    print("📡 [Orchestrator]: Routing full history to Coder Service to prevent loops...")
    
    try:
        response = requests.post(
            "http://127.0.0.1:8002/generate",
            json={"technical_spec": full_context} # Send the HISTORY, not just the spec
        )
        result = response.json()
        generated_code = result.get("code", "")
    except Exception as e:
        generated_code = f"# Error: {e}"

    return {
        "messages": [HumanMessage(content=generated_code)],
        "next_agent": "qa",
        "current_code": generated_code
    }
    
    # ==========================================
    # 🛠️ NEW "HANDS" LOGIC: Save to File System
    # ==========================================
    print("🛠️ [Coder Agent]: Extracting and saving code to local workspace...")
    
    # 1. Create a workspace folder if it doesn't exist
    os.makedirs("workspace", exist_ok=True)
    
    # 2. Extract the exact Python code from the LLM's markdown block
    match = re.search(r'```python\n(.*?)```', code_output, re.DOTALL)
    
    if match:
        clean_code = match.group(1)
        # 3. Save it to a real file on your hard drive!
        file_path = os.path.join("workspace", "average_age_calculator.py")
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(clean_code)
            
        print(f"✅ [Coder Agent]: Successfully saved script to {file_path}")
    else:
        print("⚠️ [Coder Agent]: Could not find python markdown blocks to save.")
        
    return {
        "messages": [response],
        "current_code": code_output,
        "next_agent": "end"
    }
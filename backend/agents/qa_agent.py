import os
import re
import requests
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from core.state import SquadState

# Initialize the LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=os.environ.get("GOOGLE_API_KEY"))

def qa_node(state: SquadState):
    """The QA Agent tests the code by sending it to the remote MCP Server."""
    print("🕵️‍♂️ [QA Agent]: Preparing to test code...")
    
    # 1. Get the code the Coder just wrote
    current_code = state.get("current_code", "")
    if not current_code: # Fallback if state key differs
        current_code = state["messages"][-1].content
    
    # 2. Strip away the markdown formatting so Python can run it
    clean_code = current_code
    match = re.search(r'```python\n(.*?)```', current_code, re.DOTALL)
    if match:
        clean_code = match.group(1)
        
    # 3. Send the code over the network to the MCP Server!
    print("🔌 [QA Agent]: Sending code to MCP Server (Port 8001) for safe execution...")
    try:
        response = requests.post(
            "http://127.0.0.1:8001/execute",
            json={"code": clean_code, "filename": "test_run.py"}
        )
        result = response.json()
        terminal_output = result.get("output", "")
        status = result.get("status", "error")
    except Exception as e:
        terminal_output = f"Failed to connect to MCP Server. Is it running on port 8001? Error: {e}"
        status = "error"

    # 4. Format the results for Gemini
    if status == "success":
        print("🟢 [QA Agent]: MCP Server reported success!")
        formatted_output = f"SUCCESS!\nTerminal Output:\n{terminal_output}"
    else:
        print("🔴 [QA Agent]: MCP Server reported a crash! Grabbing error traceback...")
        formatted_output = f"CRASHED!\nTerminal Error:\n{terminal_output}"

    # 5. Ask Gemini to read the terminal results
    system_instruction = """You are the strict Lead QA Engineer of an elite AI squad.
    You just executed the Coder's Python script. Read the Terminal Output below.
    
    RULES:
    1. If the terminal output says SUCCESS and there are no crash errors, respond with EXACTLY the word "PASS".
    2. If the terminal output shows a CRASH, FileNotFoundError, or syntax error, respond with "FAIL:" followed by strict instructions on how to fix the exact error shown in the traceback.
    3. Do NOT write the corrected code yourself. Just provide the feedback."""
    
    messages = [
        SystemMessage(content=system_instruction),
        HumanMessage(content=f"Terminal Output from execution:\n{formatted_output}\n\nOriginal Code:\n{current_code}")
    ]
    
    # Generate the QA report
    response_llm = llm.invoke(messages)
    feedback = response_llm.content.strip()
    
    # Route based on the output
    if feedback.startswith("PASS"):
        print("✅ [QA Agent]: Code Approved! Ready for production.")
        return {"qa_feedback": "PASS"}
    else:
        print(f"❌ [QA Agent]: Bugs found! Sending traceback to Coder.")
        return {"qa_feedback": feedback}
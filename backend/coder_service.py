import requests
from langchain_core.messages import HumanMessage
from core.state import SquadState
from fastapi import FastAPI


app = FastAPI(title="ACP Coder Microservice")

def coder_node(state: SquadState):
    # Instead of just sending the spec, send the last few messages
    # which include the QA feedback!
    history = "\n".join([m.content for m in state["messages"][-3:]])
    
    print("📡 [Orchestrator]: Routing full context to Coder Service...")
    try:
        response = requests.post(
            "http://127.0.0.1:8002/generate",
            json={"technical_spec": history} # Now the Coder sees why it failed!
        )
        # ... rest of your code ...
        result = response.json()
        generated_code = result.get("code", "")
        print("✅ [Orchestrator]: Received code back from Coder Microservice.")
        
    except Exception as e:
        print(f"🔴 [Orchestrator]: Failed to reach Coder Service: {e}")
        generated_code = "# Failed to connect to Coder Microservice."

    # 3. Pass the code down the pipeline to the QA Agent
    return {
        "messages": [HumanMessage(content=generated_code)],
        "next_agent": "qa",
        "current_code": generated_code # Save to state so QA can grab it easily
    }
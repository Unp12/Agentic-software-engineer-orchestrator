from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
import os
from dotenv import load_dotenv

# 1. LOAD THE ENV FILE FIRST! 
# This must happen before we import the agents.
load_dotenv()

# 2. Now we can safely import our graph
from core.graph import agentic_orchestrator

# Initialize the Server
app = FastAPI(title="Agentic Software Engineering Orchestrator")

# Enable CORS so our React frontend can talk to this API later
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ... (The rest of your main.py code stays exactly the same)

# Define the data we expect from the user
class FeatureRequest(BaseModel):
    prompt: str

@app.post("/api/generate")
async def generate_feature(request: FeatureRequest):
    print(f"\n🚀 [SYSTEM]: Received new feature request: '{request.prompt}'")
    
    # 1. Setup the initial blank whiteboard (SquadState)
    initial_state = {
        "messages": [HumanMessage(content=request.prompt)],
        "next_agent": "pm",
        "current_code": "",
        "qa_feedback": ""
    }
    
    # 2. Execute the LangGraph workflow
    # This automatically routes from PM -> Coder -> End
    # Add a recursion limit so the agents can only loop a maximum of 5 times!
    final_state = agentic_orchestrator.invoke(initial_state, {"recursion_limit": 20})
    
    
    print("✅ [SYSTEM]: Workflow complete.")
    
    # 3. Return the results back to the user
    return {
        "pm_plan": final_state["messages"][1].content, # The PM's thought process
        "generated_code": final_state["current_code"]  # The Coder's final output
    }

@app.get("/")
def health_check():
    return {"status": "Agentic Squad is Online 🟢"}
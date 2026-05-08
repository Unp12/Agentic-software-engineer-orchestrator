from langgraph.graph import StateGraph, START, END
from core.state import SquadState
from agents.pm_agent import pm_node
from agents.coder_agent import coder_node
from agents.qa_agent import qa_node # <--- Import the new QA Agent

# 1. Initialize the Graph
workflow = StateGraph(SquadState)

# 2. Register our Agents as "Nodes"
workflow.add_node("pm", pm_node)
workflow.add_node("coder", coder_node)
workflow.add_node("qa", qa_node) # <--- Add QA Node

# 3. Define the routing function
def route_after_qa(state: SquadState):
    """If QA says PASS, end the graph. If FAIL, route back to the coder."""
    if state.get("qa_feedback") == "PASS":
        return END
    else:
        return "coder"

# 4. Define the A2A Pipeline
workflow.add_edge(START, "pm")
workflow.add_edge("pm", "coder")
workflow.add_edge("coder", "qa") # Coder hands it to QA

# conditional_edges is what creates the loop!
workflow.add_conditional_edges(
    "qa",
    route_after_qa,
    {
        END: END,
        "coder": "coder"
    }
)

agentic_orchestrator = workflow.compile()
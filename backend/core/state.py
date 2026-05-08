from typing import TypedDict, Annotated, Sequence
from langgraph.graph import add_messages # ✅ Correct location
import operator

# Define the Shared "Whiteboard" (State)
class SquadState(TypedDict):
    messages: Annotated[list, add_messages]
    next_agent: str
    current_code: str
    qa_feedback: str
    iterations: int # Add this!
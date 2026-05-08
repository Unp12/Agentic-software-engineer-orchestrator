from fastapi import FastAPI
from pydantic import BaseModel
import subprocess
import os

app = FastAPI(title="Local MCP Execution Server")

# Make sure the workspace folder exists where the code will run
os.makedirs("workspace", exist_ok=True)

class CodeExecutionRequest(BaseModel):
    code: str
    filename: str = "test_run.py"

@app.post("/execute")
def execute_code(request: CodeExecutionRequest):
    print(f"🔌 [MCP Server]: Received code execution request for {request.filename}")
    
    file_path = os.path.join("workspace", request.filename)
    
    # 1. Write the file safely
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(request.code)
        
    # 2. Run the code in this isolated process
    try:
        result = subprocess.run(
            ["python", file_path],
            capture_output=True,
            text=True,
            timeout=10 # Prevents infinite loops from freezing the server
        )
        
        # 3. Return the exact terminal output back to the QA Agent
        if result.returncode == 0:
            return {"status": "success", "output": result.stdout}
        else:
            return {"status": "error", "output": result.stderr}
            
    except subprocess.TimeoutExpired:
        return {"status": "error", "output": "Execution timed out (infinite loop detected)."}
    except Exception as e:
        return {"status": "error", "output": str(e)}
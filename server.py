from fastapi import FastAPI, HTTPException
from mcp_protocol import MCPRequest, MCPResponse, make_header, SessionMessage
import uuid

app = FastAPI()

@app.post("/mcp", response_model=MCPResponse)
async def handle_mcp(req: MCPRequest):
    # Simple echo logic: respond by echoing last user message
    last_user = [msg for msg in req.instruction if msg.role == 'user'][-1]
    reply_text = f"รับทราบ: {last_user.content}"
    
    resp_header = make_header(req.header.context_id)
    response_msg = SessionMessage(role="assistant", content=reply_text)

    # Build MCPResponse and return as dict to satisfy Pydantic validation
    mcp_response = MCPResponse(header=resp_header, response=response_msg)
    return mcp_response.dict()

if __name__ == "__main__":
    import uvicorn
    uvciorn.run(app, host="0.0.0.0", port=8000)
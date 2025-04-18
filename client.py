import uuid
import asyncio
import httpx
from mcp_protocol import (
    make_header, UserProfile, SessionMessage,
    Environment, ContextPayload, Instruction, MCPRequest
)

async def main():
    context_id = str(uuid.uuid4())
    header = make_header(context_id)
    # Prepare context payload
    user_profile = UserProfile(user_id="U-100", name="Somchai", language="th")
    session_history = [
        SessionMessage(role="system", content="You are an AI technical assistant."),
        SessionMessage(role="user", content="สวัสดี")
    ]
    environment = Environment(locale="th-TH", timezone="Asia/Bangkok")
    payload = ContextPayload(
        user_profile=user_profile,
        session_history=session_history,
        environment=environment
    )
    # Instruction for the model
    instruction = [
        Instruction(role="user", content="ช่วยเชื่อมต่อ MCP กับ LLM ด้วย SDK v1.x")
    ]
    request = MCPRequest(
        header=header,
        context_payload=payload,
        instruction=instruction
    )

    # Send request
    async with httpx.AsyncClient() as client_http:
        resp = await client_http.post(
            "http://localhost:8000/mcp",
            json=request.model_dump()
        )
        resp.raise_for_status()
        data = resp.json()
        print("Response:", data)

if __name__ == "__main__":
    asyncio.run(main())
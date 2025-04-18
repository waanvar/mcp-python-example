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
    user_profile = UserProfile(user_id="U-100", name="Somchai", language="th")
    session_history = [
        SessionMessage(role="system", content="คุณคือผู้ช่วย AI เชิงเทคนิค"),
        SessionMessage(role="user", content="สวัสดี")
    ]
    environment = Environment(locale="th-TH", timezone="Asia/Bangkok")
    payload = ContextPayload(
        user_profile=user_profile,
        session_history=session_history,
        environment=environment
    )
    instruction = [
        Instruction(role="user", content="สอนฉันเกี่ยวกับ MCP")
    ]
    request = MCPRequest(
        header=header,
        context_payload=payload,
        instruction=instruction
    )

    async with httpx.AsyncClient() as client:
        resp = await client.post("http://localhost:8000/mcp", json=request.dict())
        resp.raise_for_status()
        data = resp.json()
        print("Response from server:", data)

if __name__ == "__main__":
    asyncio.run(main())
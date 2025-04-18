import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from mcp_protocol import MCPRequest, MCPResponse, make_header, SessionMessage
from openai import OpenAI


# Load environment variables
load_dotenv()

# Initialize OpenAI client (SDK v1.x)
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)
model_name = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
# Determine LLM provider: 'openai' or 'llama'
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai").lower()

app = FastAPI()

@app.post("/mcp", response_model=MCPResponse)
async def handle_mcp(req: MCPRequest):
    # Build unified messages list
    messages = [
        {"role": msg.role, "content": msg.content}
        for msg in req.context_payload.session_history
    ] + [
        {"role": instr.role, "content": instr.content}
        for instr in req.instruction
    ]

    try:
        if LLM_PROVIDER == "openai":
            # Call OpenAI ChatCompletion
            completion = client.chat.completions.create(
                model=model_name,
                messages=messages,
                temperature=0.7
            )
            assistant_content = completion.choices[0].message.content

        elif LLM_PROVIDER == "llama":
            # Local LLaMA integration
            from llama_cpp import Llama
            llama_model_path = os.getenv("LLAMA_MODEL_PATH", "./models/llama4.bin")
            llama = Llama(model_path=llama_model_path)
            llm_resp = llama.chat(
                messages=messages,
                temperature=0.7
            )
            assistant_content = llm_resp['choices'][0]['message']['content']

        else:
            raise HTTPException(status_code=400, detail="Unsupported LLM_PROVIDER")

    except Exception as e:
        # Determine error type by message
        msg = str(e)
        lower = msg.lower()
        if 'rate limit' in lower or 'quota' in lower:
            raise HTTPException(status_code=429, detail=msg)
        raise HTTPException(status_code=500, detail=msg)

    # Build MCPResponse
    resp_header = make_header(req.header.context_id)
    response_msg = SessionMessage(role="assistant", content=assistant_content)
    mcp_resp = MCPResponse(header=resp_header, response=response_msg)
    return mcp_resp.model_dump()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
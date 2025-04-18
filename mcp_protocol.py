from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime, timezone

class Header(BaseModel):
    protocol_version: str
    timestamp: str
    context_id: str

class UserProfile(BaseModel):
    user_id: str
    name: str
    language: str

class SessionMessage(BaseModel):
    role: str  # 'system', 'assistant', 'user'
    content: str

class Environment(BaseModel):
    locale: str
    timezone: str

class ContextPayload(BaseModel):
    user_profile: UserProfile
    session_history: List[SessionMessage]
    environment: Environment

class Instruction(BaseModel):
    role: str
    content: str

class Metadata(BaseModel):
    sensitivity_level: Optional[str]
    trace_id: Optional[str]

class MCPRequest(BaseModel):
    header: Header
    context_payload: ContextPayload
    instruction: List[Instruction]
    metadata: Optional[Metadata] = None

class MCPResponse(BaseModel):
    header: Header
    response: SessionMessage
    metadata: Optional[Metadata] = None

# Helper to create header

def make_header(context_id: str, version: str = "1.0") -> Header:
    return Header(
        protocol_version=version,
        timestamp=datetime.now(timezone.utc).isoformat(),
        context_id=context_id
    )
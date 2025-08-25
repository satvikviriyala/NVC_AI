import sys
import os
import grpc
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Add the libs directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'libs', 'clients', 'python')))

# Import gRPC stubs
from conversation_orchestrator_pb2 import TurnRequest
from conversation_orchestrator_pb2_grpc import ConversationOrchestratorServiceStub

app = FastAPI()

# --- gRPC Client Setup ---
# It's better to create the channel once when the app starts up.
# FastAPI's lifespan events are perfect for this.
orchestrator_channel = None
orchestrator_stub = None

@app.on_event("startup")
async def startup_event():
    global orchestrator_channel, orchestrator_stub
    orchestrator_channel = grpc.insecure_channel('conversation_orchestrator:50055')
    orchestrator_stub = ConversationOrchestratorServiceStub(orchestrator_channel)

@app.on_event("shutdown")
async def shutdown_event():
    if orchestrator_channel:
        orchestrator_channel.close()

# --- API Models ---
class ChatRequest(BaseModel):
    user_id: str
    text: str

class ChatResponse(BaseModel):
    ai_message: str

# --- API Endpoint ---
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    This endpoint receives user messages and forwards them to the orchestrator.
    """
    if not orchestrator_stub:
        raise HTTPException(status_code=503, detail="Orchestrator service not available")

    try:
        # Create a gRPC request
        grpc_request = TurnRequest(user_id=request.user_id, text=request.text)

        # Call the gRPC service
        grpc_response = orchestrator_stub.ProcessTurn(grpc_request, timeout=30.0)

        return ChatResponse(ai_message=grpc_response.ai_message)

    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail=f"gRPC error: {e.details()}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

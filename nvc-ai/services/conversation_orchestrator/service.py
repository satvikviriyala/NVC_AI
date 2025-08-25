import sys
import os

# Add the libs directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'libs', 'clients', 'python')))

import grpc
from conversation_orchestrator_pb2_grpc import ConversationOrchestratorServiceServicer
from conversation_orchestrator_pb2 import TurnResponse

# Import client stubs and request/response objects from other services
from nvc_processor_pb2 import NVCProcessRequest
from nvc_processor_pb2_grpc import NVCProcessorServiceStub
from prompt_service_pb2 import GetPromptRequest
from prompt_service_pb2_grpc import PromptServiceStub
from empathy_generator_pb2 import GenerateRequest
from empathy_generator_pb2_grpc import EmpathyGeneratorServiceStub

class ConversationOrchestratorService(ConversationOrchestratorServiceServicer):
    def __init__(self):
        # Create gRPC channels to other services
        self.nvc_processor_channel = grpc.insecure_channel('localhost:50051')
        self.prompt_service_channel = grpc.insecure_channel('localhost:50053')
        self.empathy_generator_channel = grpc.insecure_channel('localhost:50054')

        # Create gRPC stubs
        self.nvc_processor_stub = NVCProcessorServiceStub(self.nvc_processor_channel)
        self.prompt_service_stub = PromptServiceStub(self.prompt_service_channel)
        self.empathy_generator_stub = EmpathyGeneratorServiceStub(self.empathy_generator_channel)

    def ProcessTurn(self, request, context):
        """
        Processes a single turn of the conversation by calling other services in a pipeline.
        """
        try:
            # 1. Get the base system prompt
            prompt_request = GetPromptRequest(version="nvc_coach_v1")
            prompt_response = self.prompt_service_stub.GetPrompt(prompt_request)
            system_prompt = prompt_response.prompt_text

            # 2. Analyze the user's text for NVC components
            nvc_request = NVCProcessRequest(text=request.text)
            nvc_response = self.nvc_processor_stub.Process(nvc_request)

            # 3. Construct a rich prompt for the generator
            rich_prompt = f"""
{system_prompt}

---
User's Message: "{nvc_response.observation}"

Identified Feelings: {', '.join(nvc_response.feelings) if nvc_response.feelings else 'None'}
Identified Needs: {', '.join(nvc_response.needs) if nvc_response.needs else 'None'}
---

Based on the user's message and the identified feelings and needs, generate an empathetic and helpful response that aligns with NVC principles.
"""
            # 4. Generate the final response
            generate_request = GenerateRequest(prompt=rich_prompt)
            generate_response = self.empathy_generator_stub.Generate(generate_request)

            return TurnResponse(ai_message=generate_response.response_text)

        except grpc.RpcError as e:
            # Handle potential errors from downstream services
            context.set_code(e.code())
            context.set_details(f"Error from downstream service: {e.details()}")
            return TurnResponse()
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"An unexpected error occurred in the orchestrator: {e}")
            return TurnResponse()

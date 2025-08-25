import sys
import os
import pytest

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
# Add the libs directory to the Python path for generated stubs
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'libs', 'clients', 'python')))

# Import the service to be tested
from services.conversation_orchestrator.service import ConversationOrchestratorService
# Import the request object for the service
from libs.clients.python.conversation_orchestrator_pb2 import TurnRequest
# Import the response objects from the services that will be mocked
from libs.clients.python.nvc_processor_pb2 import NVCProcessResponse
from libs.clients.python.prompt_service_pb2 import GetPromptResponse
from libs.clients.python.empathy_generator_pb2 import GenerateResponse

# --- Mock gRPC Stubs ---

class MockNVCProcessorStub:
    def __init__(self, channel):
        pass  # The channel is not needed for the mock
    def Process(self, request):
        return NVCProcessResponse(
            observation=request.text,
            feelings=["sad"],
            needs=["connection"]
        )

class MockPromptServiceStub:
    def __init__(self, channel):
        pass
    def GetPrompt(self, request):
        return GetPromptResponse(prompt_text="You are a helpful NVC coach.")

class MockEmpathyGeneratorStub:
    def __init__(self, channel):
        pass
    def Generate(self, request):
        # The test will assert that the prompt contains the data from the other mocks
        if "sad" in request.prompt and "connection" in request.prompt and "NVC coach" in request.prompt:
            return GenerateResponse(response_text="This is the final generated response.")
        else:
            return GenerateResponse(response_text="ERROR: Prompt was not constructed correctly.")

@pytest.fixture
def orchestrator_service(monkeypatch):
    """
    Returns an instance of the ConversationOrchestratorService with mocked downstream stubs.
    This works by patching the stub classes in the orchestrator's service module *before* the service is instantiated.
    """
    # Import the service module to patch the stubs within its namespace
    import services.conversation_orchestrator.service as orchestrator_service_module

    monkeypatch.setattr(orchestrator_service_module, 'NVCProcessorServiceStub', MockNVCProcessorStub)
    monkeypatch.setattr(orchestrator_service_module, 'PromptServiceStub', MockPromptServiceStub)
    monkeypatch.setattr(orchestrator_service_module, 'EmpathyGeneratorServiceStub', MockEmpathyGeneratorStub)

    # Now, when we create an instance of the service, it will use our mock stubs
    return ConversationOrchestratorService()

def test_process_turn_pipeline(orchestrator_service):
    """
    Tests the full pipeline logic of the ProcessTurn method using mocked downstream services.
    """
    # Arrange
    user_id = "test_user"
    text = "I feel sad because I'm lonely."
    request = TurnRequest(user_id=user_id, text=text)

    # Act
    response = orchestrator_service.ProcessTurn(request, None)

    # Assert
    # The assertion is implicitly handled by the mock EmpathyGeneratorStub.
    # If the prompt was constructed correctly, it returns the success message.
    assert response.ai_message == "This is the final generated response."

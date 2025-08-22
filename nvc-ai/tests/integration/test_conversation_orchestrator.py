import sys
import os
import pytest

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
# Add the libs directory to the Python path for generated stubs
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'libs', 'clients', 'python')))

from services.conversation_orchestrator.service import ConversationOrchestratorService
from libs.clients.python.conversation_orchestrator_pb2 import TurnRequest

@pytest.fixture
def orchestrator_service():
    """Returns an instance of the ConversationOrchestratorService."""
    return ConversationOrchestratorService()

def test_process_turn_placeholder(orchestrator_service):
    """
    Tests the placeholder implementation of the ProcessTurn method.
    """
    # Arrange
    user_id = "test_user"
    text = "Hello, this is a test."
    request = TurnRequest(user_id=user_id, text=text)

    # Act
    response = orchestrator_service.ProcessTurn(request, None)

    # Assert
    assert "Orchestrator received" in response.ai_message
    assert text in response.ai_message
    assert user_id in response.ai_message

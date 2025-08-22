import sys
import os
import pytest
import grpc

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
# Add the libs directory to the Python path for generated stubs
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'libs', 'clients', 'python')))

from services.prompt_service.service import PromptService
from libs.clients.python.prompt_service_pb2 import GetPromptRequest

@pytest.fixture
def prompt_service():
    """Returns an instance of the PromptService."""
    return PromptService()

class MockContext:
    def __init__(self):
        self._code = None
        self._details = None

    def set_code(self, code):
        self._code = code

    def set_details(self, details):
        self._details = details

    def code(self):
        return self._code

    def details(self):
        return self._details

def test_get_prompt_returns_correct_prompt(prompt_service):
    """
    Tests that the GetPrompt method correctly reads and returns the content of a prompt file.
    """
    # Arrange
    request = GetPromptRequest(version="nvc_coach_v1")

    # Act
    response = prompt_service.GetPrompt(request, None)

    # Assert
    assert "You are an AI assistant" in response.prompt_text
    assert "Nonviolent Communication (NVC)" in response.prompt_text

def test_get_prompt_handles_not_found(prompt_service):
    """
    Tests that the GetPrompt method handles non-existent prompt versions gracefully.
    """
    # Arrange
    request = GetPromptRequest(version="non_existent_version")
    context = MockContext()

    # Act
    response = prompt_service.GetPrompt(request, context)

    # Assert
    assert response.prompt_text == ""
    assert context.code() == grpc.StatusCode.NOT_FOUND
    assert "not found" in context.details()

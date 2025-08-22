import sys
import os
import pytest
import httpx

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
# Add the libs directory to the Python path for generated stubs
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'libs', 'clients', 'python')))

from services.empathy_generator.service import EmpathyGeneratorService
from libs.clients.python.empathy_generator_pb2 import GenerateRequest

@pytest.fixture
def empathy_service():
    """Returns an instance of the EmpathyGeneratorService."""
    return EmpathyGeneratorService()

class MockHttpxResponse:
    def __init__(self, json_data, status_code=200):
        self._json_data = json_data
        self.status_code = status_code

    def json(self):
        return self._json_data

    def raise_for_status(self):
        if self.status_code >= 400:
            raise httpx.HTTPStatusError(message="Error", request=None, response=self)

@pytest.fixture
def mock_httpx_post(monkeypatch):
    """Mocks the httpx.Client.post method."""
    def mock_post(*args, **kwargs):
        return MockHttpxResponse({"response": "This is a mocked Ollama response."})

    monkeypatch.setattr(httpx.Client, "post", mock_post)

def test_generate_calls_ollama(empathy_service, mock_httpx_post):
    """
    Tests that the Generate method correctly calls the (mocked) Ollama API and returns a response.
    """
    # Arrange
    prompt = "Why is the sky blue?"
    request = GenerateRequest(prompt=prompt)

    # Act
    response = empathy_service.Generate(request, None)

    # Assert
    assert "mocked Ollama response" in response.response_text

import sys
import os
import pytest

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
# Add the libs directory to the Python path for generated stubs
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'libs', 'clients', 'python')))

from services.emotion_analyzer.service import EmotionAnalyzerService
from libs.clients.python.emotion_analyzer_pb2 import EmotionAnalysisRequest

@pytest.fixture
def emotion_service():
    """Returns an instance of the EmotionAnalyzerService."""
    return EmotionAnalyzerService()

def test_analyze_returns_mocked_response(emotion_service):
    """
    Tests that the Analyze method returns the hardcoded mocked response.
    """
    # Arrange
    request = EmotionAnalysisRequest(text="This is a test sentence.")

    # Act
    response = emotion_service.Analyze(request, None)

    # Assert
    assert response.emotion_probs is not None
    assert "neutral" in response.emotion_probs
    assert response.emotion_probs["neutral"] == 1.0

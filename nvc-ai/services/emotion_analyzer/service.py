import sys
import os

# Add the libs directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'libs', 'clients', 'python')))

from emotion_analyzer_pb2_grpc import EmotionAnalyzerServiceServicer
from emotion_analyzer_pb2 import EmotionAnalysisResponse

class EmotionAnalyzerService(EmotionAnalyzerServiceServicer):
    def Analyze(self, request, context):
        """
        Analyzes the emotion of the text.
        For the MVP, this returns a mocked response.
        """
        return EmotionAnalysisResponse(emotion_probs={"neutral": 1.0})

import sys
import os
import grpc
from concurrent import futures
import time

# Add the libs directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'libs', 'clients', 'python')))

import emotion_analyzer_pb2_grpc
from service import EmotionAnalyzerService

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    emotion_analyzer_pb2_grpc.add_EmotionAnalyzerServiceServicer_to_server(EmotionAnalyzerService(), server)
    server.add_insecure_port('[::]:50052') # Using a different port
    server.start()
    print("Emotion Analyzer Server started on port 50052")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()

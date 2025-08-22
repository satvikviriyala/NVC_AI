import sys
import os
import grpc
from concurrent import futures
import time

# Add the libs directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'libs', 'clients', 'python')))

import conversation_orchestrator_pb2_grpc
from service import ConversationOrchestratorService

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    conversation_orchestrator_pb2_grpc.add_ConversationOrchestratorServiceServicer_to_server(ConversationOrchestratorService(), server)
    server.add_insecure_port('[::]:50055') # Using a different port
    server.start()
    print("Conversation Orchestrator Server started on port 50055")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()

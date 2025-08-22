import sys
import os
import grpc
from concurrent import futures
import time

# Add the libs directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'libs', 'clients', 'python')))

import prompt_service_pb2_grpc
from service import PromptService

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    prompt_service_pb2_grpc.add_PromptServiceServicer_to_server(PromptService(), server)
    server.add_insecure_port('[::]:50053') # Using a different port
    server.start()
    print("Prompt Service Server started on port 50053")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()

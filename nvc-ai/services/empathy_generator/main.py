import sys
import os
import grpc
from concurrent import futures
import time

# Add the libs directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'libs', 'clients', 'python')))

import empathy_generator_pb2_grpc
from service import EmpathyGeneratorService

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    empathy_generator_pb2_grpc.add_EmpathyGeneratorServiceServicer_to_server(EmpathyGeneratorService(), server)
    server.add_insecure_port('[::]:50054') # Using a different port
    server.start()
    print("Empathy Generator Server started on port 50054")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()

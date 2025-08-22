import sys
import os
import grpc
from concurrent import futures
import time

# Add the libs directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'libs', 'clients', 'python')))

import nvc_processor_pb2_grpc
from service import NVCProcessorService

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    nvc_processor_pb2_grpc.add_NVCProcessorServiceServicer_to_server(NVCProcessorService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started on port 50051")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()

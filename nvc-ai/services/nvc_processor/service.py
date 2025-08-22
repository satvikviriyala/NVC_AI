import sys
import os

# Add the libs directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'libs', 'clients', 'python')))

import json
from nvc_processor_pb2_grpc import NVCProcessorServiceServicer
from nvc_processor_pb2 import NVCProcessResponse

class NVCProcessorService(NVCProcessorServiceServicer):
    def __init__(self):
        self.feelings = self._load_taxonomy('feelings.json')
        self.needs = self._load_taxonomy('needs.json')

    def _load_taxonomy(self, filename):
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'libs', 'nvc_taxonomy', filename))
        with open(path, 'r') as f:
            return set(json.load(f))

    def Process(self, request, context):
        text = request.text.lower()

        found_feelings = [feeling for feeling in self.feelings if feeling in text]
        found_needs = [need for need in self.needs if need in text]

        return NVCProcessResponse(
            observation=request.text,
            feelings=found_feelings,
            needs=found_needs
        )

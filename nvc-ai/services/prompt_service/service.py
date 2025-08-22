import sys
import os
import grpc

# Add the libs directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'libs', 'clients', 'python')))

from prompt_service_pb2_grpc import PromptServiceServicer
from prompt_service_pb2 import GetPromptResponse

class PromptService(PromptServiceServicer):
    def GetPrompt(self, request, context):
        """
        Retrieves a prompt template from a file based on the version.
        """
        version = request.version
        template_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates', f'{version}.txt'))

        if not os.path.exists(template_path):
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Prompt version '{version}' not found.")
            return GetPromptResponse()

        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                prompt_text = f.read()
            return GetPromptResponse(prompt_text=prompt_text)
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Failed to read prompt file: {e}")
            return GetPromptResponse()

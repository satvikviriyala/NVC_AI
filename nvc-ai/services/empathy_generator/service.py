import sys
import os

# Add the libs directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'libs', 'clients', 'python')))

import httpx
import grpc
from empathy_generator_pb2_grpc import EmpathyGeneratorServiceServicer
from empathy_generator_pb2 import GenerateResponse

OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://ollama:11434")
OLLAMA_API_GENERATE_URL = f"{OLLAMA_API_URL}/api/generate"
# A small, default model that should be available in Ollama
DEFAULT_MODEL = "llama3"

class EmpathyGeneratorService(EmpathyGeneratorServiceServicer):
    def Generate(self, request, context):
        """
        Generates an empathic response based on the prompt by calling the Ollama API.
        """
        try:
            payload = {
                "model": DEFAULT_MODEL,
                "prompt": request.prompt,
                "stream": False  # We want a single response for now
            }

            with httpx.Client() as client:
                response = client.post(OLLAMA_API_GENERATE_URL, json=payload, timeout=60.0)
                response.raise_for_status() # Raise an exception for bad status codes

            response_data = response.json()
            generated_text = response_data.get("response", "").strip()

            if not generated_text:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Ollama returned an empty response.")
                return GenerateResponse()

            return GenerateResponse(response_text=generated_text)

        except httpx.RequestError as e:
            context.set_code(grpc.StatusCode.UNAVAILABLE)
            context.set_details(f"Failed to connect to Ollama: {e}")
            return GenerateResponse()
        except httpx.HTTPStatusError as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Ollama returned an error: {e.response.status_code} - {e.response.text}")
            return GenerateResponse()
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"An unexpected error occurred: {e}")
            return GenerateResponse()

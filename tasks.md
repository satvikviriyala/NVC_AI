
---

### **Project: NVC Embedded AI - MVP Build Plan**

**Objective:** Construct a functional, local-first MVP based on the defined architecture. The final MVP will accept a text input, process it through a simplified NVC pipeline, generate an empathic response using a local LLM, and return it.

---

### **Phase 1: Project Scaffolding & Core Libraries**

*   **Task 1: Initialize Project Structure**
    *   **Goal:** Create the root directory and all top-level folders.
    *   **Action:**
        1.  Create a root directory named `nvc-ai`.
        2.  Inside `nvc-ai`, create the following empty directories: `apps`, `services`, `serving`, `data`, `models`, `pipelines`, `infra`, `libs`, `tests`, `docs`, `scripts`.

*   **Task 2: Initialize Version Control**
    *   **Goal:** Set up a Git repository and a basic `.gitignore` file.
    *   **Action:**
        1.  In the `nvc-ai` root, run `git init`.
        2.  Create a file named `.gitignore` in the root.
        3.  Add the following content to `.gitignore`: `__pycache__/`, `*.pyc`, `.env`, `*.db`, `data/raw/*`, `models/checkpoints/*`.

*   **Task 3: Create Core NVC Taxonomy Data**
    *   **Goal:** Define the canonical lists of feelings and needs.
    *   **Action:**
        1.  Create the directory `libs/nvc_taxonomy/`.
        2.  Create a file `libs/nvc_taxonomy/feelings.json`. Populate it with a simple list of feeling words (e.g., `["happy", "sad", "angry", "confused", "excited"]`).
        3.  Create a file `libs/nvc_taxonomy/needs.json`. Populate it with a simple list of universal needs (e.g., `["connection", "safety", "understanding", "autonomy"]`).

*   **Task 4: Define Initial gRPC Contracts (Proto)**
    *   **Goal:** Create the Protobuf files that define the communication contracts between services.
    *   **Action:**
        1.  Create the directory `libs/proto/`.
        2.  Create `libs/proto/nvc_processor.proto` with `NVCProcessRequest` and `NVCProcessResponse` messages as defined in the architecture.
        3.  Create `libs/proto/emotion_analyzer.proto` with `EmotionAnalysisRequest` and `EmotionAnalysisResponse` messages.
        4.  Create `libs/proto/empathy_generator.proto` with `GenerateRequest` and `GenerateResponse` messages.

*   **Task 5: Generate Python gRPC Client Stubs**
    *   **Goal:** Generate the necessary Python code from the `.proto` files.
    *   **Action:**
        1.  Create a `requirements.txt` in the root with `grpcio` and `grpcio-tools`.
        2.  Run the `protoc` command to generate Python stubs for all `.proto` files, outputting them into a `libs/clients/python/` directory.

### **Phase 2: Local Infrastructure Setup (Docker)**

*   **Task 6: Create the Docker Compose File**
    *   **Goal:** Define the core third-party services in a `docker-compose.yml` file.
    *   **Action:**
        1.  Create the directory `infra/local/`.
        2.  Create a file `infra/local/docker-compose.yml`.

*   **Task 7: Configure Postgres Service**
    *   **Goal:** Add the Postgres database service to the Docker Compose file.
    *   **Action:** In `infra/local/docker-compose.yml`, define a `postgres` service using the official `postgres:16` image, configure environment variables for the default user/password/db, and set up a named volume.

*   **Task 8: Configure Redis Service**
    *   **Goal:** Add the Redis cache service to the Docker Compose file.
    *   **Action:** In `infra/local/docker-compose.yml`, define a `redis` service using the official `redis:7` image and set up a named volume.

*   **Task 9: Configure Ollama Service**
    *   **Goal:** Add the Ollama LLM serving engine for easy local inference.
    *   **Action:** In `infra/local/docker-compose.yml`, define an `ollama` service using the `ollama/ollama` image, set up a named volume, and map the port `11434`.

*   **Task 10: Create `.env.example`**
    *   **Goal:** Create a template for environment variables needed by the system.
    *   **Action:**
        1.  Create a file named `.env.example` in the root directory.
        2.  Add keys for `POSTGRES_DSN`, `REDIS_URL`, and `OLLAMA_API_URL=http://ollama:11434`.

### **Phase 3: Building the Simplest Services (Bottom-Up)**

*   **Task 11: Scaffold `nvc-processor` Service**
    *   **Goal:** Create the directory structure and a basic, non-functional gRPC server.
    *   **Action:**
        1.  Create `services/nvc-processor/`.
        2.  Create `services/nvc-processor/main.py` with a main function that starts a gRPC server.
        3.  Create `services/nvc-processor/service.py` containing a class that inherits from the generated gRPC servicer and has a placeholder `Process` method that returns an empty response.

*   **Task 12: Implement Rule-Based `nvc-processor`**
    *   **Goal:** Implement a simple, testable, rule-based logic for slot filling.
    *   **Action:**
        1.  In `services/nvc-processor/service.py`, modify the `Process` method.
        2.  **Observation:** Return the input text as the `observation`.
        3.  **Feelings:** Scan the input text for any word that exists in `libs/nvc_taxonomy/feelings.json`.
        4.  **Needs:** Scan the input text for any word that exists in `libs/nvc_taxonomy/needs.json`.
        5.  Return a populated `NVCProcessResponse`.

*   **Task 13: Write Unit Test for `nvc-processor`**
    *   **Goal:** Create a test that verifies the rule-based logic.
    *   **Action:**
        1.  Create `tests/integration/test_nvc_processor.py`.
        2.  Write a `pytest` function that calls the `nvc-processor`'s `Process` method directly with sample text (e.g., "I feel sad because I need connection.") and asserts that the returned slots are correct.

*   **Task 14: Scaffold `emotion-analyzer` Service**
    *   **Goal:** Create the service structure with a mocked response.
    *   **Action:**
        1.  Create `services/emotion-analyzer/` with `main.py` and `service.py`.
        2.  Implement the gRPC server.
        3.  In the `Analyze` method, return a hardcoded response (e.g., `{"emotion_probs": {"neutral": 1.0}}`). This allows other services to integrate with it before the ML model is ready.

*   **Task 15: Scaffold `prompt-service`**
    *   **Goal:** Create a service that reads a prompt template from a file.
    *   **Action:**
        1.  Create `services/prompt-service/` with `main.py` and `service.py`.
        2.  Create a directory `services/prompt-service/templates/`.
        3.  Create `services/prompt-service/templates/nvc_coach_v1.txt`. Write a simple NVC system prompt in it.
        4.  Implement a gRPC method `GetPrompt(version)` that reads the corresponding file and returns its content.

### **Phase 4: Implementing the Generation and Orchestration Core**

*   **Task 16: Scaffold `empathy-generator` Service**
    *   **Goal:** Create the service structure that will eventually call the LLM.
    *   **Action:** Create `services/empathy-generator/` with `main.py`, `service.py`, and a placeholder gRPC `Generate` method.

*   **Task 17: Connect `empathy-generator` to Ollama**
    *   **Goal:** Implement the logic to call the local Ollama service.
    *   **Action:**
        1.  In `services/empathy-generator/service.py`, use a Python HTTP client (like `requests` or `httpx`).
        2.  The `Generate` method should take a prompt, construct a request payload for Ollama's API, and send it to the `OLLAMA_API_URL`.
        3.  Return the text from Ollama's response.

*   **Task 18: Scaffold `conversation-orchestrator` Service**
    *   **Goal:** Create the main orchestrator service structure.
    *   **Action:** Create `services/conversation-orchestrator/` with `main.py` and `service.py`. Implement a placeholder gRPC method `ProcessTurn`.

*   **Task 19: Implement `orchestrator`'s Pipeline Logic**
    *   **Goal:** Wire the services together within the orchestrator.
    *   **Action:** In the `ProcessTurn` method of the orchestrator:
        1.  Initialize gRPC clients for the `nvc-processor`, `emotion-analyzer`, and `empathy-generator`.
        2.  Call `nvc-processor` with the user's input text.
        3.  (Skip `emotion-analyzer` for now, as it's mocked).
        4.  Construct a new prompt by combining a system message with the structured output from `nvc-processor`.
        5.  Call `empathy-generator` with this new, rich prompt.
        6.  Return the final response from the `empathy-generator`.

### **Phase 5: Exposing the Service & Creating a Client**

*   **Task 20: Scaffold `api-gateway` Service**
    *   **Goal:** Create a simple HTTP server (e.g., using FastAPI or Flask) that will be the public entry point.
    *   **Action:**
        1.  Create `services/api-gateway/`.
        2.  Create a `main.py` with a FastAPI app.
        3.  Define a single POST endpoint, `/chat`.

*   **Task 21: Connect `api-gateway` to `orchestrator`**
    *   **Goal:** The gateway should forward requests to the orchestrator via gRPC.
    *   **Action:**
        1.  In `services/api-gateway/main.py`, initialize a gRPC client for the `conversation-orchestrator`.
        2.  In the `/chat` endpoint, call the orchestrator's `ProcessTurn` method with the request body.
        3.  Return the orchestrator's response as the HTTP response.

*   **Task 22: Add All Services to Docker Compose**
    *   **Goal:** Make all custom services runnable via `docker-compose up`.
    *   **Action:** For each service (`nvc-processor`, `emotion-analyzer`, `empathy-generator`, `orchestrator`, `api-gateway`):
        1.  Create a `Dockerfile` in its directory.
        2.  Add a corresponding service definition in `infra/local/docker-compose.yml`, using `build: ./services/...` and exposing the correct ports.

*   **Task 23: Create a Minimalist Web Client**
    *   **Goal:** Build a very simple HTML page with JavaScript to test the entire stack.
    *   **Action:**
        1.  Create `apps/web-client/`.
        2.  Create `apps/web-client/index.html`.
        3.  The HTML should have a text input, a "Send" button, and a `<div>` to display the response.
        4.  Add a `<script>` block that uses `fetch` to POST the input's value to the `api-gateway`'s `/chat` endpoint and displays the result in the response `<div>`.

### **Phase 6: Adding Basic State and Validation**

*   **Task 24: Scaffold `session-state` Service**
    *   **Goal:** Create a service to manage conversation history.
    *   **Action:** Create `services/session-state/` with a gRPC service definition for `GetSession` and `UpdateSession`.

*   **Task 25: Implement Redis Logic in `session-state`**
    *   **Goal:** Use the Redis container to store and retrieve messages.
    *   **Action:** In `services/session-state/service.py`, use the `redis` Python library to connect to the `REDIS_URL`. Implement the `Get` and `Update` methods to append messages to a list stored against a session ID key.

*   **Task 26: Integrate `session-state` into `orchestrator`**
    *   **Goal:** The orchestrator should now load and save conversation history.
    *   **Action:**
        1.  In the `orchestrator`, before processing, call `session-state`'s `GetSession` to retrieve the last K turns.
        2.  Prepend this history to the context sent to the `empathy-generator`.
        3.  After receiving a response, call `UpdateSession` to save the new user message and AI response.

*   **Task 27: Scaffold `compliance-validator` Service**
    *   **Goal:** Create the service with a simple, rule-based validation check.
    *   **Action:**
        1.  Create `services/compliance-validator/` with a gRPC service.
        2.  Implement a `Validate` method that checks if the response text contains judgmental phrases (e.g., "you should have," "you always"). Return `{ok: false}` if found, `{ok: true}` otherwise.

*   **Task 28: Integrate `compliance-validator` into `orchestrator`**
    *   **Goal:** The orchestrator should validate every LLM response before returning it.
    *   **Action:** After the `empathy-generator` returns a response, the `orchestrator` must call the `compliance-validator`. If the response is not `ok`, for the MVP, it can simply prepend "[VALIDATION FAILED]: " to the response text.

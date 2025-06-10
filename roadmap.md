Of course. A detailed roadmap is essential for turning the design document into a real project. This roadmap breaks down the MVP development into clear, sequential phases, steps, and tasks. It assumes a small team (or a single developer) and prioritizes proving the core concept above all else.

---

### **MVP Development Roadmap: Project Myriad (or Neutrino)**

**Project Goal:** To build a functional prototype that validates the core architecture of orchestrating multiple, minimalist, specialized AI agents to answer a query.
**Target Query for MVP:** "Why was the lightbulb important for factories?"

---

### **Phase 1: Foundation & Core Component Setup (Weeks 1-2)**

**Goal:** Establish the project structure, development environment, and build the non-intelligent "scaffolding" of the system. This phase is all about creating the "nervous system" before the "neurons" are intelligent.

*   **Step 1.1: Environment and Project Initialization**
    *   **Task 1.1.1:** Initialize a Git repository for version control.
    *   **Task 1.1.2:** Create a project structure with directories: `/orchestrator`, `/agents`, `/common`, `/tests`.
    *   **Task 1.1.3:** Set up a virtual environment (e.g., venv, conda) and create a `requirements.txt` file.
    *   **Task 1.1.4:** Install initial dependencies: `Python`, `Flask` (or `FastAPI`), `requests`.

*   **Step 1.2: Build the Central Orchestrator Skeleton**
    *   **Task 1.2.1:** Create the main `orchestrator.py` script.
    *   **Task 1.2.2:** Implement the `AI_REGISTRY` dictionary, hardcoding the future addresses of the agents (e.g., `http://localhost:5001`).
    *   **Task 1.2.3:** Write the core orchestration logic: a function that takes a list of keywords, iterates the registry, and prepares to make API calls. For now, these calls will fail, which is expected.
    *   **Task 1.2.4:** Add comprehensive logging to track the orchestrator's state (e.g., "Received keywords," "Querying Lightbulb_AI," "Received response").

*   **Step 1.3: Develop the Simplest Small Agent (The Template)**
    *   **Task 1.3.1:** In the `/agents` directory, create a `Lightbulb_AI` folder.
    *   **Task 1.3.2:** Inside, create a Flask/FastAPI app (`agent_app.py`).
    *   **Task 1.3.3:** Create a single `/query` endpoint that, for now, just returns a hardcoded success message: `{"status": "Lightbulb_AI is online"}`.
    *   **Task 1.3.4:** Create a `Dockerfile` for the agent. This containerizes the agent, making it an independent microservice and preparing for future scalability.
    *   **Task 1.3.5:** Write a simple `run.sh` script to build the Docker image and run the container on a specific port (e.g., 5001).

**Phase 1 Deliverable:** A runnable orchestrator script that can successfully ping a single, non-intelligent agent running in a Docker container and log the interaction.

---

### **Phase 2: Implementing Agent Intelligence & Communication (Week 3)**

**Goal:** Populate the agents with their specialized knowledge and establish a working data flow from the Orchestrator to the agents and back.

*   **Step 2.1: Define the Standard Communication Protocol**
    *   **Task 2.1.1:** Formally decide on the JSON structure for all communication.
        *   Request: `{ "query": "core_info" }`
        *   Response: `{ "source_agent": "AgentName", "data": { ... } }`
    *   **Task 2.1.2:** Document this protocol in a `PROTOCOL.md` file in the project root.

*   **Step 2.2: Implement Intelligence for `Lightbulb_AI`**
    *   **Task 2.2.1:** Modify the `Lightbulb_AI`'s `/query` endpoint.
    *   **Task 2.2.2:** Add the hardcoded knowledge dictionary as described in the design document.
    *   **Task 2.2.3:** Update the endpoint to return this dictionary as the `data` payload in the standardized JSON response.
    *   **Task 2.2.4:** Write a unit test to verify the `/query` endpoint returns the correct data structure and content.

*   **Step 2.3: Clone and Specialize for `Factory_AI`**
    *   **Task 2.3.1:** Duplicate the `Lightbulb_AI` directory and rename it to `Factory_AI`.
    *   **Task 2.3.2:** Modify its Flask app to run on a different port (e.g., 5002).
    *   **Task 2.3.3:** Replace the knowledge dictionary with the factory-specific information.
    *   **Task 2.3.4:** Update its Dockerfile and `run.sh` script for the new port.
    *   **Task 2.3.5:** Write a unit test for the `Factory_AI`'s endpoint.

*   **Step 2.4: Integrate into the Orchestrator**
    *   **Task 2.4.1:** Update the `Orchestrator`'s logic to make real `requests.get()` calls to the agents.
    *   **Task 2.4.2:** Implement error handling (e.g., what if an agent is offline or returns an error?).
    *   **Task 2.4.3:** Update the logging to show the actual data being received from each agent.

**Phase 2 Deliverable:** The Orchestrator can now successfully query two distinct, intelligent agents running in separate containers and collect their specialized knowledge packets.

---

### **Phase 3: Parsing, Synthesis, and Final Output (Week 4)**

**Goal:** Complete the full data-flow loop by processing the initial user input and synthesizing the collected agent data into a coherent final answer.

*   **Step 3.1: Build the Input Parser**
    *   **Task 3.1.1:** Create the `InputParser` module (`parser.py`).
    *   **Task 3.1.2:** Implement the simple keyword-extraction logic based on the MVP's target query.
    *   **Task 3.1.3:** Write unit tests for the parser (e.g., `test_parser("...lightbulb and factories...")` should return `['lightbulb', 'factories']`).
    *   **Task 3.1.4:** Integrate the parser into the main `orchestrator.py` script. The system can now take the raw query string as input.

*   **Step 3.2: Build the Output Synthesizer**
    *   **Task 3.2.1:** Create the `OutputSynthesizer` module (`synthesizer.py`).
    *   **Task 3.2.2:** Implement the simple, rule-based logic for combining the data from the `Lightbulb_AI` and `Factory_AI` into a single sentence.
    *   **Task 3.2.3:** The function should take a list of JSON objects (the agent responses) and return a final string.
    *   **Task 3.2.4:** Write unit tests for the synthesizer to ensure it correctly combines the expected inputs.

*   **Step 3.3: Final Assembly and End-to-End Test**
    *   **Task 3.3.1:** In the `Orchestrator`, after collecting the agent responses, pass them to the `OutputSynthesizer`.
    *   **Task 3.3.2:** The final output of the `Orchestrator` should now be the human-readable sentence.
    *   **Task 3.3.3:** Create a `main.py` entry point that allows a user to run the entire system from one command.
    *   **Task 3.3.4:** Perform a full, end-to-end test: run the two agent containers, then run `main.py` with the target query, and verify the final output is correct.
    *   **Task 3.3.5:** Write a comprehensive `README.md` file explaining how to set up and run the MVP.

**Phase 3 Deliverable:** A fully functional MVP prototype. When executed, it takes the target query as input and produces the correct, synthesized sentence as output, with all components working in concert.

---

**Post-MVP (Phase 4 and Beyond):**

*   **Step 4.1: Refactor & Harden:** Clean up code, improve error handling, and add more robust testing.
*   **Step 4.2: Demonstrate Ambiguity:** Implement the "drive" example with an `Ambiguity_Resolution_AI` as the next proof-of-concept.
*   **Step 4.3: Explore Dynamic Instantiation:** Begin research and development on a "factory for factories"—an AI that can create and register a new agent on the fly.

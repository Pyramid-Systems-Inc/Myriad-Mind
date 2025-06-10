Excellent. Let's build the definitive, highly-detailed roadmap for the **Aligned MVP 2.0**. This plan is meticulously structured to ensure that every step we take directly serves the core principles of the Myriad Architecture.

The focus is on **process and proof**. We need to see in our logs that the "thinking" is happening where it's supposed to: within the specialized agents.

---

### **Aligned MVP 2.0 Development Roadmap: Project Myriad**

**Core Hypothesis to Validate:** Intelligence can emerge from the orchestration of minimalist, specialized agents, where each agent contributes a piece of reasoned knowledge, rather than being a dumb data store.

**MVP Target Query:** "Define a lightbulb and explain its limitation."

---

### **Phase 1: Architecture & Environment Setup (Est. Time: 3-4 days)**

**Goal:** Lay a robust and clean foundation. This is the "measure twice, cut once" phase. All components will be skeletons, but the communication paths and data structures will be clearly defined.

*   **Step 1.1: Project Initialization & Version Control**
    *   **Task 1.1.1:** `git init` a new repository.
    *   **Task 1.1.2:** Create the directory structure:
        ```
        /project_myriad
        |-- /agents
        |   |-- /lightbulb_definition_ai
        |   |-- /lightbulb_function_ai
        |-- /orchestration
        |-- /processing
        |   |-- /input_processor
        |   |-- /output_processor
        |-- /tests
        |-- docker-compose.yml
        |-- README.md
        |-- .gitignore
        ```
    *   **Task 1.1.3:** Initialize Python virtual environment and `requirements.txt` with `flask`, `requests`, `pytest`.

*   **Step 1.2: Define the Core Data Protocols**
    *   **Task 1.2.1:** Create a `PROTOCOLS.md` file.
    *   **Task 1.2.2:** Define the **Processor-to-Orchestrator Protocol (The "Task List")**:
        ```json
        // Sent from Input Processor to Orchestrator
        {
          "query_id": "xyz-123",
          "tasks": [
            { "task_id": 1, "intent": "define", "concept": "lightbulb", "args": {} },
            { "task_id": 2, "intent": "explain_limitation", "concept": "lightbulb", "args": {} }
          ]
        }
        ```
    *   **Task 1.2.3:** Define the **Orchestrator-to-Agent Protocol (The "Agent Job")**:
        ```json
        // Sent from Orchestrator to an Agent
        { "intent": "define" } // or { "intent": "explain_limitation" }
        ```
    *   **Task 1.2.4:** Define the **Agent-to-Orchestrator Protocol (The "Agent Result")**:
        ```json
        // Sent from Agent back to Orchestrator
        {
          "agent_name": "Lightbulb_Definition_AI",
          "status": "success",
          "data": "an electric device that produces light via an incandescent filament"
        }
        ```

*   **Step 1.3: Docker Compose Setup**
    *   **Task 1.3.1:** Create a `docker-compose.yml` file.
    *   **Task 1.3.2:** Define services for the two agents (`lightbulb_definition_ai`, `lightbulb_function_ai`), exposing their respective ports (e.g., 5001, 5002). This allows us to launch the entire agent network with one command: `docker-compose up`.

**Phase 1 Deliverable:** A structured project repository with clearly defined data contracts and a `docker-compose.yml` that is ready to run the (not yet built) agent services.

---

### **Phase 2: Agent Implementation & Cognitive Logic (Est. Time: 4-5 days)**

**Goal:** Build the specialized "neurons" of our system. The focus here is on embedding the reasoning *inside* the agents.

*   **Step 2.1: Implement `Lightbulb_Definition_AI` (Type A Fact-Base)**
    *   **Task 2.1.1:** Inside `/agents/lightbulb_definition_ai`, create a simple Flask app.
    *   **Task 2.1.2:** Create a `/query` endpoint that accepts POST requests.
    *   **Task 2.1.3:** Implement logic: If `request.json['intent'] == 'define'`, return the hardcoded definition in the standard "Agent Result" format.
    *   **Task 2.1.4:** Create a `Dockerfile` for this agent.
    *   **Task 2.1.5:** Write a unit test using `pytest` to call the endpoint and verify the correct data is returned for the "define" intent.

*   **Step 2.2: Implement `Lightbulb_Function_AI` (Type B Function-Executor)**
    *   **Task 2.2.1:** Inside `/agents/lightbulb_function_ai`, create a similar Flask app.
    *   **Task 2.2.2:** Create a `/query` endpoint.
    *   **Task 2.2.3:** **CRITICAL TASK:** Implement the cognitive logic:
        ```python
        if request.json['intent'] == 'explain_limitation':
            # This is the "thinking" happening inside the agent
            reasoned_limitation = "it generates significant waste heat, making it inefficient."
            return jsonify({ "agent_name": "Lightbulb_Function_AI", "status": "success", "data": reasoned_limitation })
        ```
    *   **Task 2.2.4:** Create a `Dockerfile` for this agent.
    *   **Task 2.2.5:** Write a unit test to specifically validate that the "explain_limitation" intent returns the reasoned data.

*   **Step 2.3: Network Test**
    *   **Task 2.3.1:** Run `docker-compose up --build`.
    *   **Task 2.3.2:** From your local machine (outside of Docker), use a tool like `curl` or Postman to manually send requests to `localhost:5001` and `localhost:5002` to confirm both agents are online and responding correctly.

**Phase 2 Deliverable:** Two independent, containerized microservice agents, each responding correctly to their specialized intent. We have proven that the cognitive logic resides within the specialist agent.

---

### **Phase 3: Building the Central Nervous System (Est. Time: 4-5 days)**

**Goal:** Create the routing and processing layers that manage the flow of information.

*   **Step 3.1: Implement the Input Processor**
    *   **Task 3.1.1:** Create a Python module in `/processing/input_processor`.
    *   **Task 3.1.2:** Write a function `process_query(text: str) -> dict`.
    *   **Task 3.1.3:** Implement the logic to parse the MVP query string. This can be rule-based for the MVP (e.g., using regex or `if 'define' in text and 'limitation' in text`).
    *   **Task 3.1.4:** The function must return the correctly structured "Task List" JSON object as defined in the protocol.
    *   **Task 3.1.5:** Write unit tests to ensure the parser correctly translates the MVP query into the Task List object.

*   **Step 3.2: Implement the Orchestrator**
    *   **Task 3.2.1:** Create the main script in `/orchestration`.
    *   **Task 3.2.2:** Implement the Agent Registry: a dictionary mapping (`concept`, `intent`) tuples to agent URLs.
        ```python
        REGISTRY = {
            ('lightbulb', 'define'): 'http://lightbulb_definition_ai:5001/query',
            ('lightbulb', 'explain_limitation'): 'http://lightbulb_function_ai:5002/query'
        }
        # Note: We use the service name from docker-compose, not localhost.
        ```
    *   **Task 3.2.3:** Write the main orchestration loop:
        1.  Accepts a "Task List" object.
        2.  Initializes an empty dictionary `results = {}`.
        3.  Iterates through each `task` in the list.
        4.  Looks up the correct agent URL from the `REGISTRY`.
        5.  Makes a `requests.post()` call to that agent with the correct "Agent Job" payload.
        6.  Stores the agent's response in the `results` dictionary, keyed by `task_id`.
    *   **Task 3.2.4:** Implement robust logging for every step (e.g., "Dispatching task 1 to Lightbulb_Definition_AI...").

*   **Step 3.3: Implement the Output Processor**
    *   **Task 3.3.1:** Create a Python module in `/processing/output_processor`.
    *   **Task 3.3.2:** Write a function `synthesize_output(results: dict) -> str`.
    *   **Task 3.3.3:** Implement simple assembly logic. This should be "dumb" string formatting, not reasoning.
        ```python
        # Example logic
        definition = results['1']['data']
        limitation = results['2']['data']
        return f"A lightbulb is defined as: '{definition}'. A key limitation is that {limitation}"
        ```
    *   **Task 3.3.4:** Write a unit test for the synthesizer, giving it a mock `results` dictionary and asserting the output string is correct.

**Phase 3 Deliverable:** A complete, testable set of orchestration and processing modules. They are not yet connected, but each part is individually verified.

---

### **Phase 4: Integration, End-to-End Testing & Validation (Est. Time: 2-3 days)**

**Goal:** Connect all the pieces, run the full system, and formally validate the core hypothesis.

*   **Step 4.1: Create the Main Application Entrypoint**
    *   **Task 4.1.1:** Create a `main.py` at the project root.
    *   **Task 4.1.2:** This script will:
        1.  Take the raw query string as an argument.
        2.  Call the `InputProcessor` to get the Task List.
        3.  Pass the Task List to the `Orchestrator` to get the results.
        4.  Pass the results to the `OutputProcessor` to get the final sentence.
        5.  Print the final sentence to the console.

*   **Step 4.2: The Full System Test**
    *   **Task 4.2.1:** Run `docker-compose up` to start the agent network.
    *   **Task 4.2.2:** In a separate terminal, run `python main.py "Define a lightbulb and explain its limitation."`
    *   **Task 4.2.3:** **VALIDATION STEP:**
        *   **Check 1 (Correctness):** Does the final output sentence match the expected result?
        *   **Check 2 (Architectural Purity):** Review the Orchestrator's logs. Do they clearly show it dispatching two separate tasks to two different agents? Do they show the reasoned data ("...waste heat...") coming *from* the `Lightbulb_Function_AI` and *not* being created by the `OutputProcessor`?

*   **Step 4.3: Documentation**
    *   **Task 4.3.1:** Thoroughly update the `README.md` with a project description, architecture overview, and step-by-step instructions on how to run the MVP.

**Phase 4 Deliverable:** A fully functional and documented MVP that successfully demonstrates the core principles of the Myriad Cognitive Architecture. We have tangible proof that our design is viable.
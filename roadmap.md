Excellent. Let's build the definitive, highly-detailed roadmap for the **Aligned MVP 2.0**. This plan is meticulously structured to ensure that every step we take directly serves the core principles of the Myriad Architecture.

The focus is on **process and proof**. We need to see in our logs that the "thinking" is happening where it's supposed to: within the specialized agents.

---

### **Aligned MVP 2.0 Development Roadmap: Project Myriad**

**Core Hypothesis to Validate:** Intelligence can emerge from the orchestration of minimalist, specialized agents, where each agent contributes a piece of reasoned knowledge, rather than being a dumb data store.

**MVP Target Query:** "Define a lightbulb and explain its limitation."

---

### **Phase 1: Architecture & Environment Setup (Est. Time: 3-4 days) - ✅ COMPLETED**

**Goal:** Lay a robust and clean foundation. This is the "measure twice, cut once" phase. All components will be skeletons, but the communication paths and data structures will be clearly defined.

*   **Step 1.1: Project Initialization & Version Control** ✅ **COMPLETED**
    *   **Task 1.1.1:** ✅ Repository initialized with proper version control
    *   **Task 1.1.2:** ✅ Complete directory structure created:
        ```
        /Myriad-Mind
        |-- /agents
        |   |-- /lightbulb_definition_ai (ready for implementation)
        |   |-- /lightbulb_function_ai (ready for implementation)
        |-- /orchestration (ready for implementation)
        |-- /processing
        |   |-- /input_processor (ready for implementation)
        |   |-- /output_processor (ready for implementation)
        |-- /tests (ready for test implementation)
        |-- docker-compose.yml ✅
        |-- main.py ✅ (Phase 4 integration placeholder)
        |-- README.md ✅
        |-- .gitignore ✅
        |-- design and concept.md ✅ (Full architectural blueprint)
        ```
    *   **Task 1.1.3:** ✅ [`requirements.txt`](requirements.txt:1) initialized with core dependencies: [`flask`](requirements.txt:1), [`requests`](requirements.txt:2), [`pytest`](requirements.txt:3)

*   **Step 1.2: Define the Core Data Protocols** ✅ **COMPLETED**
    *   **Task 1.2.1:** ✅ [`PROTOCOLS.md`](PROTOCOLS.md:1) file created with comprehensive documentation
    *   **Task 1.2.2:** ✅ **Processor-to-Orchestrator Protocol** defined in [`PROTOCOLS.md`](PROTOCOLS.md:5-26)
    *   **Task 1.2.3:** ✅ **Orchestrator-to-Agent Protocol** defined in [`PROTOCOLS.md`](PROTOCOLS.md:27-41)
    *   **Task 1.2.4:** ✅ **Agent-to-Orchestrator Protocol** defined in [`PROTOCOLS.md`](PROTOCOLS.md:42-58)

*   **Step 1.3: Docker Compose Setup** ✅ **COMPLETED**
    *   **Task 1.3.1:** ✅ [`docker-compose.yml`](docker-compose.yml:1) file created
    *   **Task 1.3.2:** ✅ Services defined for both agents with proper networking:
        - [`lightbulb_definition_ai`](docker-compose.yml:4) on port 5001
        - [`lightbulb_function_ai`](docker-compose.yml:15) on port 5002
        - Configured with [`myriad_network`](docker-compose.yml:27) for inter-service communication

*   **Step 1.4: Additional Foundation Work** ✅ **COMPLETED**
    *   ✅ [`design and concept.md`](design and concept.md:1) - Complete architectural blueprint and philosophy
    *   ✅ [`main.py`](main.py:1) - Application entrypoint with integration flow documented
    *   ✅ Comprehensive project documentation and vision alignment

**Phase 1 Deliverable:** ✅ **DELIVERED** - A fully structured project repository with clearly defined data contracts, complete architectural documentation, and a [`docker-compose.yml`](docker-compose.yml:1) ready to orchestrate agent services once implemented.

**🚀 READY FOR PHASE 2:** The foundation is solid. All directories are created, protocols are defined, and the development environment is fully prepared for agent implementation.

---

### **Phase 2: Agent Implementation & Cognitive Logic (Est. Time: 4-5 days)**

**Goal:** Build the specialized "neurons" of our system. The focus here is on embedding the reasoning *inside* the agents.

*   **Step 2.1: Implement `Lightbulb_Definition_AI` (Type A Fact-Base)** ✅ **COMPLETED**
    *   **Task 2.1.1:** ✅ Inside `/agents/lightbulb_definition_ai`, created [`app.py`](agents/lightbulb_definition_ai/app.py:1) Flask application
    *   **Task 2.1.2:** ✅ Created [`/query`](agents/lightbulb_definition_ai/app.py:7) endpoint that accepts POST requests
    *   **Task 2.1.3:** ✅ Implemented logic: [`request.json['intent'] == 'define'`](agents/lightbulb_definition_ai/app.py:19) returns hardcoded definition in standard "Agent Result" format
    *   **Task 2.1.4:** ✅ Created [`Dockerfile`](agents/lightbulb_definition_ai/Dockerfile:1) for this agent
    *   **Task 2.1.5:** ✅ Written comprehensive unit tests in [`test_app.py`](agents/lightbulb_definition_ai/test_app.py:1) using `pytest` - all 4 tests pass

*   **Step 2.2: Implement `Lightbulb_Function_AI` (Type B Function-Executor)** ✅ **COMPLETED**
    *   **Task 2.2.1:** ✅ Inside [`/agents/lightbulb_function_ai`](agents/lightbulb_function_ai/app.py:1), created Flask application
    *   **Task 2.2.2:** ✅ Created [`/query`](agents/lightbulb_function_ai/app.py:13) endpoint that accepts POST requests
    *   **Task 2.2.3:** ✅ **CRITICAL TASK:** Implemented the cognitive logic:
        - [`'explain_limitation'`](agents/lightbulb_function_ai/app.py:23) intent returns reasoned limitation: "it generates significant waste heat, making it inefficient."
        - Additional function intents: [`'turn_on'`](agents/lightbulb_function_ai/app.py:31), [`'turn_off'`](agents/lightbulb_function_ai/app.py:39), [`'dim'`](agents/lightbulb_function_ai/app.py:47), [`'status'`](agents/lightbulb_function_ai/app.py:73)
        - Internal state management for simulated lightbulb (on/off, brightness level)
    *   **Task 2.2.4:** ✅ Created [`Dockerfile`](agents/lightbulb_function_ai/Dockerfile:1) for this agent
    *   **Task 2.2.5:** ✅ Written comprehensive unit tests in [`test_app.py`](agents/lightbulb_function_ai/test_app.py:1) with 16 test cases covering all intents and error scenarios

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
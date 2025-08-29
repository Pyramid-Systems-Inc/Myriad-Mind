### **Myriad Cognitive Architecture - Advanced Learning Roadmap (roadmapPlusPlus.md)**

**Project Goal:** To evolve the Myriad system's cognitive capabilities by implementing a rich, human-like learning ecosystem. This roadmap details the creation of agents and processes for declarative, procedural, Socratic, corrective, and generative learning, transforming Myriad into a true "student" of knowledge.

---

### **Phase 1: Declarative and Procedural Learning (The "Classroom")**

**Goal:** To build the foundational mechanisms for learning from structured information ("textbooks") and learning new skills ("math problems"). This gives the system the ability to absorb knowledge in two fundamental forms: facts and functions.

*   **Step 1.1: Implement the `Curriculum_Ingestor_AI`**
    *   **Task 1.1.1:** Create the new `Curriculum_Ingestor_AI` service. This agent will have a `POST /ingest/document` endpoint.
    *   **Task 1.1.2:** Implement the core NLP logic for this agent. It must be able to parse a large text document to perform **entity recognition** (e.g., "James Watt") and **relationship extraction** (e.g., "James Watt" -> IMPROVED -> "steam engine").
    *   **Task 1.1.3:** Implement the **Batch Neurogenesis** logic. After parsing, the ingestor will formulate a single, large request to the `LifecycleManager` containing all new concepts to create and the relationships to form between them in the knowledge graph.
    *   **Task 1.1.4:** Create an integration test where you feed the ingestor a Wikipedia URL and verify that multiple new "Concept Genome" files are created and linked in the system's long-term memory.

*   **Step 1.2: Implement the `Procedure_Interpreter_AI`**
    *   **Task 1.2.1:** Create the new `Procedure_Interpreter_AI` service with a `POST /learn/procedure` endpoint.
    *   **Task 1.2.2:** The service will accept a structured JSON object describing a function (inputs, outputs, code body).
    *   **Task 1.2.3:** Implement the **Agent Scaffolding** logic. The interpreter will use a code template to dynamically generate the full `app.py` for a new `Function-Executor` agent based on the procedure's definition.
    *   **Task 1.2.4:** Integrate this service with the `LifecycleManager`, which will take the generated code, containerize it, and deploy it as a new, fully functional agent microservice.
    *   **Task 1.2.5:** Create an integration test where you submit a simple Python function (e.g., a compound interest formula) and verify that a new, callable agent appears on the network.

**Phase 1 Deliverable:** A system that can perform two types of large-scale learning. It can "read" a chapter and build a knowledge graph of interconnected facts, and it can be "taught" a new skill by being given a piece of code, which it turns into a new tool in its cognitive toolkit.

---

### **Phase 2: Socratic and Corrective Learning (The "Tutor")**

**Goal:** To give the system a sense of "self-awareness" regarding its own knowledge. It will learn to identify its own confusion and to process external feedback to correct its mistakes.

*   **Step 2.1: Implement Uncertainty Detection**
    *   **Task 2.1.1:** Enhance the standard agent response protocol to include an optional `uncertainty_signal` field.
    *   **Task 2.1.2:** Modify the `Orchestrator` to detect when it receives conflicting data from multiple high-confidence agents. This is a **Contradiction Event**.
    *   **Task 2.1.3:** When such an event is detected, the `Orchestrator` should halt its normal synthesis process and escalate the problem.

*   **Step 2.2: Implement the Socratic Questioning Loop**
    *   **Task 2.2.1:** Create the `Self_Explanation_AI` service. Its initial role will be to handle uncertainty.
    *   **Task 2.2.2:** The `Orchestrator` will send the `uncertainty_signal` to this new service's `/resolve/uncertainty` endpoint.
    *   **Task 2.2.3:** The `Self_Explanation_AI` will formulate a clear question and options for the user (or an "Oracle" agent) and send it back as a `clarification_required` response. This is the system actively asking for help.

*   **Step 2.3: Implement the Corrective Feedback Loop**
    *   **Task 2.3.1:** Create the `Feedback_Processor_AI` service with a `POST /feedback/submit` endpoint.
    *   **Task 2.3.2:** Implement the **Error Tracing** logic. The processor must be able to use a `query_id` to look up logs and identify which agent(s) contributed to an incorrect final answer.
    *   **Task 2.3.3:** Implement the **Knowledge Update** logic. This involves connecting to the long-term memory (Graph Database / file system) and adding a "dispute" annotation to the incorrect fact, lowering its confidence score without deleting it.
    *   **Task 2.3.4:** The provided correction is then routed to the `Curriculum_Ingestor_AI` as a new, high-priority piece of information to be learned.

**Phase 2 Deliverable:** A more robust and honest AI. When faced with conflicting information, it stops and asks for help instead of guessing. It has a mechanism to receive, process, and learn from corrections provided by a human user, allowing it to refine its accuracy over time.

---

### **Phase 3: Generative Learning & Cognitive Validation (The "Student Becomes the Teacher")**

**Goal:** To validate the system's emergent understanding by forcing it to synthesize and generate novel explanations of complex topics, thereby testing the integrity of its learned knowledge graph.

*   **Step 3.1: Enhance the `Self_Explanation_AI` for Generative Tasks**
    *   **Task 3.1.1:** Implement the `POST /explain` endpoint on the `Self_Explanation_AI`.
    *   **Task 3.1.2:** Implement the **Internal Querying** logic. When asked to explain a topic, this agent must act like a user, breaking the topic down into sub-questions that it sends to the `Orchestrator`.
    *   **Task 3.1.3:** It will collect all the raw data packets from the agents that the `Orchestrator` activates in response to its internal queries.

*   **Step 3.2: Implement High-Level Synthesis and Generation**
    *   **Task 3.2.1:** The `Self_Explanation_AI` will use a powerful `Micro-Generator` agent (Type D) to perform its final synthesis. This generative agent's specific purpose is to weave a collection of disparate facts into a coherent narrative.
    *   **Task 3.2.2:** The final output should be a newly generated text, not just a concatenation of agent responses.
    *   **Task 3.2.3:** Implement the **Self-Identified Gaps** feature. During its internal querying, if the `Self_Explanation_AI` fails to get information on a sub-topic it deems important, it must report this gap in its final output.

*   **Step 3.3: End-to-End System Validation**
    *   **Task 3.3.1:** Bootstrap the system with a curriculum on a complex topic (e.g., the basics of photosynthesis).
    *   **Task 3.3.2:** Write an integration test that calls the `POST /explain` endpoint with the topic "photosynthesis."
    *   **Task 3.3.3:** Verify that the generated output is a coherent, simplified summary that correctly uses the information from the underlying bootstrapped agents.
    *   **Task 3.3.4:** Verify that the system correctly identifies a related concept it was not taught (e.g., "Calvin cycle") as a "self-identified gap."

**Phase 3 Deliverable:** A fully cognitive AI architecture. It can learn declaratively and procedurally, question its own knowledge, correct its errors based on feedback, and demonstrate its holistic understanding by generating novel explanations. This completes the core framework for a system that doesn't just process information, but actively learns.
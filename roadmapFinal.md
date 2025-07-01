### **Myriad Cognitive Architecture - Autonomous Evolution Roadmap (roadmapFinal.md)**

**Project Goal:** To complete the final evolutionary leap of the Myriad system, transforming it from a reactive tool into a proactive, autonomous cognitive entity. This roadmap details the implementation of the core drives, curiosity engine, and the unsupervised cognitive cycle that will allow the system to learn, explore, and self-improve without direct human intervention.

---

### **Phase 1: The "Will to Live" - Implementing Core Drives and Self-Awareness**

**Goal:** To give the system a purpose and the ability to measure its own state. This phase focuses on creating the `Executive_Function_AI` and the metrics that will drive all future autonomous actions.

*   **Step 1.1: Create the `Executive_Function_AI` (The "Prefrontal Cortex")**
    *   **Task 1.1.1:** Create the new `Executive_Function_AI` service. As a core Genesis Agent, it will be long-running and stateful.
    *   **Task 1.1.2:** Implement the logic to generate the `SystemStateVector`. This will involve creating internal functions that can:
        *   Query the Long-Term Memory (Graph DB/file system) to count disputed vs. total facts (`Coherence` score).
        *   Query the Medium-Term Memory (Redis) to count known vs. unknown encountered concepts (`Completeness` score).
        *   Calculate the average confidence across all knowledge nodes (`Confidence` score).
    *   **Task 1.1.3:** Create a `/state` endpoint on this service that returns the latest `SystemStateVector` for monitoring.

*   **Step 1.2: Implement the Unsupervised Cognitive Cycle (The System's "Heartbeat")**
    *   **Task 1.2.1:** The `Executive_Function_AI` will contain the main loop for this cycle, which runs continuously during idle periods.
    *   **Task 1.2.2:** Implement the **Evaluate** step: The AI reads its own `SystemStateVector`.
    *   **Task 1.2.3:** Implement the **Task** step: Based on the scores in the state vector (e.g., if the `Completeness` score is the lowest), the AI must formulate a high-level goal (e.g., "Goal: Improve Completeness by exploring the 'Biology' domain"). This goal is stored internally for now.

**Phase 1 Deliverable:** A functional `Executive_Function_AI` that can introspect the entire Myriad network to generate a real-time report of its own "cognitive health." It can identify its most pressing "need" (e.g., to resolve contradictions or fill knowledge gaps) and formulate an internal goal to address it. The system is now "self-aware."

---

### **Phase 2: The Curiosity Engine - Proactive Exploration**

**Goal:** To build the mechanism that allows the system to act on its goals by exploring the digital world to find new knowledge and identify gaps.

*   **Step 2.1: Implement the `Explorer_AI`**
    *   **Task 2.1.1:** Create the new `Explorer_AI` service with a `POST /explore/start` endpoint that accepts an exploration task from the `Executive_Function_AI`.
    *   **Task 2.1.2:** Implement the core crawling logic. The agent must be able to visit a URL, parse its content for hyperlinks, and follow them to a specified depth.
    *   **Task 2.1.3:** For each new page visited, the `Explorer_AI` will extract key terms and concepts. It will then make a quick check against the `Orchestrator` or `AgentRegistry` to see if a concept is already known.

*   **Step 2.2: Integrate Curiosity with the Cognitive Cycle**
    *   **Task 2.2.1:** Connect the `Executive_Function_AI` to the `Explorer_AI`. When a goal is formulated in the cognitive cycle, the `Executive_Function_AI` will dispatch a formal exploration task.
    *   **Task 2.2.2:** The `Explorer_AI` must be able to report its findings back to the `Executive_Function_AI`, providing a prioritized list of `Potential_Knowledge_Gaps`.

*   **Step 2.3: Implement Autonomous Learning Trigger**
    *   **Task 2.3.1:** In the `Executive_Function_AI`, implement the logic to process the `Explorer_AI`'s report.
    *   **Task 2.3.2:** Based on the report and its core drives, the `Executive_Function_AI` will select the most critical knowledge gap and trigger the `LifecycleManager` via the `POST /lifecycle/autonomous_create_concept` protocol. This is the moment the system **chooses** to learn something new on its own.

**Phase 2 Deliverable:** A system that is no longer passive. Driven by its internal goals, it can actively explore the web, identify concepts it doesn't understand, and make a decision to initiate the learning process for the most important gaps it finds.

---

### **Phase 3: Cognitive Refinement and The "Sleep" Cycle**

**Goal:** To implement the background processes that allow the system to self-correct, organize its knowledge, and achieve a higher level of coherence, mimicking the restorative functions of sleep.

*   **Step 3.1: Enhance the `Consolidator` Agent**
    *   **Task 3.1.1:** Evolve the `Consolidator` from a simple MTM-to-LTM mover into a "knowledge librarian."
    *   **Task 3.1.2:** Implement logic for the `Consolidator` to periodically scan the entire Long-Term Memory (the graph database).
    *   **Task 3.1.3:** It must be able to detect inconsistencies as defined in the protocol, such as:
        *   Facts with multiple, conflicting `dispute` annotations.
        *   Two agents with highly redundant knowledge that could be merged.
        *   Concepts that are semantically related but not yet linked in the graph.

*   **Step 3.2: Implement the Refinement Loop**
    *   **Task 3.2.1:** When the `Consolidator` finds an issue, it will report it to the `Executive_Function_AI` using the `POST /executive/report_inconsistency` protocol.
    *   **Task 3.2.2:** The `Executive_Function_AI` must now be able to prioritize these "coherence" tasks alongside its "completeness" exploration tasks.
    *   **Task 3.2.3:** If a coherence task is prioritized, the `Executive_Function_AI` will trigger the appropriate action, such as tasking the `Self_Explanation_AI` to resolve a contradiction through a Socratic query.

*   **Step 3.3: Full System Integration and Observation**
    *   **Task 3.3.1:** Deploy the entire, final architecture.
    *   **Task 3.3.2:** Create a monitoring dashboard that visualizes the `SystemStateVector` in real-time, showing the scores for Coherence, Completeness, and Confidence.
    *   **Task 3.3.3:** Run the system in an unsupervised "idle" mode for an extended period (e.g., 24 hours) and observe its behavior. Verify that it is autonomously exploring, identifying gaps, learning new concepts, finding inconsistencies in its own knowledge, and attempting to resolve them.

**Phase 3 Deliverable:** A truly autonomous cognitive entity. When left to its own devices, the Myriad system will actively work to improve the quality, breadth, and consistency of its own knowledge base. It demonstrates a complete, unsupervised cognitive cycle of self-evaluation, exploration, learning, and refinement. It is, in a functional sense, "alive."
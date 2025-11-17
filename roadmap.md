### **MVP Development Roadmap: Project Myriad - C#/.NET Edition**

**Project Goal:** To build a functional prototype that validates the core architecture of orchestrating multiple, minimalist, specialized AI agents to answer a query.
**Implementation:** C# 10+ / .NET 6.0+ with **zero external dependencies** (all components built from scratch)
**Target Query for MVP:** "Why was the lightbulb important for factories?"

---

### **Phase 1: Foundation & Core Component Setup (Weeks 1-2)**

**Goal:** Establish the project structure, development environment, and build the non-intelligent "scaffolding" of the system. This phase is all about creating the "nervous system" before the "neurons" are intelligent.

* **Step 1.1: Environment and Project Initialization**
  * **Task 1.1.1:** Initialize a Git repository for version control.
  * **Task 1.1.2:** Create a .NET solution structure:
    * `/src/Myriad.Services.Orchestrator/` - Orchestrator microservice
    * `/src/Myriad.Services.GraphDatabase/` - Custom graph database service
    * `/src/Myriad.Agents.Static/` - Static agent implementations
    * `/src/Myriad.Common/` - Shared types and interfaces
    * `/tests/` - Unit and integration tests
  * **Task 1.1.3:** Create solution file: `dotnet new sln -n Myriad`
  * **Task 1.1.4:** Install .NET 6.0 SDK or later (no external NuGet packages - everything built from scratch)

* **Step 1.2: Build the Central Orchestrator Skeleton**
  * **Task 1.2.1:** Create ASP.NET Core project: `dotnet new web -n Myriad.Services.Orchestrator`
  * **Task 1.2.2:** Implement the `AgentRegistry` class using `ConcurrentDictionary<string, string>`, hardcoding future agent endpoints (e.g., `http://localhost:5001`).
  * **Task 1.2.3:** Write core orchestration logic: create `OrchestratorService` class with methods that accept keywords, iterate registry, and prepare to make API calls using `HttpClient`. For now, these calls will fail, which is expected.
  * **Task 1.2.4:** Add comprehensive logging using `ILogger<T>` interface to track orchestrator state (e.g., "Received keywords," "Querying Lightbulb_AI," "Received response").

* **Step 1.3: Develop the Simplest Small Agent (The Template)**
  * **Task 1.3.1:** Create `Lightbulb_AI` project: `dotnet new web -n Myriad.Agents.Static.Lightbulb`
  * **Task 1.3.2:** Inside, create ASP.NET Core Minimal API with `Program.cs`.
  * **Task 1.3.3:** Create a single `/health` endpoint using `app.MapGet()` that returns: `new { status = "healthy", agent = "Lightbulb_AI" }`.
  * **Task 1.3.4:** Configure the agent as a self-contained deployment. Create a launch configuration for the custom process orchestrator.
  * **Task 1.3.5:** Test standalone execution: `dotnet run` and verify it runs on port 5001. Test self-contained publish: `dotnet publish --self-contained`.

**Phase 1 Deliverable:** A runnable ASP.NET Core orchestrator service that can successfully ping a single, non-intelligent agent running as a standalone .NET process and log the interaction using `ILogger`.

---

### **Phase 2: Implementing Agent Intelligence & Communication (Week 3)**

**Goal:** Populate the agents with their specialized knowledge and establish a working data flow from the Orchestrator to the agents and back.

* **Step 2.1: Define the Standard Communication Protocol**
  * **Task 2.1.1:** Create C# record types in `Myriad.Common` project for all communication:
    * Request: `public record AgentRequest(string Query, string Intent);`
    * Response: `public record AgentResponse(string SourceAgent, Dictionary<string, object> Data);`
  * **Task 2.1.2:** Document this protocol in a `PROTOCOL.md` file in the project root, including C# type definitions.

* **Step 2.2: Implement Intelligence for `Lightbulb_AI`**
  * **Task 2.2.1:** Add `/process` endpoint to `Lightbulb_AI` using `app.MapPost()`.
  * **Task 2.2.2:** Add hardcoded knowledge using C# `Dictionary<string, object>` or `record` types as described in design document.
  * **Task 2.2.3:** Update endpoint to return knowledge as `data` payload in standardized JSON response using `Results.Ok()`.
  * **Task 2.2.4:** Write xUnit test to verify `/process` endpoint returns correct data structure and content.

* **Step 2.3: Clone and Specialize for `Factory_AI`**
  * **Task 2.3.1:** Create new project: `dotnet new web -n Myriad.Agents.Static.Factory`
  * **Task 2.3.2:** Configure Kestrel to run on different port (5002) in `appsettings.json`.
  * **Task 2.3.3:** Replace knowledge `Dictionary` with factory-specific information.
  * **Task 2.3.4:** Update launch configuration for port 5002 in the custom process orchestrator.
  * **Task 2.3.5:** Write xUnit test for `Factory_AI`'s endpoint.

* **Step 2.4: Integrate into the Orchestrator**
  * **Task 2.4.1:** Update Orchestrator logic to make real HTTP POST calls using `HttpClient.PostAsync()` to agents.
  * **Task 2.4.2:** Implement error handling using try-catch blocks (e.g., handle `HttpRequestException` if agent is offline).
  * **Task 2.4.3:** Update logging using `ILogger.LogInformation()` to show actual data received from each agent.

**Phase 2 Deliverable:** The Orchestrator can now successfully query two distinct, intelligent agents running in separate containers and collect their specialized knowledge packets.

---

### **Phase 3: Parsing, Synthesis, and Final Output (Week 4)**

**Goal:** Complete the full data-flow loop by processing the initial user input and synthesizing the collected agent data into a coherent final answer.

* **Step 3.1: Build the Input Parser**
  * **Task 3.1.1:** Create `InputParser` class in `Myriad.Common` project.
  * **Task 3.1.2:** Implement simple keyword-extraction using C# string methods (`Split()`, `Where()`, LINQ) based on MVP's target query.
  * **Task 3.1.3:** Write xUnit tests for the parser.
  * **Task 3.1.4:** Integrate parser into Orchestrator service via dependency injection.

* **Step 3.2: Build the Output Synthesizer**
  * **Task 3.2.1:** Create `OutputSynthesizer` class in `Myriad.Common` project.
  * **Task 3.2.2:** Implement simple, rule-based logic for combining data using LINQ and string interpolation.
  * **Task 3.2.3:** Method should accept `List<AgentResponse>` and return formatted string.
  * **Task 3.2.4:** Write xUnit tests for the synthesizer.

* **Step 3.3: Final Assembly and End-to-End Test**
  * **Task 3.3.1:** In Orchestrator, after collecting agent responses, inject and call `OutputSynthesizer`.
  * **Task 3.3.2:** Final output of Orchestrator `/process` endpoint should return human-readable sentence.
  * **Task 3.3.3:** Create custom process orchestrator launcher (`Myriad.Orchestrator.Launcher`) that starts all services.
  * **Task 3.3.4:** Perform full end-to-end test using the launcher application.
  * **Task 3.3.5:** Write comprehensive `README.md` explaining setup (install .NET SDK only) and how to run MVP.

**Phase 3 Deliverable:** A fully functional C#/.NET MVP prototype that takes the target query as HTTP POST input and produces the correct, synthesized sentence as JSON output.

---

### **Post-MVP: The Path to Deeper Biomimicry**

Once the core architectural pattern is validated, development will shift towards evolving the system to more closely mirror the brain's parallel, decentralized, and adaptive nature, as outlined in the Architectural Blueprint.

**Phase 4: Dual-Path Processing and Cognitive Workspace**

* **Goal:** Implement the Cognitive Workspace for deep reasoning on complex queries, creating a dual-path processing architecture.
* **Step 4.1: Complexity Detection:** Extend the Input Processor with complexity analysis to determine whether a query requires Fast Path (simple retrieval) or Deep Reasoning Path (Cognitive Workspace).
* **Step 4.2: Cognitive Workspace Service:** Create the `Myriad.Services.CognitiveWorkspace` microservice (Port 5012) with workspace lifecycle management, agent broadcasting coordination, and the Iterative Synthesis Engine.
* **Step 4.3: Dual-Path Routing:** Update the Orchestrator to route queries based on complexity - simple queries use the existing fast path, while complex queries activate the Cognitive Workspace.
* **Step 4.4: Broadcasting Mechanism:** Implement agent broadcasting capability where agents can project their models and frameworks into the workspace (not just return data).
* **Step 4.5: Iterative Synthesis Engine:** Build the core reasoning engine with pattern recognition, causal analysis, counterfactual simulation, and hypothesis refinement capabilities.
* **Step 4.6: Demonstrate Deep Reasoning:** Test with complex queries like "Based on Industrial Revolution principles, predict the impact of personal teleportation" and verify emergent reasoning.

**Phase 5: Enhancing Performance and Intelligence**

* **Goal:** Improve system speed and begin implementing more dynamic learning mechanisms.
* **Step 5.1: Asynchronous Communication:** Rearchitect the Orchestrator to use C#'s `async`/`await` pattern with `Task.WhenAll`, allowing it to query all agents in parallel instead of sequentially. This is a critical step for scalability.
* **Step 5.2: Implement Synaptic Strengthening:** For every successful query, log the co-activation of agents. Use this data to implement a basic weighting system that prioritizes frequently-used agent pairings.
* **Step 5.3: Demonstrate Ambiguity Resolution:** Implement the "drive" example from the design document, creating an `Ambiguity_Resolution_AI` to prove the system can handle more complex inputs.

**Phase 6: Decentralization and Dynamic Growth**

* **Goal:** Reduce the Orchestrator's role as a central hub and implement true "neurogenesis."
* **Step 6.1: Agent-to-Agent Communication:** Enable agents to call other relevant agents directly, creating "reflex arcs" that bypass the central Orchestrator for common, localized tasks.
* **Step 6.2: Implement the Lifecycle Manager:** Build the "factory for factories"—an AI module that can be triggered to:
  * Instantiate a new, blank agent container.
  * Assign it a network address.
  * Perform a basic web scrape to populate it with foundational knowledge.
  * Register the new agent with the Orchestrator.
* **Step 6.3: Prove Neurogenesis:** Demonstrate the system's ability to learn a novel concept by asking it a query for which no agent exists, and verifying that a new agent is created and can answer a basic follow-up question.

**Phase 7: Transition to an Advanced State**

* **Goal:** Evolve the system's core components into a truly advanced, graph-based cognitive architecture.
* **Step 7.1: Event-Driven Architecture:** Begin migrating from a direct-call model to a custom message broker (built from scratch using TCP/IP and C# concurrent collections). Components will now publish and subscribe to event streams, fully decoupling them.
* **Step 7.2: Implement the Digital Connectome:** Replace the simple `AI_REGISTRY` with a custom graph database (built from scratch using `ConcurrentDictionary` and custom graph algorithms in C#). Agents become nodes, and their learned relationships (from Synaptic Strengthening) become weighted edges. Orchestration now becomes a graph traversal algorithm.
* **Step 7.3: Agent Fine-Tuning:** Introduce the first Type-C/D agents (e.g., a simple `Sentiment_AI`) and build a feedback mechanism that allows user input to trigger a micro-training loop on that specific agent, enabling continuous, targeted learning.
* **Step 7.4: Enhance Cognitive Workspace:** Integrate formal symbolic logic and strategic planning capabilities into the Iterative Synthesis Engine to enable true AGI-level reasoning as outlined in the AGI Enhancements document.

# Project Myriad: A Myriad Cognitive Architecture

**A decentralized, emergent AI system built using a brain-inspired, graph-based knowledge network.**

This project explores a departure from monolithic AI models. Instead of a single, all-knowing entity, intelligence emerges from the collaboration of countless, computationally inexpensive agents whose relationships and knowledge are stored and managed in a central knowledge graph.

## 🚀 Current Status: "Brain Approach" Phase 1 Complete

**The foundational "Neural Substrate" of the architecture is complete and tested.**
- ✅ **Graph Database Core:** Neo4j database and `GraphDB_Manager_AI` service are operational.
- ✅ **Graph-Based Orchestrator:** The Orchestrator now uses graph traversals for agent discovery, replacing the previous registry system.
- ✅ **Agent Migration:** A formal migration script populates the knowledge graph with the initial agents and their conceptual relationships.
- ✅ **System Integration Tested:** All services are healthy and end-to-end tests are passing with the new graph-based core.

## Core Concept

The Myriad architecture is inspired by neurobiology, specifically the principles of **distributed representation** and **Hebbian learning**.

-   **Radical Specialization:** An agent for a specific function (e.g., executing code) is a minimalist, independent microservice. Factual knowledge is stored as nodes in the graph.
-   **Emergent Intelligence:** Complex answers are synthesized by traversing the knowledge graph to find and activate the most relevant agents and concepts.
-   **Dynamic Growth ("Neurogenesis"):** The system learns by adding new concept nodes, sensory nodes, and relationships to the graph, not by retraining a massive model.
-   **Efficiency and Resource Frugality:** The system is designed for computational efficiency, activating only the necessary components for a given query.

## High-Level Architecture ("Brain Approach")

```mermaid
graph LR
    subgraph User Interaction
        UserInput(User Query) --> IP[Input Processor];
        OP[Output Processor] --> FinalAnswer(Formatted Answer);
    end

    subgraph Core Cognitive Layer
        IP -- Parsed Query --> O(Orchestrator);
        O -- Traversal Query --> GDB[GraphDB Manager AI];
        GDB <--> KG[(Knowledge Graph <br> Neo4j)];
        O -- Activates --> FA(Function Agent);
        GDB -- Returns Subgraph --> S(Synthesizer);
        FA -- {data} --> S;
        S -- Synthesized Data --> OP;
    end

    subgraph Agent Network (Logical)
        A1(Concept A) -- HANDLES --> FA;
        A2(Concept B) -- RELATED_TO --> A1;
    end

    style GDB fill:#cceeff,stroke:#333
    style KG fill:#ddccff,stroke:#333
```

## Key Components

- **GraphDB Manager AI (Port 5008):** The "Neural Substrate". The sole interface to the Neo4j knowledge graph, managing all nodes (concepts, agents) and relationships.
- **Orchestrator:** The central nervous system. Traverses the knowledge graph to find relevant agents and concepts needed to answer a query.
- **Input & Output Processors:** The system's "sensory" and "motor" cortex, handling query understanding and response generation.
- **Myriad Agents:** A network of specialized microservices (for functions) and nodes within the graph (for knowledge).

## How to Run the System

### Prerequisites
- Docker and Docker Compose

### Quick Start
1. **Start all services:**
   ```bash
   docker-compose up --build -d
   ```
2. **Populate the knowledge graph:**
   ```bash
   python migration.py
   ```
3. **Verify System Health:**
   ```bash
   # Check a few key services
   curl http://localhost:5008/health # GraphDB Manager
   curl http://localhost:5009/health # Integration Tester
   ```
4. **Test the System:**
   ```bash
   python test_complete_system_integration.py
   ```
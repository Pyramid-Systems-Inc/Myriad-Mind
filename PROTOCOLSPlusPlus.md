### **Myriad Cognitive Architecture - Advanced Learning Protocols (PROTOCOLSPlusPlus.md)**

**Preamble:** This document specifies the protocols for the most advanced learning modalities of the Myriad system. It details the mechanisms for declarative, procedural, Socratic, corrective, and generative learning, turning the architecture into a comprehensive cognitive framework that can ingest, practice, question, refine, and synthesize knowledge.

---

#### **1. Declarative Learning Protocol ("The Textbook")**

*   **Purpose:** To enable the system to ingest, parse, and learn from large, structured documents, creating and linking multiple concept clusters in a single operation.
*   **Service:** `Curriculum_Ingestor_AI` (a Genesis Agent)
*   **Protocol: User/System → Curriculum_Ingestor_AI (`Ingest Document`)**
    *   **Endpoint:** `POST /ingest/document`
    *   **Payload:**
        ```json
        {
          "source_type": "url", // or "file_path", "raw_text"
          "source_uri": "https://en.wikipedia.org/wiki/Industrial_Revolution",
          "ingestion_id": "ingest_12345",
          "ingestion_options": {
            "max_new_concepts": 50,
            "min_relevance_score": 0.7
          }
        }
        ```
*   **Internal Protocol: Curriculum_Ingestor_AI → LifecycleManager (`Batch Create Concepts`)**
    *   **Endpoint:** `POST /lifecycle/batch_create_concepts`
    *   **Payload:**
        ```json
        {
          "ingestion_id": "ingest_12345",
          "concepts_to_create": [
            {"concept_name": "James Watt", "context": "An 18th-century inventor..."},
            {"concept_name": "steam engine", "context": "A heat engine that performs mechanical work..."}
          ],
          "relationships_to_create": [
            {
              "subject": "James Watt",
              "predicate": "IMPROVED", // from a controlled vocabulary
              "object": "steam engine",
              "confidence": 0.95,
              "source_sentence": "James Watt's improvements to the steam engine were fundamental..."
            }
          ]
        }
        ```

---

#### **2. Procedural Learning Protocol ("The Math Problems")**

*   **Purpose:** To enable the system to learn new skills and functions by interpreting code or structured instructions.
*   **Service:** `Procedure_Interpreter_AI` (a Genesis Agent)
*   **Protocol: User/System → Procedure_Interpreter_AI (`Learn Procedure`)**
    *   **Endpoint:** `POST /learn/procedure`
    *   **Payload:**
        ```json
        {
          "procedure_name": "compound_interest_calculator",
          "procedure_type": "python_function", // or "step_by_step_list"
          "description": "Calculates compound interest.",
          "inputs": [
            {"name": "principal", "type": "number", "description": "The initial amount."},
            {"name": "rate", "type": "number", "description": "The annual interest rate as a decimal."},
            {"name": "time", "type": "number", "description": "The number of years the amount is invested."}
          ],
          "output": {"name": "final_amount", "type": "number"},
          "implementation": {
            "code": "return principal * (1 + rate) ** time"
          }
        }
        ```
*   **Internal Protocol: Procedure_Interpreter_AI → LifecycleManager (`Create Function Agent`)**
    *   **Endpoint:** `POST /lifecycle/create_function_agent`
    *   **Payload:**
        ```json
        {
          "agent_name": "Compound_Interest_AI",
          "agent_type": "FunctionExecutor", // Type B
          "scaffolded_code": "from flask import Flask...\n\ndef execute(...): ...\n",
          "api_spec": {
            // OpenAPI/Swagger spec for the new agent's endpoint
          }
        }
        ```

---

#### **3. Socratic Learning Protocol ("Asking for Help")**

*   **Purpose:** To enable the system to recognize its own uncertainty and actively seek clarification from external sources.
*   **Service:** `Orchestrator` (enhanced logic) and `Self_Explanation_AI` (Genesis Agent)
*   **Internal Protocol 1: Agent → Orchestrator (`Signal Uncertainty`)**
    *   **This is an addition to the standard Agent-to-Orchestrator response.**
    *   **Added Payload Fields:**
        ```json
        {
          // ... standard agent response ...
          "uncertainty_signal": {
            "type": "contradiction", // or "low_confidence", "knowledge_gap"
            "conflicting_data": {
              "source_A": {"value": "1879", "confidence": 0.9},
              "source_B": {"value": "1881", "confidence": 0.88}
            },
            "clarification_needed": "What was the definitive year for this event?"
          }
        }
        ```
*   **Internal Protocol 2: Orchestrator → Self_Explanation_AI (`Resolve Uncertainty`)**
    *   **Endpoint:** `POST /resolve/uncertainty`
    *   **Payload:** The `uncertainty_signal` object received from an agent.
*   **External Protocol: Self_Explanation_AI → User/Oracle (`Request Clarification`)**
    *   **This is a response payload sent back to the original querier.**
    *   **Payload:**
        ```json
        {
          "status": "clarification_required",
          "query_id": "xyz",
          "explanation": "To provide an accurate answer, clarification is needed. The system has found conflicting information regarding the event year.",
          "question_to_user": "Which year is correct for the commercialization of the lightbulb: 1879 or 1881?",
          "response_options": ["1879", "1881", "Unsure"],
          "internal_context": { ... } // for stateful follow-up
        }
        ```

---

#### **4. Corrective Learning Protocol ("Getting Graded")**

*   **Purpose:** To allow the system to process external feedback, trace errors, and apply corrections to its knowledge base.
*   **Service:** `Feedback_Processor_AI` (a Genesis Agent)
*   **Protocol: User/System → Feedback_Processor_AI (`Submit Feedback`)**
    *   **Endpoint:** `POST /feedback/submit`
    *   **Payload:**
        ```json
        {
          "query_id": "xyz",
          "feedback_type": "correction", // or "rating", "suggestion"
          "target_agent_id": "History_AI_v1.2", // Optional, if known
          "incorrect_information": "The system stated the event was in 1881.",
          "correct_information": "The correct year is 1879.",
          "user_confidence": 0.99,
          "source_of_correction": "User provided, cites primary source document."
        }
        ```
*   **Internal Protocol: Feedback_Processor_AI → Graph Database/LTM (`Update Knowledge`)**
    *   **This is not a network call, but a description of the database transaction.**
    *   **Action:**
        1.  **Find Node:** Locate the agent node for `History_AI_v1.2`.
        2.  **Find Fact:** Locate the specific fact "event_year: 1881".
        3.  **Lower Confidence:** Decrease the confidence score of this fact.
        4.  **Add Dispute Annotation:** Attach a new property to the fact:
            ```json
            "disputes": [
              {
                "user": "User_ABC",
                "timestamp": "...",
                "correction": "1879",
                "user_confidence": 0.99
              }
            ]
            ```
        5.  **Trigger Learning:** Send a message to the `Curriculum_Ingestor_AI` to treat the correction as a new, high-priority piece of knowledge to be learned and potentially consolidated.

---

#### **5. Generative Learning Protocol ("The Feynman Technique")**

*   **Purpose:** To enable the system to test its own understanding by synthesizing its knowledge into a novel, simplified explanation.
*   **Service:** `Self_Explanation_AI` (Genesis Agent)
*   **Protocol: User/System → Self_Explanation_AI (`Explain Topic`)**
    *   **Endpoint:** `POST /explain`
    *   **Payload:**
        ```json
        {
          "topic": "Industrial Revolution",
          "target_audience": "high_school_student", // "expert", "child"
          "explanation_format": "narrative_summary" // "bullet_points", "analogy"
        }
        ```
*   **Response Protocol: Self_Explanation_AI → User (`Generated Explanation`)**
    *   **This is the final output of the generative process.**
    *   **Payload:**
        ```json
        {
          "topic": "Industrial Revolution",
          "explanation": "The Industrial Revolution was a period of major change... It began with the invention of the steam engine, which led to the growth of factories...",
          "synthesis_metadata": {
            "primary_concepts_used": ["steam engine", "factory", "textile manufacturing"],
            "agents_consulted": ["Steam_Engine_AI", "Factory_History_AI", ...],
            "confidence_in_explanation": 0.92
          },
          "self_identified_gaps": [
            "The specific economic impact on agriculture is not well-detailed in my current knowledge base."
          ]
        }
        ```
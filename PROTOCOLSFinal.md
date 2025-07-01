### **Myriad Cognitive Architecture - Autonomous Cognitive Protocols (PROTOCOLSFinal.md)**

**Preamble:** This document specifies the protocols for the final evolutionary stage of the Myriad system: the transition from a reactive learning tool to a proactive, autonomous cognitive entity. These protocols define the "internal monologue" of the system, governing its core drives, curiosity, and unsupervised learning cycle.

---

#### **1. Core Drives Protocol (The System's "Purpose")**

*   **Purpose:** To quantify the system's "health" and "purpose" into a set of core metrics that the `Executive_Function_AI` can monitor and act upon. This is not a network protocol but a data structure representing the system's state.
*   **Service:** `Executive_Function_AI` (a Genesis Agent)
*   **Data Structure: `SystemStateVector`**
    *   This JSON object is continuously updated by the `Executive_Function_AI` by querying other system components.
    *   **Format:**
        ```json
        {
          "timestamp": "2024-03-15T18:00:00Z",
          "drives": {
            "coherence": {
              "score": 0.85, // 1.0 = no contradictions
              "metric": "Ratio of disputed facts to total facts",
              "priority_modifier": 1.2 // High priority to fix pain
            },
            "completeness": {
              "score": 0.70, // 1.0 = no known gaps
              "metric": "Ratio of known concepts to encountered concepts",
              "priority_modifier": 1.5 // High priority to satisfy hunger
            },
            "confidence": {
              "score": 0.88, // Average confidence of all facts
              "metric": "Mean confidence score across LTM",
              "priority_modifier": 0.8
            }
          },
          "system_status": {
            "last_user_query_at": "2024-03-15T17:55:00Z",
            "last_learning_cycle_at": "2024-03-15T17:30:00Z",
            "is_idle": true
          }
        }
        ```

---

#### **2. The Curiosity Protocol (Proactive Exploration)**

*   **Purpose:** To define the communication between the system's "will" (`Executive_Function_AI`) and its "curiosity" (`Explorer_AI`).
*   **Services:** `Executive_Function_AI`, `Explorer_AI` (both Genesis Agents)
*   **Protocol 1: Executive_Function_AI → Explorer_AI (`Dispatch Exploration Task`)**
    *   **Endpoint:** `POST /explore/start`
    *   **Payload:**
        ```json
        {
          "task_id": "explore_bio_123",
          "goal": "Expand knowledge adjacent to the 'Biology' concept cluster.",
          "start_nodes": ["concept_cluster_dog", "concept_cluster_plant"],
          "exploration_depth": 3, // How many links away to crawl
          "max_new_concepts": 20
        }
        ```
*   **Protocol 2: Explorer_AI → Executive_Function_AI (`Report Findings`)**
    *   **This is a callback or response to the exploration task.**
    *   **Endpoint:** `POST /executive/report_findings` (on the Executive Function AI)
    *   **Payload:**
        ```json
        {
          "source_task_id": "explore_bio_123",
          "summary": "Explored 50 pages, found 15 potential new concepts.",
          "potential_knowledge_gaps": [
            {
              "concept_name": "CRISPR",
              "relevance_score": 0.95, // Based on proximity to known concepts
              "source_url": "https://en.wikipedia.org/wiki/CRISPR",
              "context_snippet": "CRISPR is a family of DNA sequences found in prokaryotes..."
            },
            {
              "concept_name": "mitochondria",
              "relevance_score": 0.92,
              "source_url": "...",
              "context_snippet": "..."
            }
          ]
        }
        ```

---

#### **3. The Autonomous Learning Protocol (Self-Directed Neurogenesis)**

*   **Purpose:** To enable the system to decide for itself what to learn next, based on its drives and curiosity.
*   **Services:** `Executive_Function_AI`, `LifecycleManager`
*   **Protocol: Executive_Function_AI → LifecycleManager (`Trigger Autonomous Learning`)**
    *   **This is a prioritized, internal trigger, distinct from a user--driven one.**
    *   **Endpoint:** `POST /lifecycle/autonomous_create_concept`
    *   **Payload:**
        ```json
        {
          "learning_task_id": "learn_crispr_789",
          "priority": 1.5, // Calculated from the drive scores
          "reason": "Highest relevance gap found during 'Biology' exploration.",
          "concept_to_learn": {
            "concept_name": "CRISPR",
            "initial_data_sources": {
              "text_url": "https://en.wikipedia.org/wiki/CRISPR",
              "image_query": "CRISPR Cas9 gene editing",
              "sound_query": null // Not applicable for this concept
            }
          }
        }
        ```
    *   **Action:** The `LifecycleManager` receives this and begins the full multi-modal neurogenesis process, creating a new, permanent "Concept Genome" file for "CRISPR."

---

#### **4. The Cognitive Refinement Protocol (The "Sleep" Cycle)**

*   **Purpose:** To allow the system to self-organize, self-correct, and improve its existing knowledge base during idle periods.
*   **Services:** `Consolidator` (background worker), `Executive_Function_AI`
*   **Protocol: Consolidator → Executive_Function_AI (`Report Inconsistency`)**
    *   **Endpoint:** `POST /executive/report_inconsistency`
    *   **Payload:**
        ```json
        {
          "report_id": "consistency_report_456",
          "inconsistency_type": "contradictory_facts", // or "redundant_agents", "weak_link"
          "details": {
            "fact": "boiling_point_of_water",
            "conflicting_nodes": [
              {
                "agent_id": "Water_Facts_AI",
                "value": "100 C",
                "confidence": 0.99
              },
              {
                "agent_id": "Cooking_Basics_AI",
                "value": "212 F",
                "confidence": 0.98
              }
            ]
          },
          "suggested_action": "Trigger Socratic query to resolve unit conflict."
        }
        ```
*   **Action:** The `Executive_Function_AI` receives this report. In its next cognitive cycle, it will see this "coherence" problem and may prioritize tasking the `Self_Explanation_AI` to resolve the contradiction, either by using a `Unit_Conversion_AI` or by asking an Oracle. This creates a loop of continuous self-improvement.
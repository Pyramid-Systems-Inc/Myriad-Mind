### **Myriad Cognitive Architecture - Advanced Protocols (PROTOCOLSPlus.md)**

**Preamble:** This document specifies the advanced, biomimetic protocols for the Myriad system. It builds upon the foundational communication established in the original plan and details the mechanisms for true learning, multi-modal understanding, and a tiered memory system, reflecting a "child learning" model.

---

#### **1. The Genesis Protocol: Defining the "Primal Core"**

This protocol doesn't define a network message but rather the initial state of the system at "birth." The system is pre-loaded with a **Genesis Agent Set**, which are immutable, foundational agents providing the tools for all future learning.

*   **1.1. Primal Sensory Cortex Agents (Foundation Models):**
    *   `Image_Embedding_AI`: A service wrapping a model like CLIP.
        *   **Endpoint:** `POST /embed/image`
        *   **Input:** An image file.
        *   **Output:** `{ "embedding": [0.123, -0.456, ...], "model": "CLIP-ViT-B-32" }`
    *   `Audio_Embedding_AI`: A service wrapping a model like VGGish.
        *   **Endpoint:** `POST /embed/audio`
        *   **Input:** An audio file (e.g., WAV).
        *   **Output:** `{ "embedding": [0.789, 0.112, ...], "model": "VGGish" }`
    *   `Text_Embedding_AI`: A service wrapping a Sentence Transformer model.
        *   **Endpoint:** `POST /embed/text`
        *   **Input:** `{ "text": "A sentence to embed." }`
        *   **Output:** `{ "embedding": [0.555, -0.222, ...], "model": "all-MiniLM-L6-v2" }`

*   **1.2. Primal Logic & Management Agents:**
    *   These include the `Orchestrator`, `LifecycleManager`, `Consolidator`, and `Arithmetic_AI`. Their functions are considered "instinctual" and are part of the core, non-learned architecture.

---

#### **2. Neurogenesis 2.0 Protocol (Few-Shot, Multi-Modal Learning)**

This protocol defines how a new **Concept Cluster** is created from a few examples.

*   **2.1. Trigger Protocol: Orchestrator → LifecycleManager**
    *   **Purpose:** To signal a knowledge gap and initiate the creation of a new concept cluster.
    *   **Endpoint:** `POST /lifecyle/create_concept`
    *   **Payload:**
        ```json
        {
          "concept_name": "dog",
          "triggering_query": "What is a dog?"
        }
        ```

*   **2.2. Long-Term Memory Protocol: The "Concept Genome" File**
    *   **Purpose:** Defines the structure of a learned concept cluster stored permanently on disk. The `LifecycleManager` writes this file; the `Orchestrator` reads it.
    *   **Location:** A shared volume, e.g., `/memory/long_term/{concept_name}.json`
    *   **Format:**
        ```json
        {
          "concept_name": "dog",
          "cluster_id": "concept_cluster_dog_1678886400",
          "created_at": "2024-03-15T12:00:00Z",
          "textual_knowledge": {
            "definition": "The dog is a domesticated descendant of the wolf...",
            "source": "https://en.wikipedia.org/wiki/Dog"
          },
          "visual_knowledge": {
            "prototype_embedding": [0.123, -0.456, ...],
            "embedding_model": "CLIP-ViT-B-32",
            "source_images": ["dog1.jpg", "dog2.jpg", "dog3.jpg"]
          },
          "auditory_knowledge": {
            "prototype_embedding": [0.789, 0.112, ...],
            "embedding_model": "VGGish",
            "source_sounds": ["bark1.wav", "bark2.wav"]
          },
          "related_concepts": {
            "wolf": {"relationship": "ancestor", "strength": 0.9},
            "pet": {"relationship": "instance_of", "strength": 0.8}
          }
        }
        ```

---

#### **3. The Tiered Memory Protocol**

This defines the communication with the different layers of the system's memory.

*   **3.1. Short-Term Memory (Implicit Protocol):**
    *   **Location:** Internal state of the `Orchestrator` during a single query execution.
    *   **Function:** Holds all temporary data for a single "thought." It is ephemeral and requires no external protocol.

*   **3.2. Medium-Term Memory (MTM) Protocol (Redis-based):**
    *   **Purpose:** To track recent interactions for fast retrieval and consolidation analysis.
    *   **Service:** `MediumTerm_Memory_AI` (a wrapper around a Redis instance).
    *   **Protocol 1: Orchestrator → MTM (`Log Interaction`)**
        *   **Endpoint:** `POST /mtm/log`
        *   **Payload:**
            ```json
            {
              "concepts": ["lightbulb", "factory"],
              "agents_used": ["Lightbulb_Definition_AI", "Factory_History_AI"],
              "query_hash": "a1b2c3d4e5f6"
            }
            ```
        *   **Action:** The MTM service increments access counters and updates timestamps for the given concepts in Redis (e.g., `INCR concept:lightbulb:count`, `SET concept:lightbulb:last_access 1678886400`). Entries have a TTL (e.g., 24 hours) to enable "forgetting."

    *   **Protocol 2: Consolidator → MTM (`Get Hot Concepts`)**
        *   **Endpoint:** `GET /mtm/hot_concepts?threshold=10`
        *   **Response:**
            ```json
            {
              "hot_concepts": [
                {"concept": "nft", "access_count": 52},
                {"concept": "web3", "access_count": 25}
              ]
            }
            ```

*   **3.3. Memory Consolidation Protocol ("Sleep"):**
    *   **Purpose:** To move important concepts from MTM to permanent LTM (Long-Term Memory).
    *   **Protocol: Consolidator → LifecycleManager (`Trigger Consolidation`)**
        *   **Endpoint:** `POST /lifecycle/consolidate`
        *   **Payload:**
            ```json
            {
              "concept_name": "nft",
              "reason": "Accessed 52 times in the last 24 hours."
            }
            ```
        *   **Action:** Triggers the full Neurogenesis 2.0 workflow for the specified concept.

---

#### **4. The Conceptual Bootstrapping Protocol ("Curriculum")**

This defines the data format for the system's initial, guided learning phase.

*   **Purpose:** To provide a structured "curriculum" to teach the system its foundational concepts.
*   **Location:** A directory in the project, e.g., `/curriculum/level_1/`.
*   **Format:** A manifest file, e.g., `_manifest.json`, that points to learning materials.
    ```json
    // /curriculum/level_1/_manifest.json
    {
      "curriculum_level": 1,
      "description": "Core Physical World Primitives",
      "concepts": [
        {
          "name": "ball",
          "text_definition": "A spherical object used in games.",
          "image_urls": [
            "https://example.com/images/red_ball.jpg",
            "https://example.com/images/soccer_ball.jpg"
          ],
          "sound_files": [
            "/curriculum/level_1/sounds/ball_bounce.wav"
          ]
        },
        {
          "name": "box",
          // ... similar structure
        }
      ]
    }
    ```
*   **Action:** A `bootstrap.py` script reads this manifest, gathers the data, and feeds it to the `LifecycleManager` to create the initial set of concept clusters.
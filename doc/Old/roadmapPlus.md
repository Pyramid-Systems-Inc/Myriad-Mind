### **Myriad Cognitive Architecture - Advanced Development Roadmap (roadmapPlus.md)**

**Project Goal:** To evolve the Myriad system from a static expert system into a dynamic, learning organism that mimics human cognition. This involves implementing few-shot multi-modal learning, a tiered memory system, and a structured learning curriculum.

---

### **Phase 1: The "Primal Core" & Few-Shot Learning Machinery (Weeks 1-2)**

**Goal:** Establish the foundational, pre-trained "sensory" agents and the core mechanics of the new, few-shot `LifecycleManager`. This phase is about building the *tools* for learning before the learning itself begins.

*   **Step 1.1: Implement the Genesis Agent Set (The "Primal Cortex")**
    *   **Task 1.1.1:** Create the `Image_Embedding_AI` service. This is a Flask/FastAPI wrapper around a pre-trained model like CLIP. It will have one endpoint (`/embed/image`) that takes an image and returns a numerical vector.
    *   **Task 1.1.2:** Create the `Audio_Embedding_AI` service (using VGGish or a similar model). It will have one endpoint (`/embed/audio`) for converting sound files to vectors.
    *   **Task 1.1.3:** Create the `Text_Embedding_AI` service (using a Sentence Transformer). It will have one endpoint (`/embed/text`).
    *   **Task 1.1.4:** Add these three new services to `docker-compose.yml` so they are part of the core system startup. These agents are considered immutable "instincts."

*   **Step 1.2: Rearchitect the LifecycleManager for Multi-Modal Learning**
    *   **Task 1.2.1:** Create the new `LifecycleManager` service (`/lifecycle_manager`) with a `POST /create_concept` endpoint.
    *   **Task 1.2.2:** Implement the **Multi-Modal Information Gathering** logic. When triggered, the manager must:
        *   Scrape a text definition (e.g., from Wikipedia).
        *   Use a search API to download the top 3-5 images for the concept.
        *   Use a search API to download 1-2 representative sounds for the concept.
    *   **Task 1.2.3:** Implement the **Vector Consolidation** logic. The manager will call the new embedding agents to get vectors for all gathered data and then average them to create a "prototype embedding" for each modality (visual, auditory).

*   **Step 1.3: Implement the "Concept Genome" Storage**
    *   **Task 1.3.1:** Define a shared volume in `docker-compose.yml` (e.g., `/memory_data`) that will be mounted by the `LifecycleManager` and `Orchestrator`.
    *   **Task 1.3.2:** The `LifecycleManager` will now save its output not as a new container, but as a single `concept_name.json` file in `/memory/long_term/` on the shared volume, following the "Concept Genome" protocol. This file *is* the long-term memory.
    *   **Task 1.3.3:** Modify the `Orchestrator`'s `get_agent_url` logic. Instead of a hardcoded dictionary, it will now check for the existence of `{concept}.json` in the long-term memory directory.

**Phase 1 Deliverable:** A functional `LifecycleManager` that, when triggered for a new concept like "dog," can gather text, images, and sounds, use the Genesis embedding agents to create prototype vectors, and save the result as a single "Concept Genome" file to a persistent volume.

---

### **Phase 2: Tiered Memory & The "Sleep" Cycle (Weeks 3-4)**

**Goal:** Implement the brain's memory hierarchy (short, medium, long-term) to make the system more efficient and enable intelligent consolidation of knowledge.

*   **Step 2.1: Implement Medium-Term Memory (MTM)**
    *   **Task 2.1.1:** Add a Redis service to `docker-compose.yml`.
    *   **Task 2.1.2:** Create a new `MediumTerm_Memory_AI` service. This is a simple Flask wrapper around the Redis instance.
    *   **Task 2.1.3:** Implement the `POST /mtm/log` endpoint. After a successful query, the `Orchestrator` will call this endpoint to log which concepts were accessed together. The MTM service will use Redis commands (`INCR`, `SET`) to track access counts and timestamps with a TTL (e.g., 24 hours) to allow for "forgetting."

*   **Step 2.2: Integrate MTM into the Orchestrator's "Thought Process"**
    *   **Task 2.2.1:** Modify the `Orchestrator`. Before trying to access Long-Term Memory (the JSON files), it first makes a call to the MTM service.
    *   **Task 2.2.2:** If the MTM has a "hot" entry for the concept(s), the Orchestrator can use this cached information to prioritize agent activation, bypassing a full LTM lookup.
    *   **Task 2.2.3:** The primary trigger for Neurogenesis now shifts. The `Orchestrator` triggers the `LifecycleManager` only if a concept is not found in **either** MTM or LTM.

*   **Step 2.3: Implement the Consolidation Process (The "Sleep Cycle")**
    *   **Task 2.3.1:** Create a new `Consolidator` service. This is not an API service, but a background worker process.
    *   **Task 2.3.2:** The `Consolidator` runs on a schedule (e.g., using a `cron` job or a simple `time.sleep` loop).
    *   **Task 2.3.3:** On each run, it calls the MTM's `GET /mtm/hot_concepts` endpoint to get a list of frequently accessed concepts that do not yet have a permanent "Concept Genome" file in LTM.
    *   **Task 2.3.4:** For each "hot" concept, the `Consolidator` calls the `LifecycleManager`'s `POST /lifecycle/consolidate` endpoint, triggering the permanent storage of that concept. This is the act of moving knowledge from working memory to long-term memory.

**Phase 2 Deliverable:** A fully integrated tiered memory system. The `Orchestrator` uses a fast Redis-based MTM for recent interactions. A background `Consolidator` process intelligently decides which frequently-used concepts are important enough to be consolidated into permanent "Concept Genome" files by the `LifecycleManager`.

---

### **Phase 3: The Curriculum & Bootstrapping (Week 5)**

**Goal:** To give the Myriad "child" its foundational education, allowing it to build a hierarchy of knowledge from the ground up.

*   **Step 3.1: Design and Create the Level 1 Curriculum**
    *   **Task 3.1.1:** Create the `/curriculum/level_1/` directory structure.
    *   **Task 3.1.2:** Manually create the `_manifest.json` file for Level 1 concepts ("Core Physical World Primitives").
    *   **Task 3.1.3:** Populate the manifest with ~20-30 foundational concepts (`ball`, `box`, `red`, `blue`, `roll`, `push`, etc.). For each concept, provide a clean text definition and gather a few high-quality sample images and sounds.

*   **Step 3.2: Build the Bootstrapping Engine**
    *   **Task 3.2.1:** Create a `bootstrap.py` script at the project root.
    *   **Task 3.2.2:** This script will parse the `_manifest.json`.
    *   **Task 3.2.3:** For each concept in the manifest, it will make a call to the `LifecycleManager`'s `POST /lifecycle/create_concept` endpoint, feeding it the curated data from the curriculum. This simulates a "teacher" guiding the AI's first learning steps.

*   **Step 3.3: Run the Bootstrap and Verify Foundational Knowledge**
    *   **Task 3.3.1:** Run the entire system with `docker-compose up --build`.
    *   **Task 3.3.2:** Execute `python bootstrap.py`.
    *   **Task 3.3.3:** Verify that the `/memory/long_term/` directory is now populated with JSON files for all the Level 1 concepts (`ball.json`, `box.json`, etc.).
    *   **Task 3.3.4:** Write an integration test that asks a simple query about a Level 1 concept (e.g., "What is a red ball?") and confirms the system can now correctly identify and describe it using its newly formed concept clusters.

**Phase 3 Deliverable:** A "bootstrapped" Myriad system that has learned its first ~20-30 foundational concepts from a curated curriculum. The system is no longer a blank slate; it has a base layer of knowledge about the physical world, upon which all future autonomous learning will be built.
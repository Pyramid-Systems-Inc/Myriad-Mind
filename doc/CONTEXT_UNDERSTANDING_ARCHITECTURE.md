# Human-Like Context Understanding Architecture for Myriad Cognitive System

**Version:** 1.0  
**Date:** 2025-10-11  
**Status:** Strategic Architecture Proposal

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [How Humans Understand Context](#how-humans-understand-context)
3. [Current Myriad Capabilities Analysis](#current-myriad-capabilities-analysis)
4. [Gap Analysis](#gap-analysis)
5. [Proposed Multi-Layer Context Architecture](#proposed-multi-layer-context-architecture)
6. [Technical Implementation Approaches](#technical-implementation-approaches)
7. [Integration with Existing Components](#integration-with-existing-components)
8. [Implementation Roadmap](#implementation-roadmap)
9. [Example Scenarios](#example-scenarios)
10. [Trade-offs and Design Decisions](#trade-offs-and-design-decisions)
11. [Open Questions for Discussion](#open-questions-for-discussion)
12. [References](#references)

---

## Executive Summary

This document proposes a comprehensive architecture for implementing human-like context understanding in the Myriad Cognitive System. The current system excels at single-query processing with uncertainty detection and ambiguity resolution, but lacks the conversational memory and contextual carryover that characterizes human cognition.

**Key Recommendations:**

1. **Implement a 4-layer context system**: Session, User, World, and Discourse contexts working together to provide comprehensive understanding
2. **Add conversation state management**: Track conversation history, entity mentions, and topic flow using Redis for session storage and Neo4j for persistent context
3. **Enhance reference resolution**: Enable the system to understand pronouns ("it", "that", "they") and implicit references across conversation turns
4. **Build contextual agent selection**: Extend the Enhanced Graph Intelligence to consider conversation history when selecting agents
5. **Phased implementation**: Start with basic session context (1 week), progress through graph-based persistent context (2 weeks), add semantic understanding (2-3 weeks), and culminate in advanced LLM-powered reasoning (3-4 weeks)

**Expected Impact:**

- Transform single-turn query processing into natural multi-turn conversations
- Reduce user frustration from having to repeat context
- Enable more intelligent agent selection based on conversation flow
- Create a foundation for long-term user personalization and preference learning

---

## How Humans Understand Context

Human context understanding operates through multiple interconnected cognitive systems that work seamlessly together:

### 1. Working Memory (Short-Term Context)

Humans maintain approximately 7±2 items in active working memory, which includes:

- **Recent conversation turns** (last 3-5 exchanges)
- **Active concepts** currently being discussed
- **Current goals** of the conversation
- **Pending questions** or unresolved topics

**Example:**

```
Turn 1: "What is a lightbulb?"
Turn 2: "Who invented it?"  ← "it" automatically resolves to "lightbulb" from working memory
```

### 2. Long-Term Memory (Episodic & Semantic)

Humans recall past interactions and general knowledge:

- **Episodic memory**: Previous conversations with the same person
- **Semantic memory**: General world knowledge and common sense
- **Personal context**: User preferences, expertise level, communication style

**Example:**

```
Yesterday: User asked detailed questions about quantum mechanics
Today: System adjusts explanation depth for advanced audience
```

### 3. Pragmatic Inference (Reading Between the Lines)

Humans infer unstated information through:

- **Common sense reasoning**: "The coffee spilled" implies it's now on something
- **Cultural context**: Shared understanding of norms and conventions
- **Situational awareness**: Time, place, and social context
- **Theory of mind**: Understanding speaker's intent and knowledge state

**Example:**

```
User: "Can you explain neural networks?"
Human inference: User wants a technical explanation, not about biological neurons
```

### 4. Discourse Understanding (Conversation Flow)

Humans track conversation structure:

- **Topic coherence**: Recognizing when topics shift or continue
- **Question-answer pairs**: Linking responses to earlier questions
- **Ellipsis completion**: Filling in omitted but understood information
- **Anaphora resolution**: Understanding what pronouns refer to

**Example:**

```
Turn 1: "Tell me about Einstein"
Turn 2: "What about his theories?"  ← Ellipsis: "Tell me about Einstein's theories"
Turn 3: "When did he publish them?" ← Anaphora: "he"=Einstein, "them"=theories
```

### 5. Contextual Integration

All these systems work together seamlessly:

```mermaid
graph TB
    subgraph "Human Context Understanding"
        WM[Working Memory\n3-5 recent turns]
        LTM[Long-Term Memory\nPast interactions]
        PI[Pragmatic Inference\nCommon sense]
        DU[Discourse Understanding\nConversation flow]
        
        WM <--> LTM
        WM <--> PI
        WM <--> DU
        LTM <--> PI
        PI <--> DU
        
        INPUT[New Query] --> WM
        WM --> OUTPUT[Contextual Understanding]
        LTM --> OUTPUT
        PI --> OUTPUT
        DU --> OUTPUT
    end
    
    style WM fill:#e1f5fe
    style LTM fill:#fff3e0
    style PI fill:#f3e5f5
    style DU fill:#e8f5e9
```

**Key Insight:** Human context understanding is **multi-modal**, **hierarchical**, and **predictive**. We don't just store past information—we actively integrate it with current input to anticipate needs and fill gaps.

---

## Current Myriad Capabilities Analysis

### What Exists Today

Myriad already has sophisticated single-query processing capabilities:

#### ✅ Input Processing ([`input_processor.py`](../src/myriad/services/processing/input_processor/input_processor.py:1))

**Strengths:**

- Multi-language parsing with language detection
- Intent recognition with confidence scoring
- Ambiguity detection and resolution
- Uncertainty assessment with multiple signal types
- Socratic questioning for clarification

**Current Context Usage:**

```python
def process_query(self, raw_query: str, user_context: Optional[Dict] = None) -> TaskList:
    # user_context is accepted but minimally used
    # Only passed through to sub-components
    # No persistent context tracking
```

**Limitations:**

- `user_context` is optional and not systematically populated
- No conversation history tracking
- No entity persistence across queries
- Context is reset between queries

#### ✅ Ambiguity Resolution ([`ambiguity_resolver.py`](../src/myriad/services/processing/input_processor/ambiguity_resolver.py:1))

**Strengths:**

- Detects concept, intent, context, and scope ambiguity
- Context-based disambiguation using `user_context`
- Fallback to most likely interpretation

**Current Context Usage:**

```python
def resolve_ambiguity(self, query: str, ambiguity_detection: AmbiguityDetection, 
                      context: Optional[Dict] = None) -> DisambiguationResult:
    # Can use 'previous_queries' from context if provided
    if 'previous_queries' in context and context['previous_queries']:
        prev_query_text = ' '.join(context['previous_queries'])
        # Uses previous queries for disambiguation
```

**Limitations:**

- `previous_queries` must be manually provided by caller
- No automatic history management
- Limited to simple keyword matching in previous queries
- No semantic similarity or entity tracking

#### ✅ Intent Recognition ([`intent_recognizer.py`](../src/myriad/services/processing/input_processor/intent_recognizer.py:1))

**Strengths:**

- Pattern-based intent detection with confidence scoring
- Context-aware adjustments based on query length and domain
- Alternative intent suggestions

**Limitations:**

- Context factors are derived only from current query
- No memory of user's typical intent patterns
- Cannot learn from interaction history

#### ✅ Uncertainty Detection ([`uncertainty_signals.py`](../src/myriad/core/uncertainty/uncertainty_signals.py:1))

**Strengths:**

- Comprehensive uncertainty type detection
- Confidence scoring and recommended actions
- Integration with Socratic questioning

**Limitations:**

- Uncertainty assessment is per-query only
- No tracking of recurring uncertainties
- Cannot learn which clarifications are most effective

#### ✅ Enhanced Graph Intelligence ([`enhanced_graph_intelligence.py`](../src/myriad/core/intelligence/enhanced_graph_intelligence.py:1))

**Strengths:**

- Multi-criteria agent relevance scoring
- Context-aware agent selection with complexity analysis
- Performance tracking and clustering
- Hebbian learning for agent-concept relationships

**Current Context Usage:**

```python
def discover_intelligent_agents(self, concept: str, intent: str, 
                               context: Optional[Dict[str, Any]] = None) -> List[AgentRelevanceScore]:
    query_context = self._parse_query_context(concept, intent, context or {})
    # Uses urgency and preferences from context if provided
```

**Limitations:**

- Context is limited to current query metadata
- No conversation history consideration
- Cannot track which agents work well together over time
- User preferences are not persisted

### What's Missing for Human-Like Context

| Human Capability | Current Status | Gap |
|-----------------|---------------|-----|
| **Working Memory** | ❌ None | No conversation history tracking |
| **Entity Tracking** | ❌ None | Entities mentioned aren't remembered |
| **Reference Resolution** | ❌ None | Cannot resolve "it", "that", "they" |
| **Topic Continuity** | ❌ None | Each query treated as independent |
| **User Profiles** | ❌ None | No persistent user preferences |
| **Contextual Agent Selection** | ⚠️ Partial | Context not used for agent discovery |
| **Conversation Flow** | ❌ None | No understanding of turn sequences |
| **Implicit Context** | ❌ None | Cannot infer unstated information |
| **Common Sense Reasoning** | ⚠️ Limited | Only through LLM in agents |
| **Preference Learning** | ❌ None | Cannot adapt to user over time |

---

## Gap Analysis

### Critical Gaps

#### 1. **No Conversation Memory**

**Problem:**

```python
# Current behavior
Turn 1: "What is a lightbulb?"
Response: "A device that produces light..."

Turn 2: "Who invented it?"
Response: "I don't know what 'it' refers to"  ❌
```

**Impact:**

- Frustrating user experience requiring context repetition
- Inability to have natural multi-turn conversations
- Lost efficiency in clarification dialogues

#### 2. **No Reference Resolution**

**Problem:** The system cannot resolve:

- Pronouns: "it", "that", "this", "they", "he", "she"
- Demonstratives: "the one", "those", "such"
- Ellipsis: incomplete queries missing implied information

**Current Code Gap:**

```python
# input_processor.py - no reference resolution
parsed_query = self.parser.parse_query(raw_query, user_context)
# parsed_query.concepts will be empty if query is "Who invented it?"
```

#### 3. **No Entity Persistence**

**Problem:**

```python
# Current behavior
Turn 1: "Tell me about Einstein"
# System extracts: concept="Einstein"

Turn 2: "What about relativity?"
# System extracts: concept="relativity"
# Lost connection: Einstein ← works on → Relativity
```

**Impact:**

- Cannot understand relationships across turns
- Cannot track what entities have been discussed
- Cannot maintain topic coherence

#### 4. **No User Profile Management**

**Problem:**

- Cannot learn user expertise level (beginner vs expert)
- Cannot adapt explanation verbosity to preferences
- Cannot remember past conversations for context
- Cannot personalize agent selection

#### 5. **Session vs Persistent Context**

**Problem:**

- No distinction between temporary session context and long-term user context
- No storage mechanism for either type of context
- Context must be manually constructed and passed each time

---

## Proposed Multi-Layer Context Architecture

### Overview

We propose a **4-layer context system** that mimics human cognitive architecture:

```mermaid
graph TB
    subgraph "Layer 1: Session Context - Working Memory"
        SC[Session Context Manager]
        TH[Turn History\nLast 10 turns]
        ET[Entity Tracker\nActive entities]
        TT[Topic Tracker\nCurrent topics]
        GS[Goal Stack\nUser intentions]
    end
    
    subgraph "Layer 2: User Context - Episodic Memory"
        UC[User Context Manager]
        PC[Past Conversations\nConversation graphs]
        UP[User Preferences\nVerbosity, language]
        KL[Knowledge Level\nExpertise tracking]
        IP[Interaction Patterns\nBehavioral history]
    end
    
    subgraph "Layer 3: World Context - Semantic Memory"
        WC[World Context Manager]
        CS[Common Sense\nGeneral knowledge]
        TC[Temporal Context\nCurrent date/time]
        CC[Cultural Context\nDomain conventions]
        DK[Domain Knowledge\nFrom Neo4j graph]
    end
    
    subgraph "Layer 4: Discourse Context"
        DC[Discourse Context Manager]
        CF[Conversation Flow\nTurn sequences]
        QA[Q&A Pairs\nQuestion-answer linking]
        TrT[Topic Transitions\nShift detection]
        RR[Reference Resolution\nPronoun tracking]
    end
    
    INPUT[New Query] --> SC
    SC <--> UC
    SC <--> WC
    SC <--> DC
    
    UC --> DB[(Redis + Neo4j\nPersistent Storage)]
    
    SC --> OUTPUT[Enriched Query Context]
    UC --> OUTPUT
    WC --> OUTPUT
    DC --> OUTPUT
    
    OUTPUT --> IP_PROCESSOR[Input Processor\nwith Context]
    
    style SC fill:#e1f5fe
    style UC fill:#fff3e0
    style WC fill:#f3e5f5
    style DC fill:#e8f5e9
```

### Layer 1: Session Context (Working Memory)

**Purpose:** Track the immediate conversation state within a single session.

**Components:**

1. **Turn History Manager**
   - Stores last N conversation turns (default: 10)
   - Each turn contains: query, response, timestamp, entities, concepts
   - Implements sliding window with configurable size

2. **Entity Tracker**
   - Maintains active entity mentions with attributes
   - Tracks entity salience (recency + frequency)
   - Links entities to concepts in Neo4j graph

3. **Topic Tracker**
   - Identifies current active topics
   - Detects topic shifts vs continuations
   - Maintains topic hierarchy (subtopics)

4. **Goal Stack**
   - Infers user's current goal from intent history
   - Tracks multi-turn goal completion
   - Suggests related goals

**Storage:** Redis with TTL (30-60 minutes session timeout)

**Data Structure:**

```python
{
    "session_id": "sess_abc123",
    "user_id": "user_xyz789",
    "created_at": "2025-10-11T00:00:00Z",
    "last_active": "2025-10-11T00:15:30Z",
    "turn_history": [
        {
            "turn_id": 1,
            "query": "What is a lightbulb?",
            "resolved_query": "What is a lightbulb?",
            "concepts": ["lightbulb"],
            "entities": {"lightbulb": {"type": "Concept", "salience": 0.9}},
            "intent": "define",
            "response_summary": "Device that produces light...",
            "timestamp": "2025-10-11T00:00:00Z"
        },
        {
            "turn_id": 2,
            "query": "Who invented it?",
            "resolved_query": "Who invented the lightbulb?",
            "concepts": ["lightbulb", "invention"],
            "entities": {
                "lightbulb": {"type": "Concept", "salience": 0.8, "referent_from": "it"},
                "Thomas Edison": {"type": "Person", "salience": 0.9, "discovered_in_turn": 2}
            },
            "intent": "analyze_historical_context",
            "timestamp": "2025-10-11T00:05:00Z"
        }
    ],
    "entity_tracker": {
        "lightbulb": {
            "first_mention": 1,
            "last_mention": 2,
            "mention_count": 2,
            "salience": 0.85,
            "type": "Concept",
            "attributes": {}
        },
        "Thomas Edison": {
            "first_mention": 2,
            "last_mention": 2,
            "mention_count": 1,
            "salience": 0.9,
            "type": "Person",
            "attributes": {"role": "inventor"}
        }
    },
    "active_topics": ["technology", "invention_history"],
    "current_goal": "learn_about_lightbulb_history"
}
```

### Layer 2: User Context (Episodic Memory)

**Purpose:** Maintain long-term user profile and conversation history.

**Components:**

1. **Conversation History Graph**
   - Stores past conversations as subgraphs in Neo4j
   - Links conversations by topics and concepts
   - Enables "remember when we talked about X?" queries

2. **User Preference Model**
   - Verbosity preference (brief, moderate, detailed)
   - Language preference
   - Domain interests
   - Learning vs lookup mode

3. **Knowledge Level Tracker**
   - Tracks user expertise per domain
   - Adapts explanation depth automatically
   - Identifies knowledge gaps

4. **Interaction Pattern Analyzer**
   - Common query types
   - Preferred clarification methods
   - Time-of-day patterns
   - Collaboration preferences

**Storage:** Neo4j graph database for relationships, Redis for fast access cache

**Neo4j Schema Extension:**

```cypher
// New nodes
(User {user_id, created_at, preferences})
(Conversation {conversation_id, session_id, started_at, ended_at, topic, summary})
(Turn {turn_id, query, resolved_query, response_summary, timestamp})

// New relationships
(User)-[STARTED]->(Conversation)
(Conversation)-[HAS_TURN {sequence}]->(Turn)
(Turn)-[MENTIONS {salience}]->(Concept)
(Turn)-[REFERENCES {referent_type}]->(Entity)
(Turn)-[FOLLOWS]->(Turn)  // Conversation flow
(User)-[HAS_PREFERENCE {type, value}]->(PreferenceNode)
(User)-[KNOWS_ABOUT {expertise_level}]->(Concept)
```

### Layer 3: World Context (Semantic Memory)

**Purpose:** Provide general knowledge and common sense reasoning.

**Components:**

1. **Common Sense Knowledge Base**
   - Physical causality (water freezes at 0°C)
   - Typical properties (birds fly, fish swim)
   - Social conventions (greetings, politeness)
   - Spatial/temporal relationships

2. **Temporal Context Manager**
   - Current date/time affects relevance
   - Historical vs current events
   - Seasonal context
   - Time-sensitive information

3. **Cultural Context Provider**
   - Domain-specific conventions
   - Regional variations
   - Language idioms and expressions

4. **Domain Knowledge Integration**
   - Leverages existing Neo4j concept graph
   - Cross-domain relationship inference
   - Knowledge graph embeddings

**Storage:** Combination of Neo4j (structured) and vector database (semantic similarity)

### Layer 4: Discourse Context

**Purpose:** Understand conversation structure and flow.

**Components:**

1. **Conversation Flow Analyzer**
   - Identifies turn-taking patterns
   - Detects adjacency pairs (question→answer)
   - Tracks conversational implicature

2. **Topic Transition Detector**
   - Identifies smooth transitions vs abrupt shifts
   - Maintains topic hierarchy
   - Suggests related topics

3. **Reference Resolution Engine**
   - Pronoun resolution (it, that, they)
   - Definite reference (the one, those)
   - Ellipsis completion (missing information)

4. **Question-Answer Tracker**
   - Links answers to earlier questions
   - Tracks multi-part answers
   - Identifies follow-up questions

**Storage:** In-memory structures within session context, persisted to Neo4j for learning

---

## Technical Implementation Approaches

### Approach 1: Redis-Based Session Management

**Best for:** Layer 1 (Session Context) - fast, temporary storage

**Architecture:**

```python
class SessionContextManager:
    """Manages short-term conversation context in Redis"""
    
    def __init__(self, redis_client):
        self.redis = redis_client
        self.session_ttl = 1800  # 30 minutes
    
    def get_or_create_session(self, user_id: str, session_id: Optional[str] = None) -> str:
        """Get existing session or create new one"""
        if session_id and self.redis.exists(f"session:{session_id}"):
            # Extend TTL on access
            self.redis.expire(f"session:{session_id}", self.session_ttl)
            return session_id
        
        # Create new session
        new_session_id = f"sess_{user_id}_{int(time.time())}"
        session_data = {
            "session_id": new_session_id,
            "user_id": user_id,
            "created_at": datetime.now().isoformat(),
            "turn_history": json.dumps([]),
            "entity_tracker": json.dumps({}),
            "active_topics": json.dumps([]),
            "current_goal": ""
        }
        
        self.redis.hmset(f"session:{new_session_id}", session_data)
        self.redis.expire(f"session:{new_session_id}", self.session_ttl)
        
        return new_session_id
    
    def add_turn(self, session_id: str, turn_data: Dict[str, Any]):
        """Add a new turn to the conversation history"""
        session_key = f"session:{session_id}"
        
        # Get current history
        history_json = self.redis.hget(session_key, "turn_history")
        history = json.loads(history_json) if history_json else []
        
        # Add new turn
        turn_data["turn_id"] = len(history) + 1
        turn_data["timestamp"] = datetime.now().isoformat()
        history.append(turn_data)
        
        # Keep only last 10 turns (sliding window)
        if len(history) > 10:
            history = history[-10:]
        
        # Update Redis
        self.redis.hset(session_key, "turn_history", json.dumps(history))
        self.redis.hset(session_key, "last_active", datetime.now().isoformat())
        
        # Update entity tracker
        self._update_entity_tracker(session_id, turn_data.get("entities", {}))
    
    def get_recent_context(self, session_id: str, n_turns: int = 3) -> List[Dict]:
        """Get last N turns for context"""
        history_json = self.redis.hget(f"session:{session_id}", "turn_history")
        history = json.loads(history_json) if history_json else []
        return history[-n_turns:]
    
    def _update_entity_tracker(self, session_id: str, new_entities: Dict[str, Dict]):
        """Update entity salience and tracking"""
        session_key = f"session:{session_id}"
        
        tracker_json = self.redis.hget(session_key, "entity_tracker")
        tracker = json.loads(tracker_json) if tracker_json else {}
        
        for entity_name, entity_data in new_entities.items():
            if entity_name in tracker:
                # Update existing entity
                tracker[entity_name]["mention_count"] += 1
                tracker[entity_name]["last_mention"] = len(json.loads(
                    self.redis.hget(session_key, "turn_history")
                ))
                # Increase salience with recency boost
                tracker[entity_name]["salience"] = min(1.0, 
                    tracker[entity_name]["salience"] * 0.9 + 0.3
                )
            else:
                # New entity
                tracker[entity_name] = {
                    "first_mention": len(json.loads(
                        self.redis.hget(session_key, "turn_history")
                    )),
                    "last_mention": len(json.loads(
                        self.redis.hget(session_key, "turn_history")
                    )),
                    "mention_count": 1,
                    "salience": entity_data.get("salience", 0.8),
                    "type": entity_data.get("type", "Unknown"),
                    "attributes": entity_data.get("attributes", {})
                }
        
        # Decay salience of old entities
        for entity_name in tracker:
            if entity_name not in new_entities:
                tracker[entity_name]["salience"] *= 0.95  # Decay factor
        
        self.redis.hset(session_key, "entity_tracker", json.dumps(tracker))
```

**Advantages:**

- ✅ Fast read/write performance (microseconds)
- ✅ Automatic TTL expiration for session cleanup
- ✅ Simple key-value operations
- ✅ Horizontally scalable

**Disadvantages:**

- ❌ Limited query capabilities
- ❌ No relationships between sessions
- ❌ Must serialize/deserialize JSON

### Approach 2: Neo4j Graph-Based Context

**Best for:** Layer 2 (User Context) and Layer 4 (Discourse Context) - relationship-rich data

**Architecture:**

```python
class GraphContextManager:
    """Manages persistent conversation context in Neo4j"""
    
    def __init__(self, graphdb_url: str):
        self.graphdb_url = graphdb_url
    
    def create_conversation(self, user_id: str, session_id: str) -> str:
        """Create a new conversation node"""
        payload = {
            "label": "Conversation",
            "properties": {
                "conversation_id": f"conv_{session_id}",
                "session_id": session_id,
                "started_at": datetime.now().isoformat(),
                "topic": "general",
                "status": "active"
            }
        }
        
        response = requests.post(
            f"{self.graphdb_url}/create_node",
            json=payload,
            timeout=5
        )
        
        if response.status_code == 201:
            conv_node_id = response.json()["node_id"]
            
            # Link to user
            self._create_user_conversation_link(user_id, conv_node_id)
            
            return f"conv_{session_id}"
        
        return None
    
    def add_turn_to_conversation(self, conversation_id: str, turn_data: Dict[str, Any]):
        """Add a turn node and link it to conversation"""
        # Create Turn node
        turn_payload = {
            "label": "Turn",
            "properties": {
                "turn_id": turn_data["turn_id"],
                "query": turn_data["query"],
                "resolved_query": turn_data.get("resolved_query", turn_data["query"]),
                "response_summary": turn_data.get("response_summary", ""),
                "intent": turn_data.get("intent", "unknown"),
                "timestamp": turn_data["timestamp"]
            }
        }
        
        turn_response = requests.post(
            f"{self.graphdb_url}/create_node",
            json=turn_payload,
            timeout=5
        )
        
        if turn_response.status_code == 201:
            turn_node_id = turn_response.json()["node_id"]
            
            # Link turn to conversation
            self._link_turn_to_conversation(conversation_id, turn_node_id, turn_data["turn_id"])
            
            # Link turn to mentioned concepts
            for concept in turn_data.get("concepts", []):
                self._link_turn_to_concept(turn_node_id, concept, 
                                          turn_data.get("entities", {}).get(concept, {}).get("salience", 0.5))
            
            # Link to previous turn (conversation flow)
            if turn_data["turn_id"] > 1:
                self._link_to_previous_turn(conversation_id, turn_node_id, turn_data["turn_id"])
    
    def get_user_conversation_history(self, user_id: str, limit: int = 10) -> List[Dict]:
        """Retrieve recent conversations for a user"""
        query = {
            "cypher": f"""
                MATCH (u:User {{user_id: $user_id}})-[STARTED]->(c:Conversation)
                RETURN c
                ORDER BY c.started_at DESC
                LIMIT {limit}
            """,
            "parameters": {"user_id": user_id}
        }
        
        response = requests.post(
            f"{self.graphdb_url}/query",
            json=query,
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json().get("results", [])
        
        return []
    
    def get_related_past_conversations(self, concept: str, user_id: str) -> List[Dict]:
        """Find past conversations that mentioned a concept"""
        query = {
            "cypher": """
                MATCH (u:User {user_id: $user_id})-[STARTED]->(c:Conversation)
                      -[HAS_TURN]->(t:Turn)-[MENTIONS]->(concept:Concept {name: $concept})
                RETURN DISTINCT c, collect(t) as turns
                ORDER BY c.started_at DESC
                LIMIT 5
            """,
            "parameters": {
                "user_id": user_id,
                "concept": concept.lower()
            }
        }
        
        response = requests.post(
            f"{self.graphdb_url}/query",
            json=query,
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json().get("results", [])
        
        return []
```

**Advantages:**

- ✅ Rich relationship queries
- ✅ Natural conversation flow representation
- ✅ Links to existing concept graph
- ✅ Powerful pattern matching

**Disadvantages:**

- ❌ Slower than Redis for simple lookups
- ❌ More complex to query
- ❌ Requires careful indexing for performance

### Approach 3: Vector Embeddings for Semantic Context

**Best for:** Layer 3 (World Context) - semantic similarity and inference

**Architecture:**

```python
class SemanticContextManager:
    """Manages semantic understanding using vector embeddings"""
    
    def __init__(self, vector_db_client, embedding_model):
        self.vector_db = vector_db_client
        self.embedding_model = embedding_model
    
    def embed_query(self, query: str) -> List[float]:
        """Convert query to semantic embedding"""
        return self.embedding_model.encode(query)
    
    def find_semantically_similar_past_queries(self, query: str, user_id: str, 
                                              threshold: float = 0.7, limit: int = 5) -> List[Dict]:
        """Find past queries similar in meaning"""
        query_embedding = self.embed_query(query)
        
        # Search vector database
        results = self.vector_db.similarity_search(
            embedding=query_embedding,
            filter={"user_id": user_id},
            threshold=threshold,
            limit=limit
        )
        
        return results
    
    def enrich_with_semantic_context(self, query: str, concepts: List[str]) -> Dict[str, Any]:
        """Add semantic context to query"""
        # Find related concepts through embedding similarity
        related_concepts = []
        
        for concept in concepts:
            concept_embedding = self.embed_query(concept)
            similar = self.vector_db.similarity_search(
                embedding=concept_embedding,
                collection="concepts",
                limit=3
            )
            related_concepts.extend(similar)
        
        return {
            "original_concepts": concepts,
            "related_concepts": related_concepts,
            "semantic_expansion": [r["name"] for r in related_concepts]
        }
```

**Advantages:**

- ✅ Captures semantic similarity beyond keywords
- ✅ Enables "fuzzy" context matching
- ✅ Can find related concepts automatically
- ✅ Supports multi-language semantic search

**Disadvantages:**

- ❌ Requires embedding model (adds latency)
- ❌ Black-box similarity (less explainable)
- ❌ Storage overhead for embeddings
- ❌ Needs vector database infrastructure

### Approach 4: LLM-Powered Context Reasoning

**Best for:** Complex inference and common sense reasoning

**Architecture:**

```python
class LLMContextReasoner:
    """Uses LLM for complex context understanding"""
    
    def __init__(self, llm_client):
        self.llm = llm_client
    
    def resolve_reference(self, current_query: str, conversation_history: List[Dict]) -> str:
        """Use LLM to resolve pronouns and references"""
        
        # Build context prompt
        history_text = "\n".join([
            f"Turn {turn['turn_id']}: User: {turn['query']}"
            for turn in conversation_history[-3:]  # Last 3 turns
        ])
        
        prompt = f"""Given this conversation history:

{history_text}

New query: "{current_query}"

If the new query contains pronouns or references (it, that, they, he, she, etc.), 
rewrite the query with explicit references. If no references exist, return the original query.

Rewritten query:"""
        
        response = self.llm.generate(prompt, max_tokens=100)
        resolved_query = response.strip()
        
        return resolved_query if resolved_query else current_query
    
    def infer_implicit_context(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Infer unstated information from query"""
        
        prompt = f"""Query: "{query}"
        
Context:
- Active topics: {context.get('active_topics', [])}
- Recent entities: {list(context.get('entity_tracker', {}).keys())[:5]}

What implicit information or assumptions can be inferred from this query?
Respond in JSON format:
{{
    "implicit_intent": "...",
    "assumed_knowledge": [...],
    "inferred_relationships": [...]
}}"""
        
        response = self.llm.generate(prompt, max_tokens=200)
        
        try:
            inferred = json.loads(response)
            return inferred
        except json.JSONDecodeError:
            return {}
    
    def common_sense_reasoning(self, query: str, concepts: List[str]) -> Dict[str, Any]:
        """Apply common sense reasoning"""
        
        prompt = f"""Query: "{query}"
Concepts: {concepts}

Provide common sense context about these concepts:
1. Typical properties or characteristics
2. Common relationships between concepts
3. Expected knowledge prerequisites
4. Real-world constraints or assumptions

Respond in JSON format:
{{
    "properties": {{}},
    "relationships": [],
    "prerequisites": [],
    "constraints": []
}}"""
        
        response = self.llm.generate(prompt, max_tokens=300)
        
        try:
            common_sense = json.loads(response)
            return common_sense
        except json.JSONDecodeError:
            return {}
```

**Advantages:**

- ✅ Most flexible and powerful
- ✅ Can handle complex reasoning
- ✅ Natural language understanding
- ✅ Minimal rule engineering

**Disadvantages:**

- ❌ Expensive (API costs or compute)
- ❌ Higher latency
- ❌ Non-deterministic outputs
- ❌ Requires careful prompt engineering

---

## Integration with Existing Components

### Enhanced Input Processor Integration

**Current:** [`input_processor.py`](../src/myriad/services/processing/input_processor/input_processor.py:1)

**Modifications:**

```python
class ContextAwareInputProcessor(InputProcessor):
    """Enhanced Input Processor with context awareness"""
    
    def __init__(self):
        super().__init__()
        
        # Add context managers
        self.session_context = SessionContextManager(redis_client)
        self.user_context = GraphContextManager(graphdb_url)
        self.semantic_context = SemanticContextManager(vector_db, embedding_model)
        self.llm_reasoner = LLMContextReasoner(llm_client)
    
    def process_query_with_context(self, raw_query: str, user_id: str, 
                                   session_id: Optional[str] = None) -> TaskList:
        """Process query with full context awareness"""
        
        # Step 1: Get or create session
        session_id = self.session_context.get_or_create_session(user_id, session_id)
        
        # Step 2: Retrieve recent context
        recent_turns = self.session_context.get_recent_context(session_id, n_turns=3)
        entity_tracker = self.session_context.get_entity_tracker(session_id)
        
        # Step 3: Resolve references using LLM
        resolved_query = self.llm_reasoner.resolve_reference(raw_query, recent_turns)
        
        # Step 4: Enrich with semantic context
        semantic_enrichment = self.semantic_context.enrich_with_semantic_context(
            resolved_query, 
            self._extract_initial_concepts(resolved_query)
        )
        
        # Step 5: Build enriched user context
        enriched_context = {
            "session_id": session_id,
            "user_id": user_id,
            "previous_queries": [turn["query"] for turn in recent_turns],
            "entity_tracker": entity_tracker,
            "active_topics": self.session_context.get_active_topics(session_id),
            "semantic_context": semantic_enrichment,
            "user_preferences": self.user_context.get_user_preferences(user_id)
        }
        
        # Step 6: Process with original pipeline (now context-aware)
        query_metadata, parsed_query = self._parse_with_language_support(
            resolved_query, enriched_context
        )
        
        intent_result = self.intent_recognizer.recognize_intent(
            resolved_query, enriched_context
        )
        
        # Step 7: Context-aware ambiguity resolution
        ambiguity_detection = self.ambiguity_resolver.detect_ambiguity(
            resolved_query, parsed_query.concepts, intent_result
        )
        
        if ambiguity_detection.is_ambiguous:
            # Use past context for disambiguation
            disambiguation_result = self.ambiguity_resolver.resolve_ambiguity(
                resolved_query, ambiguity_detection, enriched_context
            )
        
        # Step 8: Generate task list (as before)
        task_list = self._generate_task_list(
            parsed_query, intent_result, ambiguity_detection, 
            disambiguation_result, uncertainty_assessment, 
            query_metadata.detected_language.value
        )
        
        # Step 9: Store turn in session context
        turn_data = {
            "query": raw_query,
            "resolved_query": resolved_query,
            "concepts": parsed_query.concepts,
            "entities": self._extract_entities_with_salience(parsed_query, entity_tracker),
            "intent": intent_result.primary_intent,
            "response_summary": ""  # Will be filled by output processor
        }
        
        self.session_context.add_turn(session_id, turn_data)
        
        # Step 10: Persist to graph (async, non-blocking)
        if len(recent_turns) == 0:  # First turn
            conv_id = self.user_context.create_conversation(user_id, session_id)
        else:
            conv_id = f"conv_{session_id}"
        
        self.user_context.add_turn_to_conversation(conv_id, turn_data)
        
        return task_list_message
```

### Enhanced Graph Intelligence Integration

**Current:** [`enhanced_graph_intelligence.py`](../src/myriad/core/intelligence/enhanced_graph_intelligence.py:1)

**Modifications:**

```python
class ContextAwareGraphIntelligence(EnhancedGraphIntelligence):
    """Graph intelligence with conversation context"""
    
    def discover_agents_with_context(self, concept: str, intent: str,
                                     session_context: Dict[str, Any],
                                     user_context: Dict[str, Any]) -> List[AgentRelevanceScore]:
        """Discover agents considering conversation context"""
        
        # Step 1: Standard discovery
        base_agents = self.discover_intelligent_agents(concept, intent, session_context)
        
        # Step 2: Boost agents that appeared in recent conversation
        recent_agent_usage = self._get_recent_agent_usage(session_context.get("session_id"))
        
        for agent_score in base_agents:
            if agent_score.agent_id in recent_agent_usage:
                # Boost relevance for agents recently used in conversation
                recency_boost = recent_agent_usage[agent_score.agent_id]["recency_score"]
                agent_score.relevance_score = min(1.0, 
                    agent_score.relevance_score * (1.0 + recency_boost * 0.2)
                )
                agent_score.reasoning.append(
                    f"Recently used in conversation (boost: {recency_boost:.2f})"
                )
        
        # Step 3: Consider user's past successful agent interactions
        user_agent_preferences = self._get_user_agent_preferences(
            user_context.get("user_id")
        )
        
        for agent_score in base_agents:
            if agent_score.agent_id in user_agent_preferences:
                pref_data = user_agent_preferences[agent_score.agent_id]
                if pref_data["success_rate"] > 0.8:
                    # Boost agents user had success with
                    agent_score.relevance_score = min(1.0,
                        agent_score.relevance_score * 1.1
                    )
                    agent_score.reasoning.append(
                        f"High past success rate with this user ({pref_data['success_rate']:.2f})"
                    )
        
        # Step 4: Consider collaborative agent patterns
        if len(recent_agent_usage) > 0:
            # Find agents that often collaborate with recently used agents
            collaborative_agents = self._find_collaborative_agents(
                list(recent_agent_usage.keys())
            )
            
            for collab_agent, collab_score in collaborative_agents.items():
                # Add collaborative agents to candidates if not already present
                if not any(a.agent_id == collab_agent for a in base_agents):
                    collab_agent_profile = self.agent_profiles.get(collab_agent)
                    if collab_agent_profile:
                        new_score = AgentRelevanceScore(
                            agent_id=collab_agent,
                            relevance_score=collab_score * 0.7,  # Reduced for indirect match
                            expertise_match=0.5,
                            capability_match=0.5,
                            domain_overlap=0.5,
                            performance_factor=0.8,
                            availability_factor=1.0,
                            confidence_level=0.6,
                            reasoning=[f"Often collaborates with recently used agents"]
                        )
                        base_agents.append(new_score)
        
        # Step 5: Re-sort by updated relevance scores
        base_agents.sort(key=lambda x: x.relevance_score, reverse=True)
        
        return base_agents[:self.config['max_agents_per_query']]
    
    def _get_recent_agent_usage(self, session_id: str) -> Dict[str, Dict]:
        """Get agents used in recent conversation turns"""
        # Query session context for agent usage
        pass
    
    def _get_user_agent_preferences(self, user_id: str) -> Dict[str, Dict]:
        """Get user's historical agent interaction patterns"""
        # Query user context from Neo4j
        pass
    
    def _find_collaborative_agents(self, agent_ids: List[str]) -> Dict[str, float]:
        """Find agents that often work with given agents"""
        # Query Neo4j for agent collaboration patterns
        pass
```

### Orchestrator Integration

**Current:** [`orchestrator.py`](../src/myriad/services/orchestrator/orchestrator.py:1)

**Modifications:**

```python
# Add context-aware agent discovery
def discover_agent_via_graph_with_context(concept: str, intent: str, 
                                         session_context: Dict[str, Any],
                                         user_context: Dict[str, Any]) -> Optional[str]:
    """Context-aware agent discovery"""
    
    if ENHANCED_INTELLIGENCE_AVAILABLE:
        try:
            # Use context-aware discovery
            agent_scores = enhanced_intelligence.discover_agents_with_context(
                concept=concept,
                intent=intent,
                session_context=session_context,
                user_context=user_context
            )
            
            if agent_scores:
                best_agent = agent_scores[0]
                agent_profile = enhanced_intelligence.agent_profiles.get(best_agent.agent_id)
                if agent_profile and agent_profile.endpoint:
                    return agent_profile.endpoint
        except Exception as e:
            logger.error(f"Context-aware discovery failed: {e}")
            return _discover_agent_basic_fallback(concept, intent)
    
    return _discover_agent_basic_fallback(concept, intent)
```

---

## Implementation Roadmap

### Phase 1: Basic Session Context (Week 1)

**Goal:** Enable conversation memory within a session

**Tasks:**

1. ✅ Set up Redis infrastructure in Docker Compose
2. ✅ Implement `SessionContextManager` class
3. ✅ Add turn history tracking (last 10 turns)
4. ✅ Implement basic entity tracking with salience
5. ✅ Create reference resolution using entity tracker
6. ✅ Integrate with Input Processor
7. ✅ Add session ID to API requests
8. ✅ Implement automatic session creation

**Deliverable:** System can resolve "Who invented it?" after "What is a lightbulb?"

**Acceptance Criteria:**

- Session context persists for 30 minutes
- Pronouns are resolved using entity tracker
- Turn history is maintained in sliding window
- Entity salience decays over time

### Phase 2: Graph-Based Persistent Context (Weeks 2-3)

**Goal:** Store conversation history in Neo4j for long-term learning

**Tasks:**

1. ✅ Extend Neo4j schema with User, Conversation, Turn nodes
2. ✅ Implement `GraphContextManager` class
3. ✅ Create conversation-to-user relationships
4. ✅ Link turns to concepts via MENTIONS relationship
5. ✅ Implement conversation flow tracking (FOLLOWS relationships)
6. ✅ Add user preference storage
7. ✅ Create query endpoints for past conversation retrieval
8. ✅ Integrate with context-aware agent selection

**Deliverable:** System learns from past conversations and personalizes responses

**Acceptance Criteria:**

- Conversations are persisted to Neo4j
- Can query "Have we talked about X before?"
- User preferences affect agent selection
- Conversation patterns are tracked

### Phase 3: Semantic Context Enhancement (Weeks 4-5)

**Goal:** Add semantic understanding beyond keywords

**Tasks:**

1. ✅ Set up vector database (Pinecone, Weaviate, or Neo4j vector index)
2. ✅ Integrate sentence embedding model
3. ✅ Implement `SemanticContextManager` class
4. ✅ Index past queries as vectors
5. ✅ Add semantic similarity search
6. ✅ Implement concept expansion via embeddings
7. ✅ Integrate with ambiguity resolution

**Deliverable:** System understands semantically similar queries even with different wording

**Acceptance Criteria:**

- Semantic search finds related past queries
- Concept expansion suggests related concepts
- Ambiguity resolution uses semantic similarity
- Performance < 200ms for semantic operations

### Phase 4: Advanced Context Reasoning (Weeks 6-9)

**Goal:** Add LLM-powered inference and common sense reasoning

**Tasks:**

1. ✅ Integrate LLM client (OpenAI, Anthropic, or local model)
2. ✅ Implement `LLMContextReasoner` class
3. ✅ Add pronoun resolution via LLM
4. ✅ Implement ellipsis completion
5. ✅ Add implicit context inference
6. ✅ Implement common sense reasoning
7. ✅ Optimize prompts for cost/quality
8. ✅ Add caching for LLM outputs
9. ✅ Implement fallback for LLM failures
10. ✅ Performance testing and optimization

**Deliverable:** System has human-like context understanding with inference

**Acceptance Criteria:**

- Complex references are correctly resolved
- Implicit context is inferred accurately
- Common sense reasoning improves responses
- LLM fallback maintains functionality
- Average query processing time < 500ms

### Phase 5: User Profiling & Learning (Weeks 10-12)

**Goal:** Learn user preferences and adapt over time

**Tasks:**

1. ✅ Implement user preference extraction
2. ✅ Add expertise level tracking
3. ✅ Create interaction pattern analysis
4. ✅ Implement adaptive explanation depth
5. ✅ Add A/B testing for personalization
6. ✅ Create user feedback integration
7. ✅ Implement privacy controls
8. ✅ Add GDPR compliance features

**Deliverable:** System personalizes to individual users over time

**Acceptance Criteria:**

- User expertise is accurately estimated
- Explanation verbosity adapts automatically
- Privacy controls function correctly
- Performance doesn't degrade with user history growth

---

## Example Scenarios

### Scenario 1: Multi-Turn Technical Question

**Without Context:**

```
Turn 1:
User: "What is a transistor?"
System: "A semiconductor device..."

Turn 2:
User: "How does it work in a CPU?"
System: ❌ "I don't understand what 'it' refers to."
```

**With Context:**

```
Turn 1:
User: "What is a transistor?"
System: "A semiconductor device..."
[Stored in session: entity="transistor", salience=0.9]

Turn 2:
User: "How does it work in a CPU?"
[Reference resolution: "it" → "transistor"]
[Resolved query: "How does a transistor work in a CPU?"]
System: ✅ "In a CPU, transistors act as switches..."
[Updated entities: transistor (salience=0.85), CPU (salience=0.9)]

Turn 3:
User: "What about cache memory?"
[Topic shift detected: CPU → cache memory]
[Context: Still within "computer architecture" domain]
System: ✅ "Cache memory uses transistors to provide..."
[Links cache memory to transistor and CPU in conversation graph]
```

### Scenario 2: Implicit Context

**Without Context:**

```
User: "I'm learning about renewable energy"
System: "That's great! How can I help?"

User: "Tell me about solar panels"
System: "Solar panels convert sunlight to electricity..."

User: "And wind turbines?"
System: ❌ Treats as independent query about wind turbines
```

**With Context:**

```
User: "I'm learning about renewable energy"
[Goal inference: user_goal="learn_about_renewable_energy"]
[Context: learning_mode=true, expertise_level=beginner]
System: "That's great! I can help you understand different renewable energy sources."

User: "Tell me about solar panels"
[Topic: renewable_energy → solar_panels]
[Context: Adjust for beginner learning mode]
System: ✅ "Solar panels convert sunlight to electricity. They're one of the most common renewable energy sources. Would you like to know how they work or their advantages?"

User: "And wind turbines?"
[Ellipsis completion: "Tell me about wind turbines"]
[Implicit context: comparing renewable energy sources]
System: ✅ "Wind turbines harness wind energy to generate electricity. Compared to solar panels, they work best in windy areas and can generate power 24/7. Both are important renewable sources. Would you like me to compare them in more detail?"
```

### Scenario 3: User Profile Context

**First Interaction:**

```
User: "Explain quantum mechanics"
[No user history available]
System: [Detailed technical explanation with equations]
User: "That's too complex"
[Stores preference: verbosity=moderate, expertise_quantum=beginner]

User: "Can you simplify?"
System: ✅ [Simpler explanation with analogies]
[Updates preference: verbosity=simple, prefers_analogies=true]
```

**Later Interaction:**

```
User: "Explain relativity"
[Retrieves user profile: verbosity=simple, prefers_analogies=true, expertise_physics=beginner]
[Adapts automatically without being told]
System: ✅ [Simple explanation with analogies from the start]
"Think of relativity like being on a moving train..."

[No complaint from user]
[Reinforces preference: learning_style confirmed]
```

### Scenario 4: Context-Aware Agent Selection

**Without Context:**

```
Turn 1: "What is machine learning?"
[Selects: ML_Definition_Agent based on concept only]

Turn 2: "How do neural networks learn?"
[Selects: Neural_Network_Agent based on concept only]
[No consideration of previous agent or conversation flow]
```

**With Context:**

```
Turn 1: "What is machine learning?"
[Selects: ML_Definition_Agent based on concept]
[Records: Used ML_Definition_Agent successfully]

Turn 2: "How do neural networks learn?"
[Context: Recent conversation about ML, user interested in learning]
[Enhanced selection considers:]
  - Neural networks are subset of ML (domain continuity)
  - ML_Definition_Agent and Neural_Network_Agent often collaborate
  - User is in learning mode (not just lookup)
  
[Selects: Neural_Network_Agent WITH collaboration hint to ML_Definition_Agent]
[Agent selection reasoning includes:]
  ✅ "Neural networks are part of machine learning (topic continuity)"
  ✅ "Often used with ML_Definition_Agent (collaboration pattern)"
  ✅ "User is learning progressively (educational flow)"

System: ✅ [More coherent response that builds on previous explanation]
"Building on what we discussed about machine learning, neural networks learn by..."
```

---

## Trade-offs and Design Decisions

### Decision 1: Redis + Neo4j Hybrid vs. Neo4j Only

**Option A: Redis + Neo4j Hybrid (RECOMMENDED)**

**Pros:**

- ✅ Fast session access (microseconds)
- ✅ Automatic session expiration
- ✅ Reduced Neo4j query load
- ✅ Clear separation: temporary vs permanent

**Cons:**

- ❌ Two systems to maintain
- ❌ Data synchronization complexity
- ❌ Additional infrastructure cost

**Option B: Neo4j Only**

**Pros:**

- ✅ Single source of truth
- ✅ Unified query interface
- ✅ Simpler architecture

**Cons:**

- ❌ Slower for frequent session access
- ❌ Manual session cleanup required
- ❌ Higher Neo4j load

**Decision:** Use Hybrid Approach (Option A)

**Rationale:**

- Session context is accessed on every query (needs speed)
- Redis TTL provides automatic cleanup
- Neo4j is better for relationship-rich persistent data
- Clear responsibility separation aids maintenance

### Decision 2: Entity Salience Calculation

**Option A: Simple Decay Model (RECOMMENDED)**

```python
# On mention: increase salience
entity.salience = min(1.0, entity.salience * 0.9 + 0.3)

# No mention: decay salience
entity.salience *= 0.95
```

**Pros:**

- ✅ Simple and predictable
- ✅ Fast computation
- ✅ No training required

**Cons:**

- ❌ Fixed decay rate may not fit all scenarios
- ❌ Doesn't learn optimal parameters

**Option B: Learned Salience Model**

Train a model to predict entity salience based on:

- Recency
- Frequency
- Entity type
- Conversation context

**Pros:**

- ✅ Potentially more accurate
- ✅ Adapts to patterns

**Cons:**

- ❌ Requires training data
- ❌ More complex
- ❌ Slower inference

**Decision:** Start with Simple Decay (Option A), evolve to Learned (Option B) in Phase 5

**Rationale:**

- Simple model sufficient for MVP
- Can collect data for training during Phases 1-4
- Easy to swap implementations later

### Decision 3: Reference Resolution Strategy

**Option A: Rule-Based Resolution (Fast, Phase 1)**

```python
def resolve_reference(pronoun: str, entity_tracker: Dict) -> str:
    # Get most salient entity matching pronoun type
    if pronoun in ["it", "that", "this"]:
        # Return highest salience non-person entity
        entities = [(name, data) for name, data in entity_tracker.items() 
                   if data["type"] != "Person"]
        return max(entities, key=lambda x: x[1]["salience"])[0]
```

**Pros:**

- ✅ Fast (microseconds)
- ✅ Deterministic
- ✅ No external dependencies

**Cons:**

- ❌ Limited accuracy (~70%)
- ❌ Doesn't handle complex cases

**Option B: LLM-Based Resolution (Accurate, Phase 4)**

```python
def resolve_reference(pronoun: str, conversation_history: List[Dict]) -> str:
    prompt = f"In the query '{query}', what does '{pronoun}' refer to?"
    return llm.generate(prompt)
```

**Pros:**

- ✅ High accuracy (~95%)
- ✅ Handles complex cases
- ✅ Natural language understanding

**Cons:**

- ❌ Slower (100-500ms)
- ❌ Costs money (API calls)
- ❌ Non-deterministic

**Decision:** Hybrid Approach

Phase 1-3: Use rule-based with confidence scoring

```python
result, confidence = rule_based_resolution(pronoun, entity_tracker)
if confidence < 0.7:
    result = llm_resolution(pronoun, conversation_history)  # Fallback to LLM
```

Phase 4+: LLM with rule-based fallback for speed

```python
try:
    result = cached_llm_resolution(pronoun, conversation_history)
except (TimeoutError, RateLimitError):
    result, _ = rule_based_resolution(pronoun, entity_tracker)  # Fast fallback
```

**Rationale:**

- Get working system quickly with rules
- Add LLM for accuracy where needed
- Cache LLM results for common patterns
- Always have fast fallback

### Decision 4: Context Window Size

**Option A: Fixed Window (10 turns)**
**Option B: Adaptive Window (5-20 turns based on complexity)**
**Option C: Sliding Window with Summarization**

**Decision:** Option A for Phase 1, evolve to Option C in Phase 5

**Rationale:**

- Fixed window is simplest to implement and reason about
- 10 turns covers most conversations
- Summarization can be added later for longer conversations
- Adaptive window adds complexity without clear benefit

### Decision 5: Privacy & Data Retention

**Policy:**

1. **Session Context**: Automatic deletion after 30-60 minutes TTL
2. **User Context**: Retained indefinitely with opt-out option
3. **Conversation History**: Retained for 90 days, then summarized
4. **Personal Information**: Never stored in plain text
5. **User Control**: Dashboard to view/delete all stored data

**GDPR Compliance:**

- Right to access: API to retrieve all user data
- Right to erasure: Cascade delete all user context
- Right to portability: Export user data in JSON format
- Purpose limitation: Context only used for improving responses

---

## Open Questions for Discussion

### Technical Questions

1. **Vector Database Selection**
   - Use Pinecone (managed, easy) or Weaviate (self-hosted, flexible)?
   - Or extend Neo4j with vector index plugin?
   - Trade-off: Simplicity vs control vs cost

2. **LLM Provider**
   - OpenAI GPT-4 (expensive, best quality)?
   - Anthropic Claude (mid-cost, good privacy)?
   - Local model (free, slower, lower quality)?
   - Mix: Local for simple, API for complex?

3. **Conversation Graph Pruning**
   - How aggressively should we prune old conversation nodes?
   - Keep last N conversations vs last N days?
   - Summarize old conversations vs delete?

4. **Multi-User Context Sharing**
   - Should users share anonymized context patterns?
   - Privacy-preserving learning across users?
   - Federated learning approach?

### Product Questions

5. **User Control Granularity**
   - How much control should users have over context?
   - Toggle for "remember my preferences" vs "private mode"?
   - Conversation-level privacy settings?

6. **Explanation vs Performance**
   - Should system explain why it interpreted context a certain way?
   - "I interpreted 'it' as lightbulb because..." adds latency
   - Trade-off transparency for speed?

7. **Context Reset Points**
   - Should topic shifts reset some context?
   - Explicit "new conversation" vs automatic detection?
   - Risk: Losing useful context vs carrying irrelevant context

### Ethical Questions

8. **Bias in Context**
   - Can context tracking amplify biases?
   - Example: User asks about "doctors" → system assumes male from past context
   - Mitigation strategies?

9. **Manipulation Risk**
   - Can remembering user preferences lead to filter bubbles?
   - Should system sometimes challenge assumptions?
   - Balance between personalization and exposure to diverse views?

10. **Transparency**
    - Should users know what context is being used?
    - Visible "memory" panel showing active context?
    - Opt-in vs opt-out for advanced features?

---

## References

### Academic Research

1. **Working Memory & Context**

- Baddeley, A. (2003). "Working memory: looking back and looking forward." *Nature Reviews Neuroscience*
- Cowan, N. (2001). "The magical number 4 in short-term memory." *Behavioral and Brain Sciences*

2. **Reference Resolution**

- Hobbs, J. R. (1978). "Resolving pronoun references." *Lingua*
- Grosz, B. J., Joshi, A. K., & Weinstein, S. (1995). "Centering: A framework for modeling the local coherence of discourse." *Computational Linguistics*

3. **Dialogue Systems**

- Jurafsky, D., & Martin, J. H. (2021). "Speech and Language Processing" (3rd ed.), Chapter 24: Dialogue Systems
- Young, S., et al. (2013). "POMDP-based statistical spoken dialog systems." *Proceedings of the IEEE*

### Technical Implementations

4. **Conversation Memory Systems**

- Google Meena: Adiwardana et al. (2020). "Towards a Human-like Open-Domain Chatbot"
- Meta BlenderBot: Roller et al. (2021). "Recipes for building an open-domain chatbot"

5. **Context Tracking**

- Rasa Dialogue Management: <https://rasa.com/docs/rasa/dialogue-management/>
- Microsoft Bot Framework: Context and State Management

6. **Graph-Based Context**

- Neo4j Conversational AI: <https://neo4j.com/use-cases/conversational-ai/>
- Knowledge Graphs for Dialogue: Chen et al. (2019)

### Myriad System Documentation

7. **Related Architecture Documents**

- [`ARCHITECTURE.md`](ARCHITECTURE.md) - Core system design
- [`GRAPH_SCHEMA.md`](GRAPH_SCHEMA.md) - Neo4j schema with Hebbian learning
- [`PROTOCOLS.md`](PROTOCOLS.md) - Communication protocols

8. **Existing Components**

- [`input_processor.py`](../src/myriad/services/processing/input_processor/input_processor.py) - Current input processing
- [`enhanced_graph_intelligence.py`](../src/myriad/core/intelligence/enhanced_graph_intelligence.py) - Agent selection
- [`orchestrator.py`](../src/myriad/services/orchestrator/orchestrator.py) - Task coordination

---

## Appendix A: API Design Proposals

### Context Management API

**Base URL:** `/api/v1/context`

#### Session Management

**POST /sessions/create**

```json
{
 "user_id": "user_xyz789",
 "metadata": {
   "source": "web_ui",
   "user_agent": "Mozilla/5.0..."
 }
}

Response:
{
 "session_id": "sess_abc123",
 "created_at": "2025-10-11T00:00:00Z",
 "ttl": 1800
}
```

**GET /sessions/{session_id}**

```json
Response:
{
 "session_id": "sess_abc123",
 "user_id": "user_xyz789",
 "created_at": "2025-10-11T00:00:00Z",
 "last_active": "2025-10-11T00:15:30Z",
 "turn_count": 5,
 "active_entities": ["lightbulb", "Thomas Edison"],
 "current_topic": "technology_history"
}
```

**POST /sessions/{session_id}/turns**

```json
{
 "query": "Who invented it?",
 "resolved_query": "Who invented the lightbulb?",
 "concepts": ["lightbulb", "invention"],
 "entities": {
   "lightbulb": {"type": "Concept", "salience": 0.85},
   "Thomas Edison": {"type": "Person", "salience": 0.9}
 },
 "intent": "analyze_historical_context"
}

Response:
{
 "turn_id": 2,
 "stored": true,
 "entity_updates": {
   "lightbulb": {"salience_delta": -0.05},
   "Thomas Edison": {"salience_delta": 0.9, "new_entity": true}
 }
}
```

#### Context Retrieval

**GET /sessions/{session_id}/context**

```json
Query parameters:
- n_turns: Number of recent turns (default: 3)
- include_entities: Boolean (default: true)
- include_topics: Boolean (default: true)

Response:
{
 "session_id": "sess_abc123",
 "recent_turns": [...],
 "entity_tracker": {...},
 "active_topics": ["technology", "invention_history"],
 "current_goal": "learn_about_lightbulb_history"
}
```

**POST /context/resolve_reference**

```json
{
 "query": "Who invented it?",
 "session_id": "sess_abc123",
 "reference_type": "pronoun"  // Optional: "pronoun", "definite", "ellipsis"
}

Response:
{
 "resolved_query": "Who invented the lightbulb?",
 "references": [
   {
     "original": "it",
     "resolved_to": "lightbulb",
     "confidence": 0.95,
     "reasoning": "Most salient object entity in recent context"
   }
 ],
 "method": "llm_powered"  // or "rule_based"
}
```

#### User Profile Management

**GET /users/{user_id}/profile**

```json
Response:
{
 "user_id": "user_xyz789",
 "preferences": {
   "verbosity": "moderate",
   "language": "en",
   "explanation_style": "analogies"
 },
 "expertise_levels": {
   "physics": "beginner",
   "programming": "advanced",
   "history": "intermediate"
 },
 "interaction_patterns": {
   "avg_session_duration": 450,
   "preferred_clarification": "multiple_choice",
   "typical_query_complexity": "medium"
 },
 "conversation_stats": {
   "total_conversations": 42,
   "total_turns": 387,
   "most_discussed_topics": ["technology", "science", "history"]
 }
}
```

**PUT /users/{user_id}/preferences**

```json
{
 "verbosity": "detailed",
 "explanation_style": "technical"
}

Response:
{
 "updated": true,
 "preferences": {...}
}
```

**GET /users/{user_id}/conversations**

```json
Query parameters:
- limit: Number of conversations (default: 10)
- topic: Filter by topic (optional)
- date_from: ISO timestamp (optional)
- date_to: ISO timestamp (optional)

Response:
{
 "conversations": [
   {
     "conversation_id": "conv_def456",
     "session_id": "sess_abc123",
     "started_at": "2025-10-11T00:00:00Z",
     "ended_at": "2025-10-11T00:30:00Z",
     "turn_count": 12,
     "topics": ["lightbulb", "Thomas Edison", "invention"],
     "summary": "Discussion about lightbulb invention and history"
   }
 ],
 "total": 42,
 "page": 1
}
```

---

## Appendix B: Performance Benchmarks

### Target Performance Metrics

| Operation | Target Latency | Max Acceptable | Notes |
|-----------|---------------|----------------|-------|
| **Session Context Retrieval** | < 5ms | < 20ms | Redis lookup |
| **Entity Tracker Update** | < 10ms | < 50ms | Redis write |
| **Reference Resolution (Rule)** | < 50ms | < 100ms | In-memory computation |
| **Reference Resolution (LLM)** | < 200ms | < 500ms | API call overhead |
| **Graph Context Query** | < 100ms | < 300ms | Neo4j traversal |
| **Semantic Search** | < 150ms | < 400ms | Vector DB lookup |
| **Full Context Enrichment** | < 300ms | < 800ms | Combined operations |

### Scalability Targets

| Metric | Phase 1 | Phase 3 | Phase 5 |
|--------|---------|---------|---------|
| **Concurrent Sessions** | 100 | 1,000 | 10,000 |
| **Active Users** | 500 | 5,000 | 50,000 |
| **Conversations/Day** | 1,000 | 10,000 | 100,000 |
| **Storage per User** | 1 MB | 5 MB | 20 MB |
| **Total Graph Nodes** | 10K | 100K | 1M |

### Cost Estimates (Monthly)

**Phase 1 (Redis Only):**

- Redis Cloud: $20-50
- Neo4j storage: Included in existing
- Total: ~$50/month

**Phase 3 (+ Vector DB):**

- Redis Cloud: $50-100
- Neo4j storage: $100-200
- Vector DB (Pinecone): $70-150
- Total: ~$320/month

**Phase 4 (+ LLM):**

- Infrastructure: $320
- LLM API (GPT-4): $200-500 (10K queries)
- Total: ~$820/month

**Phase 5 (Production):**

- Infrastructure: $500-1000
- LLM API: $500-2000
- Total: ~$2,500/month (50K users)

---

## Appendix C: Testing Strategy

### Unit Tests

**1. Session Context Manager**

```python
def test_session_creation():
   """Test session is created with correct TTL"""
   
def test_turn_history_sliding_window():
   """Test only last 10 turns are kept"""
   
def test_entity_salience_decay():
   """Test entity salience decays correctly"""
   
def test_entity_salience_boost():
   """Test mentioned entities get salience boost"""
```

**2. Reference Resolution**

```python
def test_pronoun_resolution_rule_based():
   """Test rule-based pronoun resolution"""
   
def test_pronoun_resolution_llm():
   """Test LLM-powered pronoun resolution"""
   
def test_reference_resolution_confidence():
   """Test confidence scoring for resolutions"""
   
def test_ellipsis_completion():
   """Test completion of elliptical queries"""
```

**3. Graph Context Manager**

```python
def test_conversation_creation():
   """Test conversation node creation in Neo4j"""
   
def test_turn_linking():
   """Test turn nodes are correctly linked"""
   
def test_concept_mention_tracking():
   """Test MENTIONS relationships created"""
   
def test_conversation_retrieval():
   """Test past conversation retrieval"""
```

### Integration Tests

**1. End-to-End Context Flow**

```python
def test_multi_turn_conversation():
   """
   Test complete multi-turn conversation:
   1. "What is a lightbulb?"
   2. "Who invented it?"
   3. "When?"
   """
   
def test_context_persistence():
   """Test context survives across API calls"""
   
def test_session_expiration():
   """Test session expires after TTL"""
```

**2. Reference Resolution Integration**

```python
def test_reference_in_input_processor():
   """Test reference resolution in input processor"""
   
def test_reference_with_ambiguity():
   """Test reference resolution when ambiguous"""
   
def test_multi_reference_resolution():
   """Test multiple references in single query"""
```

**3. Context-Aware Agent Selection**

```python
def test_agent_selection_with_context():
   """Test agents selected considering context"""
   
def test_collaborative_agent_discovery():
   """Test discovery of collaborative agents"""
   
def test_user_preference_in_selection():
   """Test user preferences affect selection"""
```

### Performance Tests

**1. Load Testing**

```python
def test_concurrent_sessions():
   """Test 100 concurrent active sessions"""
   
def test_session_context_latency():
   """Test session retrieval under load"""
   
def test_graph_query_performance():
   """Test Neo4j query performance"""
```

**2. Stress Testing**

```python
def test_memory_usage():
   """Test memory usage with many sessions"""
   
def test_cache_effectiveness():
   """Test LLM caching effectiveness"""
   
def test_fallback_performance():
   """Test fallback performance when systems fail"""
```

---

## Appendix D: Migration Path

### Phase 0: Pre-Migration (Current State)

**Current System:**

- Single-query processing
- Optional `user_context` parameter (rarely used)
- No persistent context
- Stateless orchestration

**Compatibility:** Must maintain backward compatibility

### Phase 1: Add Session Context (Non-Breaking)

**Changes:**

- Add optional `session_id` parameter to `/process` endpoint
- Add new `/context/*` endpoints
- Modify [`InputProcessor.process_query()`](../src/myriad/services/processing/input_processor/input_processor.py:96) to accept session_id
- Keep existing behavior if session_id not provided

**Backward Compatibility:**

```python
def process_query(self, raw_query: str,
                user_context: Optional[Dict] = None,
                session_id: Optional[str] = None) -> TaskList:  # New optional param
   """
   If session_id provided: Use context-aware processing
   If session_id None: Use original single-query processing
   """
```

**Migration:**

- Existing clients continue to work unchanged
- New clients opt-in by providing session_id
- No data migration required

### Phase 2: Graph Extension (Additive)

**Changes:**

- Extend Neo4j schema (additive, no breaking changes)
- Add new relationship types
- No changes to existing relationships

**Migration:**

```cypher
// Add new node types
CREATE CONSTRAINT user_id_unique IF NOT EXISTS ON (u:User) ASSERT u.user_id IS UNIQUE;
CREATE CONSTRAINT conversation_id_unique IF NOT EXISTS ON (c:Conversation) ASSERT c.conversation_id IS UNIQUE;
CREATE CONSTRAINT turn_id_unique IF NOT EXISTS ON (t:Turn) ASSERT t.turn_id IS UNIQUE;

// Existing data unaffected
```

### Phase 3-5: Feature Additions (Non-Breaking)

**Changes:**

- Add vector database (new infrastructure)
- Add LLM integration (new service)
- Enhance existing components
- Add new endpoints

**Migration:**

- All changes are additive
- Existing functionality preserved
- New features opt-in

---

## Summary & Key Recommendations

### Critical Success Factors

1. **Start Simple, Evolve Gradually**

- Phase 1 provides immediate value with minimal complexity
- Each phase builds on previous success
- Can pause/adjust based on results

2. **Maintain Backward Compatibility**

- All changes are opt-in
- Existing clients unaffected
- Graceful degradation when features unavailable

3. **Performance First**

- Redis for session speed
- Caching for expensive operations
- Always have fast fallbacks

4. **Privacy by Design**

- TTL-based automatic cleanup
- User control over data
- GDPR compliance built-in

5. **Measure Everything**

- Instrument all context operations
- Track resolution accuracy
- Monitor performance continuously

### Top 3 Recommendations

**1. Implement Phase 1 Immediately (Highest ROI)**

- Redis-based session context
- Basic reference resolution
- Minimal infrastructure changes
- Expected impact: 3-5x improvement in multi-turn UX

**2. Design for Incremental Adoption**

- Optional session_id parameter
- Feature flags for new capabilities
- A/B testing for validation
- Expected benefit: Safe rollout, easy rollback

**3. Build Context-Aware Agent Selection Early**

- Extend Enhanced Graph Intelligence with context
- Track agent collaboration patterns
- Use conversation history in selection
- Expected impact: 20-30% better agent selection

### Next Steps

1. **Review & Discuss** (Week 1)

- Team review of architecture
- Resolve open questions
- Prioritize phases

2. **Technical Spike** (Week 2)

- Redis POC for session context
- Reference resolution prototype
- Performance benchmarking

3. **Implementation** (Weeks 3+)

- Phase 1 development
- Testing & validation
- Phased rollout

### Expected Outcomes

**User Experience:**

- Natural multi-turn conversations ✅
- No need to repeat context ✅
- Personalized interactions ✅
- Faster, more relevant responses ✅

**System Capabilities:**

- Human-like context understanding ✅
- Conversation memory ✅
- Reference resolution ✅
- Adaptive agent selection ✅

**Technical Excellence:**

- Scalable architecture ✅
- Maintainable codebase ✅
- Observable system ✅
- Privacy-compliant ✅

---

**Document Version:** 1.0
**Last Updated:** 2025-10-11
**Status:** Ready for Review
**Next Review:** After Phase 1 completion

**Contributors:**

- Myriad Architecture Team
- Cognitive Systems Research Group

**Approval Required From:**

- Technical Lead (Architecture)
- Product Manager (Features)
- Security Officer (Privacy/Compliance)
- Infrastructure Lead (Operations)

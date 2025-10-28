# Implementation Plan - Sprint 5: Context Integration & Memory System

**Sprint 5 of 7** | [← Previous Sprint](implementation-sprint-4.md) | [Next Sprint →](implementation-sprint-6.md)

This document covers Sprint 5 of the Myriad-Mind implementation plan, focusing on context understanding testing and tiered memory architecture (Weeks 13-18).

[← Back to Implementation Overview](../INDEX.md#implementation) | [View All Sprints](../INDEX.md#implementation)

---

## Sprint 5: Context Testing & Tiered Memory (Weeks 13-18)

**Goal:** Validate context understanding and implement STM/MTM/LTM memory architecture.

**Target Outcome:** Robust multi-turn conversations with human-like memory management across short, medium, and long-term storage.

---

### Phase 4.3: Integration Testing for Context (Week 13-15)

**Create comprehensive tests for context understanding**

#### Implementation Steps

**4.3.1 Create Context Understanding Test Suite (Day 1-3)**

Create new file: `tests/test_context_understanding.py`

```python
"""
Comprehensive test suite for context understanding and multi-turn conversations.
"""

import pytest
import time
from src.myriad.services.context.session_manager import SessionManager, ConversationTurn
from src.myriad.services.context.reference_resolver import ReferenceResolver

@pytest.fixture
def session_manager():
    """Create session manager for testing"""
    import redis
    redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
    return SessionManager(redis_client)

@pytest.fixture
def reference_resolver():
    """Create reference resolver for testing"""
    return ReferenceResolver()

def test_multi_turn_conversation(client, session_manager):
    """Test multi-turn conversation with references"""
    
    # Turn 1: Ask about lightbulb
    response1 = client.post('/process', json={
        'query': 'What is a lightbulb?',
        'tasks': [{'task_id': 1, 'concept': 'lightbulb', 'intent': 'define'}]
    })
    
    assert response1.status_code == 200
    session_id = response1.json['session_id']
    assert session_id is not None
    
    # Turn 2: Ask about "it" (should resolve to lightbulb)
    response2 = client.post('/process', json={
        'session_id': session_id,
        'query': 'Who invented it?',
        'tasks': []  # System should infer from context
    })
    
    # Verify it resolved the reference
    assert response2.status_code == 200
    assert 'lightbulb' in str(response2.json).lower() or 'edison' in str(response2.json).lower()
    
    # Turn 3: Ask about "the previous one"
    response3 = client.post('/process', json={
        'session_id': session_id,
        'query': 'Tell me more about the previous one',
        'tasks': []
    })
    
    assert response3.status_code == 200
    assert 'context' in response3.json
    assert response3.json['context']['turn_number'] == 3

def test_reference_resolution_accuracy(reference_resolver, session_manager):
    """Test accuracy of reference resolution"""
    
    # Create session with history
    session = session_manager.create_session('test_user')
    
    # Add a turn discussing "lightbulb"
    turn1 = ConversationTurn(
        turn_id='1',
        timestamp=time.time(),
        user_query='What is a lightbulb?',
        system_response='A lightbulb is an electric light source.',
        concepts_discussed=['lightbulb'],
        agents_used=[],
        entities_mentioned={}
    )
    session.add_turn(turn1)
    
    # Test pronoun resolution
    test_cases = [
        ('Tell me more about it', 'lightbulb'),
        ('What about that?', 'lightbulb'),
        ('How does this work?', 'lightbulb'),
        ('Explain the previous one', 'lightbulb')
    ]
    
    for query, expected_concept in test_cases:
        resolved = reference_resolver.resolve_query(query, session)
        assert expected_concept.lower() in resolved.lower(), \
            f"Failed to resolve '{query}' to '{expected_concept}'"

def test_session_persistence(session_manager):
    """Test session persistence across requests"""
    
    # Create session
    session = session_manager.create_session('user123')
    session_id = session.session_id
    
    # Add turns
    for i in range(5):
        turn = ConversationTurn(
            turn_id=str(i),
            timestamp=time.time(),
            user_query=f'Query {i}',
            system_response=f'Response {i}',
            concepts_discussed=[f'concept_{i}'],
            agents_used=[],
            entities_mentioned={}
        )
        session_manager.add_turn_to_session(session_id, turn)
    
    # Retrieve session
    retrieved_session = session_manager.get_session(session_id)
    
    assert retrieved_session is not None
    assert len(retrieved_session.turns) == 5
    assert retrieved_session.user_id == 'user123'
    assert len(retrieved_session.active_concepts) == 5

def test_session_expiration(session_manager):
    """Test session expiration after TTL"""
    
    # Create session with short TTL
    session_manager.session_ttl = 2  # 2 seconds
    session = session_manager.create_session('temp_user')
    session_id = session.session_id
    
    # Verify it exists
    assert session_manager.get_session(session_id) is not None
    
    # Wait for expiration
    time.sleep(3)
    
    # Should be gone now
    assert session_manager.get_session(session_id) is None

def test_context_hints_extraction(client):
    """Test context hints are correctly extracted"""
    
    from src.myriad.services.processing.input_processor.input_processor import EnhancedInputProcessor
    
    processor = EnhancedInputProcessor()
    
    # Test continuation request
    hints1 = processor.extract_context_hints("Tell me more about lightbulbs", None)
    assert hints1['continuation_request'] == True
    assert hints1['needs_full_history'] == True
    
    # Test reference to previous
    hints2 = processor.extract_context_hints("What about that invention?", None)
    assert hints2['needs_previous_concept'] == True
    
    # Test new topic (no references)
    hints3 = processor.extract_context_hints("What is a computer?", None)
    assert hints3['needs_previous_concept'] == False

def test_entity_extraction():
    """Test entity extraction from queries"""
    
    from src.myriad.services.processing.input_processor.input_processor import EnhancedInputProcessor
    
    processor = EnhancedInputProcessor()
    
    # Test with entities
    result = processor.process_input("Thomas Edison invented the lightbulb in 1879")
    
    assert 'entities' in result
    assert len(result['concepts']) > 0
    
    # Should extract person and date entities
    entities = result['entities']
    assert any(label in ['PERSON', 'DATE', 'ORG'] for label in entities.keys())

@pytest.mark.integration
def test_full_conversation_flow(client):
    """Test complete conversation flow with multiple turns"""
    
    conversation = [
        ("What is artificial intelligence?", "artificial intelligence"),
        ("Who invented it?", "artificial intelligence"),  # Reference resolution
        ("Tell me more", "artificial intelligence"),      # Continuation
        ("What about machine learning?", "machine learning"),  # Topic shift
        ("How does that relate to AI?", "machine learning")    # Reference + relation
    ]
    
    session_id = None
    
    for i, (query, expected_concept) in enumerate(conversation):
        payload = {'query': query}
        if session_id:
            payload['session_id'] = session_id
        
        response = client.post('/process', json=payload)
        assert response.status_code == 200
        
        if not session_id:
            session_id = response.json['session_id']
        
        # Verify context is maintained
        assert 'context' in response.json
        assert response.json['context']['turn_number'] == i + 1

def test_reference_resolution_edge_cases(reference_resolver, session_manager):
    """Test edge cases in reference resolution"""
    
    # Empty session
    empty_session = session_manager.create_session('test')
    assert reference_resolver.resolve_query("What about it?", empty_session) == "What about it?"
    
    # Session with no concepts
    session = session_manager.create_session('test2')
    turn = ConversationTurn(
        turn_id='1',
        timestamp=time.time(),
        user_query='Hello',
        system_response='Hi',
        concepts_discussed=[],
        agents_used=[],
        entities_mentioned={}
    )
    session.add_turn(turn)
    
    resolved = reference_resolver.resolve_query("Tell me about it", session)
    # Should handle gracefully, returning original or None
    assert resolved is not None
```

**4.3.2 Performance Testing (Day 4-5)**

Create performance tests for context operations:

```python
def test_session_retrieval_performance(session_manager):
    """Test session retrieval is fast enough"""
    
    # Create session with many turns
    session = session_manager.create_session('perf_test')
    
    for i in range(100):
        turn = ConversationTurn(
            turn_id=str(i),
            timestamp=time.time(),
            user_query=f'Query {i}',
            system_response=f'Response {i}',
            concepts_discussed=[f'concept_{i}'],
            agents_used=[],
            entities_mentioned={}
        )
        session_manager.add_turn_to_session(session.session_id, turn)
    
    # Test retrieval speed
    start = time.time()
    retrieved = session_manager.get_session(session.session_id)
    elapsed = time.time() - start
    
    assert elapsed < 0.1, f"Session retrieval too slow: {elapsed}s"
    assert len(retrieved.turns) == 100

def test_reference_resolution_performance(reference_resolver):
    """Test reference resolution speed"""
    
    import statistics
    
    session = ConversationSession(
        session_id='test',
        user_id='test',
        started_at=time.time(),
        last_activity=time.time()
    )
    
    # Add history
    for i in range(10):
        turn = ConversationTurn(
            turn_id=str(i),
            timestamp=time.time(),
            user_query=f'Query {i}',
            system_response=f'Response {i}',
            concepts_discussed=[f'concept_{i}'],
            agents_used=[],
            entities_mentioned={}
        )
        session.add_turn(turn)
    
    # Test resolution speed
    times = []
    queries = [
        "Tell me about it",
        "What about that?",
        "Explain the previous one",
        "Continue with this"
    ]
    
    for _ in range(100):
        for query in queries:
            start = time.time()
            reference_resolver.resolve_query(query, session)
            times.append(time.time() - start)
    
    avg_time = statistics.mean(times)
    assert avg_time < 0.01, f"Reference resolution too slow: {avg_time}s average"
```

**Success Criteria:**

- ✅ All context understanding tests pass
- ✅ Reference resolution >90% accurate
- ✅ Session management stable under load
- ✅ No memory leaks in long conversations
- ✅ Performance meets targets (<100ms for context operations)

---

## SPRINT 6: Tiered Memory System (Weeks 16-18)

**Goal:** Implement STM/MTM/LTM architecture for efficient information management.

**Target Outcome:** System manages information like human brain with working memory, session memory, and long-term storage.

### Phase 6.1: Memory Architecture Design (Week 16)

#### Memory Tier Specifications

**Short-Term Memory (STM)**

- **Capacity:** 7±2 items (Miller's Law)
- **Duration:** Active query duration only
- **Storage:** In-memory Python data structures
- **Purpose:** Working memory for current task
- **Implementation:** Python dict/list in orchestrator

**Medium-Term Memory (MTM)**

- **Capacity:** Unlimited within session
- **Duration:** 30-60 minutes (configurable TTL)
- **Storage:** Redis with TTL
- **Purpose:** Conversation history, recent context
- **Implementation:** Redis with session keys (already started in Sprint 4-5)

**Long-Term Memory (LTM)**

- **Capacity:** Unlimited
- **Duration:** Permanent (with decay)
- **Storage:** Neo4j graph database
- **Purpose:** Persistent knowledge, learned concepts
- **Implementation:** Existing graph database (already operational)

#### Implementation Steps

**6.1.1 Create Memory Manager (Day 1-3)**

Create new file: `src/myriad/core/memory/memory_manager.py`

```python
"""
Tiered Memory System for Myriad Cognitive Architecture
Implements STM/MTM/LTM hierarchy similar to human memory.
"""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from collections import deque
import time
import redis
import json

@dataclass
class MemoryItem:
    """Single item in memory"""
    key: str
    value: Any
    timestamp: float
    access_count: int = 0
    importance: float = 0.5  # 0.0-1.0
    tier: str = "STM"  # STM, MTM, or LTM

class ShortTermMemory:
    """Working memory with limited capacity"""
    
    def __init__(self, capacity: int = 7):
        self.capacity = capacity
        self.items: deque = deque(maxlen=capacity)
        self.item_map: Dict[str, MemoryItem] = {}
    
    def add(self, key: str, value: Any, importance: float = 0.5):
        """Add item to STM, evicting oldest if full"""
        
        # If already exists, update
        if key in self.item_map:
            item = self.item_map[key]
            item.value = value
            item.timestamp = time.time()
            item.access_count += 1
            item.importance = max(item.importance, importance)
            return
        
        # Create new item
        item = MemoryItem(
            key=key,
            value=value,
            timestamp=time.time(),
            importance=importance,
            tier="STM"
        )
        
        # If full, evict oldest low-importance item
        if len(self.items) >= self.capacity:
            evicted = self.items.popleft()
            del self.item_map[evicted.key]
        
        self.items.append(item)
        self.item_map[key] = item
    
    def get(self, key: str) -> Optional[Any]:
        """Retrieve from STM"""
        item = self.item_map.get(key)
        if item:
            item.access_count += 1
            return item.value
        return None
    
    def get_all(self) -> List[MemoryItem]:
        """Get all items in STM"""
        return list(self.items)
    
    def clear(self):
        """Clear STM"""
        self.items.clear()
        self.item_map.clear()

class MediumTermMemory:
    """Session-based memory with Redis backend"""
    
    def __init__(self, redis_client, ttl: int = 1800):
        self.redis = redis_client
        self.ttl = ttl  # 30 minutes default
        self.prefix = "mtm:"
    
    def add(self, session_id: str, key: str, value: Any, importance: float = 0.5):
        """Add item to MTM"""
        item = MemoryItem(
            key=key,
            value=value,
            timestamp=time.time(),
            importance=importance,
            tier="MTM"
        )
        
        redis_key = f"{self.prefix}{session_id}:{key}"
        self.redis.setex(
            redis_key,
            self.ttl,
            json.dumps({
                'value': value,
                'timestamp': item.timestamp,
                'importance': importance
            })
        )
    
    def get(self, session_id: str, key: str) -> Optional[Any]:
        """Retrieve from MTM"""
        redis_key = f"{self.prefix}{session_id}:{key}"
        data = self.redis.get(redis_key)
        
        if data:
            item_dict = json.loads(data)
            return item_dict['value']
        return None
    
    def get_session_items(self, session_id: str) -> List[Dict]:
        """Get all items for a session"""
        pattern = f"{self.prefix}{session_id}:*"
        keys = self.redis.keys(pattern)
        
        items = []
        for key in keys:
            data = self.redis.get(key)
            if data:
                items.append(json.loads(data))
        
        return items
    
    def extend_ttl(self, session_id: str, key: str):
        """Extend TTL for frequently accessed items"""
        redis_key = f"{self.prefix}{session_id}:{key}"
        self.redis.expire(redis_key, self.ttl)

class LongTermMemory:
    """Persistent memory via Neo4j graph"""
    
    def __init__(self, graphdb_url: str):
        self.graphdb_url = graphdb_url
    
    def consolidate(self, item: MemoryItem):
        """Move important item from MTM to LTM"""
        
        # Items with high importance or access count get consolidated
        if item.importance > 0.7 or item.access_count > 3:
            # Store in graph database
            # This would call GraphDB Manager to create/update nodes
            pass
    
    def retrieve(self, key: str) -> Optional[Any]:
        """Retrieve from LTM (graph database)"""
        # Query graph database
        # Already implemented via existing graph queries
        pass

class MemoryManager:
    """Unified memory manager coordinating all tiers"""
    
    def __init__(self, redis_client, graphdb_url: str):
        self.stm = ShortTermMemory(capacity=7)
        self.mtm = MediumTermMemory(redis_client, ttl=1800)
        self.ltm = LongTermMemory(graphdb_url)
        
        # Consolidation thread
        self.consolidation_enabled = True
    
    def remember(self, session_id: str, key: str, value: Any, 
                importance: float = 0.5, tier: str = "auto"):
        """Store in appropriate memory tier"""
        
        if tier == "auto":
            if importance > 0.8:
                tier = "MTM"  # High importance → session memory
            else:
                tier = "STM"  # Normal → working memory
        
        if tier == "STM":
            self.stm.add(key, value, importance)
        elif tier == "MTM":
            self.mtm.add(session_id, key, value, importance)
            # Also keep in STM for quick access
            self.stm.add(key, value, importance)
    
    def recall(self, session_id: str, key: str) -> Optional[Any]:
        """Recall from memory (tries STM → MTM → LTM)"""
        
        # Try STM first (fastest)
        result = self.stm.get(key)
        if result is not None:
            return result
        
        # Try MTM
        result = self.mtm.get(session_id, key)
        if result is not None:
            # Promote to STM for quick access
            self.stm.add(key, result)
            return result
        
        # Try LTM
        result = self.ltm.retrieve(key)
        if result is not None:
            # Promote to STM
            self.stm.add(key, result)
            return result
        
        return None
    
    def consolidate_session(self, session_id: str):
        """Consolidate important MTM items to LTM"""
        items = self.mtm.get_session_items(session_id)
        
        for item_dict in items:
            if item_dict.get('importance', 0) > 0.7:
                # Create memory item
                item = MemoryItem(
                    key="",  # Would be extracted from item_dict
                    value=item_dict['value'],
                    timestamp=item_dict['timestamp'],
                    importance=item_dict['importance'],
                    tier="MTM"
                )
                
                # Consolidate to LTM
                self.ltm.consolidate(item)
```

**Success Criteria:**

- ✅ STM maintains 7±2 most recent items
- ✅ MTM persists session data in Redis
- ✅ LTM integration with existing graph
- ✅ Memory consolidation working

---

### Phase 6.2: Integration with Existing Systems (Week 17-18)

**Integrate memory manager with orchestrator, session manager, and graph database**

#### Implementation Steps

**6.2.1 Integrate with Orchestrator (Day 1-3)**

File: [`src/myriad/services/orchestrator/app.py`](../../src/myriad/services/orchestrator/app.py:1)

```python
from core.memory.memory_manager import MemoryManager

# Initialize memory manager
memory_manager = MemoryManager(
    redis_client=redis_client,
    graphdb_url=GRAPHDB_MANAGER_URL
)

@app.route('/process', methods=['POST'])
def process():
    """Process with tiered memory"""
    data = request.get_json()
    session_id = data.get('session_id')
    
    # Store current query in STM
    memory_manager.remember(
        session_id or 'default',
        'current_query',
        data.get('query'),
        importance=0.5,
        tier='STM'
    )
    
    # Process tasks
    results = process_tasks(data.get('tasks', []))
    
    # Store important results in MTM
    for task_id, result in results.items():
        if result.get('status') == 'success':
            memory_manager.remember(
                session_id or 'default',
                f'result_{task_id}',
                result,
                importance=0.7,
                tier='MTM'
            )
    
    return jsonify(results)
```

**6.2.2 Add Memory Consolidation (Day 4-5)**

Create background task for memory consolidation:

```python
import threading

def consolidation_loop(memory_manager, interval=300):
    """Background loop for memory consolidation"""
    while True:
        try:
            # Get active sessions from Redis
            pattern = "session:*"
            session_keys = redis_client.keys(pattern)
            
            for key in session_keys:
                session_id = key.split(':')[1]
                
                # Consolidate session to LTM
                memory_manager.consolidate_session(session_id)
                
            time.sleep(interval)
        except Exception as e:
            logger.error(f"Consolidation error: {e}")
            time.sleep(interval)

# Start consolidation thread
consolidation_thread = threading.Thread(
    target=consolidation_loop,
    args=(memory_manager, 300),
    daemon=True
)
consolidation_thread.start()
```

**6.2.3 Testing Memory System (Day 6-7)**

Create comprehensive tests:

```python
def test_stm_capacity_limit():
    """Test STM respects capacity limit"""
    stm = ShortTermMemory(capacity=7)
    
    # Add 10 items
    for i in range(10):
        stm.add(f'item_{i}', f'value_{i}')
    
    # Should only have 7
    assert len(stm.get_all()) == 7
    
    # First 3 should be evicted
    assert stm.get('item_0') is None
    assert stm.get('item_9') is not None

def test_memory_tier_cascade():
    """Test memory retrieval cascades through tiers"""
    memory_mgr = MemoryManager(redis_client, graphdb_url)
    
    # Store in MTM
    memory_mgr.remember('session1', 'test_key', 'test_value', tier='MTM')
    
    # Clear STM
    memory_mgr.stm.clear()
    
    # Recall should find in MTM and promote to STM
    value = memory_mgr.recall('session1', 'test_key')
    assert value == 'test_value'
    assert memory_mgr.stm.get('test_key') == 'test_value'

def test_memory_consolidation():
    """Test important memories consolidate to LTM"""
    memory_mgr = MemoryManager(redis_client, graphdb_url)
    
    # Add high-importance item to MTM
    memory_mgr.remember(
        'session1',
        'important_concept',
        {'name': 'AI', 'type': 'concept'},
        importance=0.9,
        tier='MTM'
    )
    
    # Trigger consolidation
    memory_mgr.consolidate_session('session1')
    
    # Should be available in LTM (verify via graph query)
```

**Success Criteria:**

- ✅ Orchestrator uses STM for active queries
- ✅ Session manager uses MTM for conversations
- ✅ Important knowledge consolidated to LTM
- ✅ Memory retrieval follows STM→MTM→LTM cascade
- ✅ All memory tests passing

---

## Sprint 5 Summary

### Completed Deliverables

**Week 13-15: Context Testing**

- ✅ Comprehensive context understanding test suite
- ✅ Reference resolution validation (>90% accuracy)
- ✅ Performance testing for context operations
- ✅ Edge case handling

**Week 16: Memory Architecture**

- ✅ Tiered memory system (STM/MTM/LTM)
- ✅ Memory capacity management
- ✅ Automatic memory consolidation
- ✅ Memory tier specifications

**Week 17-18: Memory Integration**

- ✅ Integration with orchestrator
- ✅ Integration with session manager
- ✅ Background consolidation loop
- ✅ Memory system testing

### Key Achievements

1. **Validated Context Understanding**: Comprehensive testing ensures reliability
2. **Human-Like Memory**: Three-tier system mimics human cognitive architecture
3. **Efficient Storage**: Right data in right tier (fast vs persistent)
4. **Automatic Management**: Consolidation and eviction without manual intervention

### Memory System Characteristics

| Tier | Capacity | Speed | Duration | Use Case |
|------|----------|-------|----------|----------|
| STM | 7±2 items | <1ms | Query only | Active processing |
| MTM | Unlimited | <10ms | 30-60 min | Session context |
| LTM | Unlimited | <100ms | Permanent | Knowledge base |

### Next Steps

Sprint 6 will implement multi-modal learning, enabling the system to understand and learn from images, audio, and other sensory data beyond just text.

---

## Continue Reading

**Next:** [Sprint 6: Multi-Modal Learning](implementation-sprint-6.md) - Image and audio processing, multi-modal embeddings (Weeks 19-21)

**Related Documentation:**

- [Project Index](../INDEX.md)
- [Architecture Overview](../ARCHITECTURE.md)
- [Context Understanding](../CONTEXT_UNDERSTANDING_ARCHITECTURE.md)
- [Graph Schema](../GRAPH_SCHEMA.md)

[← Previous Sprint](implementation-sprint-4.md) | [↑ Back to Index](../INDEX.md) | [Next Sprint →](implementation-sprint-6.md)

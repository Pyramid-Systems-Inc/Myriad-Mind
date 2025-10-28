# Implementation Plan - Sprint 4: Context Understanding - Part 1

**Sprint 4 of 7** | [← Previous Sprint](implementation-sprint-3.md) | [Next Sprint →](implementation-sprint-5.md)

This document covers Sprint 4 of the Myriad-Mind implementation plan, focusing on conversation session management and reference resolution (Weeks 10-12).

[← Back to Implementation Overview](../INDEX.md#implementation) | [View All Sprints](../INDEX.md#implementation)

---

## SPRINT 4-5: Context Understanding (Weeks 10-15)

**Goal:** Enable multi-turn conversations, reference resolution, and contextual memory.

**Target Outcome:** System can handle "it", "that", "the previous one" in conversations like humans.

---

## Sprint 4 Focus: Session Management & Reference Resolution (Weeks 10-12)

### Phase 4.1: Conversation Session Manager (Week 10)

#### Current Problem

- No conversation history tracking
- Each query processed independently
- Cannot handle references like "tell me more" or "what about it?"

#### Implementation Steps

**4.1.1 Create Session Manager Service (Day 1-3)**

Create new file: `src/myriad/services/context/session_manager.py`

```python
"""
Session Manager for Multi-Turn Conversations
Tracks conversation history, resolves references, maintains context.
"""

import time
import uuid
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
import redis
import json

@dataclass
class ConversationTurn:
    """Single turn in a conversation"""
    turn_id: str
    timestamp: float
    user_query: str
    system_response: str
    concepts_discussed: List[str]
    agents_used: List[str]
    entities_mentioned: Dict[str, str]  # {"it": "lightbulb", "that": "invention"}

@dataclass
class ConversationSession:
    """Complete conversation session"""
    session_id: str
    user_id: str
    started_at: float
    last_activity: float
    turns: List[ConversationTurn] = field(default_factory=list)
    active_concepts: List[str] = field(default_factory=list)
    context_summary: str = ""
    
    def add_turn(self, turn: ConversationTurn):
        """Add a conversation turn"""
        self.turns.append(turn)
        self.last_activity = time.time()
        
        # Update active concepts
        for concept in turn.concepts_discussed:
            if concept not in self.active_concepts:
                self.active_concepts.append(concept)
    
    def get_recent_context(self, num_turns: int = 3) -> str:
        """Get context from recent turns"""
        recent = self.turns[-num_turns:]
        context_parts = []
        
        for turn in recent:
            context_parts.append(f"User: {turn.user_query}")
            context_parts.append(f"System: {turn.system_response}")
        
        return "\n".join(context_parts)
    
    def resolve_reference(self, reference: str) -> Optional[str]:
        """Resolve pronouns and references"""
        if not self.turns:
            return None
        
        last_turn = self.turns[-1]
        
        # Simple reference resolution
        reference_map = {
            "it": last_turn.concepts_discussed[0] if last_turn.concepts_discussed else None,
            "that": last_turn.concepts_discussed[0] if last_turn.concepts_discussed else None,
            "this": last_turn.concepts_discussed[0] if last_turn.concepts_discussed else None,
            "the previous one": last_turn.concepts_discussed[0] if last_turn.concepts_discussed else None,
        }
        
        # Check entity mentions from last turn
        if reference.lower() in last_turn.entities_mentioned:
            return last_turn.entities_mentioned[reference.lower()]
        
        return reference_map.get(reference.lower())

class SessionManager:
    """Manages conversation sessions"""
    
    def __init__(self, redis_client):
        self.redis = redis_client
        self.session_ttl = 3600  # 1 hour
    
    def create_session(self, user_id: str) -> ConversationSession:
        """Create a new conversation session"""
        session = ConversationSession(
            session_id=str(uuid.uuid4()),
            user_id=user_id,
            started_at=time.time(),
            last_activity=time.time()
        )
        
        self._save_session(session)
        return session
    
    def get_session(self, session_id: str) -> Optional[ConversationSession]:
        """Retrieve a session from storage"""
        key = f"session:{session_id}"
        data = self.redis.get(key)
        
        if not data:
            return None
        
        session_dict = json.loads(data)
        
        # Reconstruct session object
        session = ConversationSession(
            session_id=session_dict['session_id'],
            user_id=session_dict['user_id'],
            started_at=session_dict['started_at'],
            last_activity=session_dict['last_activity'],
            active_concepts=session_dict.get('active_concepts', []),
            context_summary=session_dict.get('context_summary', '')
        )
        
        # Reconstruct turns
        for turn_dict in session_dict.get('turns', []):
            turn = ConversationTurn(
                turn_id=turn_dict['turn_id'],
                timestamp=turn_dict['timestamp'],
                user_query=turn_dict['user_query'],
                system_response=turn_dict['system_response'],
                concepts_discussed=turn_dict.get('concepts_discussed', []),
                agents_used=turn_dict.get('agents_used', []),
                entities_mentioned=turn_dict.get('entities_mentioned', {})
            )
            session.turns.append(turn)
        
        return session
    
    def _save_session(self, session: ConversationSession):
        """Save session to Redis"""
        key = f"session:{session.session_id}"
        
        # Convert to dict
        session_dict = {
            'session_id': session.session_id,
            'user_id': session.user_id,
            'started_at': session.started_at,
            'last_activity': session.last_activity,
            'active_concepts': session.active_concepts,
            'context_summary': session.context_summary,
            'turns': [
                {
                    'turn_id': turn.turn_id,
                    'timestamp': turn.timestamp,
                    'user_query': turn.user_query,
                    'system_response': turn.system_response,
                    'concepts_discussed': turn.concepts_discussed,
                    'agents_used': turn.agents_used,
                    'entities_mentioned': turn.entities_mentioned
                }
                for turn in session.turns
            ]
        }
        
        self.redis.setex(
            key,
            self.session_ttl,
            json.dumps(session_dict)
        )
    
    def add_turn_to_session(self, session_id: str, turn: ConversationTurn):
        """Add a turn to existing session"""
        session = self.get_session(session_id)
        if session:
            session.add_turn(turn)
            self._save_session(session)
```

**4.1.2 Create Reference Resolver (Day 3-5)**

Create new file: `src/myriad/services/context/reference_resolver.py`

```python
"""
Reference Resolution for Context Understanding
Resolves pronouns, anaphora, and contextual references.
"""

import re
from typing import Dict, List, Optional, Tuple

class ReferenceResolver:
    """Resolves references in user queries"""
    
    # Common reference patterns
    REFERENCE_PATTERNS = {
        'pronoun': [
            r'\b(it|its|itself)\b',
            r'\b(that|this|these|those)\b',
            r'\b(he|she|him|her|his|hers|they|them|their)\b'
        ],
        'demonstrative': [
            r'\b(the (same|previous|last|first) (one|thing|concept|item))\b',
            r'\b(the one (mentioned|discussed|above))\b'
        ],
        'contextual': [
            r'\b(tell me more|explain further|elaborate|continue)\b',
            r'\b(what about|how about)\b'
        ]
    }
    
    def __init__(self):
        self.compiled_patterns = {
            category: [re.compile(pattern, re.IGNORECASE) 
                      for pattern in patterns]
            for category, patterns in self.REFERENCE_PATTERNS.items()
        }
    
    def contains_reference(self, query: str) -> bool:
        """Check if query contains any references"""
        for category, patterns in self.compiled_patterns.items():
            for pattern in patterns:
                if pattern.search(query):
                    return True
        return False
    
    def extract_references(self, query: str) -> List[Tuple[str, str]]:
        """Extract all references and their types"""
        references = []
        
        for category, patterns in self.compiled_patterns.items():
            for pattern in patterns:
                matches = pattern.finditer(query)
                for match in matches:
                    references.append((match.group(0), category))
        
        return references
    
    def resolve_query(self, query: str, session: 'ConversationSession') -> str:
        """Resolve references in query using session context"""
        if not self.contains_reference(query):
            return query
        
        resolved_query = query
        references = self.extract_references(query)
        
        for ref_text, ref_type in references:
            # Try to resolve the reference
            resolution = session.resolve_reference(ref_text)
            
            if resolution:
                # Replace reference with actual concept
                resolved_query = resolved_query.replace(ref_text, resolution)
        
        return resolved_query
    
    def extract_concepts_from_response(self, response: str) -> List[str]:
        """Extract concepts mentioned in system response"""
        # Simple extraction - look for capitalized words and known patterns
        concepts = []
        
        # Pattern for quoted concepts
        quoted = re.findall(r'"([^"]+)"', response)
        concepts.extend(quoted)
        
        # Pattern for "about X" or "regarding X"
        about_pattern = re.findall(r'\b(?:about|regarding|concerning)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)', response)
        concepts.extend(about_pattern)
        
        return list(set(concepts))  # Remove duplicates
```

**4.1.3 Integrate with Orchestrator (Day 6-7)**

File: [`src/myriad/services/orchestrator/app.py`](../../src/myriad/services/orchestrator/app.py:1)

```python
from context.session_manager import SessionManager, ConversationTurn
from context.reference_resolver import ReferenceResolver
import redis

# Initialize context management
redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)
session_manager = SessionManager(redis_client)
reference_resolver = ReferenceResolver()

@app.route('/process', methods=['POST'])
def process():
    """Process query with context awareness"""
    data = request.get_json()
    
    # Get or create session
    session_id = data.get('session_id')
    user_id = data.get('user_id', 'anonymous')
    
    if not session_id:
        session = session_manager.create_session(user_id)
        session_id = session.session_id
    else:
        session = session_manager.get_session(session_id)
        if not session:
            session = session_manager.create_session(user_id)
            session_id = session.session_id
    
    # Get query
    query = data.get('query', '')
    
    # Resolve references if present
    if reference_resolver.contains_reference(query):
        resolved_query = reference_resolver.resolve_query(query, session)
        print(f"🔍 Reference resolution: '{query}' → '{resolved_query}'")
        query = resolved_query
    
    # Process query (existing logic)
    tasks = data.get('tasks', [])
    results = process_tasks(tasks)
    
    # Extract concepts from results
    concepts_discussed = []
    for result in results.values():
        if 'concept' in result:
            concepts_discussed.append(result['concept'])
    
    # Create conversation turn
    turn = ConversationTurn(
        turn_id=str(uuid.uuid4()),
        timestamp=time.time(),
        user_query=query,
        system_response=str(results),
        concepts_discussed=concepts_discussed,
        agents_used=[],  # Would extract from results
        entities_mentioned={}
    )
    
    # Add to session
    session_manager.add_turn_to_session(session_id, turn)
    
    # Return results with session info
    return jsonify({
        "session_id": session_id,
        "results": results,
        "context": {
            "turn_number": len(session.turns),
            "active_concepts": session.active_concepts[:5]  # Top 5
        }
    })
```

**Success Criteria:**

- ✅ System tracks conversation history
- ✅ Resolves "it", "that", "the previous one" correctly
- ✅ Maintains context across multiple turns
- ✅ Session expires after inactivity

---

### Phase 4.2: Enhanced Input Processing (Week 11-12)

**Upgrade Input Processor to extract entities and track references**

#### Implementation Steps

**4.2.1 Add Entity Extraction (Day 1-3)**

File: [`src/myriad/services/processing/input_processor/input_processor.py`](../../src/myriad/services/processing/input_processor/input_processor.py:1)

Add entity extraction capabilities:

```python
import spacy

class EnhancedInputProcessor:
    """Input processor with entity extraction and reference detection"""
    
    def __init__(self):
        # Load spaCy model for NLP
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except:
            print("⚠️  spaCy model not found, downloading...")
            os.system("python -m spacy download en_core_web_sm")
            self.nlp = spacy.load("en_core_web_sm")
        
        self.reference_resolver = ReferenceResolver()
    
    def process_input(self, query: str, session_context: Optional[dict] = None) -> dict:
        """Process input with entity extraction and reference detection"""
        
        # Parse query with spaCy
        doc = self.nlp(query)
        
        # Extract entities
        entities = {}
        for ent in doc.ents:
            entities[ent.label_] = ent.text
        
        # Detect references
        has_references = self.reference_resolver.contains_reference(query)
        references = self.reference_resolver.extract_references(query) if has_references else []
        
        # Extract concepts (nouns and noun phrases)
        concepts = []
        for chunk in doc.noun_chunks:
            concepts.append(chunk.text.lower())
        
        return {
            "original_query": query,
            "entities": entities,
            "has_references": has_references,
            "references": references,
            "concepts": concepts,
            "requires_context": has_references,
            "processed_at": time.time()
        }
```

**4.2.2 Add Context Hints (Day 4-5)**

Provide context hints to orchestrator:

```python
def extract_context_hints(self, query: str, session: Optional['ConversationSession']) -> dict:
    """Extract hints about what context is needed"""
    
    hints = {
        "needs_previous_concept": False,
        "needs_full_history": False,
        "continuation_request": False,
        "topic_shift": False
    }
    
    # Check for continuation requests
    continuation_patterns = [
        "tell me more", "continue", "elaborate", "explain further",
        "what else", "more details", "go on"
    ]
    
    query_lower = query.lower()
    if any(pattern in query_lower for pattern in continuation_patterns):
        hints["continuation_request"] = True
        hints["needs_full_history"] = True
    
    # Check for references to previous concept
    if self.reference_resolver.contains_reference(query):
        hints["needs_previous_concept"] = True
    
    # Check for topic shift (new concepts introduced)
    if session and session.active_concepts:
        doc = self.nlp(query)
        query_concepts = [chunk.text.lower() for chunk in doc.noun_chunks]
        
        overlap = set(query_concepts) & set(session.active_concepts)
        if not overlap and query_concepts:
            hints["topic_shift"] = True
    
    return hints
```

**4.2.3 Integration with Orchestrator (Day 6-7)**

Update orchestrator to use enhanced input processing:

```python
from processing.input_processor.input_processor import EnhancedInputProcessor

input_processor = EnhancedInputProcessor()

@app.route('/process', methods=['POST'])
def process():
    """Process with enhanced input understanding"""
    data = request.get_json()
    query = data.get('query', '')
    
    # Get session
    session_id = data.get('session_id')
    session = session_manager.get_session(session_id) if session_id else None
    
    # Process input
    processed_input = input_processor.process_input(query, session)
    
    # Get context hints
    context_hints = input_processor.extract_context_hints(query, session)
    
    # Log processing
    print(f"📝 Input Processing:")
    print(f"   Entities: {processed_input['entities']}")
    print(f"   References: {processed_input['has_references']}")
    print(f"   Context hints: {context_hints}")
    
    # Continue with existing processing...
```

**Success Criteria:**

- ✅ Input processor detects references
- ✅ Extracts entities for session tracking
- ✅ Provides context hints to orchestrator
- ✅ NLP-based entity recognition working

---

## Sprint 4 Summary

### Completed Deliverables

**Week 10: Session Management**

- ✅ Conversation session manager with Redis storage
- ✅ Reference resolver for pronouns and contextual references
- ✅ Session tracking with automatic expiration
- ✅ Multi-turn conversation support

**Week 11-12: Enhanced Input Processing**

- ✅ Entity extraction using spaCy
- ✅ Reference detection in user queries
- ✅ Context hint generation
- ✅ Integration with orchestrator

### Key Achievements

1. **Conversation Memory**: System now remembers conversation history
2. **Reference Resolution**: Can resolve "it", "that", "previous one" accurately
3. **Context Awareness**: Understands when context is needed
4. **Entity Tracking**: Extracts and tracks important entities

### Example Use Case

```
User: "What is a lightbulb?"
System: [Creates session, processes query, returns definition]

User: "Who invented it?"
System: [Resolves "it" → "lightbulb", queries for inventor]

User: "Tell me more about the previous one"
System: [Resolves "previous one" → "lightbulb", provides details]
```

### Next Steps

Sprint 5 will complete the context understanding implementation with integration testing and begin the tiered memory system (STM/MTM/LTM), bringing us closer to human-like memory architecture.

---

## Continue Reading

**Next:** [Sprint 5: Context Integration & Memory System](implementation-sprint-5.md) - Testing context understanding and implementing tiered memory (Weeks 13-18)

**Related Documentation:**

- [Project Index](../INDEX.md)
- [Architecture Overview](../ARCHITECTURE.md)
- [Context Understanding](../CONTEXT_UNDERSTANDING_ARCHITECTURE.md)
- [Testing Guide](../TESTING_GUIDE.md)

[← Previous Sprint](implementation-sprint-3.md) | [↑ Back to Index](../INDEX.md) | [Next Sprint →](implementation-sprint-5.md)

# Myriad-Mind Architecture: Microservices

**Architecture Documentation** | [Overview](architecture-overview.md) | [Graph Intelligence](architecture-graph-intelligence.md) | [Neurogenesis](architecture-neurogenesis.md)

Comprehensive documentation of the microservices architecture, service catalog, communication patterns, and deployment infrastructure.

[← Back to Overview](architecture-overview.md) | [Graph Intelligence →](architecture-graph-intelligence.md)

---

## Table of Contents

- [Microservice Architecture Overview](#microservice-architecture-overview)
- [Service Catalog](#service-catalog)
- [Communication Patterns](#communication-patterns)
- [Service Discovery](#service-discovery)
- [Production Infrastructure](#production-infrastructure)
- [Deployment Architecture](#deployment-architecture)
- [API Contracts](#api-contracts)
- [Evolution Roadmap](#evolution-roadmap)

---

## Microservice Architecture Overview

### Design Philosophy

The Myriad system follows a **microservices architecture** where each service is:

- **Independently Deployable**: Can be updated without affecting other services
- **Single Responsibility**: Focused on one specific aspect of cognition
- **Technology Agnostic**: Services communicate via HTTP/JSON
- **Fault Tolerant**: Failure of one service doesn't cascade
- **Horizontally Scalable**: Can run multiple instances for load distribution

### Current Architecture State

**Status**: Transition from library-based to true microservices in progress

**Current Pattern**:

```
┌─────────────────────┐
│ Integration Tester  │
│   (Flask Service)   │ ← Exposed HTTP endpoint
│   Port: 5009        │
└──────────┬──────────┘
           │ imports
           ▼
  ┌────────────────────┐
  │   orchestrator.py  │ ← Pure Python library
  │  (Library Module)  │    No HTTP interface
  └────────────────────┘
```

**Target Pattern** (See [Sprint 1](../implementation/implementation-sprint-1.md)):

```
┌──────────────┐      ┌──────────────┐
│   Client     │─────▶│ Orchestrator │ ← Independent microservice
└──────────────┘      │  Port: 5010  │
                      └──────┬───────┘
                             │ HTTP calls
                             ▼
                      ┌──────────────┐
                      │   Agents     │
                      └──────────────┘
```

---

## Service Catalog

### Core Services

#### 1. Orchestrator Service

**Current Status**: Library embedded in Integration Tester  
**Target Status**: Standalone microservice (Sprint 1)

**Responsibilities**:

- Central task coordination and routing
- Agent discovery via graph traversal
- Neurogenesis pipeline coordination
- Hebbian weight updates after agent interactions
- Task dependency management

**Location**: [`src/myriad/services/orchestrator/`](../../src/myriad/services/orchestrator/)  
**Port**: 5010 (planned)  
**Dependencies**: GraphDB Manager, Redis, Dynamic Lifecycle Manager

**Key Endpoints** (Planned):

```python
GET  /health          # Service health check
GET  /metrics         # Performance metrics
POST /process         # Main query processing
GET  /agents          # List available agents
POST /discover        # Agent discovery for concept/intent
GET  /status          # Service status and dependencies
```

**Critical Issues** ([Finding #1](../SEGMENT_1_ARCHITECTURE_FINDINGS.md)):

- Currently imported as library, not true service
- Creates single point of failure through Integration Tester
- Cannot scale independently
- No independent health monitoring

**Recommendations**:

1. Extract to standalone Flask service
2. Add HTTP API wrapper
3. Update Integration Tester to call via HTTP
4. Add resource limits and health checks

#### 2. GraphDB Manager AI

**Status**: ✅ Operational as microservice

**Responsibilities**:

- Neo4j database interface (CRUD operations)
- Agent-concept relationship management
- Hebbian learning weight updates
- Graph traversal queries for agent discovery
- Schema validation and enforcement

**Location**: [`src/myriad/services/graphdb_manager/`](../../src/myriad/services/graphdb_manager/)  
**Port**: 5008  
**Dependencies**: Neo4j database

**Key Endpoints**:

```python
POST /create_node           # Create graph node
POST /create_relationship   # Create relationship
POST /query                 # Execute Cypher query
GET  /get_agents_for_concept # Agent discovery
POST /hebbian/strengthen    # Strengthen connection
POST /hebbian/decay         # Decay unused connections
GET  /health                # Health check
```

**Hebbian Learning Features** ([`app.py:321-423`](../../src/myriad/services/graphdb_manager/app.py:321)):

- Weight strengthening on success (+0.05 default)
- Weight decay on failure (-0.02 default)
- Background decay thread (15-minute intervals)
- Usage tracking (success_rate, usage_count)

#### 3. Input Processor

**Status**: ✅ Operational as microservice (underutilized)

**Responsibilities**:

- Multi-language query parsing
- Intent recognition with confidence scoring
- Ambiguity detection and resolution
- Uncertainty assessment
- Socratic dialogue for clarification
- Enhanced task list generation

**Location**: [`src/myriad/services/processing/input_processor/`](../../src/myriad/services/processing/input_processor/)  
**Port**: 5003  
**Dependencies**: None (standalone)

**Key Capabilities**:

- **Multi-language**: Arabic, English, French, Spanish, Chinese
- **Intent Recognition**: Pattern-based with confidence
- **Ambiguity Resolver**: Context-aware disambiguation ([`ambiguity_resolver.py`](../../src/myriad/services/processing/input_processor/ambiguity_resolver.py))
- **Uncertainty Signals**: Multiple signal types ([`uncertainty_signals.py`](../../src/myriad/core/uncertainty/uncertainty_signals.py))

**Integration Gap** ([Finding #7](../SEGMENT_1_ARCHITECTURE_FINDINGS.md)):

- Not integrated into main orchestration flow
- Orchestrator bypasses Input Processor
- Advanced features unused in production

#### 4. Output Processor

**Status**: ✅ Operational as microservice (underutilized)

**Responsibilities**:

- Multi-agent response synthesis
- Response formatting and presentation
- Multi-language translation
- Evidence attribution
- Quality assessment

**Location**: [`src/myriad/services/processing/output_processor/`](../../src/myriad/services/processing/output_processor/)  
**Port**: 5004  
**Dependencies**: None (standalone)

**Key Features**:

- **Synthesizer**: Weighted correlation ([`synthesizer.py`](../../src/myriad/services/processing/output_processor/synthesizer.py))
- **Formatter**: Multiple output formats ([`formatter.py`](../../src/myriad/services/processing/output_processor/formatter.py))
- **Multi-language**: Response translation

**Integration Gap**: Same as Input Processor - not in main flow

#### 5. Integration Tester AI

**Status**: ✅ Operational (acts as orchestration gateway)

**Current Role**: Gateway for orchestration requests  
**Port**: 5009  
**Dependencies**: Orchestrator library, all other services

**Responsibilities**:

- Exposes `/run_orchestration` endpoint
- Calls orchestrator library functions
- Integration testing and validation

**Future Role**: Pure testing service after orchestrator extraction

### Intelligence & Lifecycle Services

#### 6. Enhanced Graph Intelligence

**Type**: Library/Module (embedded in orchestrator)  
**Location**: [`src/myriad/core/intelligence/`](../../src/myriad/core/intelligence/)

**Responsibilities**:

- Multi-criteria agent relevance scoring
- Context-aware discovery
- Dynamic agent clustering
- Performance tracking
- Intelligent routing with fallback strategies

**Key Features**:

- Expertise match scoring
- Capability assessment
- Domain overlap detection
- Performance factor weighting
- Hebbian weight integration

**Future**: Could be extracted as microservice for scalability

#### 7. Dynamic Lifecycle Manager

**Type**: Library/Module (embedded in orchestrator)  
**Location**: [`src/myriad/core/lifecycle/`](../../src/myriad/core/lifecycle/)

**Responsibilities**:

- Dynamic agent creation
- Template selection
- Code generation
- Docker orchestration
- Agent health monitoring
- Lifecycle management

**Resource Management Issues** ([Finding #4](../SEGMENT_1_ARCHITECTURE_FINDINGS.md)):

- No CPU/memory limits on agents
- No maximum concurrent agent limit
- Port range 7000-9999 allows 3000 agents
- No idle timeout or TTL policies

**Planned Improvements** (Sprint 1):

- Maximum concurrent agents (20 default)
- CPU limit: 0.5 cores per agent
- Memory limit: 256MB per agent
- Idle timeout: 30 minutes
- Max age: 24 hours
- Background lifecycle management thread

#### 8. Autonomous Learning Engine

**Type**: Library/Module (used by dynamic agents)  
**Location**: [`src/myriad/core/learning/`](../../src/myriad/core/learning/)

**Responsibilities**:

- 5-phase learning system for new agents
- Knowledge acquisition
- Capability development
- Performance optimization
- Cross-domain learning

**Learning Phases**:

1. Bootstrap: Initial knowledge setup
2. Research: Multi-source learning
3. Develop: Capability creation
4. Optimize: Self-improvement
5. Validate: Quality assurance

### Agent Network

#### Static Agents

**Purpose**: Handle well-known concepts with specialized logic  
**Location**: [`src/myriad/agents/`](../../src/myriad/agents/)  
**Deployment**: Pre-built Docker containers

**Examples**:

- **Lightbulb Definition AI** (Port 5001)
- **Lightbulb Function AI** (Port 5002)

**Characteristics**:

- Hand-crafted specialized logic
- Optimized for specific domains
- Static deployment (always running)
- Known capabilities and endpoints

#### Dynamic Agents

**Purpose**: Handle unknown concepts discovered at runtime  
**Location**: `dynamic_agents/` (runtime generation)  
**Deployment**: Auto-generated Docker containers

**Characteristics**:

- Auto-generated from templates
- Dynamic port allocation (7000-9999)
- Learning-enabled via Autonomous Learning Engine
- Temporary or permanent based on usage

**Templates Available**:

1. `factbase_basic`: Simple knowledge storage
2. `factbase_enhanced`: Advanced reasoning
3. `function_basic`: Impact analysis
4. `specialist_basic`: Domain expertise

---

## Communication Patterns

### Current Pattern: Synchronous HTTP

**Implementation**: All services use synchronous HTTP POST with retry logic

**Session Configuration** ([`orchestrator.py:24-38`](../../src/myriad/services/orchestrator/orchestrator.py:24)):

```python
_http_session = requests.Session()
_adapter = HTTPAdapter(
    pool_connections=20,
    pool_maxsize=20,
    max_retries=Retry(
        total=3,
        backoff_factor=0.3,
        status_forcelist=[502, 503, 504]
    )
)
```

**Communication Flow**:

```
Orchestrator → GraphDB Manager → Neo4j
           ↓
           → Agent 1 (HTTP POST, wait for response)
           ↓
           → Agent 2 (HTTP POST, wait for response)
           ↓
           → Agent 3 (HTTP POST, wait for response)
```

**Issues** ([Finding #6](../SEGMENT_1_ARCHITECTURE_FINDINGS.md)):

- **Sequential Processing**: Tasks processed one at a time
- **Blocking I/O**: Each call blocks until response
- **No Timeout Strategy**: Mixed timeouts (5s, 8s, 10s)
- **Cascading Failures**: One slow agent blocks queue
- **No Circuit Breakers**: Continues calling failed services

### Target Pattern: Asynchronous + Circuit Breakers

**Implementation**: Async I/O with resilience patterns (Sprint 3)

**Async Orchestrator** (Planned):

```python
import asyncio
import aiohttp
from circuitbreaker import circuit

async def send_task_to_agent_async(task: dict) -> Optional[dict]:
    """Async agent task execution with circuit breaker"""
    
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.post(agent_url, json=payload) as response:
            if response.status == 200:
                return await response.json()

async def process_tasks_async(tasks: list) -> dict:
    """Process independent tasks concurrently"""
    
    independent_tasks = [t for t in tasks if not t.get('dependencies')]
    
    # Execute in parallel
    task_futures = [
        send_task_to_agent_async(task)
        for task in independent_tasks
    ]
    
    results = await asyncio.gather(*task_futures)
    return results
```

**Benefits**:

- 3-5x performance improvement
- Parallel task execution
- Circuit breaker protection
- Graceful degradation

### Agent-to-Agent Communication (Reflex Arcs)

**Pattern**: Direct peer-to-peer collaboration

**Implementation**:

```python
# Agent discovers peers via GraphDB
peer_agents = self.discover_peers(related_concept)

# Direct HTTP call to peer (no orchestrator)
response = requests.post(
    f"{peer_agent_endpoint}/collaborate",
    json={"context": context, "request_type": "knowledge_share"}
)
```

**Benefits**:

- Faster response (no orchestrator hop)
- Distributed intelligence
- Reduced orchestrator load
- Enables emergent collaboration patterns

---

## Service Discovery

### Current: Graph-Based Discovery

**Mechanism**: Graph traversal via GraphDB Manager

**Discovery Flow**:

```python
# 1. Orchestrator receives task
concept = "lightbulb"
intent = "define"

# 2. Query GraphDB Manager for agents
response = requests.post(
    f"{GRAPHDB_MANAGER_URL}/get_agents_for_concept",
    json={"concept": concept, "intent": intent}
)

# 3. GraphDB traverses graph
query = """
    MATCH (a:Agent)-[r:HANDLES_CONCEPT]->(c:Concept {name: $concept})
    RETURN a, r
    ORDER BY r.weight DESC, r.success_rate DESC
"""

# 4. Enhanced Graph Intelligence scores agents
agents = enhanced_intelligence.discover_intelligent_agents(
    concept, intent, context
)

# 5. Select best agent
best_agent = agents[0]  # Highest relevance score
```

**Scoring Criteria** ([`enhanced_graph_intelligence.py`](../../src/myriad/core/intelligence/enhanced_graph_intelligence.py)):

- Expertise match (28%)
- Capability match (22%)
- Domain overlap (18%)
- Performance factor (14%)
- Availability factor (8%)
- Hebbian weight (10%)

### Future: Service Mesh

**Target**: Distributed service discovery with health tracking

**Components** (Planned):

- Service registry (Consul/etcd)
- Health checks
- Load balancing
- Circuit breakers
- Service mesh (Istio/Linkerd)

---

## Production Infrastructure

### Current State: Minimal

**Deployed Services** ([`docker-compose.yml`](../../docker-compose.yml)):

- Neo4j (database)
- Redis (caching)
- GraphDB Manager
- Integration Tester
- 2x Lightbulb Agents
- Input Processor
- Output Processor

**Missing Components** ([Finding #2](../SEGMENT_1_ARCHITECTURE_FINDINGS.md)):

- ❌ API Gateway (rate limiting, auth)
- ❌ Service Mesh (retries, circuit breakers)
- ❌ Monitoring Stack (Prometheus, Grafana)
- ❌ Load Balancing
- ❌ Security Layer (auth, TLS)
- ❌ Backup/Recovery

### Target: Production-Ready Stack

#### Monitoring Stack (Sprint 2)

**Prometheus Configuration**:

```yaml
# monitoring/prometheus.yml
scrape_configs:
  - job_name: 'orchestrator'
    static_configs:
      - targets: ['orchestrator:5010']
    metrics_path: '/metrics'
  
  - job_name: 'graphdb_manager'
    static_configs:
      - targets: ['graphdb_manager_ai:5008']
    metrics_path: '/metrics'
```

**Grafana Dashboards**:

- System health overview
- Agent performance metrics
- Hebbian learning statistics
- Request latency distribution
- Error rates and success rates

**Metrics to Track**:

- Query processing time
- Agent discovery latency
- Neurogenesis events
- Hebbian weight distribution
- Active agent count
- Memory usage per service

#### API Gateway (Sprint 2)

**Technology**: Traefik or Kong

**Features**:

- Rate limiting
- Authentication/Authorization
- TLS termination
- Request routing
- Load balancing

**Configuration Example**:

```yaml
# Traefik routing
http:
  routers:
    orchestrator:
      rule: "PathPrefix(`/api/v1/process`)"
      service: orchestrator
      middlewares:
        - auth
        - rate-limit
```

#### Resource Limits (Sprint 1-2)

**Docker Compose Updates**:

```yaml
services:
  orchestrator:
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 1G
        reservations:
          memory: 512M
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5010/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

**All Services Need**:

- CPU limits
- Memory limits
- Health checks
- Restart policies
- Resource reservations

---

## Deployment Architecture

### Current: Docker Compose

**Deployment File**: [`docker-compose.yml`](../../docker-compose.yml)

**Architecture**:

```
┌────────────────────────────────────┐
│     docker-compose.yml             │
├────────────────────────────────────┤
│  - Neo4j                           │
│  - Redis                           │
│  - GraphDB Manager (5008)          │
│  - Integration Tester (5009)       │
│  - Input Processor (5003)          │
│  - Output Processor (5004)         │
│  - Lightbulb Definition AI (5001)  │
│  - Lightbulb Function AI (5002)    │
│  - [Orchestrator (5010) - planned] │
│  - [Prometheus (9090) - planned]   │
│  - [Grafana (3000) - planned]      │
└────────────────────────────────────┘
```

**Network**: `myriad_network` (bridge)

### Target: Kubernetes (Future)

**Benefits**:

- Horizontal pod autoscaling
- Rolling updates
- Self-healing
- Service discovery
- Configuration management
- Secret management

**Deployment Strategy**:

1. Start with Docker Compose (current)
2. Add monitoring and resource limits (Sprint 1-2)
3. Kubernetes migration (post-Sprint 8)

---

## API Contracts

### Standard Response Format

All services should follow consistent response format:

```json
{
  "status": "success" | "error" | "partial",
  "data": { ... },
  "metadata": {
    "timestamp": "2025-01-16T00:00:00Z",
    "service": "orchestrator",
    "version": "5.0",
    "processing_time_ms": 145
  },
  "errors": [...]  // Only if status is "error" or "partial"
}
```

### Health Check Standard

```json
{
  "status": "healthy" | "degraded" | "unhealthy",
  "service": "service_name",
  "version": "x.y.z",
  "timestamp": "ISO-8601",
  "dependencies": {
    "neo4j": "healthy",
    "redis": "healthy"
  }
}
```

### Orchestrator API (Planned)

**POST /process** - Main query processing

```json
Request:
{
  "query": "What is a lightbulb?",
  "session_id": "sess_abc123",  // Optional
  "user_id": "user_xyz789",     // Optional
  "context": {...}              // Optional
}

Response:
{
  "status": "success",
  "session_id": "sess_abc123",
  "results": {
    "task_1": {
      "agent": "Lightbulb_Definition_AI",
      "response": "...",
      "confidence": 0.95
    }
  },
  "metadata": {...}
}
```

**POST /discover** - Agent discovery

```json
Request:
{
  "concept": "lightbulb",
  "intent": "define"
}

Response:
{
  "agents": [
    {
      "agent_id": "lightbulb_definition_ai",
      "endpoint": "http://lightbulb_definition:5001",
      "relevance_score": 0.95,
      "reasoning": ["Exact concept match", "High success rate"]
    }
  ]
}
```

---

## Evolution Roadmap

### Phase 1: Microservice Extraction (Weeks 1-2)

**Goal**: True microservice architecture

- [x] Extract orchestrator as standalone service
- [x] Add HTTP API wrapper
- [x] Update Integration Tester to use HTTP
- [ ] Add health checks
- [ ] Add metrics endpoints

**See**: [Sprint 1](../implementation/implementation-sprint-1.md)

### Phase 2: Production Infrastructure (Weeks 3-6)

**Goal**: Production-ready deployment

- [ ] Add Prometheus monitoring
- [ ] Add Grafana dashboards
- [ ] Implement resource limits
- [ ] Add health checks to all services
- [ ] Create backup strategy

**See**: [Sprint 2](../implementation/implementation-sprint-2.md)

### Phase 3: Async Communication (Weeks 7-9)

**Goal**: High-performance parallel processing

- [ ] Convert to async I/O
- [ ] Implement circuit breakers
- [ ] Add message queue (RabbitMQ/Redis)
- [ ] Parallel task execution

**See**: [Sprint 3](../implementation/implementation-sprint-3.md)

### Phase 4: Service Mesh (Future)

**Goal**: Advanced resilience and observability

- [ ] Implement service mesh (Istio/Linkerd)
- [ ] Distributed tracing
- [ ] Advanced load balancing
- [ ] Mutual TLS

---

## Related Documentation

### Architecture

- **[System Overview](architecture-overview.md)**: Core philosophy and design principles
- **[Graph Intelligence](architecture-graph-intelligence.md)**: Neo4j schema and agent discovery
- **[Neurogenesis](architecture-neurogenesis.md)**: Dynamic agent creation and learning

### Implementation

- **[Sprint 1](../implementation/implementation-sprint-1.md)**: Orchestrator extraction and resource limits
- **[Sprint 2](../implementation/implementation-sprint-2.md)**: Production infrastructure
- **[Sprint 3](../implementation/implementation-sprint-3.md)**: Async communication

### Technical Findings

- **[Segment 1 Findings](../SEGMENT_1_ARCHITECTURE_FINDINGS.md)**: Architectural assessment and recommendations
- **[Protocols](../protocols/protocols-level-1-foundation.md)**: Communication protocols

---

**Document Version:** 1.0  
**Last Updated:** 2025-01-16  
**Status:** Active Development

[← Overview](architecture-overview.md) | [↑ Back to Index](../INDEX.md) | [Graph Intelligence →](architecture-graph-intelligence.md)

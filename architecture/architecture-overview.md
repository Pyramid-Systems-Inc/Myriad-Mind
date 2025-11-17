# Myriad Cognitive Architecture - High-Level Overview

**Version**: 5.0 C#/.NET Edition
**Technology Stack**: ASP.NET Core, C# 10+, Docker
**Database**: Custom Graph Implementation (Neo4j-inspired, built from scratch)

---

## Table of Contents

1. [System Architecture](#system-architecture)
2. [Technology Stack](#technology-stack)
3. [Layer Architecture](#layer-architecture)
4. [Component Interaction](#component-interaction)
5. [Data Flow](#data-flow)
6. [Deployment Architecture](#deployment-architecture)

---

## System Architecture

The Myriad architecture is a multi-tiered, decentralized system of microservices built on ASP.NET Core. Data flows through a series of specialized processors, activating concept agents as needed.

### Architectural Layers

```
┌─────────────────────────────────────────────────────────────┐
│                    User Interface Layer                      │
│  - REST API Endpoints                                        │
│  - Query Input / Response Output                             │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│              Enhanced Graph Intelligence Layer                │
│  - Context Analysis & Intent Recognition                     │
│  - Relevance Scoring & Agent Clustering                      │
│  - Smart Routing & Performance Tracking                      │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    Core Cognitive Layer                       │
│  - Input Processor (Sensory Cortex)                         │
│  - Orchestrator (Central Nervous System)                     │
│  - Output Processor (Motor Cortex)                           │
│  - Synthesizer (Integration)                                 │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    Knowledge Graph Layer                      │
│  - GraphDB Manager AI (Neural Substrate)                    │
│  - Concept Nodes & Relationship Edges                        │
│  - Hebbian Learning & Weight Updates                         │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                  Intelligent Agent Network                    │
│  - Static Agents (Pre-deployed)                              │
│  - Dynamic Agents (Created via Neurogenesis)                 │
│  - Agent-to-Agent Communication (Reflex Arcs)                │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    System Management Layer                    │
│  - Lifecycle Manager (Neurogenesis)                          │
│  - Autonomous Learning Engine                                │
│  - Performance Monitoring & Optimization                      │
└─────────────────────────────────────────────────────────────┘
```

---

## Technology Stack

### Core Technologies

**Primary Language**: C# 10+

- Async/await patterns for concurrency
- Pattern matching for sophisticated logic
- Records for immutable data structures
- Nullable reference types for safety

**Framework**: ASP.NET Core 6.0+

- Minimal APIs for lightweight endpoints
- Built-in dependency injection
- Configuration management
- Health checks and diagnostics

**Containerization**: Docker

- Each agent runs in isolated container
- Docker Compose for multi-service orchestration
- Container networking for service discovery

### Custom-Built Components (Zero External Dependencies)

**Graph Database**:

- In-memory graph structure using C# collections
- Custom traversal algorithms
- Persistence layer using JSON serialization
- Neo4j-inspired query language (custom parser)

**Message Queue** (Future):

- Custom implementation using TCP/IP sockets
- Priority queuing with C# concurrent collections
- Pub/sub pattern implementation

**HTTP Client**:

- Built on top of System.Net.Http
- Custom retry logic and circuit breakers
- Connection pooling

**Serialization**:

- Custom JSON parser and serializer
- Protocol buffer implementation for binary data

---

## Layer Architecture

### 1. User Interface Layer

**Responsibility**: Gateway to the system

**Components**:

- [`API Gateway`](components-detailed.md:api-gateway): Entry point for all external requests
- [`Request Validator`](components-detailed.md:request-validator): Input validation and sanitization
- [`Response Formatter`](components-detailed.md:response-formatter): Output formatting and serialization

**Technology**: ASP.NET Core Minimal APIs

**Endpoints**:

```csharp
POST /api/query              // Main query endpoint
GET  /api/health             // Health check
GET  /api/agents             // List available agents
GET  /api/metrics            // System metrics
POST /api/learn              // Learning endpoint
```

### 2. Enhanced Graph Intelligence Layer

**Responsibility**: Smart agent discovery and routing

**Components**:

- [`Context Analyzer`](graph-intelligence.md:context-analyzer): Query complexity and domain analysis
- [`Relevance Scorer`](graph-intelligence.md:relevance-scorer): Multi-criteria agent evaluation
- [`Agent Clusterer`](graph-intelligence.md:agent-clusterer): Dynamic agent organization
- [`Performance Tracker`](graph-intelligence.md:performance-tracker): Success rate monitoring

**Key Features**:

- Multi-criteria relevance scoring
- Context-aware agent discovery
- Dynamic performance-based clustering
- Intelligent routing with fallback strategies

### 3. Core Cognitive Layer

**Responsibility**: Query processing and orchestration

**Components**:

#### Input Processor (Sensory Cortex)

- **Parser**: Keyword and entity extraction
- **Intent Recognizer**: Goal identification with confidence scoring
- **Ambiguity Resolver**: Context-based disambiguation
- **Task Generator**: Creates structured task lists

#### Orchestrator (Central Nervous System)

- **Graph Traversal**: Agent discovery via knowledge graph
- **Parallel Dispatch**: Concurrent agent activation
- **Neurogenesis Coordinator**: Unknown concept handling
- **Result Aggregation**: Response collection

#### Output Processor (Motor Cortex)

- **Synthesizer**: Multi-agent response integration
- **Formatter**: Multi-format response generation
- **Quality Assessor**: Confidence scoring

### 4. Knowledge Graph Layer

**Responsibility**: Persistent knowledge representation

**Components**:

- [`GraphDB Manager AI`](components-detailed.md:graphdb-manager): Graph database interface
- [`Node Store`](components-detailed.md:node-store): Concept and agent nodes
- [`Edge Store`](components-detailed.md:edge-store): Weighted relationships
- [`Hebbian Updater`](components-detailed.md:hebbian-updater): Connection strengthening

**Schema**:

```csharp
// Node Types
public record ConceptNode(string Id, string Name, Dictionary<string, object> Properties);
public record AgentNode(string Id, string Endpoint, List<string> Capabilities);
public record SensoryNode(string Id, float[] EmbeddingVector, string Modality);

// Edge Types
public record Relationship(
    string FromId, 
    string ToId, 
    string Type,
    float Weight,
    int UsageCount,
    float SuccessRate,
    DateTime LastUpdated,
    float DecayRate
);
```

### 5. Intelligent Agent Network

**Responsibility**: Specialized knowledge and function execution

**Agent Types**:

**Type A - Fact-Base Agents**:

```csharp
// Stores and retrieves factual knowledge
public interface IFactBaseAgent
{
    Task<FactResponse> GetFactsAsync(string concept);
    Task<bool> ValidateFactAsync(string fact);
}
```

**Type B - Function-Executor Agents**:

```csharp
// Performs calculations and transformations
public interface IFunctionAgent
{
    Task<FunctionResult> ExecuteAsync(Dictionary<string, object> parameters);
    Task<AnalysisResult> AnalyzeImpactAsync(string context);
}
```

**Type C - Pattern-Matcher Agents**:

```csharp
// Classifies and identifies patterns
public interface IPatternMatcherAgent
{
    Task<ClassificationResult> ClassifyAsync(object input);
    Task<float> GetConfidenceAsync(string pattern);
}
```

**Type D - Micro-Generator Agents**:

```csharp
// Generates content and explanations
public interface IGeneratorAgent
{
    Task<string> GenerateExplanationAsync(string concept);
    Task<string> SynthesizeContentAsync(List<string> sources);
}
```

**Cognitive Regions**:

- Technology Region: Software, hardware, computing agents
- Science Region: Physics, chemistry, biology agents
- History Region: Historical events and figures
- Arts Region: Literature, music, visual arts
- General Region: Cross-domain and newly created agents

### 6. System Management Layer

**Responsibility**: System evolution and optimization

**Components**:

#### Lifecycle Manager (Neurogenesis)

- **Concept Detector**: Identifies unknown concepts
- **Research Coordinator**: Multi-agent research orchestration
- **Template Selector**: Chooses appropriate agent template
- **Agent Creator**: Instantiates and deploys new agents
- **Graph Registrar**: Integrates agents into knowledge graph

#### Autonomous Learning Engine

- **Knowledge Acquisition**: Multi-source learning
- **Capability Development**: Skill creation
- **Performance Optimization**: Self-improvement
- **Cross-Domain Learning**: Knowledge transfer
- **Session Manager**: Background learning coordination

#### Performance Monitor

- **Metrics Collector**: Response times, success rates
- **Health Checker**: Agent availability monitoring
- **Resource Tracker**: Memory and CPU usage
- **Alert Manager**: Anomaly detection

---

## Component Interaction

### Standard Query Flow

```
User Query
    ↓
[Input Processor]
    ↓ (Parsed Query + Intent + Task List)
[Enhanced Graph Intelligence]
    ↓ (Relevant Agents with Relevance Scores)
[Orchestrator]
    ↓ (Parallel HTTP Requests)
[Agent Network]
    ↓ (Individual Responses)
[Synthesizer]
    ↓ (Integrated Response)
[Output Processor]
    ↓ (Formatted Answer)
User Response
```

### Neurogenesis Flow (Unknown Concept)

```
Unknown Concept Detected
    ↓
[Lifecycle Manager - Concept Detector]
    ↓
[Research Coordinator]
    ↓ (Queries Existing Agents)
[Agent Network - Research Collaboration]
    ↓ (Research Results)
[Template Selector]
    ↓ (Chosen Template)
[Agent Creator]
    ↓ (New Agent Instance)
[Docker Container]
    ↓ (Running Agent)
[Graph Registrar]
    ↓ (Agent Node Created)
[GraphDB Manager]
    ↓ (Now Discoverable)
Future Queries Can Access New Agent
```

### Agent-to-Agent Communication (Reflex Arc)

```
[Agent A] Needs Additional Context
    ↓
[GraphDB Manager] - Query Related Agents
    ↓
[Agent B] Discovered
    ↓
[Direct HTTP Call] A → B
    ↓
[Agent B] Returns Context
    ↓
[Agent A] Enhances Response
    ↓
[Hebbian Update] Strengthens A-B Connection
```

---

## Data Flow

### Request/Response Protocol

**Standard Request**:

```json
{
  "query": "Why was the lightbulb important for factories?",
  "context": {
    "user_id": "user123",
    "session_id": "session456",
    "preferences": {
      "detail_level": "medium",
      "format": "explanatory"
    }
  }
}
```

**Processed Query** (Input Processor → Orchestrator):

```json
{
  "original_query": "Why was the lightbulb important for factories?",
  "intent": "explain_importance",
  "concepts": ["lightbulb", "factory", "industrial_revolution"],
  "tasks": [
    {
      "task_id": "task1",
      "action": "define",
      "target": "lightbulb",
      "priority": 1
    },
    {
      "task_id": "task2",
      "action": "explain_relationship",
      "targets": ["lightbulb", "factory"],
      "priority": 2
    }
  ]
}
```

**Agent Discovery Response** (Graph Intelligence → Orchestrator):

```json
{
  "agents": [
    {
      "agent_id": "lightbulb_def_ai",
      "endpoint": "http://lightbulb-definition:5001",
      "relevance_score": 0.95,
      "confidence": 0.92,
      "reason": "Primary concept match"
    },
    {
      "agent_id": "factory_ai",
      "endpoint": "http://factory-ai:5002",
      "relevance_score": 0.88,
      "confidence": 0.85,
      "reason": "Secondary concept match"
    }
  ]
}
```

**Agent Response** (Agent → Orchestrator):

```json
{
  "source_agent": "lightbulb_def_ai",
  "task_id": "task1",
  "success": true,
  "data": {
    "definition": "An electric light with a wire filament...",
    "key_attributes": ["artificial_lighting", "electrical", "industrial_era"],
    "related_concepts": ["electricity", "edison", "innovation"]
  },
  "confidence": 0.95,
  "processing_time_ms": 12
}
```

**Final Response** (Output Processor → User):

```json
{
  "answer": "The lightbulb was crucial for factories because it enabled...",
  "confidence": 0.91,
  "sources": [
    {
      "agent": "lightbulb_def_ai",
      "contribution": "definition and attributes"
    },
    {
      "agent": "factory_ai",
      "contribution": "industrial impact analysis"
    }
  ],
  "metadata": {
    "agents_activated": 3,
    "total_processing_time_ms": 145,
    "new_agents_created": 0
  }
}
```

---

## Deployment Architecture

### Docker Compose Structure

```yaml
services:
  # Core Services
  orchestrator:
    image: myriad/orchestrator:latest
    ports: ["5000:80"]
    environment:
      - GRAPH_DB_ENDPOINT=http://graphdb-manager:5008
      - LIFECYCLE_MANAGER_ENDPOINT=http://lifecycle-manager:5009
    
  graphdb-manager:
    image: myriad/graphdb-manager:latest
    ports: ["5008:80"]
    volumes:
      - graph-data:/data
  
  input-processor:
    image: myriad/input-processor:latest
    ports: ["5010:80"]
  
  output-processor:
    image: myriad/output-processor:latest
    ports: ["5011:80"]
  
  lifecycle-manager:
    image: myriad/lifecycle-manager:latest
    ports: ["5009:80"]
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
  
  # Static Agents
  lightbulb-definition:
    image: myriad/agents/lightbulb-definition:latest
    ports: ["5001:80"]
  
  lightbulb-function:
    image: myriad/agents/lightbulb-function:latest
    ports: ["5002:80"]
  
  factory-ai:
    image: myriad/agents/factory:latest
    ports: ["5003:80"]
  
  # Dynamic agents are created at runtime

volumes:
  graph-data:
```

### Scalability Strategy

**Horizontal Scaling**:

- Multiple instances of high-demand agents
- Load balancer for orchestrator
- Distributed graph database (future)

**Vertical Scaling**:

- Resource allocation per agent type
- Memory limits for container isolation
- CPU affinity for performance-critical agents

**Auto-scaling Triggers**:

- Request queue depth
- Response time degradation
- Agent utilization percentage

---

## Performance Characteristics

### Expected Metrics

**Simple Queries** (e.g., "What is 2+2?"):

- Agents Activated: 1
- Response Time: < 10ms
- Resource Usage: Minimal (single function agent)

**Medium Complexity** (e.g., "Explain the lightbulb"):

- Agents Activated: 2-3
- Response Time: 50-200ms
- Resource Usage: Low (few fact-base agents)

**Complex Queries** (e.g., "Why was lightbulb important for factories?"):

- Agents Activated: 5-10
- Response Time: 200-500ms
- Resource Usage: Moderate (multiple agents + synthesis)

**Neurogenesis Events** (Unknown concept):

- Agents Activated: 10-20 (for research)
- Response Time: 2-10 seconds (first query only)
- Resource Usage: High (agent creation + deployment)
- Subsequent Queries: Normal complexity metrics

---

**Next**: See [`components-detailed.md`](components-detailed.md) for in-depth component specifications.

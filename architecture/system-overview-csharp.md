# Myriad Cognitive Architecture - System Overview (C#/.NET Edition)

**Architecture Documentation** | [Components](components-detailed.md) | [Graph Intelligence](graph-intelligence-csharp.md) | [Neurogenesis](neurogenesis-csharp.md)

Comprehensive overview of the Myriad-Mind system architecture adapted for C# and .NET, including design principles, component relationships, and zero-dependency implementation strategy.

[← Back to Index](../INDEX.md#architecture) | [Implementation Guide →](implementation-guide.md)

---

## Table of Contents

- [Core Philosophy](#core-philosophy)
- [Design Principles](#design-principles)
- [System Architecture Overview](#system-architecture-overview)
- [Current Implementation Status](#current-implementation-status)
- [Technology Stack (C#/.NET)](#technology-stack-cnet)
- [Component Catalog](#component-catalog)
- [Process Flow](#process-flow)
- [Architectural Evolution Path](#architectural-evolution-path)

---

## Core Philosophy

The Myriad Cognitive Architecture is a fundamental departure from the paradigm of monolithic, large-scale AI models. It is founded on the principle that true, scalable, and explainable intelligence is not born from a single, all-knowing entity, but emerges from the dynamic collaboration of countless, hyper-specialized, and minimalist agents.

### Guiding Principles

Our guiding principles are inspired by neurobiology:

1. **Radical Specialization (The Neuron)**

   Like a neuron in the brain is specialized for a task, each "Myriad Agent" is the smallest possible unit of knowledge or function. It knows one thing, and it knows it perfectly. An agent for "the concept of gravity" does not know about poetry.

2. **Emergent Intelligence (The Brain)**

   Intelligence is not located in any single agent but is an emergent property of the entire network. A complex answer is synthesized from the simple, factual outputs of many collaborating agents.

3. **Dynamic Growth (Neurogenesis)**

   The system's primary method of learning new concepts is not by retraining a massive model, but by creating, training, and integrating a *new agent* into the network. The brain grows by adding neurons, and so does Myriad.

4. **Efficiency and Resource Frugality**

   The system must be computationally efficient. Querying "What is 2+2?" should activate a tiny, near-instantaneous function agent, not a multi-billion parameter LLM.

5. **Biomimetic Learning**

   Learning occurs through Hebbian principles: "agents that fire together, wire together." Connection weights strengthen with successful collaboration.

---

## Design Principles

### Agent-Centric Architecture

- **Microservice Independence**: Each agent is a self-contained ASP.NET Core microservice
- **Minimal Coupling**: Agents communicate through well-defined REST interfaces
- **Specialized Knowledge**: Each agent embodies a single concept or function
- **Collaborative Intelligence**: Complex tasks emerge from agent coordination

### Graph-Based Knowledge (Custom Implementation)

- **Zero External Dependencies**: Custom graph database built from scratch in C#
- **Relationship-Driven**: Agent discovery via graph traversal, not lookup tables
- **Hebbian Weighting**: Connection strengths evolve based on successful collaboration
- **Dynamic Structure**: Graph grows and adapts with new knowledge

### Biomimetic Principles

- **Neurogenesis**: System creates new agents for unknown concepts
- **Synaptic Plasticity**: Agent relationships strengthen with use
- **Resource Efficiency**: Minimal activation for simple queries
- **Emergent Behavior**: Intelligence emerges from network, not individual components

### C#/.NET Specific Principles

- **Async/Await First**: All I/O operations use `async`/`await` patterns
- **Strong Typing**: Leverage C# type system for compile-time safety
- **LINQ for Queries**: Graph traversal using LINQ expressions
- **Dependency Injection**: Built-in ASP.NET Core DI container
- **Records and Pattern Matching**: Modern C# features for clean code
- **Zero External Libraries**: Every component built from scratch

---

## System Architecture Overview

The Myriad architecture is a multi-tiered, decentralized system of ASP.NET Core microservices organized into cognitive regions:

```
┌─────────────────────────────────────────────────────────────┐
│                    User Interface Layer                      │
│           ASP.NET Core Minimal APIs / Controllers            │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│              Enhanced Graph Intelligence Layer                │
│  - Context Analyzer (C# Service)                             │
│  - Relevance Scorer (LINQ-based)                             │
│  - Agent Clustering (Background Service)                     │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    Core Cognitive Layer                       │
│  - Input Processor (ASP.NET Core Service)                   │
│  - Orchestrator (Central Service)                            │
│  - Output Processor (ASP.NET Core Service)                   │
│  - Synthesizer (Integration Logic)                           │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                Custom Graph Database Layer                    │
│  - GraphDB Manager (C# Service)                             │
│  - In-Memory Graph (ConcurrentDictionary)                    │
│  - Persistence Layer (JSON Serialization)                    │
│  - Hebbian Learning Engine (Background Service)              │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                  Intelligent Agent Network                    │
│  - Static Agents (Pre-deployed ASP.NET Services)            │
│  - Dynamic Agents (Created via Neurogenesis)                 │
│  - Agent-to-Agent Communication (HttpClient)                 │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    System Management Layer                    │
│  - Lifecycle Manager (Neurogenesis)                          │
│  - Autonomous Learning Engine                                │
│  - Performance Monitoring (IHostedService)                   │
└─────────────────────────────────────────────────────────────┘
```

### Hierarchical Organization

The architecture mimics the hierarchical and specialized structure of a biological brain:

1. **Cognitive Regions**: Broad domains of knowledge (Technology, Science, Arts, etc.)
2. **Regional Agents**: Specialized agents within each domain
3. **Two-Step Discovery**:
   - Region Routing: Identify relevant cognitive region
   - Agent Selection: Find best agent within region

This reduces search space and improves efficiency, similar to the brain activating specific cortical areas.

---

## Current Implementation Status

**System Version:** 5.0 C#  
**Status:** Documentation and Architecture Definition Phase  
**Target Framework:** .NET 6.0+ / .NET 8.0  
**Language:** C# 10+ with nullable reference types enabled

### Planned Implementation Phases

#### Phase 1: Foundation Infrastructure (Weeks 1-4)

- ⬜ **Custom Graph Database**: In-memory graph with persistence
  - `GraphNode<TData>` generic class
  - `GraphEdge<TWeight>` with Hebbian properties
  - `GraphDatabase` service with CRUD operations
  - JSON-based persistence layer

- ⬜ **GraphDB Manager Service**: ASP.NET Core REST API
  - Minimal API endpoints for graph operations
  - LINQ-based graph traversal
  - Hebbian learning methods
  - Health check endpoints

- ⬜ **Orchestrator Service**: Central coordination
  - Agent discovery via graph traversal
  - Parallel agent invocation using `Task.WhenAll`
  - Neurogenesis coordination
  - Circuit breaker pattern (custom implementation)

- ⬜ **Migration System**: Configuration-based graph population
  - JSON configuration files
  - Startup migration service
  - Agent registration automation

#### Phase 2: Enhanced Processing Pipeline (Weeks 5-8)

- ⬜ **Input Processor Service**: Advanced NLP
  - Keyword extraction (custom algorithms)
  - Intent recognition (pattern-based)
  - Ambiguity resolution
  - Task generation

- ⬜ **Output Processor Service**: Response synthesis
  - Multi-agent response correlation
  - Format generation (text, JSON, XML)
  - Quality assessment
  - Confidence scoring

- ⬜ **Specialized Agents**: Domain-specific microservices
  - `LightbulbDefinitionAgent` (Type A - Fact-Base)
  - `LightbulbFunctionAgent` (Type B - Function-Executor)
  - Base agent interfaces and abstract classes

#### Phase 3: Agent-to-Agent Communication (Weeks 9-12)

- ⬜ **Direct Peer Discovery**: Graph-based peer location
- ⬜ **Reflex Arcs**: Direct HTTP communication between agents
- ⬜ **Collaboration Patterns**: Request/response protocols
- ⬜ **Chained Collaboration**: Multi-hop agent interactions

#### Phase 4: Biomimetic Neurogenesis (Weeks 13-18)

- ⬜ **Concept Detection**: Unknown concept identification
- ⬜ **Multi-Agent Research**: Collaborative knowledge gathering
- ⬜ **Template Selection**: Policy-based agent template choice
- ⬜ **Dynamic Lifecycle Manager**: Agent creation and deployment
  - C# code generation using Roslyn
  - Docker image creation (Docker SDK for .NET)
  - Container orchestration
  - Health monitoring

- ⬜ **Agent Templates**:
  - `FactBaseBasicTemplate.cs`
  - `FactBaseEnhancedTemplate.cs`
  - `FunctionBasicTemplate.cs`
  - `SpecialistBasicTemplate.cs`

#### Phase 5: Autonomous Learning Engine (Weeks 19-24)

- ⬜ **Learning Framework**: 5-phase learning system
  - Bootstrap phase
  - Research phase
  - Development phase
  - Optimization phase
  - Validation phase

- ⬜ **Knowledge Acquisition**: Multi-source learning
- ⬜ **Capability Development**: Skill creation
- ⬜ **Performance Optimization**: Self-improvement
- ⬜ **Cross-Domain Learning**: Knowledge transfer

#### Phase 6: Enhanced Graph Intelligence (Weeks 25-30)

- ⬜ **Multi-Criteria Relevance Scoring**
- ⬜ **Context-Aware Discovery**
- ⬜ **Dynamic Agent Clustering**
- ⬜ **Real-Time Performance Tracking**
- ⬜ **Intelligent Routing with Fallbacks**

---

## Technology Stack (C#/.NET)

### Core Infrastructure

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Framework** | .NET | 6.0 / 8.0 | Application runtime |
| **Web Framework** | ASP.NET Core | 6.0+ | Microservice hosting |
| **Language** | C# | 10+ | Implementation language |
| **API Style** | Minimal APIs | - | Lightweight endpoints |
| **Serialization** | System.Text.Json | Built-in | JSON parsing (custom) |
| **Async** | Task Parallel Library | Built-in | Concurrency |

### Custom-Built Components (Zero External Dependencies)

**Graph Database**:

```csharp
// Custom implementation using C# collections
public class GraphDatabase
{
    private readonly ConcurrentDictionary<string, GraphNode> _nodes;
    private readonly ConcurrentDictionary<string, GraphEdge> _edges;
    private readonly ReaderWriterLockSlim _lock;
    
    public Task<GraphNode> GetNodeAsync(string id);
    public Task<IEnumerable<GraphNode>> TraverseAsync(string startId, Func<GraphNode, bool> predicate);
    public Task AddEdgeAsync(GraphEdge edge);
    public Task<float> GetEdgeWeightAsync(string fromId, string toId, string edgeType);
}
```

**HTTP Client**:

```csharp
// Built on System.Net.Http with custom retry logic
public class ResilientHttpClient
{
    private readonly HttpClient _httpClient;
    private readonly CircuitBreaker _circuitBreaker;
    
    public async Task<HttpResponseMessage> SendWithRetryAsync(
        HttpRequestMessage request, 
        int maxRetries = 3, 
        TimeSpan? timeout = null);
}
```

**Circuit Breaker**:

```csharp
// Custom implementation
public class CircuitBreaker
{
    private volatile CircuitState _state = CircuitState.Closed;
    private int _failureCount;
    private DateTime _lastFailureTime;
    
    public async Task<T> ExecuteAsync<T>(Func<Task<T>> operation);
    private void OnSuccess();
    private void OnFailure();
}
```

**JSON Parser** (Custom Implementation):

```csharp
// Custom JSON parser without external libraries
public class SimpleJsonParser
{
    public static Dictionary<string, object> Parse(string json);
    public static string Stringify(Dictionary<string, object> obj);
}
```

**Message Queue** (Future):

```csharp
// Custom TCP/IP based message queue
public class InMemoryMessageQueue
{
    private readonly ConcurrentQueue<Message> _queue;
    private readonly SemaphoreSlim _semaphore;
    
    public Task EnqueueAsync(Message message);
    public Task<Message> DequeueAsync(CancellationToken cancellationToken);
}
```

### Communication & Integration

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **HTTP API** | ASP.NET Minimal APIs | Inter-service communication |
| **Session Management** | In-Memory Cache | Conversation context (custom) |
| **Serialization** | Custom JSON | Standardized data exchange |
| **Health Checks** | IHealthCheck interface | Service monitoring |

### Processing & Intelligence

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **NLP Processing** | Custom algorithms | Query understanding |
| **Pattern Matching** | Regex + Custom | Intent detection |
| **Graph Traversal** | LINQ + Custom BFS/DFS | Agent discovery |
| **Scoring** | Custom algorithms | Relevance calculation |

### Deployment & Operations

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Containerization** | Docker | Agent isolation |
| **Orchestration** | Docker Compose | Multi-service coordination |
| **Monitoring** | Custom metrics (future) | Performance tracking |
| **Logging** | ILogger interface | Debug and audit |

---

## Component Catalog

### Core Services (ASP.NET Core)

1. **Orchestrator Service**
   - **Location**: `src/Myriad.Services.Orchestrator/`
   - **Port**: 5000
   - **Purpose**: Central coordination, agent discovery, task routing
   - **Key Classes**:
     - `OrchestratorService.cs` - Main service logic
     - `AgentDiscoveryEngine.cs` - Graph-based discovery
     - `NeurogenesisCoordinator.cs` - Unknown concept handling
     - `HebbianUpdater.cs` - Connection strengthening

2. **GraphDB Manager Service**
   - **Location**: `src/Myriad.Services.GraphDatabase/`
   - **Port**: 5008
   - **Purpose**: Graph database interface
   - **Key Classes**:
     - `GraphDatabaseService.cs` - Core graph operations
     - `GraphNode.cs` - Node representation
     - `GraphEdge.cs` - Edge with Hebbian properties
     - `GraphTraversal.cs` - Traversal algorithms
     - `PersistenceEngine.cs` - JSON-based persistence

3. **Input Processor Service**
   - **Location**: `src/Myriad.Services.InputProcessor/`
   - **Port**: 5003
   - **Purpose**: Query parsing and understanding
   - **Key Classes**:
     - `InputProcessorService.cs` - Main processor
     - `KeywordExtractor.cs` - Entity extraction
     - `IntentRecognizer.cs` - Intent detection
     - `AmbiguityResolver.cs` - Disambiguation
     - `TaskGenerator.cs` - Task list creation

4. **Output Processor Service**
   - **Location**: `src/Myriad.Services.OutputProcessor/`
   - **Port**: 5004
   - **Purpose**: Response synthesis and formatting
   - **Key Classes**:
     - `OutputProcessorService.cs` - Main processor
     - `ResponseSynthesizer.cs` - Multi-agent correlation
     - `ResponseFormatter.cs` - Format generation
     - `QualityAssessor.cs` - Confidence scoring

### Intelligence & Learning

5. **Enhanced Graph Intelligence**
   - **Location**: `src/Myriad.Core.Intelligence/`
   - **Type**: Class Library
   - **Key Classes**:
     - `EnhancedGraphIntelligence.cs` - Main intelligence engine
     - `RelevanceScorer.cs` - Multi-criteria scoring
     - `AgentClusterer.cs` - Dynamic clustering
     - `PerformanceTracker.cs` - Metrics tracking
     - `ContextAnalyzer.cs` - Query context analysis

6. **Autonomous Learning Engine**
   - **Location**: `src/Myriad.Core.Learning/`
   - **Type**: Class Library
   - **Key Classes**:
     - `AutonomousLearningEngine.cs` - Learning orchestrator
     - `KnowledgeAcquisition.cs` - Information gathering
     - `CapabilityDevelopment.cs` - Skill creation
     - `SelfOptimizer.cs` - Performance improvement
     - `CrossDomainLearner.cs` - Knowledge transfer

7. **Dynamic Lifecycle Manager**
   - **Location**: `src/Myriad.Core.Lifecycle/`
   - **Type**: Class Library
   - **Key Classes**:
     - `DynamicLifecycleManager.cs` - Agent creation orchestrator
     - `TemplateSelector.cs` - Template selection policy
     - `CodeGenerator.cs` - C# code generation (Roslyn)
     - `DockerOrchestrator.cs` - Container management
     - `HealthMonitor.cs` - Agent health checks

### Agent Network

8. **Static Agents**
   - **Location**: `src/Myriad.Agents.Static/`
   - **Examples**:
     - `LightbulbDefinitionAgent/` - Fact-base agent
     - `LightbulbFunctionAgent/` - Function-executor agent
     - `FactoryAgent/` - Domain knowledge agent
   - **Base Classes**:
     - `AgentBase.cs` - Common agent functionality
     - `IAgent.cs` - Agent interface
     - `AgentCapability.cs` - Capability definition

9. **Dynamic Agents**
   - **Location**: `dynamic_agents/` (runtime generation)
   - **Generated from Templates**:
     - `templates/FactBaseBasicTemplate.cs`
     - `templates/FactBaseEnhancedTemplate.cs`
     - `templates/FunctionBasicTemplate.cs`
     - `templates/SpecialistBasicTemplate.cs`

### Common Libraries

10. **Myriad.Common**
    - **Location**: `src/Myriad.Common/`
    - **Purpose**: Shared types and utilities
    - **Key Classes**:
      - `GraphNode<T>.cs` - Generic graph node
      - `GraphEdge<T>.cs` - Generic graph edge
      - `AgentResponse.cs` - Standard response type
      - `TaskList.cs` - Task list structure
      - `ProtocolDefinitions.cs` - Communication protocols

---

## Process Flow

### Standard Query Processing

```
User Query (HTTP POST)
    ↓
[Input Processor Service]
    ↓ (Enhanced Task List)
[Enhanced Graph Intelligence]
    ↓ (Relevant Agent List with Scores)
[Orchestrator Service]
    ↓ (Parallel HTTP Requests via Task.WhenAll)
[Agent Network]
    ↓ (Individual Agent Responses)
[Response Synthesizer]
    ↓ (Integrated Response)
[Output Processor Service]
    ↓ (Formatted Answer)
User Response (HTTP Response)
```

### C# Async Pattern Example

```csharp
public async Task<AgentResponse> ProcessQueryAsync(string query, CancellationToken cancellationToken)
{
    // 1. Parse query
    var taskList = await _inputProcessor.ProcessAsync(query, cancellationToken);
    
    // 2. Discover agents
    var relevantAgents = await _graphIntelligence.DiscoverAgentsAsync(
        taskList.PrimaryConcept, 
        taskList.PrimaryIntent,
        cancellationToken);
    
    // 3. Execute tasks in parallel
    var agentTasks = relevantAgents.Select(agent => 
        ExecuteAgentTaskAsync(agent, taskList, cancellationToken));
    
    var agentResponses = await Task.WhenAll(agentTasks);
    
    // 4. Update Hebbian weights
    await UpdateHebbianWeightsAsync(agentResponses, cancellationToken);
    
    // 5. Synthesize and format
    var synthesized = await _synthesizer.SynthesizeAsync(agentResponses, cancellationToken);
    var formatted = await _outputProcessor.FormatAsync(synthesized, cancellationToken);
    
    return formatted;
}
```

### Neurogenesis Flow (C# Implementation)

```csharp
public async Task<Agent> CreateAgentForConceptAsync(string concept, CancellationToken cancellationToken)
{
    // 1. Detect unknown concept
    var exists = await _graphDatabase.ConceptExistsAsync(concept, cancellationToken);
    if (exists) return null;
    
    // 2. Multi-agent research
    var researchResults = await ConductResearchAsync(concept, cancellationToken);
    
    // 3. Select template
    var template = await _templateSelector.SelectTemplateAsync(researchResults, cancellationToken);
    
    // 4. Generate agent code
    var generatedCode = await _codeGenerator.GenerateFromTemplateAsync(
        template, 
        concept, 
        researchResults,
        cancellationToken);
    
    // 5. Build and deploy
    var dockerImage = await _dockerOrchestrator.BuildImageAsync(generatedCode, cancellationToken);
    var container = await _dockerOrchestrator.DeployContainerAsync(dockerImage, cancellationToken);
    
    // 6. Register in graph
    var agent = new Agent
    {
        Name = $"{concept}_ai",
        Type = template.Type,
        Endpoint = container.Endpoint,
        Capabilities = template.Capabilities
    };
    
    await _graphDatabase.RegisterAgentAsync(agent, concept, cancellationToken);
    
    // 7. Start autonomous learning
    await _learningEngine.StartLearningSessionAsync(agent, cancellationToken);
    
    return agent;
}
```

---

## Architectural Evolution Path

### Current State (v5.0 - Documentation Phase)

- Architecture fully defined for C#/.NET
- Component specifications complete
- Zero-dependency strategy established
- Implementation roadmap defined

### Planned Evolution

#### Stage 1: Foundation (Weeks 1-4)

**Goal**: Core infrastructure

- Custom graph database implementation
- GraphDB Manager Service (ASP.NET Core)
- Basic orchestrator with synchronous calls
- Simple agent templates

**C# Features Used**:

- `ConcurrentDictionary<TKey, TValue>` for thread-safe graph storage
- `ReaderWriterLockSlim` for read-heavy operations
- `System.Text.Json` for serialization
- ASP.NET Core Minimal APIs

#### Stage 2: Async Processing (Weeks 5-8)

**Goal**: High-performance parallel processing

- Convert all I/O to `async`/`await`
- Implement `Task.WhenAll` for parallel agent calls
- Add circuit breakers (custom implementation)
- Connection pooling with `HttpClient` factory

**C# Features Used**:

- `async`/`await` pattern throughout
- `Task.WhenAll` for parallelism
- `IHttpClientFactory` for connection management
- `CancellationToken` for graceful cancellation

#### Stage 3: Enhanced Intelligence (Weeks 9-12)

**Goal**: Smart agent discovery

- Multi-criteria relevance scoring
- LINQ-based graph traversal
- Dynamic agent clustering
- Performance tracking with `IHostedService`

**C# Features Used**:

- LINQ for graph queries
- `IHostedService` for background tasks
- Pattern matching for complex logic
- Records for immutable data

#### Stage 4: Neurogenesis (Weeks 13-18)

**Goal**: Dynamic agent creation

- Roslyn for C# code generation
- Docker SDK for .NET for container management
- Template-based agent creation
- Automated deployment pipeline

**C# Features Used**:

- Roslyn `SyntaxFactory` for code generation
- Docker.DotNet SDK for container orchestration
- Source generators (potential)
- Reflection for dynamic capabilities

#### Stage 5: Context Understanding (Weeks 19-24)

**Goal**: Multi-turn conversations

- Custom session management (in-memory)
- Reference resolution
- Entity tracking
- Conversation flow analysis

**C# Features Used**:

- `ConcurrentDictionary` for session cache
- LINQ for entity queries
- Pattern matching for reference resolution
- Records for session state

### Long-Term Vision

**Event-Driven Architecture**:

- Custom message queue using TCP/IP
- Pub/sub pattern with `IObservable<T>`
- Event sourcing for audit trail

**Advanced Optimization**:

- Span<T> for zero-allocation parsing
- ValueTask<T> for hot paths
- Aggressive inlining with `[MethodImpl]`
- Memory pools for object reuse

---

**Document Version:** 1.0 C#  
**Last Updated:** 2025-01-09  
**Status:** Architecture Definition Phase

[↑ Back to Index](../INDEX.md) | [Components →](components-detailed.md) | [Graph Intelligence →](graph-intelligence-csharp.md)

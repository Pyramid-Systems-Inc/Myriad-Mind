# Myriad Cognitive Architecture - Documentation Index

**Version**: 5.0 C#/.NET Edition
**Status**: Architecture Definition Phase - Documentation Complete
**Last Updated**: 2025-01-10

---

## 🎯 Quick Start

**New to the Project?** Start here:

1. 📖 [README.md](README.md) - Project overview and getting started
2. 🧠 [Core Philosophy](architecture/core-philosophy.md) - Understand the biological inspiration
3. 🏗️ [System Overview](architecture/system-overview-csharp.md) - Complete architecture walkthrough
4. 🗺️ [Development Roadmap](roadmap/README.md) - Phased implementation guide

**Ready to Implement?** Follow the phased roadmap:

- [Phase 1: Foundation](roadmap/phase-1-foundation.md) - Setup and scaffolding (2-3 weeks)
- [Phase 2: Core Services](roadmap/phase-2-core-services.md) - Graph DB and processing (3-4 weeks)
- [Phase 3: MVP Complete](roadmap/phase-3-mvp.md) - Enhanced intelligence (2-3 weeks)
- [Phase 4: Advanced Features](roadmap/phase-4-advanced-features.md) - Context and synthesis (4-5 weeks)
- [Phase 5: Production](roadmap/phase-5-production.md) - Kubernetes and scaling (5-6 weeks)

---

## 📚 Core Documentation

### Foundational Documents

| Document | Description | Purpose |
|----------|-------------|---------|
| [README.md](README.md) | Project overview, prerequisites, setup | Start here for project introduction |
| [Design & Concept](design%20and%20concept.md) | Complete architectural blueprint (v5.0) | Comprehensive design philosophy |
| [Implementation Roadmap](roadmap/README.md) | Phased implementation guides | Step-by-step development plan |

### Architecture Documentation

| Document | Focus Area | Key Topics |
|----------|------------|------------|
| [Core Philosophy](architecture/core-philosophy.md) | Design principles | Biological inspiration, dual-path processing, GWT foundation |
| [System Overview](architecture/system-overview-csharp.md) | Complete architecture | Dual-path architecture, components, technology stack |
| [Graph Intelligence](architecture/graph-intelligence-csharp.md) | Knowledge representation | Custom graph DB, Hebbian learning, multi-layer context |
| [Microservices](architecture/microservices-csharp.md) | Service architecture | Service catalog, communication patterns, deployment |
| [Neurogenesis](architecture/neurogenesis-csharp.md) | Dynamic learning | Agent creation, templates, autonomous learning |
| [Context Understanding](architecture/context-understanding-csharp.md) | Conversation memory | Session management, reference resolution, user profiling |
| [Cognitive Synthesizer](architecture/cognitive-synthesizer-csharp.md) | Output generation | Four-stage synthesis, narrative weaving, layered responses |
| [AGI Enhancements](architecture/agi-enhancements-overview.md) | AGI roadmap | Deep reasoning, attention, meta-cognition, world models |
| [Production Deployment](architecture/production-deployment-csharp.md) | Scalability & ops | Kubernetes, cognitive tiers, knowledge substrate |

---

## 🏗️ Architecture Overview

### System Layers

```
┌─────────────────────────────────────────────┐
│         User Interface Layer                 │
│    (REST API Endpoints - ASP.NET Core)       │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│    Enhanced Graph Intelligence Layer         │
│  (Context Analysis, Relevance Scoring)       │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│         Core Cognitive Layer                 │
│  (Orchestrator, Cognitive Workspace,         │
│   Input/Output Processor)                    │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│      Custom Graph Database Layer             │
│  (ConcurrentDictionary, Custom Algorithms)   │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│      Intelligent Agent Network               │
│  (Static + Dynamic ASP.NET Core Services)    │
└─────────────────────────────────────────────┘
```

### Core Components

1. **Orchestrator Service** - Central coordination and dual-path routing (Port 5000)
2. **Cognitive Workspace** - Deep reasoning for complex queries (Port 5012)
3. **GraphDB Manager** - Custom graph database service (Port 5008)
4. **Input Processor** - Query parsing, complexity detection (Port 5003)
5. **Output Processor** - Response synthesis (Port 5004)
6. **Agent Network** - Specialized microservices (Ports 5001+)

---

## 💻 Technology Stack

### Core Technologies

- **Language**: C# 10+
- **Framework**: ASP.NET Core 6.0+ / .NET 6.0+
- **API Style**: Minimal APIs
- **Deployment**: Self-Contained .NET Deployments
- **Orchestration**: Custom Process Launcher (built from scratch)

### Zero External Dependencies

**Everything built from scratch:**

- ✅ Custom Graph Database (`ConcurrentDictionary` + algorithms)
- ✅ Custom JSON Parser (no external libraries)
- ✅ Custom HTTP Client Wrapper (retry logic, circuit breaker)
- ✅ Custom Message Queue (future: TCP/IP based)
- ✅ Custom Resilience Patterns (circuit breaker, retry)
- ✅ Custom Process Orchestrator (multi-service launcher, no Docker)
- ✅ Custom Packaging Format (self-contained .NET deployments)

---

## 📖 Documentation by Topic

### Design & Architecture

**Core Concepts:**

- [Core Philosophy](architecture/core-philosophy.md) - Biological inspiration, guiding principles, dual-path processing
- [Design Principles](architecture/core-philosophy.md#design-paradigm) - From monolithic to distributed
- [Global Workspace Theory](architecture/core-philosophy.md#5-global-workspace-theory-cognitive-workspace) - Cognitive Workspace foundation

**System Design:**

- [Architecture Overview](architecture/system-overview-csharp.md) - Complete system architecture with dual-path processing
- [Component Catalog](architecture/system-overview-csharp.md#component-catalog) - All services including Cognitive Workspace
- [Process Flow](architecture/system-overview-csharp.md#process-flow) - Dual-path query processing flow

### Implementation Details

**Graph Intelligence:**

- [Custom Graph Database](architecture/graph-intelligence-csharp.md#custom-graph-database-core) - In-memory graph implementation
- [Graph Schema](architecture/graph-intelligence-csharp.md#graph-schema-design) - Node and edge types
- [Hebbian Learning](architecture/graph-intelligence-csharp.md#hebbian-learning-system) - Connection strengthening
- [Context Understanding](architecture/graph-intelligence-csharp.md#context-understanding-architecture) - Multi-layer memory

**Microservices:**

- [Service Catalog](architecture/microservices-csharp.md#service-catalog) - All microservices
- [Communication Patterns](architecture/microservices-csharp.md#communication-patterns) - HTTP, async, circuit breakers
- [Deployment](architecture/microservices-csharp.md#deployment-architecture) - Docker Compose, Kubernetes ready

**Neurogenesis:**

- [Neurogenesis Pipeline](architecture/neurogenesis-csharp.md#biomimetic-pipeline) - Dynamic agent creation
- [Agent Templates](architecture/neurogenesis-csharp.md#template-based-agent-creation) - Four specialized templates
- [Lifecycle Management](architecture/neurogenesis-csharp.md#dynamic-lifecycle-manager) - Agent creation, monitoring, cleanup
- [Autonomous Learning](architecture/neurogenesis-csharp.md#autonomous-learning-engine) - Self-improvement system

**Context Understanding:**

- [Session Context](architecture/context-understanding-csharp.md#multi-layer-context-architecture) - Working memory and turn history
- [Reference Resolution](architecture/context-understanding-csharp.md#layer-3-reference-resolution-engine) - Pronoun and entity resolution
- [User Profiles](architecture/context-understanding-csharp.md#layer-2-user-context-episodic-memory) - Long-term user preferences
- [Integration Guide](architecture/context-understanding-csharp.md#integration-with-existing-components) - How to enhance existing services

**Cognitive Synthesis:**

- [Four-Stage Pipeline](architecture/cognitive-synthesizer-csharp.md#four-stage-synthesis-pipeline) - Thematic analysis to polished output
- [Narrative Weaving](architecture/cognitive-synthesizer-csharp.md#stage-2-narrative-weaver-ai) - Creating flowing narratives
- [Layered Responses](architecture/cognitive-synthesizer-csharp.md#stage-3-summarizer--expander-ai) - Summary + details + related topics
- [Confidence Modulation](architecture/cognitive-synthesizer-csharp.md#stage-4-final-formatter-with-confidence-modulation) - Language adaptation
- [Workspace vs Synthesizer](architecture/cognitive-synthesizer-csharp.md#architectural-distinctions) - Complementary roles

**Deep Reasoning:**

- [Cognitive Workspace](design%20and%20concept.md#35-the-cognitive-workspace-the-prefrontal-cortex) - GWT-inspired deep reasoning
- [Fast Path vs Deep Path](design%20and%20concept.md#4-process-flows-fast-path-vs-deep-reasoning) - Dual processing pathways
- [Iterative Synthesis](design%20and%20concept.md#42-deep-reasoning-flow-creative-synthesis-via-cognitive-workspace) - Pattern recognition and causal analysis
- [AGI Enhancements](architecture/agi-enhancements-overview.md) - Path to full AGI capabilities

**Production Deployment:**

- [Knowledge Substrate](architecture/production-deployment-csharp.md#knowledge-substrate-architecture) - Three-layer storage system
- [Cognitive Tiers](architecture/production-deployment-csharp.md#cognitive-tiers-model) - myriad-swift, myriad-base, myriad-max
- [Kubernetes Architecture](architecture/production-deployment-csharp.md#kubernetes-production-architecture) - K8s operator and CRDs
- [Implementation Roadmap](architecture/production-deployment-csharp.md#implementation-roadmap) - Production deployment phases

### Development Guide

**Getting Started:**

- [Implementation Roadmap](roadmap/README.md) - Overview of all phases
- [Phase 1: Foundation](roadmap/phase-1-foundation.md) - Setup and scaffolding (2-3 weeks)
- [Phase 2: Core Services](roadmap/phase-2-core-services.md) - Graph DB and processing (3-4 weeks)
- [Phase 3: MVP Complete](roadmap/phase-3-mvp.md) - Enhanced intelligence (2-3 weeks)

**Advanced Implementation:**

- [Phase 4: Advanced Features](roadmap/phase-4-advanced-features.md) - Context understanding and synthesis (4-5 weeks)
- [Phase 5: Production Ready](roadmap/phase-5-production.md) - Kubernetes deployment and scaling (5-6 weeks)

---

## 🔍 Quick Reference by Role

### For Architects

**Must Read:**

1. [Core Philosophy](architecture/core-philosophy.md) - Design principles
2. [System Overview](architecture/system-overview-csharp.md) - Complete architecture
3. [Design & Concept](design%20and%20concept.md) - Architectural blueprint

**Key Topics:**

- Biological inspiration and biomimicry
- Microservices architecture patterns
- Graph-based knowledge representation
- Event-driven evolution path

### For Developers

**Start Here:**

1. [README.md](README.md) - Project setup
2. [Implementation Roadmap](roadmap/README.md) - Development phases
3. [Phase 1 Guide](roadmap/phase-1-foundation.md) - First steps
4. [Microservices Architecture](architecture/microservices-csharp.md) - Service implementation

**Key Topics:**

- ASP.NET Core Minimal APIs
- Custom graph database implementation
- Circuit breaker and resilience patterns
- Docker containerization
- Zero external dependencies approach

### For AI/ML Engineers

**Focus On:**

1. [Neurogenesis Systems](architecture/neurogenesis-csharp.md) - Dynamic agent creation
2. [Hebbian Learning](architecture/graph-intelligence-csharp.md#hebbian-learning-system) - Connection strengthening
3. [Autonomous Learning](architecture/neurogenesis-csharp.md#autonomous-learning-engine) - Self-improvement
4. [Context Understanding](architecture/context-understanding-csharp.md) - Conversation memory and reference resolution

**Key Topics:**

- Template-based agent creation
- Multi-agent collaborative research
- Autonomous knowledge acquisition
- Performance-based adaptation
- Human-like context understanding

### For DevOps/Production Engineers

**Focus On:**

1. [Production Deployment](architecture/production-deployment-csharp.md) - Kubernetes and scaling
2. [Microservices](architecture/microservices-csharp.md) - Service architecture patterns
3. [Knowledge Substrate](architecture/production-deployment-csharp.md#knowledge-substrate-architecture) - Three-layer storage

**Key Topics:**

- Kubernetes operators and CRDs
- Cognitive tier policies
- Auto-scaling strategies
- Cost optimization
- Monitoring and observability

---

## 🎯 Implementation Phases

### Current Status: Architecture Definition Phase ✅

**Completed:**

- ✅ Comprehensive architecture documentation (9 core documents)
- ✅ C#/.NET technology stack definition
- ✅ Zero-dependency implementation strategy
- ✅ Detailed development roadmap
- ✅ Dual-path processing architecture (Fast Path + Cognitive Workspace)
- ✅ Global Workspace Theory integration
- ✅ Production deployment architecture
- ✅ Context understanding system design
- ✅ Cognitive synthesis pipeline design
- ✅ AGI enhancement roadmap

### Next Steps: Foundation Phase

**Phase 1 (Weeks 1-2): Foundation & Core Component Setup**

Focus: Setup C# projects and basic scaffolding

Tasks:

1. Initialize .NET solution structure
2. Create Orchestrator service skeleton (ASP.NET Core)
3. Create first static agent (Lightbulb_AI)
4. Setup Docker containerization
5. Implement basic agent registry

**Deliverable**: Orchestrator can ping a containerized agent

See: [Phase 1 Implementation Guide](roadmap/phase-1-foundation.md)

---

## 📊 Project Structure

```
myriad-csharp/
├── architecture/                    # 📚 Architecture documentation
│   ├── core-philosophy.md          # Design principles
│   ├── system-overview-csharp.md   # System architecture
│   ├── graph-intelligence-csharp.md # Graph DB & Hebbian learning
│   ├── microservices-csharp.md     # Service architecture
│   ├── neurogenesis-csharp.md      # Dynamic agent creation
│   ├── context-understanding-csharp.md # Conversation memory
│   ├── cognitive-synthesizer-csharp.md # Output synthesis
│   └── production-deployment-csharp.md # Production deployment
│
├── src/                            # 💻 Source code (planned)
│   ├── Myriad.Services.Orchestrator/
│   ├── Myriad.Services.GraphDatabase/
│   ├── Myriad.Services.InputProcessor/
│   ├── Myriad.Services.OutputProcessor/
│   ├── Myriad.Agents.Static/
│   ├── Myriad.Core.Graph/
│   ├── Myriad.Core.Intelligence/
│   ├── Myriad.Core.Lifecycle/
│   ├── Myriad.Core.Learning/
│   └── Myriad.Common/
│
├── tests/                          # 🧪 Tests (planned)
│   ├── Myriad.Tests.Unit/
│   └── Myriad.Tests.Integration/
│
├── roadmap/                        # 🗺️ Implementation guides
│   ├── README.md                   # Roadmap overview
│   ├── phase-1-foundation.md       # Phase 1: Foundation (2-3 weeks)
│   ├── phase-2-core-services.md    # Phase 2: Core Services (3-4 weeks)
│   ├── phase-3-mvp.md              # Phase 3: MVP Complete (2-3 weeks)
│   ├── phase-4-advanced-features.md # Phase 4: Advanced Features (4-5 weeks)
│   └── phase-5-production.md       # Phase 5: Production (5-6 weeks)
│
├── design and concept.md           # 📐 Architectural blueprint
├── README.md                       # 📖 Project overview
├── INDEX.md                        # 📇 This file
└── docker-compose.yml             # 🐳 Service orchestration (planned)
```

---

## 🔗 External Resources

### .NET & C# Learning

- [ASP.NET Core Documentation](https://docs.microsoft.com/aspnet/core)
- [C# Language Reference](https://docs.microsoft.com/dotnet/csharp)
- [Minimal APIs Overview](https://docs.microsoft.com/aspnet/core/fundamentals/minimal-apis)

### .NET Deployment & Packaging

- [.NET Self-Contained Deployments](https://docs.microsoft.com/dotnet/core/deploying)
- [.NET Publishing Options](https://docs.microsoft.com/dotnet/core/tools/dotnet-publish)
- [Process Management in .NET](https://docs.microsoft.com/dotnet/api/system.diagnostics.process)

### Architecture Patterns

- [Microservices Patterns](https://microservices.io/patterns)
- [Circuit Breaker Pattern](https://docs.microsoft.com/azure/architecture/patterns/circuit-breaker)
- [Event-Driven Architecture](https://docs.microsoft.com/azure/architecture/guide/architecture-styles/event-driven)

---

## 📝 Document Conventions

### File Naming

- **Markdown Files**: Use lowercase with hyphens (e.g., `system-overview-csharp.md`)
- **C# Projects**: Use PascalCase with dots (e.g., `Myriad.Services.Orchestrator`)
- **Architecture Docs**: Prefix with category in folder structure

### Cross-References

Links use relative paths:

- Within architecture folder: `[Graph Intelligence](graph-intelligence-csharp.md)`
- To root documents: `[README](../README.md)`
- To code (planned): `[OrchestratorService.cs](../src/Myriad.Services.Orchestrator/OrchestratorService.cs)`

### Code Examples

All code examples are in C# 10+ with:

- XML documentation comments
- Nullable reference types enabled
- Modern C# features (records, pattern matching, etc.)

---

## 🚀 Next Steps

1. **Review Documentation** - Read architecture documents thoroughly
2. **Setup Development Environment** - Install .NET SDK 8.0+
3. **Follow Roadmap** - Start with [Phase 1: Foundation](roadmap/phase-1-foundation.md)
4. **Build Incrementally** - Complete each phase before moving to the next
5. **Test Continuously** - Validate acceptance criteria at each step
6. **Deploy to Production** - Complete all 5 phases for full system (16-21 weeks total)

---

## 📞 Contributing & Support

This is an architecture definition and educational project. The focus is on implementing the complete system from scratch in C# without external dependencies.

**Contribution Areas:**

- Implementing core services (ASP.NET Core)
- Custom graph database algorithms
- Agent templates and neurogenesis
- Testing and validation
- Documentation improvements

**Philosophy**: Every component must be built from scratch to maintain the zero-dependency principle and educational value.

---

**Last Updated**: 2025-01-10
**Version**: 5.0 C#/.NET Edition
**Status**: Architecture Definition Complete - Ready for Implementation

**Documentation Stats:**

- 📄 9 Architecture Documents
- 🔧 250+ Code Examples
- 📊 Complete Implementation Roadmaps
- 🏗️ Production-Ready Designs
- 🧠 Dual-Path Processing Architecture
- 🌐 Global Workspace Theory Integration

[Back to README](README.md) | [Start with Core Philosophy](architecture/core-philosophy.md)

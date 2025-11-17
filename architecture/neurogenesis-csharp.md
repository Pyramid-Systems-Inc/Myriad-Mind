# Myriad Cognitive Architecture - Neurogenesis & Autonomous Learning (C#/.NET Edition)

**Architecture Documentation** | [Overview](system-overview-csharp.md) | [Graph Intelligence](graph-intelligence-csharp.md) | [Microservices](microservices-csharp.md)

Comprehensive documentation of the dynamic agent creation system (neurogenesis), autonomous learning engine, and template-based agent generation - all built from scratch in C# without external dependencies.

[← Back to Index](../INDEX.md#architecture) | [Implementation Guide →](implementation-guide.md)

---

## Table of Contents

- [Neurogenesis Overview](#neurogenesis-overview)
- [Biomimetic Pipeline](#biomimetic-pipeline)
- [Dynamic Lifecycle Manager](#dynamic-lifecycle-manager)
- [Template-Based Agent Creation](#template-based-agent-creation)
- [Multi-Agent Research System](#multi-agent-research-system)
- [Autonomous Learning Engine](#autonomous-learning-engine)
- [Code Generation with Roslyn](#code-generation-with-roslyn)
- [Deployment Automation](#deployment-automation)
- [Implementation Guidelines](#implementation-guidelines)

---

## Neurogenesis Overview

### Biological Inspiration

**Neurogenesis** is the process by which the brain creates new neurons. In the Myriad architecture, this principle is implemented as the **dynamic creation of new agents** when the system encounters unknown concepts.

**Key Principle**: *The system learns not by retraining existing models, but by creating new, specialized agents.*

### Architecture Goals

The neurogenesis system enables the Myriad architecture to:

1. **Detect Knowledge Gaps**: Identify when a query requires concepts not currently in the system
2. **Research Collaboratively**: Use existing agents to gather information about new concepts
3. **Generate Agents**: Automatically create C# code for new agents using templates
4. **Deploy Autonomously**: Build, containerize, and deploy new agents without human intervention
5. **Learn Continuously**: Improve new agents through autonomous learning sessions

### Zero-Dependency Implementation

All neurogenesis components are built from scratch in C#:

- ✅ **Code Generation**: Using Roslyn (Microsoft.CodeAnalysis)
- ✅ **Template Engine**: Custom C# string interpolation and Roslyn SyntaxFactory
- ✅ **Build Automation**: Using `System.Diagnostics.Process` to invoke `dotnet`
- ✅ **Container Management**: Using Docker SDK for .NET (Docker.DotNet)
- ✅ **Knowledge Acquisition**: Custom HTTP-based research coordination
- ✅ **Graph Registration**: Custom graph database integration

---

## Biomimetic Pipeline

### Five-Phase Neurogenesis Process

```csharp
namespace Myriad.Core.Lifecycle
{
    /// <summary>
    /// Represents the complete neurogenesis pipeline
    /// </summary>
    public class NeurogenesisPipeline
    {
        public enum Phase
        {
            Detection,      // Identify unknown concept
            Research,       // Gather information
            Templating,     // Select agent template
            Generation,     // Generate C# code
            Deployment      // Build and deploy
        }
        
        public async Task<Agent?> ExecuteAsync(
            string concept,
            string intent,
            CancellationToken cancellationToken)
        {
            // Phase 1: Detection
            var needsNewAgent = await DetectKnowledgeGapAsync(concept, cancellationToken);
            if (!needsNewAgent) return null;
            
            // Phase 2: Research
            var knowledgeBase = await ConductResearchAsync(concept, cancellationToken);
            
            // Phase 3: Templating
            var template = await SelectTemplateAsync(knowledgeBase, intent, cancellationToken);
            
            // Phase 4: Generation
            var agentCode = await GenerateAgentCodeAsync(
                template, 
                concept, 
                knowledgeBase, 
                cancellationToken);
            
            // Phase 5: Deployment
            var deployedAgent = await DeployAgentAsync(agentCode, concept, cancellationToken);
            
            // Post-deployment: Start autonomous learning
            await StartAutonomousLearningAsync(deployedAgent, cancellationToken);
            
            return deployedAgent;
        }
    }
}
```

### Process Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    User Query Received                       │
│         "What is quantum entanglement?"                      │
└────────────────────┬────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────┐
│    Phase 1: DETECTION - Concept Gap Identification          │
│    - Query GraphDB for "quantum_entanglement"                │
│    - No agent found → Trigger neurogenesis                   │
└────────────────────┬────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────┐
│    Phase 2: RESEARCH - Multi-Agent Collaboration            │
│    - Activate Physics_AI for context                         │
│    - Activate Science_Domain_AI for related concepts         │
│    - Research Coordinator aggregates knowledge               │
└────────────────────┬────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────┐
│    Phase 3: TEMPLATING - Agent Type Selection               │
│    - Analyze research results                                │
│    - Complexity: HIGH → FactBaseEnhanced                     │
│    - Intent: "define" → Select definition template           │
└────────────────────┬────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────┐
│    Phase 4: GENERATION - Code Creation (Roslyn)             │
│    - Load FactBaseEnhanced template                          │
│    - Generate C# code with Roslyn SyntaxFactory              │
│    - Inject knowledge from research phase                    │
│    - Create Program.cs, Models.cs, Dockerfile                │
└────────────────────┬────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────┐
│    Phase 5: DEPLOYMENT - Build & Launch                     │
│    - dotnet build (Process invocation)                       │
│    - dotnet publish --self-contained                         │
│    - Start process on available port                         │
│    - Health check validation                                 │
│    - Register in GraphDB                                     │
└────────────────────┬────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────┐
│         New Agent Active: Quantum_Entanglement_AI            │
│         Endpoint: http://localhost:6001                      │
│         Status: Learning Phase (Autonomous)                  │
└─────────────────────────────────────────────────────────────┘
```

---

## Dynamic Lifecycle Manager

### Core Implementation

**Location**: `src/Myriad.Core.Lifecycle/DynamicLifecycleManager.cs`

```csharp
namespace Myriad.Core.Lifecycle
{
    /// <summary>
    /// Manages the complete lifecycle of dynamic agents
    /// </summary>
    public class DynamicLifecycleManager
    {
        private readonly IGraphDatabase _graphDb;
        private readonly IConceptDetector _conceptDetector;
        private readonly IResearchCoordinator _researchCoordinator;
        private readonly ITemplateSelector _templateSelector;
        private readonly ICodeGenerator _codeGenerator;
        private readonly IAgentDeployer _agentDeployer;
        private readonly ILogger<DynamicLifecycleManager> _logger;
        
        // Track active dynamic agents
        private readonly ConcurrentDictionary<string, AgentLifecycle> _activeAgents;
        
        public DynamicLifecycleManager(
            IGraphDatabase graphDb,
            IConceptDetector conceptDetector,
            IResearchCoordinator researchCoordinator,
            ITemplateSelector templateSelector,
            ICodeGenerator codeGenerator,
            IAgentDeployer agentDeployer,
            ILogger<DynamicLifecycleManager> logger)
        {
            _graphDb = graphDb;
            _conceptDetector = conceptDetector;
            _researchCoordinator = researchCoordinator;
            _templateSelector = templateSelector;
            _codeGenerator = codeGenerator;
            _agentDeployer = agentDeployer;
            _logger = logger;
            _activeAgents = new ConcurrentDictionary<string, AgentLifecycle>();
        }
        
        /// <summary>
        /// Create a new agent for an unknown concept
        /// </summary>
        public async Task<Agent?> CreateAgentAsync(
            string concept,
            string intent,
            CancellationToken cancellationToken)
        {
            _logger.LogInformation(
                "Starting neurogenesis for concept: {Concept}, intent: {Intent}",
                concept, intent);
            
            try
            {
                // Phase 1: Detect if agent needed
                var exists = await _conceptDetector.ConceptExistsAsync(
                    concept, 
                    cancellationToken);
                
                if (exists)
                {
                    _logger.LogInformation("Agent already exists for concept: {Concept}", concept);
                    return null;
                }
                
                // Phase 2: Research
                _logger.LogInformation("Conducting research for: {Concept}", concept);
                var knowledgeBase = await _researchCoordinator.ConductResearchAsync(
                    concept,
                    cancellationToken);
                
                if (knowledgeBase.Facts.Count == 0)
                {
                    _logger.LogWarning("No knowledge found for concept: {Concept}", concept);
                    return null;
                }
                
                // Phase 3: Select template
                var template = await _templateSelector.SelectTemplateAsync(
                    knowledgeBase,
                    intent,
                    cancellationToken);
                
                _logger.LogInformation(
                    "Selected template: {Template} for concept: {Concept}",
                    template.Name, concept);
                
                // Phase 4: Generate code
                var generatedCode = await _codeGenerator.GenerateAsync(
                    template,
                    concept,
                    knowledgeBase,
                    cancellationToken);
                
                // Phase 5: Deploy
                var deployedAgent = await _agentDeployer.DeployAsync(
                    generatedCode,
                    concept,
                    cancellationToken);
                
                // Register in graph
                await RegisterAgentInGraphAsync(deployedAgent, concept, cancellationToken);
                
                // Track lifecycle
                _activeAgents[concept] = new AgentLifecycle
                {
                    Agent = deployedAgent,
                    CreatedAt = DateTime.UtcNow,
                    Status = AgentStatus.Active
                };
                
                _logger.LogInformation(
                    "Neurogenesis complete for {Concept}. Agent endpoint: {Endpoint}",
                    concept, deployedAgent.Endpoint);
                
                return deployedAgent;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Neurogenesis failed for concept: {Concept}", concept);
                return null;
            }
        }
        
        /// <summary>
        /// Register new agent in graph database
        /// </summary>
        private async Task RegisterAgentInGraphAsync(
            Agent agent,
            string concept,
            CancellationToken cancellationToken)
        {
            // Create agent node
            var agentNode = new AgentNode
            {
                Id = Guid.NewGuid().ToString(),
                Name = agent.Name,
                Type = agent.Type,
                Endpoint = agent.Endpoint,
                Port = agent.Port,
                Capabilities = agent.Capabilities,
                Description = agent.Description,
                Status = AgentStatus.Healthy,
                CreatedAt = DateTime.UtcNow
            };
            
            await _graphDb.UpsertNodeAsync(agentNode, cancellationToken);
            
            // Create concept node if not exists
            var conceptNode = await _graphDb.FindNodeAsync(
                n => n is ConceptNode cn && cn.Name == concept,
                cancellationToken);
            
            if (conceptNode == null)
            {
                conceptNode = new ConceptNode
                {
                    Id = Guid.NewGuid().ToString(),
                    Name = concept,
                    Domain = DetermineDomain(concept),
                    CreatedAt = DateTime.UtcNow
                };
                
                await _graphDb.UpsertNodeAsync(conceptNode, cancellationToken);
            }
            
            // Create HANDLES_CONCEPT edge
            var edge = new HandlesConceptEdge(agentNode.Id, conceptNode.Id)
            {
                Weight = 0.7f, // Initial weight for new agents
                DecayRate = 0.01f
            };
            
            await _graphDb.AddEdgeAsync(edge, cancellationToken);
            
            _logger.LogInformation(
                "Registered agent {AgentName} in graph for concept {Concept}",
                agent.Name, concept);
        }
        
        /// <summary>
        /// Monitor and manage agent health
        /// </summary>
        public async Task MonitorAgentHealthAsync(CancellationToken cancellationToken)
        {
            foreach (var lifecycle in _activeAgents.Values)
            {
                try
                {
                    var isHealthy = await CheckAgentHealthAsync(
                        lifecycle.Agent, 
                        cancellationToken);
                    
                    lifecycle.Status = isHealthy 
                        ? AgentStatus.Active 
                        : AgentStatus.Degraded;
                    
                    lifecycle.LastHealthCheck = DateTime.UtcNow;
                }
                catch (Exception ex)
                {
                    _logger.LogError(
                        ex, 
                        "Health check failed for agent: {AgentName}",
                        lifecycle.Agent.Name);
                    
                    lifecycle.Status = AgentStatus.Failed;
                }
            }
        }
        
        private async Task<bool> CheckAgentHealthAsync(
            Agent agent,
            CancellationToken cancellationToken)
        {
            try
            {
                using var httpClient = new HttpClient { Timeout = TimeSpan.FromSeconds(5) };
                var response = await httpClient.GetAsync(
                    $"{agent.Endpoint}/health", 
                    cancellationToken);
                
                return response.IsSuccessStatusCode;
            }
            catch
            {
                return false;
            }
        }
    }
    
    public class AgentLifecycle
    {
        public required Agent Agent { get; init; }
        public DateTime CreatedAt { get; init; }
        public AgentStatus Status { get; set; }
        public DateTime? LastHealthCheck { get; set; }
        public int SuccessfulQueries { get; set; }
        public int FailedQueries { get; set; }
    }
}
```

---

## Template-Based Agent Creation

### Agent Templates

Four specialized templates for different agent types:

#### 1. FactBaseBasic Template

**Purpose**: Simple knowledge storage and retrieval  
**Use Case**: Definitions, basic facts, entity information  
**Location**: `templates/FactBaseBasicTemplate.cs`

```csharp
namespace Myriad.Templates
{
    /// <summary>
    /// Template for basic fact-based agents
    /// </summary>
    public class FactBaseBasicTemplate : IAgentTemplate
    {
        public string Name => "FactBaseBasic";
        public AgentType Type => AgentType.FactBaseBasic;
        
        public string GenerateCode(
            string conceptName,
            Dictionary<string, object> knowledge)
        {
            var className = $"{ToPascalCase(conceptName)}Agent";
            var facts = SerializeFacts(knowledge);
            
            return $$"""
                using Microsoft.AspNetCore.Builder;
                using Microsoft.AspNetCore.Http;
                
                var builder = WebApplication.CreateBuilder(args);
                var app = builder.Build();
                
                // Knowledge base
                var knowledgeBase = new Dictionary<string, object>
                {
                    {{facts}}
                };
                
                // Health endpoint
                app.MapGet("/health", () => new
                {
                    status = "healthy",
                    agent = "{{className}}",
                    type = "FactBaseBasic",
                    timestamp = DateTime.UtcNow
                });
                
                // Process endpoint
                app.MapPost("/process", (QueryRequest request) =>
                {
                    return new AgentResponse
                    {
                        AgentId = "{{className}}",
                        Status = "success",
                        Data = knowledgeBase,
                        Confidence = 0.95f,
                        ProcessingTimeMs = 5
                    };
                });
                
                app.Run();
                
                record QueryRequest(string Query, string Intent);
                record AgentResponse
                {
                    public required string AgentId { get; init; }
                    public required string Status { get; init; }
                    public required Dictionary<string, object> Data { get; init; }
                    public float Confidence { get; init; }
                    public long ProcessingTimeMs { get; init; }
                }
                """;
        }
        
        private string SerializeFacts(Dictionary<string, object> knowledge)
        {
            var lines = new List<string>();
            
            foreach (var (key, value) in knowledge)
            {
                var valueStr = value switch
                {
                    string s => $"\"{s.Replace("\"", "\\\"")}\"",
                    int i => i.ToString(),
                    float f => $"{f}f",
                    bool b => b.ToString().ToLower(),
                    _ => $"\"{value}\""
                };
                
                lines.Add($"    [\"{key}\"] = {valueStr}");
            }
            
            return string.Join(",\n", lines);
        }
        
        private string ToPascalCase(string str) =>
            string.Concat(
                str.Split('_', ' ')
                   .Select(word => char.ToUpper(word[0]) + word[1..].ToLower()));
    }
}
```

#### 2. FactBaseEnhanced Template

**Purpose**: Advanced knowledge with relationships and context  
**Use Case**: Complex concepts, multi-faceted information  
**Features**:

- Related concepts tracking
- Confidence scoring
- Context-aware responses
- Multi-format data support

```csharp
public class FactBaseEnhancedTemplate : IAgentTemplate
{
    public string Name => "FactBaseEnhanced";
    public AgentType Type => AgentType.FactBaseEnhanced;
    
    public string GenerateCode(string conceptName, Dictionary<string, object> knowledge)
    {
        // Enhanced template with:
        // - Related concepts graph
        // - Confidence scoring
        // - Context analysis
        // - Multi-format responses
        
        return $$"""
            // Enhanced fact-base agent with relationship tracking
            // ... (similar structure but with additional features)
            """;
    }
}
```

#### 3. FunctionBasic Template

**Purpose**: Computational and transformation tasks  
**Use Case**: Calculations, data processing, conversions  
**Features**:

- Input validation
- Computation logic
- Result formatting

```csharp
public class FunctionBasicTemplate : IAgentTemplate
{
    public string Name => "FunctionBasic";
    public AgentType Type => AgentType.FunctionBasic;
    
    public string GenerateCode(string functionName, Dictionary<string, object> config)
    {
        // Function agent template with:
        // - Parameter validation
        // - Computation execution
        // - Error handling
        // - Result caching
        
        return $$"""
            // Function executor agent
            """;
    }
}
```

#### 4. SpecialistBasic Template

**Purpose**: Domain-specific processing  
**Use Case**: Classification, pattern matching, analysis  
**Features**:

- Domain-specific logic
- Pattern recognition
- Multi-step processing

---

## Multi-Agent Research System

### Research Coordinator

```csharp
namespace Myriad.Core.Lifecycle.Research
{
    /// <summary>
    /// Coordinates multi-agent research for new concepts
    /// </summary>
    public class ResearchCoordinator : IResearchCoordinator
    {
        private readonly IGraphDatabase _graphDb;
        private readonly IHttpClientFactory _httpClientFactory;
        private readonly ILogger<ResearchCoordinator> _logger;
        
        public async Task<KnowledgeBase> ConductResearchAsync(
            string concept,
            CancellationToken cancellationToken)
        {
            _logger.LogInformation("Starting research for: {Concept}", concept);
            
            // Step 1: Identify related agents
            var relatedAgents = await FindRelatedAgentsAsync(concept, cancellationToken);
            
            // Step 2: Query agents in parallel
            var researchTasks = relatedAgents.Select(agent =>
                QueryAgentForResearchAsync(agent, concept, cancellationToken));
            
            var results = await Task.WhenAll(researchTasks);
            
            // Step 3: Aggregate knowledge
            var knowledgeBase = AggregateKnowledge(concept, results);
            
            _logger.LogInformation(
                "Research complete for {Concept}: {FactCount} facts gathered",
                concept, knowledgeBase.Facts.Count);
            
            return knowledgeBase;
        }
        
        private async Task<List<AgentNode>> FindRelatedAgentsAsync(
            string concept,
            CancellationToken cancellationToken)
        {
            // Find agents in same domain or with related capabilities
            var domain = DetermineDomain(concept);
            
            var agents = await _graphDb.FindNodesAsync(
                n => n is AgentNode an && 
                     (an.Capabilities.Any(c => c.Contains(domain, StringComparison.OrdinalIgnoreCase)) ||
                      an.Status == AgentStatus.Healthy),
                cancellationToken);
            
            return agents.OfType<AgentNode>().Take(5).ToList();
        }
        
        private async Task<ResearchResult> QueryAgentForResearchAsync(
            AgentNode agent,
            string concept,
            CancellationToken cancellationToken)
        {
            try
            {
                var httpClient = _httpClientFactory.CreateClient();
                
                var request = new
                {
                    query = $"What do you know about {concept}?",
                    intent = "research",
                    mode = "knowledge_extraction"
                };
                
                var response = await httpClient.PostAsJsonAsync(
                    $"{agent.Endpoint}/process",
                    request,
                    cancellationToken);
                
                if (response.IsSuccessStatusCode)
                {
                    var content = await response.Content.ReadAsStringAsync(cancellationToken);
                    var data = SimpleJsonParser.Parse(content);
                    
                    return new ResearchResult
                    {
                        AgentId = agent.Name,
                        Success = true,
                        Data = data,
                        Confidence = 0.8f
                    };
                }
                
                return ResearchResult.Failed(agent.Name);
            }
            catch (Exception ex)
            {
                _logger.LogWarning(
                    ex,
                    "Research query failed for agent: {AgentName}",
                    agent.Name);
                
                return ResearchResult.Failed(agent.Name);
            }
        }
        
        private KnowledgeBase AggregateKnowledge(
            string concept,
            ResearchResult[] results)
        {
            var knowledgeBase = new KnowledgeBase
            {
                Concept = concept,
                Facts = new Dictionary<string, object>(),
                RelatedConcepts = new List<string>(),
                Sources = new List<string>()
            };
            
            foreach (var result in results.Where(r => r.Success))
            {
                // Extract facts
                if (result.Data.TryGetValue("data", out var dataObj) &&
                    dataObj is Dictionary<string, object> facts)
                {
                    foreach (var (key, value) in facts)
                    {
                        if (!knowledgeBase.Facts.ContainsKey(key))
                        {
                            knowledgeBase.Facts[key] = value;
                        }
                    }
                }
                
                // Extract related concepts
                if (result.Data.TryGetValue("related_concepts", out var relatedObj) &&
                    relatedObj is List<string> related)
                {
                    knowledgeBase.RelatedConcepts.AddRange(
                        related.Where(c => !knowledgeBase.RelatedConcepts.Contains(c)));
                }
                
                knowledgeBase.Sources.Add(result.AgentId);
            }
            
            return knowledgeBase;
        }
        
        private string DetermineDomain(string concept)
        {
            // Simple keyword-based domain classification
            var scienceKeywords = new[] { "quantum", "atom", "physics", "chemistry" };
            var techKeywords = new[] { "software", "computer", "algorithm", "data" };
            var historyKeywords = new[] { "war", "revolution", "ancient", "era" };
            
            var lower = concept.ToLowerInvariant();
            
            if (scienceKeywords.Any(k => lower.Contains(k))) return "Science";
            if (techKeywords.Any(k => lower.Contains(k))) return "Technology";
            if (historyKeywords.Any(k => lower.Contains(k))) return "History";
            
            return "General";
        }
    }
    
    public class KnowledgeBase
    {
        public required string Concept { get; init; }
        public Dictionary<string, object> Facts { get; init; } = new();
        public List<string> RelatedConcepts { get; init; } = new();
        public List<string> Sources { get; init; } = new();
        public float Complexity { get; set; } = 0.5f;
    }
    
    public class ResearchResult
    {
        public required string AgentId { get; init; }
        public bool Success { get; init; }
        public Dictionary<string, object> Data { get; init; } = new();
        public float Confidence { get; init; }
        
        public static ResearchResult Failed(string agentId) => new()
        {
            AgentId = agentId,
            Success = false,
            Confidence = 0f
        };
    }
}
```

---

## Autonomous Learning Engine

### Five-Phase Learning System

```csharp
namespace Myriad.Core.Learning
{
    /// <summary>
    /// Autonomous learning engine for continuous agent improvement
    /// </summary>
    public class AutonomousLearningEngine
    {
        private readonly IGraphDatabase _graphDb;
        private readonly IResearchCoordinator _researchCoordinator;
        private readonly ILogger<AutonomousLearningEngine> _logger;
        
        public async Task StartLearningSessionAsync(
            Agent agent,
            CancellationToken cancellationToken)
        {
            _logger.LogInformation(
                "Starting autonomous learning session for: {AgentName}",
                agent.Name);
            
            // Phase 1: Bootstrap - Initial knowledge gathering
            await BootstrapPhaseAsync(agent, cancellationToken);
            
            // Phase 2: Research - Deep knowledge acquisition
            await ResearchPhaseAsync(agent, cancellationToken);
            
            // Phase 3: Development - Capability expansion
            await DevelopmentPhaseAsync(agent, cancellationToken);
            
            // Phase 4: Optimization - Performance tuning
            await OptimizationPhaseAsync(agent, cancellationToken);
            
            // Phase 5: Validation - Quality assurance
            await ValidationPhaseAsync(agent, cancellationToken);
            
            _logger.LogInformation(
                "Learning session complete for: {AgentName}",
                agent.Name);
        }
        
        private async Task BootstrapPhaseAsync(
            Agent agent,
            CancellationToken cancellationToken)
        {
            _logger.LogInformation("Bootstrap phase for: {AgentName}", agent.Name);
            
            // Gather initial knowledge from graph neighbors
            var neighbors = await FindNeighborAgentsAsync(agent, cancellationToken);
            
            foreach (var neighbor in neighbors)
            {
                await ExchangeKnowledgeAsync(agent, neighbor, cancellationToken);
            }
        }
        
        private async Task ResearchPhaseAsync(
            Agent agent,
            CancellationToken cancellationToken)
        {
            _logger.LogInformation("Research phase for: {AgentName}", agent.Name);
            
            // Conduct collaborative research with related agents
            var concept = ExtractConceptFromAgentName(agent.Name);
            var research = await _researchCoordinator.ConductResearchAsync(
                concept,
                cancellationToken);
            
            // Expand agent knowledge
            await ExpandKnowledgeAsync(agent, research, cancellationToken);
        }
        
        private async Task DevelopmentPhaseAsync(
            Agent agent,
            CancellationToken cancellationToken)
        {
            _logger.LogInformation("Development phase for: {AgentName}", agent.Name);
            
            // Develop new capabilities based on learned knowledge
            var newCapabilities = await IdentifyCapabilityGapsAsync(agent, cancellationToken);
            
            foreach (var capability in newCapabilities)
            {
                await DevelopCapabilityAsync(agent, capability, cancellationToken);
            }
        }
        
        private async Task OptimizationPhaseAsync(
            Agent agent,
            CancellationToken cancellationToken)
        {
            _logger.LogInformation("Optimization phase for: {AgentName}", agent.Name);
            
            // Optimize response time and accuracy
            await OptimizeResponseTimeAsync(agent, cancellationToken);
            await OptimizeAccuracyAsync(agent, cancellationToken);
        }
        
        private async Task ValidationPhaseAsync(
            Agent agent,
            CancellationToken cancellationToken)
        {
            _logger.LogInformation("Validation phase for: {AgentName}", agent.Name);
            
            // Validate agent performance
            var testQueries = GenerateTestQueries(agent);
            var results = await RunTestsAsync(agent, testQueries, cancellationToken);
            
            _logger.LogInformation(
                "Validation complete: {SuccessRate}% success rate",
                results.SuccessRate * 100);
        }
        
        private string ExtractConceptFromAgentName(string agentName) =>
            agentName.Replace("_AI", "").Replace("_", " ");
    }
}
```

---

## Code Generation with Roslyn

### Roslyn-Based Code Generator

```csharp
using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.CSharp;
using Microsoft.CodeAnalysis.CSharp.Syntax;

namespace Myriad.Core.Lifecycle.CodeGen
{
    /// <summary>
    /// Generates C# agent code using Roslyn
    /// </summary>
    public class RoslynCodeGenerator : ICodeGenerator
    {
        public async Task<GeneratedCode> GenerateAsync(
            IAgentTemplate template,
            string conceptName,
            KnowledgeBase knowledgeBase,
            CancellationToken cancellationToken)
        {
            // Generate code using template
            var programCode = template.GenerateCode(conceptName, knowledgeBase.Facts);
            
            // Generate project file
            var projectFile = GenerateProjectFile(conceptName);
            
            // Generate Dockerfile
            var dockerfile = GenerateDockerfile(conceptName);
            
            // Validate syntax using Roslyn
            var syntaxTree = CSharpSyntaxTree.ParseText(programCode);
            var diagnostics = syntaxTree.GetDiagnostics();
            
            if (diagnostics.Any(d => d.Severity == DiagnosticSeverity.Error))
            {
                throw new CodeGenerationException(
                    "Generated code contains syntax errors: " +
                    string.Join(", ", diagnostics.Select(d => d.GetMessage())));
            }
            
            return new GeneratedCode
            {
                ConceptName = conceptName,
                ProgramCs = programCode,
                ProjectFile = projectFile,
                Dockerfile = dockerfile,
                TemplateName = template.Name
            };
        }
        
        private string GenerateProjectFile(string conceptName)
        {
            return $$"""
                <Project Sdk="Microsoft.NET.Sdk.Web">
                  <PropertyGroup>
                    <TargetFramework>net8.0</TargetFramework>
                    <Nullable>enable</Nullable>
                    <ImplicitUsings>enable</ImplicitUsings>
                  </PropertyGroup>
                </Project>
                """;
        }
        
        private string GenerateDockerfile(string conceptName)
        {
            return $$"""
                FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS base
                WORKDIR /app
                EXPOSE 80
                
                FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
                WORKDIR /src
                COPY ["{{conceptName}}.csproj", "./"]
                RUN dotnet restore
                COPY . .
                RUN dotnet build -c Release -o /app/build
                
                FROM build AS publish
                RUN dotnet publish -c Release -o /app/publish
                
                FROM base AS final
                WORKDIR /app
                COPY --from=publish /app/publish .
                ENTRYPOINT ["dotnet", "{{conceptName}}.dll"]
                """;
        }
    }
    
    public class GeneratedCode
    {
        public required string ConceptName { get; init; }
        public required string ProgramCs { get; init; }
        public required string ProjectFile { get; init; }
        public required string Dockerfile { get; init; }
        public required string TemplateName { get; init; }
    }
}
```

---

## Deployment Automation

### Agent Deployer

```csharp
namespace Myriad.Core.Lifecycle.Deployment
{
    /// <summary>
    /// Automates agent building and deployment
    /// </summary>
    public class AgentDeployer : IAgentDeployer
    {
        private readonly ILogger<AgentDeployer> _logger;
        private readonly string _workspaceRoot;
        private readonly PortAllocator _portAllocator;
        
        public AgentDeployer(ILogger<AgentDeployer> logger, PortAllocator portAllocator)
        {
            _logger = logger;
            _portAllocator = portAllocator;
            _workspaceRoot = Path.Combine(
                AppContext.BaseDirectory,
                "dynamic_agents");
            
            Directory.CreateDirectory(_workspaceRoot);
        }
        
        public async Task<Agent> DeployAsync(
            GeneratedCode code,
            string concept,
            CancellationToken cancellationToken)
        {
            var agentPath = Path.Combine(_workspaceRoot, code.ConceptName);
            Directory.CreateDirectory(agentPath);
            
            // Write files
            await File.WriteAllTextAsync(
                Path.Combine(agentPath, "Program.cs"),
                code.ProgramCs,
                cancellationToken);
            
            await File.WriteAllTextAsync(
                Path.Combine(agentPath, $"{code.ConceptName}.csproj"),
                code.ProjectFile,
                cancellationToken);
            
            // Build
            _logger.LogInformation("Building agent: {ConceptName}", code.ConceptName);
            await BuildAgentAsync(agentPath, cancellationToken);
            
            // Publish
            _logger.LogInformation("Publishing agent: {ConceptName}", code.ConceptName);
            await PublishAgentAsync(agentPath, cancellationToken);
            
            // Start process
            var port = _portAllocator.AllocatePort();
            var process = await StartAgentProcessAsync(agentPath, port, cancellationToken);
            
            // Wait for health check
            var endpoint = $"http://localhost:{port}";
            await WaitForHealthyAsync(endpoint, cancellationToken);
            
            return new Agent
            {
                Name = $"{code.ConceptName}_AI",
                Type = AgentType.DynamicAgent,
                Endpoint = endpoint,
                Port = port,
                Capabilities = new List<string> { concept },
                Description = $"Dynamically created agent for {concept}",
                ProcessId = process.Id
            };
        }
        
        private async Task BuildAgentAsync(string projectPath, CancellationToken cancellationToken)
        {
            var startInfo = new ProcessStartInfo
            {
                FileName = "dotnet",
                Arguments = "build -c Release",
                WorkingDirectory = projectPath,
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                UseShellExecute = false
            };
            
            using var process = Process.Start(startInfo);
            if (process == null)
                throw new DeploymentException("Failed to start build process");
            
            await process.WaitForExitAsync(cancellationToken);
            
            if (process.ExitCode != 0)
            {
                var error = await process.StandardError.ReadToEndAsync(cancellationToken);
                throw new DeploymentException($"Build failed: {error}");
            }
        }
        
        private async Task PublishAgentAsync(string projectPath, CancellationToken cancellationToken)
        {
            var startInfo = new ProcessStartInfo
            {
                FileName = "dotnet",
                Arguments = "publish -c Release -o ./publish --self-contained false",
                WorkingDirectory = projectPath,
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                UseShellExecute = false
            };
            
            using var process = Process.Start(startInfo);
            if (process == null)
                throw new DeploymentException("Failed to start publish process");
            
            await process.WaitForExitAsync(cancellationToken);
            
            if (process.ExitCode != 0)
            {
                var error = await process.StandardError.ReadToEndAsync(cancellationToken);
                throw new DeploymentException($"Publish failed: {error}");
            }
        }
        
        private async Task<Process> StartAgentProcessAsync(
            string projectPath,
            int port,
            CancellationToken cancellationToken)
        {
            var dllPath = Directory.GetFiles(
                Path.Combine(projectPath, "publish"),
                "*.dll")[0];
            
            var startInfo = new ProcessStartInfo
            {
                FileName = "dotnet",
                Arguments = $"\"{dllPath}\"",
                WorkingDirectory = Path.Combine(projectPath, "publish"),
                UseShellExecute = false,
                RedirectStandardOutput = true,
                RedirectStandardError = true
            };
            
            startInfo.Environment["ASPNETCORE_URLS"] = $"http://localhost:{port}";
            
            var process = Process.Start(startInfo);
            if (process == null)
                throw new DeploymentException("Failed to start agent process");
            
            return process;
        }
        
        private async Task WaitForHealthyAsync(
            string endpoint,
            CancellationToken cancellationToken)
        {
            using var httpClient = new HttpClient { Timeout = TimeSpan.FromSeconds(2) };
            var maxAttempts = 30;
            
            for (int i = 0; i < maxAttempts; i++)
            {
                try
                {
                    var response = await httpClient.GetAsync(
                        $"{endpoint}/health",
                        cancellationToken);
                    
                    if (response.IsSuccessStatusCode)
                    {
                        _logger.LogInformation("Agent is healthy at: {Endpoint}", endpoint);
                        return;
                    }
                }
                catch
                {
                    // Retry
                }
                
                await Task.Delay(1000, cancellationToken);
            }
            
            throw new DeploymentException(
                $"Agent failed to become healthy at: {endpoint}");
        }
    }
    
    public class PortAllocator
    {
        private int _currentPort = 6000;
        private readonly object _lock = new();
        
        public int AllocatePort()
        {
            lock (_lock)
            {
                return _currentPort++;
            }
        }
    }
}
```

---

## Implementation Guidelines

### Service Registration

```csharp
// Program.cs or Startup.cs
using Myriad.Core.Lifecycle;
using Myriad.Core.Learning;

var builder = WebApplication.CreateBuilder(args);

// Neurogenesis components
builder.Services.AddSingleton<DynamicLifecycleManager>();
builder.Services.AddSingleton<IConceptDetector, ConceptDetector>();
builder.Services.AddSingleton<IResearchCoordinator, ResearchCoordinator>();
builder.Services.AddSingleton<ITemplateSelector, TemplateSelector>();
builder.Services.AddSingleton<ICodeGenerator, RoslynCodeGenerator>();
builder.Services.AddSingleton<IAgentDeployer, AgentDeployer>();
builder.Services.AddSingleton<PortAllocator>();

// Learning engine
builder.Services.AddSingleton<AutonomousLearningEngine>();

// Templates
builder.Services.AddSingleton<IAgentTemplate, FactBaseBasicTemplate>();
builder.Services.AddSingleton<IAgentTemplate, FactBaseEnhancedTemplate>();
builder.Services.AddSingleton<IAgentTemplate, FunctionBasicTemplate>();
builder.Services.AddSingleton<IAgentTemplate, SpecialistBasicTemplate>();

var app = builder.Build();
```

### Usage Example

```csharp
// In Orchestrator Service
public class OrchestratorService
{
    private readonly DynamicLifecycleManager _lifecycleManager;
    
    public async Task<ProcessResponse> ProcessQueryAsync(
        ProcessRequest request,
        CancellationToken cancellationToken)
    {
        // Try to find agents for concepts
        var agents = await DiscoverAgentsAsync(request.Concept, cancellationToken);
        
        if (!agents.Any())
        {
            // Trigger neurogenesis
            _logger.LogInformation(
                "No agents found for '{Concept}' - creating new agent",
                request.Concept);
            
            var newAgent = await _lifecycleManager.CreateAgentAsync(
                request.Concept,
                request.Intent,
                cancellationToken);
            
            if (newAgent != null)
            {
                // Retry discovery
                agents = await DiscoverAgentsAsync(request.Concept, cancellationToken);
            }
        }
        
        // Continue with normal processing
        return await ProcessWithAgentsAsync(agents, request, cancellationToken);
    }
}
```

---

## Performance Considerations

### Agent Creation Metrics

Expected performance for neurogenesis:

| Phase | Operation | Expected Time |
|-------|-----------|---------------|
| Detection | Graph query | 10-50ms |
| Research | Multi-agent collaboration | 500ms-2s |
| Templating | Template selection | 50-100ms |
| Generation | Roslyn code generation | 100-500ms |
| Deployment | Build + Publish + Start | 5-15s |
| **Total** | **First query** | **6-18s** |
| **Subsequent** | **Normal query** | **50-500ms** |

### Optimization Strategies

1. **Template Caching**: Pre-compile templates for faster generation
2. **Parallel Build**: Build multiple agents simultaneously
3. **Incremental Compilation**: Reuse compiled dependencies
4. **Process Pooling**: Keep warm agent processes ready
5. **Knowledge Caching**: Cache research results

---

**Document Version:** 1.0 C#  
**Last Updated:** 2025-01-10  
**Status:** Architecture Definition Phase

[↑ Back to Index](../INDEX.md) | [Graph Intelligence ←](graph-intelligence-csharp.md) | [Microservices ←](microservices-csharp.md)

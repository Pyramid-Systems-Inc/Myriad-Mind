# Myriad Cognitive Architecture - Graph Intelligence & Context Understanding (C#/.NET Edition)

**Architecture Documentation** | [Overview](system-overview-csharp.md) | [Microservices](microservices-csharp.md) | [Neurogenesis](neurogenesis-csharp.md)

Comprehensive documentation of the custom graph database architecture, intelligent agent discovery, Hebbian learning, and human-like context understanding systems - all built from scratch in C#.

[← Back to Index](../INDEX.md#architecture) | [Protocols →](../protocols/)

---

## Table of Contents

- [Custom Graph Database Core](#custom-graph-database-core)
- [Graph Schema Design](#graph-schema-design)
- [GraphDB Manager Service](#graphdb-manager-service)
- [Enhanced Graph Intelligence](#enhanced-graph-intelligence)
- [Hebbian Learning System](#hebbian-learning-system)
- [Context Understanding Architecture](#context-understanding-architecture)
- [Implementation Guidelines](#implementation-guidelines)
- [Performance Optimization](#performance-optimization)

---

## Custom Graph Database Core

### Overview

The custom graph database serves as the **neural substrate** of the Myriad-Mind system, replacing external dependencies with a from-scratch C# implementation.

**Key Capabilities:**

- **Agent Discovery**: Concept-based agent lookup through graph traversal
- **Relationship Management**: Dynamic agent-concept connections with learning weights
- **Hebbian Learning**: "Neurons that fire together, wire together" principle
- **Context Tracking**: Conversation history and user profile persistence
- **Knowledge Representation**: Rich semantic relationships between concepts

### Core Architecture

```csharp
namespace Myriad.Core.Graph
{
    /// <summary>
    /// Custom graph database implementation with Hebbian learning
    /// </summary>
    public class GraphDatabase
    {
        // Node storage using concurrent dictionaries for thread safety
        private readonly ConcurrentDictionary<string, GraphNode> _nodes;
        private readonly ConcurrentDictionary<string, List<GraphEdge>> _edges;
        
        // Read/write lock for complex operations
        private readonly ReaderWriterLockSlim _rwLock;
        
        // Persistence layer
        private readonly IGraphPersistence _persistence;
        
        public GraphDatabase(IGraphPersistence persistence)
        {
            _nodes = new ConcurrentDictionary<string, GraphNode>();
            _edges = new ConcurrentDictionary<string, List<GraphEdge>>();
            _rwLock = new ReaderWriterLockSlim(LockRecursionPolicy.NoRecursion);
            _persistence = persistence;
        }
        
        /// <summary>
        /// Add or update a node in the graph
        /// </summary>
        public async Task<bool> UpsertNodeAsync(GraphNode node, CancellationToken cancellationToken = default)
        {
            _rwLock.EnterWriteLock();
            try
            {
                _nodes.AddOrUpdate(node.Id, node, (key, existing) => node);
                await _persistence.SaveNodeAsync(node, cancellationToken);
                return true;
            }
            finally
            {
                _rwLock.ExitWriteLock();
            }
        }
        
        /// <summary>
        /// Traverse graph using breadth-first search with predicate
        /// </summary>
        public async Task<IEnumerable<GraphNode>> TraverseAsync(
            string startNodeId, 
            Func<GraphNode, bool> predicate,
            int maxDepth = 3,
            CancellationToken cancellationToken = default)
        {
            _rwLock.EnterReadLock();
            try
            {
                var visited = new HashSet<string>();
                var queue = new Queue<(string nodeId, int depth)>();
                var results = new List<GraphNode>();
                
                queue.Enqueue((startNodeId, 0));
                visited.Add(startNodeId);
                
                while (queue.Count > 0 && !cancellationToken.IsCancellationRequested)
                {
                    var (currentId, depth) = queue.Dequeue();
                    
                    if (depth > maxDepth) continue;
                    
                    if (!_nodes.TryGetValue(currentId, out var currentNode)) continue;
                    
                    if (predicate(currentNode))
                    {
                        results.Add(currentNode);
                    }
                    
                    // Get edges from current node
                    if (_edges.TryGetValue(currentId, out var nodeEdges))
                    {
                        foreach (var edge in nodeEdges)
                        {
                            if (!visited.Contains(edge.ToNodeId))
                            {
                                visited.Add(edge.ToNodeId);
                                queue.Enqueue((edge.ToNodeId, depth + 1));
                            }
                        }
                    }
                }
                
                return results;
            }
            finally
            {
                _rwLock.ExitReadLock();
            }
        }
    }
}
```

---

## Graph Schema Design

### Node Types

#### 1. Agent Nodes

```csharp
namespace Myriad.Core.Graph.Nodes
{
    /// <summary>
    /// Represents an agent in the cognitive network
    /// </summary>
    public record AgentNode : GraphNode
    {
        public required string Name { get; init; }
        public required AgentType Type { get; init; }
        public required string Endpoint { get; init; }
        public required int Port { get; init; }
        public required List<string> Capabilities { get; init; }
        public required string Description { get; init; }
        public DateTime CreatedAt { get; init; }
        public AgentStatus Status { get; init; }
        
        public AgentNode() : base(NodeType.Agent) { }
    }
    
    public enum AgentType
    {
        FactBaseBasic,
        FactBaseEnhanced,
        FunctionBasic,
        SpecialistBasic,
        DynamicAgent
    }
    
    public enum AgentStatus
    {
        Healthy,
        Degraded,
        Failed
    }
}
```

#### 2. Concept Nodes

```csharp
public record ConceptNode : GraphNode
{
    public required string Name { get; init; }
    public string? PrimaryDefinition { get; init; }
    public string? Description { get; init; }
    public string Domain { get; init; } = "General";
    public float Complexity { get; init; } = 0.5f;
    public DateTime CreatedAt { get; init; }
    
    public ConceptNode() : base(NodeType.Concept) { }
}
```

#### 3. Region Nodes

```csharp
public record RegionNode : GraphNode
{
    public required string Name { get; init; }
    public string? Description { get; init; }
    public int AgentCount { get; set; }
    public int ConceptCount { get; set; }
    
    public RegionNode() : base(NodeType.Region) { }
}
```

#### 4. User Nodes

```csharp
public record UserNode : GraphNode
{
    public required string UserId { get; init; }
    public DateTime CreatedAt { get; init; }
    public Dictionary<string, object> Preferences { get; init; } = new();
    public Dictionary<string, string> ExpertiseLevels { get; init; } = new();
    
    public UserNode() : base(NodeType.User) { }
}
```

### Edge Types

#### 1. HANDLES_CONCEPT (Agent → Concept)

```csharp
namespace Myriad.Core.Graph.Edges
{
    /// <summary>
    /// Represents agent-concept relationship with Hebbian learning properties
    /// </summary>
    public record HandlesConceptEdge : GraphEdge
    {
        public float Weight { get; set; } = 0.5f;
        public int UsageCount { get; set; }
        public int SuccessCount { get; set; }
        public int FailureCount { get; set; }
        public float SuccessRate => UsageCount > 0 
            ? (float)SuccessCount / UsageCount 
            : 0.5f;
        public float DecayRate { get; init; } = 0.01f;
        public DateTime LastUpdated { get; set; }
        
        public HandlesConceptEdge(string fromNodeId, string toNodeId) 
            : base(fromNodeId, toNodeId, EdgeType.HandlesConcept)
        {
            LastUpdated = DateTime.UtcNow;
        }
        
        /// <summary>
        /// Apply Hebbian strengthening on success
        /// </summary>
        public void Strengthen(float delta = 0.05f)
        {
            Weight = Math.Min(1.0f, Weight + delta);
            UsageCount++;
            SuccessCount++;
            LastUpdated = DateTime.UtcNow;
        }
        
        /// <summary>
        /// Apply Hebbian weakening on failure
        /// </summary>
        public void Weaken(float delta = 0.02f)
        {
            Weight = Math.Max(0.0f, Weight - delta);
            UsageCount++;
            FailureCount++;
            LastUpdated = DateTime.UtcNow;
        }
        
        /// <summary>
        /// Apply time-based decay
        /// </summary>
        public void Decay()
        {
            Weight = Math.Max(0.0f, Weight * (1.0f - DecayRate));
            LastUpdated = DateTime.UtcNow;
        }
    }
}
```

---

## GraphDB Manager Service

### Service Overview

**Service**: GraphDB Manager Service  
**Port**: 5008  
**Framework**: ASP.NET Core Minimal APIs  
**Purpose**: REST interface to custom graph database

### Core Implementation

```csharp
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;
using Myriad.Core.Graph;

var builder = WebApplication.CreateBuilder(args);

// Register graph database as singleton
builder.Services.AddSingleton<IGraphDatabase, GraphDatabase>();
builder.Services.AddSingleton<IGraphPersistence, JsonGraphPersistence>();

var app = builder.Build();

/// <summary>
/// Create a new node in the graph
/// </summary>
app.MapPost("/create_node", async (
    NodeCreationRequest request,
    IGraphDatabase graphDb,
    CancellationToken cancellationToken) =>
{
    var node = request.Label switch
    {
        "Agent" => new AgentNode
        {
            Id = Guid.NewGuid().ToString(),
            Name = request.Properties["name"]?.ToString() ?? "",
            Type = Enum.Parse<AgentType>(request.Properties["type"]?.ToString() ?? "FactBaseBasic"),
            Endpoint = request.Properties["endpoint"]?.ToString() ?? "",
            Port = int.Parse(request.Properties["port"]?.ToString() ?? "0"),
            Capabilities = request.Properties["capabilities"] as List<string> ?? new(),
            Description = request.Properties["description"]?.ToString() ?? "",
            Status = AgentStatus.Healthy,
            CreatedAt = DateTime.UtcNow
        },
        "Concept" => new ConceptNode
        {
            Id = Guid.NewGuid().ToString(),
            Name = request.Properties["name"]?.ToString() ?? "",
            PrimaryDefinition = request.Properties["primary_definition"]?.ToString(),
            Description = request.Properties["description"]?.ToString(),
            Domain = request.Properties["domain"]?.ToString() ?? "General",
            CreatedAt = DateTime.UtcNow
        },
        _ => throw new ArgumentException($"Unknown node label: {request.Label}")
    };
    
    await graphDb.UpsertNodeAsync(node, cancellationToken);
    
    return Results.Created($"/node/{node.Id}", new { id = node.Id });
});

/// <summary>
/// Create relationship between nodes
/// </summary>
app.MapPost("/create_relationship", async (
    RelationshipCreationRequest request,
    IGraphDatabase graphDb,
    CancellationToken cancellationToken) =>
{
    // Find source and target nodes
    var fromNode = await graphDb.GetNodeAsync(request.FromValue, cancellationToken);
    var toNode = await graphDb.GetNodeAsync(request.ToValue, cancellationToken);
    
    if (fromNode == null || toNode == null)
    {
        return Results.NotFound("Source or target node not found");
    }
    
    // Create edge based on type
    GraphEdge edge = request.RelationshipType switch
    {
        "HANDLES_CONCEPT" => new HandlesConceptEdge(fromNode.Id, toNode.Id)
        {
            Weight = float.Parse(request.Properties["weight"]?.ToString() ?? "0.5"),
            DecayRate = float.Parse(request.Properties["decay_rate"]?.ToString() ?? "0.01")
        },
        "BELONGS_TO" => new BelongsToEdge(fromNode.Id, toNode.Id),
        _ => throw new ArgumentException($"Unknown relationship type: {request.RelationshipType}")
    };
    
    await graphDb.AddEdgeAsync(edge, cancellationToken);
    
    return Results.Created($"/relationship/{edge.Id}", new { id = edge.Id });
});

/// <summary>
/// Get agents that handle a specific concept
/// </summary>
app.MapGet("/get_agents_for_concept/{concept}", async (
    string concept,
    IGraphDatabase graphDb,
    CancellationToken cancellationToken) =>
{
    // Find concept node
    var conceptNodes = await graphDb.FindNodesAsync(
        n => n is ConceptNode cn && cn.Name.Equals(concept, StringComparison.OrdinalIgnoreCase),
        cancellationToken);
    
    var conceptNode = conceptNodes.FirstOrDefault();
    if (conceptNode == null)
    {
        return Results.Ok(new { agents = Array.Empty<object>() });
    }
    
    // Find agents connected via HANDLES_CONCEPT
    var edges = await graphDb.GetIncomingEdgesAsync(
        conceptNode.Id, 
        EdgeType.HandlesConcept,
        cancellationToken);
    
    var agentEdges = edges
        .OfType<HandlesConceptEdge>()
        .OrderByDescending(e => e.Weight)
        .ThenByDescending(e => e.SuccessRate);
    
    var agentResults = new List<object>();
    
    foreach (var edge in agentEdges)
    {
        var agentNode = await graphDb.GetNodeAsync(edge.FromNodeId, cancellationToken) as AgentNode;
        if (agentNode != null)
        {
            agentResults.Add(new
            {
                agent_id = agentNode.Name,
                endpoint = agentNode.Endpoint,
                weight = edge.Weight,
                success_rate = edge.SuccessRate,
                usage_count = edge.UsageCount
            });
        }
    }
    
    return Results.Ok(new { agents = agentResults });
});

/// <summary>
/// Strengthen Hebbian connection (success)
/// </summary>
app.MapPost("/hebbian/strengthen", async (
    HebbianUpdateRequest request,
    IGraphDatabase graphDb,
    CancellationToken cancellationToken) =>
{
    var edge = await graphDb.FindEdgeAsync(
        request.AgentId, 
        request.Concept,
        EdgeType.HandlesConcept,
        cancellationToken) as HandlesConceptEdge;
    
    if (edge == null)
    {
        return Results.NotFound("Edge not found");
    }
    
    if (request.Success)
    {
        edge.Strengthen(0.05f);
    }
    else
    {
        edge.Weaken(0.02f);
    }
    
    await graphDb.UpdateEdgeAsync(edge, cancellationToken);
    
    return Results.Ok(new
    {
        agent_id = request.AgentId,
        concept = request.Concept,
        new_weight = edge.Weight,
        success_rate = edge.SuccessRate
    });
});

/// <summary>
/// Apply decay to all edges (background task)
/// </summary>
app.MapPost("/hebbian/decay", async (
    IGraphDatabase graphDb,
    CancellationToken cancellationToken) =>
{
    var allEdges = await graphDb.GetAllEdgesAsync(EdgeType.HandlesConcept, cancellationToken);
    var decayedCount = 0;
    
    foreach (var edge in allEdges.OfType<HandlesConceptEdge>())
    {
        // Only decay recently active edges (last 10 decay intervals)
        var timeSinceUpdate = DateTime.UtcNow - edge.LastUpdated;
        if (timeSinceUpdate.TotalMinutes < 150) // 10 * 15 minutes
        {
            edge.Decay();
            await graphDb.UpdateEdgeAsync(edge, cancellationToken);
            decayedCount++;
        }
    }
    
    return Results.Ok(new { decayed_count = decayedCount });
});

app.Run();

// Request DTOs
record NodeCreationRequest(string Label, Dictionary<string, object> Properties);
record RelationshipCreationRequest(
    string FromLabel, string FromProperty, string FromValue,
    string ToLabel, string ToProperty, string ToValue,
    string RelationshipType, Dictionary<string, object> Properties);
record HebbianUpdateRequest(string AgentId, string Concept, bool Success);
```

---

## Enhanced Graph Intelligence

### Overview

The Enhanced Graph Intelligence layer provides **context-aware agent discovery** with multi-criteria relevance scoring - all implemented in C# without external ML libraries.

**Implementation**: `src/Myriad.Core.Intelligence/EnhancedGraphIntelligence.cs`

### Multi-Criteria Relevance Scoring

```csharp
namespace Myriad.Core.Intelligence
{
    /// <summary>
    /// Enhanced graph intelligence with multi-criteria agent scoring
    /// </summary>
    public class EnhancedGraphIntelligence
    {
        private readonly IGraphDatabase _graphDb;
        private readonly IPerformanceTracker _performanceTracker;
        private readonly Dictionary<string, AgentProfile> _agentProfiles;
        
        // Scoring weights (sum to 1.0)
        private const float EXPERTISE_WEIGHT = 0.28f;
        private const float CAPABILITY_WEIGHT = 0.22f;
        private const float DOMAIN_WEIGHT = 0.18f;
        private const float PERFORMANCE_WEIGHT = 0.14f;
        private const float AVAILABILITY_WEIGHT = 0.08f;
        private const float HEBBIAN_WEIGHT = 0.10f;
        
        /// <summary>
        /// Discover agents with intelligent relevance scoring
        /// </summary>
        public async Task<List<AgentRelevanceScore>> DiscoverAgentsAsync(
            string concept,
            string intent,
            QueryContext? context = null,
            CancellationToken cancellationToken = default)
        {
            context ??= new QueryContext();
            
            // Get candidate agents from graph
            var candidates = await GetCandidateAgentsAsync(concept, cancellationToken);
            
            // Score each candidate
            var scoredAgents = new List<AgentRelevanceScore>();
            
            foreach (var candidate in candidates)
            {
                var score = await CalculateRelevanceScoreAsync(
                    candidate,
                    concept,
                    intent,
                    context,
                    cancellationToken);
                
                scoredAgents.Add(score);
            }
            
            // Sort by relevance and return top N
            return scoredAgents
                .OrderByDescending(a => a.RelevanceScore)
                .Take(context.MaxAgents)
                .ToList();
        }
        
        /// <summary>
        /// Calculate comprehensive relevance score
        /// </summary>
        private async Task<AgentRelevanceScore> CalculateRelevanceScoreAsync(
            AgentNode agent,
            string concept,
            string intent,
            QueryContext context,
            CancellationToken cancellationToken)
        {
            var profile = _agentProfiles.GetValueOrDefault(agent.Name) 
                ?? await BuildAgentProfileAsync(agent, cancellationToken);
            
            // Calculate individual scores
            var expertiseScore = CalculateExpertiseMatch(profile, concept);
            var capabilityScore = CalculateCapabilityMatch(profile, intent);
            var domainScore = CalculateDomainOverlap(profile, context.Domain);
            var performanceScore = CalculatePerformanceFactor(profile);
            var availabilityScore = CalculateAvailabilityFactor(profile);
            var hebbianScore = await GetHebbianWeightAsync(agent.Name, concept, cancellationToken);
            
            // Weighted combination
            var relevanceScore = 
                (expertiseScore * EXPERTISE_WEIGHT) +
                (capabilityScore * CAPABILITY_WEIGHT) +
                (domainScore * DOMAIN_WEIGHT) +
                (performanceScore * PERFORMANCE_WEIGHT) +
                (availabilityScore * AVAILABILITY_WEIGHT) +
                (hebbianScore * HEBBIAN_WEIGHT);
            
            return new AgentRelevanceScore
            {
                AgentId = agent.Name,
                Endpoint = agent.Endpoint,
                RelevanceScore = relevanceScore,
                Confidence = CalculateConfidence(relevanceScore, profile),
                Reasoning = BuildReasoningList(
                    expertiseScore, capabilityScore, domainScore,
                    performanceScore, hebbianScore),
                ComponentScores = new Dictionary<string, float>
                {
                    ["expertise"] = expertiseScore,
                    ["capability"] = capabilityScore,
                    ["domain"] = domainScore,
                    ["performance"] = performanceScore,
                    ["availability"] = availabilityScore,
                    ["hebbian"] = hebbianScore
                }
            };
        }
        
        /// <summary>
        /// Calculate expertise match using simple keyword matching
        /// (No external NLP libraries - pure C# implementation)
        /// </summary>
        private float CalculateExpertiseMatch(AgentProfile profile, string concept)
        {
            // Direct match
            if (profile.Expertise.Any(e => 
                e.Equals(concept, StringComparison.OrdinalIgnoreCase)))
            {
                return 1.0f;
            }
            
            // Partial match using Levenshtein distance
            var conceptLower = concept.ToLowerInvariant();
            var bestMatch = 0.0f;
            
            foreach (var expertise in profile.Expertise)
            {
                var expertiseLower = expertise.ToLowerInvariant();
                
                // Simple substring match
                if (expertiseLower.Contains(conceptLower) || conceptLower.Contains(expertiseLower))
                {
                    var similarity = Math.Max(
                        (float)conceptLower.Length / expertiseLower.Length,
                        (float)expertiseLower.Length / conceptLower.Length);
                    
                    bestMatch = Math.Max(bestMatch, similarity * 0.8f);
                }
                
                // Levenshtein similarity
                var levenshteinSimilarity = CalculateLevenshteinSimilarity(conceptLower, expertiseLower);
                bestMatch = Math.Max(bestMatch, levenshteinSimilarity * 0.6f);
            }
            
            return bestMatch;
        }
        
        /// <summary>
        /// Levenshtein distance implementation (no external libraries)
        /// </summary>
        private float CalculateLevenshteinSimilarity(string s1, string s2)
        {
            var distance = CalculateLevenshteinDistance(s1, s2);
            var maxLength = Math.Max(s1.Length, s2.Length);
            
            if (maxLength == 0) return 1.0f;
            
            return 1.0f - ((float)distance / maxLength);
        }
        
        private int CalculateLevenshteinDistance(string s1, string s2)
        {
            var matrix = new int[s1.Length + 1, s2.Length + 1];
            
            for (int i = 0; i <= s1.Length; i++) matrix[i, 0] = i;
            for (int j = 0; j <= s2.Length; j++) matrix[0, j] = j;
            
            for (int i = 1; i <= s1.Length; i++)
            {
                for (int j = 1; j <= s2.Length; j++)
                {
                    var cost = s1[i - 1] == s2[j - 1] ? 0 : 1;
                    
                    matrix[i, j] = Math.Min(
                        Math.Min(matrix[i - 1, j] + 1, matrix[i, j - 1] + 1),
                        matrix[i - 1, j - 1] + cost);
                }
            }
            
            return matrix[s1.Length, s2.Length];
        }
    }
    
    // Supporting types
    public record AgentRelevanceScore
    {
        public required string AgentId { get; init; }
        public required string Endpoint { get; init; }
        public required float RelevanceScore { get; init; }
        public required float Confidence { get; init; }
        public required List<string> Reasoning { get; init; }
        public Dictionary<string, float>? ComponentScores { get; init; }
    }
    
    public record QueryContext
    {
        public string Domain { get; init; } = "General";
        public int MaxAgents { get; init; } = 5;
        public float ComplexityScore { get; init; } = 0.5f;
        public Dictionary<string, object> Metadata { get; init; } = new();
    }
}
```

---

## Hebbian Learning System

### Theoretical Foundation

**Hebb's Rule**: "Neurons that fire together, wire together"

In Myriad-Mind (C# implementation):

- **Neurons** = Agents (ASP.NET Core services)
- **Synapses** = HANDLES_CONCEPT edges
- **Firing together** = Agent successfully processes concept
- **Wire together** = Increase edge weight

### Learning Parameters

```csharp
namespace Myriad.Core.Learning
{
    /// <summary>
    /// Hebbian learning configuration
    /// </summary>
    public class HebbianLearningConfig
    {
        public float DeltaSuccess { get; set; } = 0.05f;      // Weight increase on success
        public float DeltaFailure { get; set; } = 0.02f;      // Weight decrease on failure
        public float DecayRate { get; set; } = 0.01f;         // 1% decay per interval
        public TimeSpan DecayInterval { get; set; } = TimeSpan.FromMinutes(15);
        public bool EnableAutomaticDecay { get; set; } = true;
    }
}
```

### Background Decay Service

```csharp
using Microsoft.Extensions.Hosting;

namespace Myriad.Services.GraphDatabase
{
    /// <summary>
    /// Background service for Hebbian decay
    /// </summary>
    public class HebbianDecayService : BackgroundService
    {
        private readonly IGraphDatabase _graphDb;
        private readonly HebbianLearningConfig _config;
        private readonly ILogger<HebbianDecayService> _logger;
        
        public HebbianDecayService(
            IGraphDatabase graphDb,
            HebbianLearningConfig config,
            ILogger<HebbianDecayService> logger)
        {
            _graphDb = graphDb;
            _config = config;
            _logger = logger;
        }
        
        protected override async Task ExecuteAsync(CancellationToken stoppingToken)
        {
            _logger.LogInformation("Hebbian decay service started");
            
            while (!stoppingToken.IsCancellationRequested)
            {
                try
                {
                    await Task.Delay(_config.DecayInterval, stoppingToken);
                    
                    if (!_config.EnableAutomaticDecay) continue;
                    
                    await ApplyDecayAsync(stoppingToken);
                }
                catch (Exception ex)
                {
                    _logger.LogError(ex, "Error in Hebbian decay cycle");
                }
            }
        }
        
        private async Task ApplyDecayAsync(CancellationToken cancellationToken)
        {
            var decayWindow = _config.DecayInterval.Multiply(10); // Last 10 intervals
            var cutoffTime = DateTime.UtcNow - decayWindow;
            
            var allEdges = await _graphDb.GetAllEdgesAsync(
                EdgeType.HandlesConcept, 
                cancellationToken);
            
            var decayedCount = 0;
            
            foreach (var edge in allEdges.OfType<HandlesConceptEdge>())
            {
                if (edge.LastUpdated > cutoffTime)
                {
                    edge.Decay();
                    await _graphDb.UpdateEdgeAsync(edge, cancellationToken);
                    decayedCount++;
                }
            }
            
            _logger.LogInformation(
                "Hebbian decay: Updated {Count} active relationships", 
                decayedCount);
        }
    }
}
```

---

## Context Understanding Architecture

### Multi-Layer Context System

```csharp
namespace Myriad.Core.Context
{
    /// <summary>
    /// Three-tier memory system (STM/MTM/LTM)
    /// </summary>
    public class ContextManager
    {
        private readonly ShortTermMemory _stm;
        private readonly MediumTermMemory _mtm;
        private readonly LongTermMemory _ltm;
        
        public ContextManager(IGraphDatabase graphDb)
        {
            _stm = new ShortTermMemory();
            _mtm = new MediumTermMemory();
            _ltm = new LongTermMemory(graphDb);
        }
        
        /// <summary>
        /// Store context at appropriate tier
        /// </summary>
        public async Task RememberAsync(
            string key, 
            object value,
            MemoryTier tier = MemoryTier.Short,
            CancellationToken cancellationToken = default)
        {
            switch (tier)
            {
                case MemoryTier.Short:
                    _stm.Store(key, value);
                    break;
                    
                case MemoryTier.Medium:
                    await _mtm.StoreAsync(key, value, cancellationToken);
                    break;
                    
                case MemoryTier.Long:
                    await _ltm.StoreAsync(key, value, cancellationToken);
                    break;
            }
        }
        
        /// <summary>
        /// Retrieve from memory tiers (STM → MTM → LTM)
        /// </summary>
        public async Task<T?> RecallAsync<T>(
            string key,
            CancellationToken cancellationToken = default) where T : class
        {
            // Try STM first (fastest, in-memory)
            var value = _stm.Retrieve<T>(key);
            if (value != null) return value;
            
            // Try MTM (medium speed, session cache)
            value = await _mtm.RetrieveAsync<T>(key, cancellationToken);
            if (value != null)
            {
                // Promote to STM
                _stm.Store(key, value);
                return value;
            }
            
            // Try LTM (slowest, graph database)
            value = await _ltm.RetrieveAsync<T>(key, cancellationToken);
            if (value != null)
            {
                // Promote to MTM
                await _mtm.StoreAsync(key, value, cancellationToken);
                return value;
            }
            
            return null;
        }
    }
    
    public enum MemoryTier
    {
        Short,   // Seconds to minutes
        Medium,  // Minutes to hours
        Long     // Persistent
    }
}
```

---

## Implementation Guidelines

### Service Registration

```csharp
// Program.cs or Startup.cs
using Myriad.Core.Graph;
using Myriad.Core.Intelligence;
using Myriad.Core.Context;

var builder = WebApplication.CreateBuilder(args);

// Graph database
builder.Services.AddSingleton<IGraphDatabase, GraphDatabase>();
builder.Services.AddSingleton<IGraphPersistence, JsonGraphPersistence>();

// Enhanced intelligence
builder.Services.AddSingleton<EnhancedGraphIntelligence>();
builder.Services.AddSingleton<IPerformanceTracker, PerformanceTracker>();

// Context management
builder.Services.AddSingleton<ContextManager>();

// Background services
builder.Services.AddHostedService<HebbianDecayService>();

// Configuration
builder.Services.AddSingleton(new HebbianLearningConfig
{
    DeltaSuccess = 0.05f,
    DeltaFailure = 0.02f,
    DecayRate = 0.01f,
    DecayInterval = TimeSpan.FromMinutes(15)
});

var app = builder.Build();
```

---

## Performance Optimization

### Caching Strategy

```csharp
namespace Myriad.Core.Graph
{
    public class CachedGraphDatabase : IGraphDatabase
    {
        private readonly IGraphDatabase _innerDb;
        private readonly MemoryCache _cache;
        
        public async Task<GraphNode?> GetNodeAsync(
            string id, 
            CancellationToken cancellationToken = default)
        {
            var cacheKey = $"node:{id}";
            
            if (_cache.TryGetValue<GraphNode>(cacheKey, out var cachedNode))
            {
                return cachedNode;
            }
            
            var node = await _innerDb.GetNodeAsync(id, cancellationToken);
            
            if (node != null)
            {
                _cache.Set(cacheKey, node, TimeSpan.FromMinutes(5));
            }
            
            return node;
        }
    }
}
```

---

**Document Version:** 1.0 C#  
**Last Updated:** 2025-01-09  
**Status:** Architecture Definition Phase

[↑ Back to Index](../INDEX.md) | [Microservices →](microservices-csharp.md)

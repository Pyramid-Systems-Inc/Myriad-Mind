# Phase 2: Core Services Implementation

**Duration**: 3-4 weeks
**Goal**: Build custom graph database and main processing services
**Prerequisites**: Phase 1 complete

---

## Architecture Context

This phase implements core processing infrastructure described in:
- [`graph-intelligence-csharp.md`](../architecture/graph-intelligence-csharp.md) - Custom graph database and Hebbian learning
- [`system-overview-csharp.md`](../architecture/system-overview-csharp.md) - Core cognitive layer components
- Zero external dependencies - everything built from scratch in C#

---

## Objectives

✅ **Custom Graph Database** - Neo4j-inspired implementation using `ConcurrentDictionary`
✅ **GraphDB Manager Service** - REST API for graph operations
✅ **Input Processor Service** - Query parsing and intent recognition
✅ **Output Processor Service** - Response synthesis
✅ **Multiple Static Agents** - Factory_AI, Edison_AI for testing

---

## Step 1: Custom Graph Database

### Task 1.1: Core Graph Classes

**File**: `src/Myriad.Core.Graph/GraphNode.cs`

```csharp
namespace Myriad.Core.Graph;

public abstract record GraphNode
{
    public required string Id { get; init; } = Guid.NewGuid().ToString();
    public required NodeType Type { get; init; }
    public Dictionary<string, object> Properties { get; init; } = new();
}

public record AgentNode : GraphNode
{
    public required string Name { get; init; }
    public required string Endpoint { get; init; }
    public required int Port { get; init; }
    public List<string> Capabilities { get; init; } = new();
    
    public AgentNode() : base() { Type = NodeType.Agent; }
}

public record ConceptNode : GraphNode
{
    public required string Name { get; init; }
    public string? Description { get; init; }
    
    public ConceptNode() : base() { Type = NodeType.Concept; }
}

public enum NodeType { Agent, Concept, User, Region }
```

**File**: `src/Myriad.Core.Graph/GraphEdge.cs`

```csharp
namespace Myriad.Core.Graph;

public record GraphEdge
{
    public required string Id { get; init; } = Guid.NewGuid().ToString();
    public required string FromNodeId { get; init; }
    public required string ToNodeId { get; init; }
    public required EdgeType Type { get; init; }
    public float Weight { get; set; } = 0.5f;
    public Dictionary<string, object> Properties { get; init; } = new();
}

public enum EdgeType { HandlesConcept, RelatesTo, BelongsTo }
```

### Task 1.2: Graph Database Implementation

**File**: `src/Myriad.Core.Graph/GraphDatabase.cs`

```csharp
using System.Collections.Concurrent;

namespace Myriad.Core.Graph;

public class GraphDatabase : IGraphDatabase
{
    private readonly ConcurrentDictionary<string, GraphNode> _nodes = new();
    private readonly ConcurrentDictionary<string, List<GraphEdge>> _edgesFrom = new();
    private readonly ReaderWriterLockSlim _lock = new();
    
    public Task<bool> UpsertNodeAsync(GraphNode node, CancellationToken ct = default)
    {
        _nodes.AddOrUpdate(node.Id, node, (_, _) => node);
        return Task.FromResult(true);
    }
    
    public Task<GraphNode?> GetNodeAsync(string id, CancellationToken ct = default)
    {
        _nodes.TryGetValue(id, out var node);
        return Task.FromResult(node);
    }
    
    public Task<List<GraphNode>> FindNodesAsync(
        Func<GraphNode, bool> predicate,
        CancellationToken ct = default)
    {
        var results = _nodes.Values.Where(predicate).ToList();
        return Task.FromResult(results);
    }
    
    public Task AddEdgeAsync(GraphEdge edge, CancellationToken ct = default)
    {
        if (!_edgesFrom.ContainsKey(edge.FromNodeId))
        {
            _edgesFrom[edge.FromNodeId] = new List<GraphEdge>();
        }
        
        _edgesFrom[edge.FromNodeId].Add(edge);
        return Task.CompletedTask;
    }
    
    public Task<List<GraphEdge>> GetEdgesFromAsync(
        string nodeId,
        CancellationToken ct = default)
    {
        _edgesFrom.TryGetValue(nodeId, out var edges);
        return Task.FromResult(edges ?? new List<GraphEdge>());
    }
}

public interface IGraphDatabase
{
    Task<bool> UpsertNodeAsync(GraphNode node, CancellationToken ct = default);
    Task<GraphNode?> GetNodeAsync(string id, CancellationToken ct = default);
    Task<List<GraphNode>> FindNodesAsync(Func<GraphNode, bool> predicate, CancellationToken ct = default);
    Task AddEdgeAsync(GraphEdge edge, CancellationToken ct = default);
    Task<List<GraphEdge>> GetEdgesFromAsync(string nodeId, CancellationToken ct = default);
}
```

**Acceptance**: Graph database tests pass (create nodes, edges, query)

---

## Step 2: GraphDB Manager Service

**File**: `src/Myriad.Services.GraphDatabase/Program.cs`

```csharp
using Myriad.Core.Graph;

var builder = WebApplication.CreateBuilder(args);
builder.WebHost.UseUrls("http://localhost:5008");

builder.Services.AddSingleton<IGraphDatabase, GraphDatabase>();

var app = builder.Build();

// Initialize with sample data
var graphDb = app.Services.GetRequiredService<IGraphDatabase>();
await SeedDataAsync(graphDb);

app.MapGet("/health", () => new { status = "healthy", service = "GraphDB_Manager" });

app.MapPost("/nodes", async (GraphNode node, IGraphDatabase db) =>
{
    await db.UpsertNodeAsync(node);
    return Results.Created($"/nodes/{node.Id}", node);
});

app.MapGet("/agents/concept/{concept}", async (
    string concept,
    IGraphDatabase db) =>
{
    // Find concept node
    var concepts = await db.FindNodesAsync(
        n => n is ConceptNode cn && cn.Name.Equals(concept, StringComparison.OrdinalIgnoreCase));
    
    var conceptNode = concepts.FirstOrDefault();
    if (conceptNode == null)
        return Results.Ok(new { agents = Array.Empty<object>() });
    
    // Find connected agents
    var edges = await db.GetEdgesFromAsync(conceptNode.Id);
    var agentIds = edges.Select(e => e.ToNodeId).ToList();
    
    var agents = new List<object>();
    foreach (var id in agentIds)
    {
        var node = await db.GetNodeAsync(id);
        if (node is AgentNode agent)
        {
            agents.Add(new
            {
                agent_id = agent.Name,
                endpoint = agent.Endpoint,
                capabilities = agent.Capabilities
            });
        }
    }
    
    return Results.Ok(new { agents });
});

app.Run();

async Task SeedDataAsync(IGraphDatabase db)
{
    // Create agents
    var lightbulbAgent = new AgentNode
    {
        Name = "Lightbulb_AI",
        Endpoint = "http://localhost:5001",
        Port = 5001,
        Capabilities = new() { "lightbulb", "invention", "technology" }
    };
    
    await db.UpsertNodeAsync(lightbulbAgent);
    
    // Create concepts
    var lightbulbConcept = new ConceptNode
    {
        Name = "lightbulb",
        Description = "Electric light device"
    };
    
    await db.UpsertNodeAsync(lightbulbConcept);
    
    // Link agent to concept
    await db.AddEdgeAsync(new GraphEdge
    {
        FromNodeId = lightbulbAgent.Id,
        ToNodeId = lightbulbConcept.Id,
        Type = EdgeType.HandlesConcept,
        Weight = 0.9f
    });
}
```

**Acceptance**: Can query agents by concept and get correct results

---

## Step 3: Add More Static Agents

### Task 3.1: Factory_AI

**File**: `src/Myriad.Agents.Static.Factory/Program.cs`

```csharp
using Myriad.Common.Models;

var builder = WebApplication.CreateBuilder(args);
builder.WebHost.UseUrls("http://localhost:5002");

var app = builder.Build();

app.MapGet("/health", () => new { status = "healthy", agent = "Factory_AI" });

app.MapPost("/process", (QueryRequest request) =>
{
    var knowledge = new Dictionary<string, object>
    {
        ["pre_electric_conditions"] = "Factories relied on daylight and dangerous gas lamps",
        ["working_hours"] = "Limited to daylight hours (approximately 8-10 hours)",
        ["safety_issues"] = "Gas lamps caused fires; poor visibility led to accidents",
        ["productivity_impact"] = "Electric lighting extended work hours and improved safety"
    };

    return new AgentResponse
    {
        AgentId = "Factory_AI",
        Status = "success",
        Data = knowledge,
        Confidence = 0.90f,
        ProcessingTimeMs = 5
    };
});

app.Run();
```

**Acceptance**: Factory_AI responds correctly on port 5002

---

## Step 4: Input Processor Service

**File**: `src/Myriad.Services.InputProcessor/Program.cs`

```csharp
var builder = WebApplication.CreateBuilder(args);
builder.WebHost.UseUrls("http://localhost:5003");

var app = builder.Build();

app.MapGet("/health", () => new { status = "healthy", service = "Input_Processor" });

app.MapPost("/parse", (QueryRequest request) =>
{
    // Simple keyword extraction
    var query = request.Query.ToLowerInvariant();
    var keywords = query
        .Split(' ', StringSplitOptions.RemoveEmptyEntries)
        .Where(w => w.Length > 3)
        .Distinct()
        .ToList();
    
    // Determine intent
    var intent = query.StartsWith("what") ? "define" :
                 query.StartsWith("why") ? "explain" :
                 query.StartsWith("how") ? "describe" : "general";
    
    return new
    {
        original_query = request.Query,
        keywords,
        intent,
        concepts = ExtractConcepts(keywords)
    };
});

List<string> ExtractConcepts(List<string> keywords)
{
    var concepts = new List<string>();
    var knownConcepts = new[] { "lightbulb", "factory", "factories", "invention" };
    
    foreach (var keyword in keywords)
    {
        if (knownConcepts.Contains(keyword))
            concepts.Add(keyword);
    }
    
    return concepts;
}

app.Run();
```

**Acceptance**: Parses "Why was the lightbulb important for factories?" correctly

---

## Step 5: Output Processor Service

**File**: `src/Myriad.Services.OutputProcessor/Program.cs`

```csharp
var builder = WebApplication.CreateBuilder(args);
builder.WebHost.UseUrls("http://localhost:5004");

var app = builder.Build();

app.MapGet("/health", () => new { status = "healthy", service = "Output_Processor" });

app.MapPost("/synthesize", (List<AgentResponse> responses) =>
{
    // Simple concatenation for now
    var allData = new List<string>();
    var sources = new List<string>();
    
    foreach (var response in responses)
    {
        sources.Add(response.AgentId);
        
        foreach (var (key, value) in response.Data)
        {
            allData.Add($"{key}: {value}");
        }
    }
    
    var answer = string.Join(". ", allData);
    
    return new
    {
        answer,
        sources,
        confidence = responses.Average(r => r.Confidence)
    };
});

app.Run();
```

**Acceptance**: Combines multiple agent responses into coherent answer

---

## Step 6: Update Orchestrator with Graph Discovery

**File**: Update `src/Myriad.Services.Orchestrator/Program.cs`

```csharp
app.MapPost("/process", async (
    QueryRequest request,
    IHttpClientFactory httpClientFactory) =>
{
    var httpClient = httpClientFactory.CreateClient();
    
    // Step 1: Parse query
    var parseResponse = await httpClient.PostAsJsonAsync(
        "http://localhost:5003/parse", request);
    var parsed = await parseResponse.Content.ReadFromJsonAsync<dynamic>();
    
    // Step 2: Discover agents via graph
    var concepts = parsed.concepts;
    var agentResponses = new List<AgentResponse>();
    
    foreach (var concept in concepts)
    {
        var graphResponse = await httpClient.GetAsync(
            $"http://localhost:5008/agents/concept/{concept}");
        var agentsData = await graphResponse.Content.ReadFromJsonAsync<dynamic>();
        
        // Call each discovered agent
        foreach (var agent in agentsData.agents)
        {
            var agentResponse = await httpClient.PostAsJsonAsync(
                $"{agent.endpoint}/process", request);
            var agentResult = await agentResponse.Content
                .ReadFromJsonAsync<AgentResponse>();
            agentResponses.Add(agentResult);
        }
    }
    
    // Step 3: Synthesize output
    var synthesisResponse = await httpClient.PostAsJsonAsync(
        "http://localhost:5004/synthesize", agentResponses);
    var final = await synthesisResponse.Content.ReadFromJsonAsync<dynamic>();
    
    return Results.Ok(final);
});
```

**Acceptance**: Full pipeline works end-to-end

---

## Testing

```bash
# Start all services (5 terminals)
dotnet run --project src/Myriad.Agents.Static.Lightbulb
dotnet run --project src/Myriad.Agents.Static.Factory
dotnet run --project src/Myriad.Services.GraphDatabase
dotnet run --project src/Myriad.Services.InputProcessor
dotnet run --project src/Myriad.Services.OutputProcessor
dotnet run --project src/Myriad.Services.Orchestrator

# Test end-to-end
curl -X POST http://localhost:5000/process \
  -H "Content-Type: application/json" \
  -d '{"query": "Why was the lightbulb important for factories?"}'
```

**Expected**: Gets response combining Lightbulb_AI and Factory_AI data

---

## Acceptance Criteria

- [ ] Custom graph database stores and retrieves nodes/edges
- [ ] GraphDB Manager service runs on port 5008
- [ ] Input Processor extracts concepts correctly
- [ ] Output Processor synthesizes multiple responses
- [ ] Factory_AI agent provides factory knowledge
- [ ] Orchestrator uses graph for agent discovery
- [ ] End-to-end query returns synthesized answer
- [ ] No external dependencies added

**Time Estimate**: 3-4 weeks

---

---

## What You've Built

At the end of Phase 2, you have:
- ✅ Custom graph database (zero external dependencies)
- ✅ Agent discovery via graph traversal
- ✅ Query processing pipeline (Input → Orchestrator → Agents → Output)
- ✅ Multiple specialized agents working together
- ✅ Foundation for **emergent intelligence** through agent collaboration

This establishes the principle: **intelligence emerges from the network**, not from individual components.

---

**Next Phase**: [Phase 3 - MVP Complete](phase-3-mvp.md) - Add intelligent agent selection and Hebbian learning

[Back to Roadmap](README.md) | [Architecture Docs](../architecture/)

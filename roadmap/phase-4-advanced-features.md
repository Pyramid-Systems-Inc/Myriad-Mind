# Phase 4: Advanced Features - Human-Like Capabilities

**Duration**: 4-5 weeks
**Goal**: Context understanding, cognitive synthesis, and neurogenesis
**Prerequisites**: Phase 3 complete

---

## Objectives

✅ **4-Layer Context System** - Session, User, World, and Discourse context
✅ **Reference Resolution** - Pronouns and entity tracking with salience
✅ **4-Stage Cognitive Synthesizer** - Thematic analysis → Narrative weaving → Summarization → Formatting
✅ **Dynamic Lifecycle Manager** - Full neurogenesis pipeline (5 phases)
✅ **5-Phase Autonomous Learning** - Bootstrap → Research → Development → Optimization → Validation
✅ **Multi-turn Conversations** - Session memory and entity tracking

---

## Architecture References

This phase implements components from:
- [`context-understanding-csharp.md`](../architecture/context-understanding-csharp.md) - 4-layer context architecture
- [`cognitive-synthesizer-csharp.md`](../architecture/cognitive-synthesizer-csharp.md) - 4-stage synthesis pipeline
- [`neurogenesis-csharp.md`](../architecture/neurogenesis-csharp.md) - Dynamic agent creation
- [`graph-intelligence-csharp.md`](../architecture/graph-intelligence-csharp.md) - Enhanced discovery

---

## Step 1: Multi-Layer Context System

### Overview: 4-Layer Context Architecture

Following [`context-understanding-csharp.md`](../architecture/context-understanding-csharp.md), implement comprehensive context understanding:

1. **Session Context (Working Memory)** - Immediate conversation state
2. **User Context (Episodic Memory)** - Long-term user profile
3. **World Context (Semantic Memory)** - General knowledge
4. **Discourse Context** - Conversation flow and structure

### 1.1: Session Context Manager

**File**: `src/Myriad.Core.Context/SessionContext.cs`

```csharp
namespace Myriad.Core.Context;

public class SessionContext
{
    public required string SessionId { get; init; }
    public required string UserId { get; init; }
    public LinkedList<ConversationTurn> TurnHistory { get; init; } = new();
    public Dictionary<string, TrackedEntity> EntityTracker { get; init; } = new();
    public int MaxTurns { get; init; } = 10;
    
    public void AddTurn(ConversationTurn turn)
    {
        TurnHistory.AddLast(turn);
        if (TurnHistory.Count > MaxTurns)
            TurnHistory.RemoveFirst();
        
        UpdateEntityTracker(turn);
    }
    
    private void UpdateEntityTracker(ConversationTurn turn)
    {
        foreach (var (name, mention) in turn.Entities)
        {
            if (EntityTracker.ContainsKey(name))
            {
                EntityTracker[name].Boost();
            }
            else
            {
                EntityTracker[name] = new TrackedEntity
                {
                    Name = name,
                    Type = mention.Type,
                    Salience = mention.Salience
                };
            }
        }
        
        // Decay non-mentioned entities
        foreach (var entity in EntityTracker.Values)
        {
            if (!turn.Entities.ContainsKey(entity.Name))
                entity.Decay();
        }
    }
}

public record ConversationTurn
{
    public int TurnId { get; init; }
    public required string Query { get; init; }
    public string? ResolvedQuery { get; init; }
    public List<string> Concepts { get; init; } = new();
    public Dictionary<string, EntityMention> Entities { get; init; } = new();
}

public class TrackedEntity
{
    public required string Name { get; init; }
    public required string Type { get; init; }
    public float Salience { get; set; }
    
    public void Boost(float delta = 0.3f) => 
        Salience = Math.Min(1.0f, Salience * 0.9f + delta);
    
    public void Decay(float factor = 0.95f) => 
        Salience *= factor;
}

public record EntityMention(string Type, float Salience);
```

**File**: `src/Myriad.Core.Context/SessionContextManager.cs`

```csharp
using Microsoft.Extensions.Caching.Memory;

namespace Myriad.Core.Context;

public class SessionContextManager
{
    private readonly IMemoryCache _cache;
    private readonly TimeSpan _sessionTtl = TimeSpan.FromMinutes(30);
    
    public SessionContextManager(IMemoryCache cache)
    {
        _cache = cache;
    }
    
    public SessionContext GetOrCreateSession(string userId, string? sessionId = null)
    {
        sessionId ??= $"sess_{userId}_{DateTime.UtcNow:yyyyMMddHHmmss}";
        
        if (_cache.TryGetValue<SessionContext>(sessionId, out var session))
        {
            _cache.Set(sessionId, session, _sessionTtl); // Extend TTL
            return session;
        }
        
        var newSession = new SessionContext
        {
            SessionId = sessionId,
            UserId = userId
        };
        
        _cache.Set(sessionId, newSession, _sessionTtl);
        return newSession;
    }
    
    public void AddTurn(string sessionId, ConversationTurn turn)
    {
        if (_cache.TryGetValue<SessionContext>(sessionId, out var session))
        {
            session.AddTurn(turn);
            _cache.Set(sessionId, session, _sessionTtl);
        }
    }
}
```

### 1.2: User Context Manager (Graph-Based)

**File**: `src/Myriad.Core.Context/UserContextManager.cs`

```csharp
public class UserContextManager
{
    private readonly IGraphDatabase _graphDb;
    
    public async Task<UserNode> GetOrCreateUserAsync(string userId, CancellationToken ct)
    {
        // Find or create user profile in graph
        var users = await _graphDb.FindNodesAsync(
            n => n is UserNode un && un.UserId == userId, ct);
        
        if (users.Any()) return users.First() as UserNode;
        
        // Create new user with preferences
        var newUser = new UserNode
        {
            UserId = userId,
            Preferences = new UserPreferences(),
            ExpertiseLevels = new Dictionary<string, float>()
        };
        
        await _graphDb.UpsertNodeAsync(newUser, ct);
        return newUser;
    }
    
    public async Task<string> CreateConversationAsync(
        string userId, string sessionId, CancellationToken ct)
    {
        // Create conversation node and link to user
    }
    
    public async Task AddTurnToConversationAsync(
        string conversationId, ConversationTurn turn, CancellationToken ct)
    {
        // Link turn to conversation in graph
    }
}
```

**Acceptance**: Session context persists across multiple requests, user profiles stored in graph

---

## Step 2: Reference Resolution

**File**: `src/Myriad.Core.Context/ReferenceResolver.cs`

```csharp
namespace Myriad.Core.Context;

public class ReferenceResolver
{
    public (string resolvedQuery, List<Resolution> resolutions) ResolveReferences(
        string query,
        Dictionary<string, TrackedEntity> entityTracker)
    {
        var words = query.Split(' ');
        var resolutions = new List<Resolution>();
        var resolved = query;
        
        for (int i = 0; i < words.Length; i++)
        {
            var word = words[i].ToLowerInvariant().Trim('.', ',', '?', '!');
            
            if (IsPronoun(word))
            {
                var resolution = ResolvePronoun(word, entityTracker);
                if (resolution != null && resolution.Confidence > 0.7f)
                {
                    resolutions.Add(resolution);
                    resolved = resolved.Replace(words[i], resolution.ResolvedTo);
                }
            }
        }
        
        return (resolved, resolutions);
    }
    
    private bool IsPronoun(string word) =>
        new[] { "it", "that", "this", "they", "them" }.Contains(word);
    
    private Resolution? ResolvePronoun(
        string pronoun,
        Dictionary<string, TrackedEntity> entityTracker)
    {
        var candidates = entityTracker.Values
            .Where(e => e.Type != "Person") // "it" refers to non-persons
            .OrderByDescending(e => e.Salience)
            .ToList();
        
        if (!candidates.Any())
            return null;
        
        return new Resolution
        {
            Original = pronoun,
            ResolvedTo = candidates.First().Name,
            Confidence = candidates.First().Salience,
            Method = "rule_based"
        };
    }
}

public record Resolution
{
    public required string Original { get; init; }
    public required string ResolvedTo { get; init; }
    public required float Confidence { get; init; }
    public required string Method { get; init; }
}
```

**Test**:

```
Turn 1: "What is a lightbulb?"
Turn 2: "Who invented it?" → Resolved to "Who invented the lightbulb?"
```

**Acceptance**: Pronouns correctly resolve to recent entities

---

## Step 3: Cognitive Synthesizer (Simplified)

**File**: `src/Myriad.Services.Synthesis/ThematicAnalyzer.cs`

```csharp
namespace Myriad.Services.Synthesis;

public class ThematicAnalyzerAgent
{
    public ContentPlan AnalyzeThemes(Dictionary<string, AgentResult> results)
    {
        var themes = new Dictionary<string, List<string>>();
        
        foreach (var (id, result) in results)
        {
            var theme = DetermineTheme(result.Data);
            
            if (!themes.ContainsKey(theme))
                themes[theme] = new List<string>();
            
            themes[theme].Add(id);
        }
        
        return new ContentPlan
        {
            Introduction = themes.GetValueOrDefault("Definition") ?? new(),
            Themes = themes,
            Conclusion = themes.GetValueOrDefault("Impact") ?? new()
        };
    }
    
    private string DetermineTheme(Dictionary<string, object> data)
    {
        var keys = data.Keys.Select(k => k.ToLowerInvariant());
        
        if (keys.Any(k => k.Contains("definition") || k.Contains("describe")))
            return "Definition";
        if (keys.Any(k => k.Contains("history") || k.Contains("year")))
            return "Historical";
        if (keys.Any(k => k.Contains("impact") || k.Contains("effect")))
            return "Impact";
        
        return "General";
    }
}

public record ContentPlan
{
    public List<string> Introduction { get; init; } = new();
    public Dictionary<string, List<string>> Themes { get; init; } = new();
    public List<string> Conclusion { get; init; } = new();
}
```

**Acceptance**: Facts grouped into logical themes

---

## Step 4: Dynamic Lifecycle Manager (Basic)

**File**: `src/Myriad.Core.Lifecycle/DynamicLifecycleManager.cs`

```csharp
namespace Myriad.Core.Lifecycle;

public class DynamicLifecycleManager
{
    private readonly IGraphDatabase _graphDb;
    private int _nextPort = 6000;
    
    public async Task<Agent?> CreateAgentAsync(
        string concept,
        CancellationToken ct = default)
    {
        // Check if agent exists
        var exists = await _graphDb.FindNodesAsync(
            n => n is ConceptNode cn && cn.Name == concept, ct);
        
        if (exists.Any())
            return null; // Agent already exists
        
        // Simple template-based creation
        var agentCode = GenerateAgentCode(concept);
        var port = _nextPort++;
        
        // Write agent file
        var agentDir = Path.Combine("dynamic_agents", concept);
        Directory.CreateDirectory(agentDir);
        File.WriteAllText(Path.Combine(agentDir, "Program.cs"), agentCode);
        
        // Create project file
        var projectFile = GenerateProjectFile(concept);
        File.WriteAllText(
            Path.Combine(agentDir, $"{concept}.csproj"), 
            projectFile);
        
        // Build and start (simplified - production would use Process)
        // For MVP, just register in graph
        var agent = new AgentNode
        {
            Name = $"{concept}_AI",
            Endpoint = $"http://localhost:{port}",
            Port = port,
            Capabilities = new() { concept }
        };
        
        await _graphDb.UpsertNodeAsync(agent, ct);
        
        return new Agent
        {
            Name = agent.Name,
            Endpoint = agent.Endpoint,
            Port = port
        };
    }
    
    private string GenerateAgentCode(string concept) => $$"""
        using Myriad.Common.Models;
        
        var builder = WebApplication.CreateBuilder(args);
        var app = builder.Build();
        
        app.MapGet("/health", () => new { status = "healthy", agent = "{{concept}}_AI" });
        
        app.MapPost("/process", (QueryRequest request) =>
        {
            return new AgentResponse
            {
                AgentId = "{{concept}}_AI",
                Status = "success",
                Data = new Dictionary<string, object>
                {
                    ["concept"] = "{{concept}}",
                    ["note"] = "Dynamically created agent - knowledge TBD"
                },
                Confidence = 0.5f,
                ProcessingTimeMs = 5
            };
        });
        
        app.Run();
        """;
    
    private string GenerateProjectFile(string concept) => """
        <Project Sdk="Microsoft.NET.Sdk.Web">
          <PropertyGroup>
            <TargetFramework>net8.0</TargetFramework>
          </PropertyGroup>
        </Project>
        """;
}

public record Agent
{
    public required string Name { get; init; }
    public required string Endpoint { get; init; }
    public required int Port { get; init; }
}
```

**Acceptance**: New agent created when unknown concept detected

---

## Step 5: Integration

Update Orchestrator to use all new features:

```csharp
app.MapPost("/process", async (
    QueryRequest request,
    IHttpClientFactory httpClient,
    SessionContextManager sessionMgr,
    ReferenceResolver referenceResolver,
    DynamicLifecycleManager lifecycleMgr) =>
{
    // Get/create session
    var session = sessionMgr.GetOrCreateSession(
        request.UserId ?? "default",
        request.SessionId);
    
    // Resolve references
    var (resolvedQuery, resolutions) = referenceResolver.ResolveReferences(
        request.Query,
        session.EntityTracker);
    
    // Process with resolved query
    var parsedConcepts = await ParseQuery(resolvedQuery, httpClient);
    
    // Discover or create agents
    foreach (var concept in parsedConcepts)
    {
        var agents = await DiscoverAgents(concept, httpClient);
        
        if (!agents.Any())
        {
            // Trigger neurogenesis
            await lifecycleMgr.CreateAgentAsync(concept);
        }
    }
    
    // Continue normal processing...
    var responses = await CallAgents(parsedConcepts, httpClient);
    var synthesized = await Synthesize(responses, httpClient);
    
    // Store turn
    sessionMgr.AddTurn(session.SessionId, new ConversationTurn
    {
        TurnId = session.TurnHistory.Count + 1,
        Query = request.Query,
        ResolvedQuery = resolvedQuery,
        Concepts = parsedConcepts,
        Entities = ExtractEntities(parsedConcepts)
    });
    
    return Results.Ok(synthesized);
});
```

**Acceptance**: Full pipeline with context, reference resolution, and neurogenesis

---

## Testing

**Multi-turn Conversation Test**:

```bash
# Turn 1
curl -X POST http://localhost:5000/process \
  -d '{"query":"What is a lightbulb?","userId":"user1","sessionId":"test1"}'

# Turn 2 - uses reference "it"
curl -X POST http://localhost:5000/process \
  -d '{"query":"Who invented it?","userId":"user1","sessionId":"test1"}'
```

**Expected**: Turn 2 correctly resolves "it" to "lightbulb"

---

## Acceptance Criteria

- [ ] Session context persists across turns
- [ ] Reference resolution works for pronouns
- [ ] Thematic analyzer groups facts logically
- [ ] Dynamic lifecycle manager creates new agents
- [ ] Multi-turn conversations work correctly
- [ ] Response quality significantly improved
- [ ] New agents registered in graph automatically

**Time Estimate**: 4-5 weeks

---

**Next Phase**: [Phase 5 - Production Ready](phase-5-production.md)

[Back to Roadmap](README.md)

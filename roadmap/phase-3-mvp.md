# Phase 3: MVP Complete - Enhanced Intelligence

**Duration**: 2-3 weeks  
**Goal**: Production-quality MVP with intelligent agent selection and synthesis  
**Prerequisites**: Phase 2 complete

---

## Objectives

✅ Enhanced graph intelligence  
✅ Hebbian learning (connection strengthening)  
✅ Multi-criteria agent selection  
✅ Improved response synthesis  
✅ Handle 10+ diverse queries

---

## Step 1: Enhanced Graph Intelligence

**File**: `src/Myriad.Core.Intelligence/EnhancedGraphIntelligence.cs`

```csharp
namespace Myriad.Core.Intelligence;

public class EnhancedGraphIntelligence
{
    private readonly IGraphDatabase _graphDb;
    
    public async Task<List<AgentRelevanceScore>> DiscoverAgentsAsync(
        string concept,
        string intent,
        CancellationToken ct = default)
    {
        // Find concept nodes
        var concepts = await _graphDb.FindNodesAsync(
            n => n is ConceptNode cn && 
                 cn.Name.Contains(concept, StringComparison.OrdinalIgnoreCase),
            ct);
        
        if (!concepts.Any())
            return new List<AgentRelevanceScore>();
        
        var scores = new List<AgentRelevanceScore>();
        
        foreach (var conceptNode in concepts)
        {
            // Get edges to agents
            var edges = await _graphDb.GetEdgesFromAsync(conceptNode.Id, ct);
            
            foreach (var edge in edges.Where(e => e.Type == EdgeType.HandlesConcept))
            {
                var agentNode = await _graphDb.GetNodeAsync(edge.ToNodeId, ct);
                
                if (agentNode is AgentNode agent)
                {
                    var score = CalculateRelevance(agent, concept, intent, edge.Weight);
                    scores.Add(score);
                }
            }
        }
        
        return scores.OrderByDescending(s => s.RelevanceScore).ToList();
    }
    
    private AgentRelevanceScore CalculateRelevance(
        AgentNode agent,
        string concept,
        string intent,
        float hebbianWeight)
    {
        // Simple scoring for MVP
        var capabilityMatch = agent.Capabilities.Any(c => 
            c.Contains(concept, StringComparison.OrdinalIgnoreCase)) ? 0.5f : 0.2f;
        
        var relevance = (hebbianWeight * 0.6f) + (capabilityMatch * 0.4f);
        
        return new AgentRelevanceScore
        {
            AgentId = agent.Name,
            Endpoint = agent.Endpoint,
            RelevanceScore = relevance,
            Confidence = 0.8f,
            Reasoning = new List<string>
            {
                $"Hebbian weight: {hebbianWeight:F2}",
                $"Capability match: {capabilityMatch:F2}"
            }
        };
    }
}

public record AgentRelevanceScore
{
    public required string AgentId { get; init; }
    public required string Endpoint { get; init; }
    public required float RelevanceScore { get; init; }
    public required float Confidence { get; init; }
    public required List<string> Reasoning { get; init; }
}
```

**Acceptance**: Agents ranked by relevance, not just presence

---

## Step 2: Hebbian Learning Implementation

**File**: Add to `src/Myriad.Core.Graph/GraphEdge.cs`

```csharp
public record HandlesConceptEdge : GraphEdge
{
    public int UsageCount { get; set; }
    public int SuccessCount { get; set; }
    public float SuccessRate => UsageCount > 0 ? (float)SuccessCount / UsageCount : 0.5f;
    
    /// <summary>
    /// Strengthen connection after successful use
    /// </summary>
    public void Strengthen(float delta = 0.05f)
    {
        Weight = Math.Min(1.0f, Weight + delta);
        UsageCount++;
        SuccessCount++;
    }
    
    /// <summary>
    /// Weaken connection after failure
    /// </summary>
    public void Weaken(float delta = 0.02f)
    {
        Weight = Math.Max(0.0f, Weight - delta);
        UsageCount++;
    }
}
```

**File**: Add to GraphDB Manager service

```csharp
app.MapPost("/hebbian/strengthen", async (
    string agentId,
    string concept,
    bool success,
    IGraphDatabase db) =>
{
    // Find the edge between agent and concept
    var agents = await db.FindNodesAsync(
        n => n is AgentNode an && an.Name == agentId);
    var concepts = await db.FindNodesAsync(
        n => n is ConceptNode cn && cn.Name == concept);
    
    if (!agents.Any() || !concepts.Any())
        return Results.NotFound();
    
    var edges = await db.GetEdgesFromAsync(agents.First().Id);
    var edge = edges.FirstOrDefault(e => 
        e.ToNodeId == concepts.First().Id && 
        e is HandlesConceptEdge) as HandlesConceptEdge;
    
    if (edge == null)
        return Results.NotFound();
    
    if (success)
        edge.Strengthen();
    else
        edge.Weaken();
    
    return Results.Ok(new { 
        agent_id = agentId,
        concept,
        new_weight = edge.Weight,
        success_rate = edge.SuccessRate
    });
});
```

**Acceptance**: Agent-concept connections strengthen/weaken based on usage

---

## Step 3: Improved Response Synthesis

**File**: `src/Myriad.Services.OutputProcessor/Synthesizer.cs`

```csharp
namespace Myriad.Services.OutputProcessor;

public class ResponseSynthesizer
{
    public SynthesizedResponse Synthesize(List<AgentResponse> responses)
    {
        var paragraphs = new List<string>();
        var sources = new List<string>();
        
        // Group by agent for better organization
        foreach (var response in responses.OrderByDescending(r => r.Confidence))
        {
            sources.Add(response.AgentId);
            
            var sentences = new List<string>();
            foreach (var (key, value) in response.Data)
            {
                sentences.Add($"{FormatKey(key)}: {value}");
            }
            
            paragraphs.Add(string.Join(". ", sentences));
        }
        
        return new SynthesizedResponse
        {
            Answer = string.Join("\n\n", paragraphs),
            Sources = sources,
            Confidence = responses.Average(r => r.Confidence)
        };
    }
    
    private string FormatKey(string key)
    {
        // Convert snake_case to Title Case
        return string.Join(" ", key.Split('_')
            .Select(w => char.ToUpper(w[0]) + w[1..].ToLower()));
    }
}

public record SynthesizedResponse
{
    public required string Answer { get; init; }
    public required List<string> Sources { get; init; }
    public required float Confidence { get; init; }
}
```

**Acceptance**: Output is well-formatted with proper capitalization

---

## Step 4: Add More Agents for Testing

Create additional agents to test system:

1. **Edison_AI** (port 5005) - Information about Thomas Edison
2. **IndustrialRevolution_AI** (port 5006) - Industrial revolution context
3. **Electricity_AI** (port 5007) - Electrical systems

**Example**: `src/Myriad.Agents.Static.Edison/Program.cs`

```csharp
var builder = WebApplication.CreateBuilder(args);
builder.WebHost.UseUrls("http://localhost:5005");
var app = builder.Build();

app.MapGet("/health", () => new { status = "healthy", agent = "Edison_AI" });

app.MapPost("/process", (QueryRequest request) =>
{
    var knowledge = new Dictionary<string, object>
    {
        ["full_name"] = "Thomas Alva Edison",
        ["birth_year"] = 1847,
        ["key_inventions"] = new[] { "phonograph", "motion_pictures", "practical_lightbulb" },
        ["lightbulb_year"] = 1879,
        ["impact"] = "Revolutionized electric lighting and power distribution"
    };

    return new AgentResponse
    {
        AgentId = "Edison_AI",
        Status = "success",
        Data = knowledge,
        Confidence = 0.95f,
        ProcessingTimeMs = 5
    };
});

app.Run();
```

**Acceptance**: 5+ agents working, graph properly connected

---

## Step 5: Integration Testing

**File**: `tests/integration-tests.ps1`

```powershell
# Test queries to validate MVP
$queries = @(
    "What is a lightbulb?",
    "Why was the lightbulb important for factories?",
    "Who invented the lightbulb?",
    "How did factories work before electricity?",
    "What was the industrial revolution?"
)

foreach ($query in $queries) {
    Write-Host "`nTesting: $query" -ForegroundColor Green
    
    $body = @{query = $query} | ConvertTo-Json
    $response = Invoke-RestMethod -Uri "http://localhost:5000/process" `
        -Method Post -Body $body -ContentType "application/json"
    
    Write-Host "Answer: $($response.answer.Substring(0, 100))..."
    Write-Host "Sources: $($response.sources -join ', ')"
    Write-Host "Confidence: $($response.confidence)"
}
```

**Acceptance**: All queries return reasonable answers with appropriate sources

---

## Step 6: Hebbian Learning Validation

After running queries, verify Hebbian learning:

```bash
# Check edge weights after usage
curl http://localhost:5008/edges/stats

# Should show increased weights for frequently used agent-concept pairs
```

**Acceptance**: Weights increase for successful queries

---

## Acceptance Criteria

- [ ] Enhanced intelligence selects best agents
- [ ] Hebbian learning strengthens connections
- [ ] Response synthesis produces readable output
- [ ] 5+ agents working correctly
- [ ] System handles 10+ different queries
- [ ] Average response confidence > 0.8
- [ ] Average response time < 500ms
- [ ] Hebbian weights update correctly

**Time Estimate**: 2-3 weeks

---

## Known Limitations (To Address in Phase 4)

- No conversation memory
- Simple keyword-based parsing
- Basic synthesis (not human-like narratives)
- No dynamic agent creation
- No context understanding

---

**Next Phase**: [Phase 4 - Advanced Features](phase-4-advanced-features.md)

[Back to Roadmap](README.md)

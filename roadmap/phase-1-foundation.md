# Phase 1: Foundation & Core Component Setup

**Duration**: 2-3 weeks
**Goal**: Establish basic infrastructure with working orchestrator and first agent
**Prerequisites**: .NET 8.0 SDK installed

---

## Architecture Context

This phase implements the foundational infrastructure described in:
- [`system-overview-csharp.md`](../architecture/system-overview-csharp.md) - Overall system architecture
- [`core-philosophy.md`](../architecture/core-philosophy.md) - Design principles and biomimetic approach
- [`microservices-csharp.md`](../architecture/microservices-csharp.md) - Microservice patterns

---

## Objectives

✅ Create .NET solution structure
✅ Build Orchestrator service skeleton
✅ Create first static agent (Lightbulb_AI)
✅ Establish HTTP communication
✅ Implement basic health checks

---

## Step 1: Initialize Solution Structure

### Task 1.1: Create Solution and Projects

```bash
# Create solution
dotnet new sln -n Myriad

# Create core services
dotnet new webapi -n Myriad.Services.Orchestrator -minimal
dotnet new webapi -n Myriad.Agents.Static.Lightbulb -minimal

# Create common library
dotnet new classlib -n Myriad.Common

# Add projects to solution
dotnet sln add src/Myriad.Services.Orchestrator
dotnet sln add src/Myriad.Agents.Static.Lightbulb
dotnet sln add src/Myriad.Common
```

### Task 1.2: Project Structure

```
Myriad/
├── Myriad.sln
└── src/
    ├── Myriad.Services.Orchestrator/
    │   ├── Program.cs
    │   └── Myriad.Services.Orchestrator.csproj
    ├── Myriad.Agents.Static.Lightbulb/
    │   ├── Program.cs
    │   └── Myriad.Agents.Static.Lightbulb.csproj
    └── Myriad.Common/
        ├── Models/
        └── Myriad.Common.csproj
```

**Acceptance**: Solution builds successfully with `dotnet build`

---

## Step 2: Create Common Data Models

### Task 2.1: Define Shared Models

**File**: `src/Myriad.Common/Models/AgentResponse.cs`

```csharp
namespace Myriad.Common.Models;

/// <summary>
/// Standard response from any agent
/// </summary>
public record AgentResponse
{
    public required string AgentId { get; init; }
    public required string Status { get; init; } // "success" or "error"
    public Dictionary<string, object> Data { get; init; } = new();
    public float Confidence { get; init; } = 1.0f;
    public long ProcessingTimeMs { get; init; }
    public string? Error { get; init; }
}
```

**File**: `src/Myriad.Common/Models/QueryRequest.cs`

```csharp
namespace Myriad.Common.Models;

public record QueryRequest
{
    public required string Query { get; init; }
    public string? SessionId { get; init; }
    public Dictionary<string, object>? Context { get; init; }
}
```

**Acceptance**: Common project builds and can be referenced by other projects

---

## Step 3: Build First Static Agent

### Task 3.1: Implement Lightbulb_AI Agent

**File**: `src/Myriad.Agents.Static.Lightbulb/Program.cs`

```csharp
using Myriad.Common.Models;

var builder = WebApplication.CreateBuilder(args);

// Configure to run on port 5001
builder.WebHost.UseUrls("http://localhost:5001");

var app = builder.Build();

// Health check endpoint
app.MapGet("/health", () => new
{
    status = "healthy",
    agent = "Lightbulb_AI",
    timestamp = DateTime.UtcNow
});

// Process endpoint - returns lightbulb knowledge
app.MapPost("/process", (QueryRequest request) =>
{
    var knowledge = new Dictionary<string, object>
    {
        ["definition"] = "An electric light with a wire filament heated to incandescence by an electric current",
        ["invention_year"] = 1879,
        ["inventor"] = "Thomas Edison",
        ["key_features"] = new[] { "artificial_lighting", "electrical", "industrial_era" },
        ["impact"] = "Revolutionized work hours by providing reliable artificial light"
    };

    return new AgentResponse
    {
        AgentId = "Lightbulb_AI",
        Status = "success",
        Data = knowledge,
        Confidence = 0.95f,
        ProcessingTimeMs = 5
    };
});

app.Run();
```

**Acceptance**: Agent runs on port 5001 and responds to `/health` and `/process`

---

## Step 4: Build Orchestrator Service

### Task 4.1: Implement Basic Orchestrator

**File**: `src/Myriad.Services.Orchestrator/Program.cs`

```csharp
using Myriad.Common.Models;

var builder = WebApplication.CreateBuilder(args);

// Configure to run on port 5000
builder.WebHost.UseUrls("http://localhost:5000");

// Add HttpClient for calling agents
builder.Services.AddHttpClient();

var app = builder.Build();

// Health check
app.MapGet("/health", () => new
{
    status = "healthy",
    service = "Orchestrator",
    timestamp = DateTime.UtcNow
});

// Main process endpoint
app.MapPost("/process", async (
    QueryRequest request,
    IHttpClientFactory httpClientFactory) =>
{
    var httpClient = httpClientFactory.CreateClient();
    
    // For MVP, hardcode single agent call
    var agentUrl = "http://localhost:5001/process";
    
    try
    {
        var response = await httpClient.PostAsJsonAsync(agentUrl, request);
        response.EnsureSuccessStatusCode();
        
        var agentResponse = await response.Content
            .ReadFromJsonAsync<AgentResponse>();
        
        return Results.Ok(new
        {
            status = "success",
            answer = agentResponse?.Data,
            agents_activated = 1
        });
    }
    catch (Exception ex)
    {
        return Results.Problem($"Error: {ex.Message}");
    }
});

app.Run();
```

**Acceptance**: Orchestrator runs on port 5000 and can call Lightbulb_AI

---

## Step 5: Testing & Validation

### Task 5.1: Manual Testing

**Test 1: Health Checks**

```bash
# Terminal 1: Start Lightbulb_AI
cd src/Myriad.Agents.Static.Lightbulb
dotnet run

# Terminal 2: Start Orchestrator
cd src/Myriad.Services.Orchestrator
dotnet run

# Terminal 3: Test health
curl http://localhost:5001/health
curl http://localhost:5000/health
```

**Expected**: Both return healthy status

**Test 2: End-to-End Query**

```bash
curl -X POST http://localhost:5000/process \
  -H "Content-Type: application/json" \
  -d '{"query": "What is a lightbulb?"}'
```

**Expected Response**:

```json
{
  "status": "success",
  "answer": {
    "definition": "An electric light with a wire filament...",
    "invention_year": 1879,
    "inventor": "Thomas Edison"
  },
  "agents_activated": 1
}
```

### Task 5.2: Create Test Script

**File**: `test-phase1.ps1` (Windows) or `test-phase1.sh` (Linux/Mac)

```powershell
# Start services
Start-Process dotnet -ArgumentList "run --project src/Myriad.Agents.Static.Lightbulb" -NoNewWindow
Start-Sleep -Seconds 3

Start-Process dotnet -ArgumentList "run --project src/Myriad.Services.Orchestrator" -NoNewWindow
Start-Sleep -Seconds 3

# Test health
Write-Host "Testing health endpoints..."
Invoke-RestMethod -Uri "http://localhost:5001/health"
Invoke-RestMethod -Uri "http://localhost:5000/health"

# Test query
Write-Host "Testing query processing..."
$body = @{query = "What is a lightbulb?"} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:5000/process" -Method Post -Body $body -ContentType "application/json"
```

**Acceptance**: Script runs successfully and returns expected responses

---

## Step 6: Documentation

### Task 6.1: Create README

**File**: `src/README.md`

```markdown
# Myriad - Phase 1 Complete

## Running the System

1. Start Lightbulb_AI agent:
   ```bash
   cd src/Myriad.Agents.Static.Lightbulb
   dotnet run
   ```

2. Start Orchestrator (in another terminal):

   ```bash
   cd src/Myriad.Services.Orchestrator
   dotnet run
   ```

3. Test the system:

   ```bash
   curl -X POST http://localhost:5000/process \
     -H "Content-Type: application/json" \
     -d '{"query": "What is a lightbulb?"}'
   ```

## Architecture

- **Orchestrator** (port 5000): Routes queries to agents
- **Lightbulb_AI** (port 5001): Static agent with lightbulb knowledge

## What's Working

✅ Basic HTTP communication
✅ Agent registration (hardcoded)
✅ Simple query processing
✅ JSON request/response

## Next Steps

- Phase 2: Add more agents and graph database

```

---

## Acceptance Criteria

**Must Complete All**:

- [ ] Solution builds without errors (`dotnet build`)
- [ ] Lightbulb_AI runs and responds to health check
- [ ] Orchestrator runs and responds to health check
- [ ] End-to-end query returns correct response
- [ ] Response time < 100ms
- [ ] Code follows C# conventions (PascalCase, async/await, etc.)
- [ ] No external NuGet packages added (only .NET SDK)

---

## Troubleshooting

**Port Already in Use**:
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <pid> /F

# Linux/Mac
lsof -ti:5000 | xargs kill -9
```

**Services Won't Start**:

- Check .NET SDK version: `dotnet --version` (should be 8.0+)
- Verify ports 5000-5001 are available
- Check firewall settings

---

## Time Estimates

- Solution setup: 2-4 hours
- Common models: 1-2 hours
- Lightbulb_AI: 2-3 hours
- Orchestrator: 3-4 hours
- Testing: 2-3 hours
- Documentation: 1-2 hours

**Total**: ~11-18 hours (1.5-2.5 days)

---

---

## What You've Built

At the end of Phase 1, you have:
- ✅ Basic microservice architecture (ASP.NET Core Minimal APIs)
- ✅ First specialized agent (Lightbulb_AI)
- ✅ Central orchestrator for coordination
- ✅ HTTP-based agent communication
- ✅ Foundation for emergent intelligence

This establishes the core principle: **radical specialization** - each agent knows one thing perfectly.

---

**Next Phase**: [Phase 2 - Core Services](phase-2-core-services.md) - Add custom graph database and processing pipeline

[Back to Roadmap](README.md) | [Architecture Docs](../architecture/)

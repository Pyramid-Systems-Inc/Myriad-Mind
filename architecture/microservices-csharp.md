# Myriad Cognitive Architecture - Microservices (C#/.NET Edition)

**Architecture Documentation** | [Overview](system-overview-csharp.md) | [Graph Intelligence](graph-intelligence-csharp.md) | [Neurogenesis](neurogenesis-csharp.md)

Comprehensive documentation of the microservices architecture adapted for C# and ASP.NET Core, including service catalog, communication patterns, deployment infrastructure, and zero-dependency implementation strategy.

[← Back to Overview](system-overview-csharp.md) | [Graph Intelligence →](graph-intelligence-csharp.md)

---

## Table of Contents

- [Microservice Architecture Overview](#microservice-architecture-overview)
- [Service Catalog](#service-catalog)
- [Communication Patterns](#communication-patterns)
- [Service Discovery](#service-discovery)
- [Production Infrastructure](#production-infrastructure)
- [Deployment Architecture](#deployment-architecture)
- [API Contracts](#api-contracts)
- [C# Implementation Patterns](#c-implementation-patterns)

---

## Microservice Architecture Overview

### Design Philosophy

The Myriad system follows a **microservices architecture** where each service is:

- **Independently Deployable**: ASP.NET Core services in separate containers
- **Single Responsibility**: Focused on one specific aspect of cognition
- **Technology Agnostic**: Services communicate via HTTP/JSON (custom serialization)
- **Fault Tolerant**: Circuit breakers prevent cascading failures
- **Horizontally Scalable**: Multiple instances behind load balancers

### C#/.NET Specific Patterns

```csharp
// Base microservice structure
namespace Myriad.Services.Common
{
    public abstract class MyriadServiceBase
    {
        protected readonly ILogger Logger;
        protected readonly IConfiguration Configuration;
        
        public MyriadServiceBase(ILogger logger, IConfiguration configuration)
        {
            Logger = logger;
            Configuration = configuration;
        }
        
        /// <summary>
        /// Configure common middleware
        /// </summary>
        public virtual void ConfigureCommonMiddleware(WebApplication app)
        {
            // Health checks
            app.MapGet("/health", () => new HealthCheckResponse
            {
                Status = "healthy",
                Service = GetType().Name,
                Timestamp = DateTime.UtcNow
            });
            
            // Metrics endpoint
            app.MapGet("/metrics", GetMetrics);
            
            // Custom error handling (no external libraries)
            app.UseExceptionHandler(errorApp =>
            {
                errorApp.Run(async context =>
                {
                    context.Response.StatusCode = 500;
                    context.Response.ContentType = "application/json";
                    
                    var error = context.Features.Get<IExceptionHandlerFeature>();
                    if (error != null)
                    {
                        Logger.LogError(error.Error, "Unhandled exception");
                        await context.Response.WriteAsJsonAsync(new
                        {
                            error = "Internal server error",
                            timestamp = DateTime.UtcNow
                        });
                    }
                });
            });
        }
        
        protected abstract Task<object> GetMetrics();
    }
}
```

---

## Service Catalog

### Core Services

#### 1. Orchestrator Service

**Framework**: ASP.NET Core Minimal APIs  
**Port**: 5000  
**Language**: C# 10+

**Project Structure**:

```
src/Myriad.Services.Orchestrator/
├── Program.cs                      // Main entry point
├── OrchestratorService.cs         // Core orchestration logic
├── AgentDiscovery/
│   ├── IAgentDiscovery.cs         // Discovery interface
│   └── GraphBasedDiscovery.cs     // Graph traversal discovery
├── TaskExecution/
│   ├── ITaskExecutor.cs           // Executor interface
│   ├── ParallelTaskExecutor.cs    // Async parallel execution
│   └── CircuitBreaker.cs          // Custom circuit breaker
├── Neurogenesis/
│   ├── INeurogenesisCoordinator.cs
│   └── NeurogenesisCoordinator.cs
└── Models/
    ├── TaskRequest.cs
    ├── TaskResponse.cs
    └── AgentResponse.cs
```

**Key Implementation**:

```csharp
// Program.cs
using Myriad.Services.Orchestrator;

var builder = WebApplication.CreateBuilder(args);

// Register services
builder.Services.AddSingleton<OrchestratorService>();
builder.Services.AddSingleton<IAgentDiscovery, GraphBasedDiscovery>();
builder.Services.AddSingleton<ITaskExecutor, ParallelTaskExecutor>();
builder.Services.AddSingleton<INeurogenesisCoordinator, NeurogenesisCoordinator>();

// Configure HttpClient factory (custom implementation)
builder.Services.AddSingleton<IHttpClientFactory, CustomHttpClientFactory>();

var app = builder.Build();

// Main processing endpoint
app.MapPost("/process", async (
    ProcessRequest request,
    OrchestratorService orchestrator,
    CancellationToken cancellationToken) =>
{
    var result = await orchestrator.ProcessQueryAsync(request, cancellationToken);
    return Results.Ok(result);
});

// Agent discovery endpoint
app.MapPost("/discover", async (
    DiscoveryRequest request,
    IAgentDiscovery discovery,
    CancellationToken cancellationToken) =>
{
    var agents = await discovery.DiscoverAgentsAsync(
        request.Concept,
        request.Intent,
        cancellationToken);
    
    return Results.Ok(new { agents });
});

// Metrics endpoint
app.MapGet("/metrics", (OrchestratorService orchestrator) =>
{
    return orchestrator.GetMetrics();
});

app.Run();

// Request models
record ProcessRequest(
    string Query,
    string? SessionId = null,
    string? UserId = null,
    Dictionary<string, object>? Context = null);

record DiscoveryRequest(string Concept, string Intent);
```

**OrchestratorService.cs**:

```csharp
namespace Myriad.Services.Orchestrator
{
    public class OrchestratorService
    {
        private readonly IAgentDiscovery _agentDiscovery;
        private readonly ITaskExecutor _taskExecutor;
        private readonly INeurogenesisCoordinator _neurogenesis;
        private readonly ILogger<OrchestratorService> _logger;
        
        // Metrics
        private long _totalQueries;
        private long _successfulQueries;
        private readonly ConcurrentDictionary<string, long> _conceptCounts;
        
        public OrchestratorService(
            IAgentDiscovery agentDiscovery,
            ITaskExecutor taskExecutor,
            INeurogenesisCoordinator neurogenesis,
            ILogger<OrchestratorService> logger)
        {
            _agentDiscovery = agentDiscovery;
            _taskExecutor = taskExecutor;
            _neurogenesis = neurogenesis;
            _logger = logger;
            _conceptCounts = new ConcurrentDictionary<string, long>();
        }
        
        public async Task<ProcessResponse> ProcessQueryAsync(
            ProcessRequest request,
            CancellationToken cancellationToken)
        {
            Interlocked.Increment(ref _totalQueries);
            
            try
            {
                // Parse query (simplified - full parsing in Input Processor)
                var concepts = ExtractConcepts(request.Query);
                var intent = DetermineIntent(request.Query);
                
                // Discover agents
                var agents = await _agentDiscovery.DiscoverAgentsAsync(
                    concepts.First(),
                    intent,
                    cancellationToken);
                
                if (!agents.Any())
                {
                    // Trigger neurogenesis
                    _logger.LogInformation(
                        "No agents found for concept '{Concept}' - triggering neurogenesis",
                        concepts.First());
                    
                    var newAgent = await _neurogenesis.CreateAgentAsync(
                        concepts.First(),
                        intent,
                        cancellationToken);
                    
                    if (newAgent != null)
                    {
                        agents = await _agentDiscovery.DiscoverAgentsAsync(
                            concepts.First(),
                            intent,
                            cancellationToken);
                    }
                }
                
                // Execute tasks in parallel
                var results = await _taskExecutor.ExecuteParallelAsync(
                    agents,
                    request.Query,
                    intent,
                    cancellationToken);
                
                // Update metrics
                Interlocked.Increment(ref _successfulQueries);
                _conceptCounts.AddOrUpdate(concepts.First(), 1, (key, count) => count + 1);
                
                return new ProcessResponse
                {
                    Status = "success",
                    SessionId = request.SessionId ?? Guid.NewGuid().ToString(),
                    Results = results,
                    Metadata = new Dictionary<string, object>
                    {
                        ["agents_activated"] = agents.Count(),
                        ["processing_time_ms"] = 0 // TODO: measure
                    }
                };
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error processing query: {Query}", request.Query);
                
                return new ProcessResponse
                {
                    Status = "error",
                    Error = "Processing failed",
                    Metadata = new Dictionary<string, object>()
                };
            }
        }
        
        public object GetMetrics()
        {
            return new
            {
                total_queries = _totalQueries,
                successful_queries = _successfulQueries,
                success_rate = _totalQueries > 0 
                    ? (double)_successfulQueries / _totalQueries 
                    : 0.0,
                top_concepts = _conceptCounts
                    .OrderByDescending(kvp => kvp.Value)
                    .Take(10)
                    .ToDictionary(kvp => kvp.Key, kvp => kvp.Value)
            };
        }
        
        private List<string> ExtractConcepts(string query) =>
            query.Split(' ', StringSplitOptions.RemoveEmptyEntries).ToList();
        
        private string DetermineIntent(string query) =>
            query.StartsWith("What") ? "define" : "explain";
    }
    
    public record ProcessResponse
    {
        public required string Status { get; init; }
        public string? SessionId { get; init; }
        public object? Results { get; init; }
        public string? Error { get; init; }
        public Dictionary<string, object>? Metadata { get; init; }
    }
}
```

#### 2. GraphDB Manager Service

**Framework**: ASP.NET Core Minimal APIs  
**Port**: 5008  
**Dependencies**: Custom graph database (zero external libraries)

**Implementation**: See [graph-intelligence-csharp.md](graph-intelligence-csharp.md)

#### 3. Input Processor Service

**Framework**: ASP.NET Core  
**Port**: 5003  
**Purpose**: Advanced query parsing and understanding

**Key Classes**:

```csharp
namespace Myriad.Services.InputProcessor
{
    public class InputProcessorService
    {
        private readonly IKeywordExtractor _keywordExtractor;
        private readonly IIntentRecognizer _intentRecognizer;
        private readonly IAmbiguityResolver _ambiguityResolver;
        
        public async Task<EnhancedQuery> ProcessQueryAsync(
            string rawQuery,
            CancellationToken cancellationToken)
        {
            // Extract keywords and concepts
            var keywords = await _keywordExtractor.ExtractAsync(rawQuery, cancellationToken);
            
            // Recognize intent
            var intent = await _intentRecognizer.RecognizeAsync(rawQuery, cancellationToken);
            
            // Detect and resolve ambiguities
            var ambiguities = await _ambiguityResolver.DetectAsync(rawQuery, keywords, cancellationToken);
            
            return new EnhancedQuery
            {
                OriginalQuery = rawQuery,
                ResolvedQuery = rawQuery, // After ambiguity resolution
                Concepts = keywords.Concepts,
                Intent = intent.PrimaryIntent,
                IntentConfidence = intent.Confidence,
                Ambiguities = ambiguities,
                TaskList = GenerateTaskList(keywords, intent)
            };
        }
    }
}
```

#### 4. Output Processor Service

**Framework**: ASP.NET Core  
**Port**: 5004  
**Purpose**: Response synthesis and formatting

```csharp
namespace Myriad.Services.OutputProcessor
{
    public class OutputProcessorService
    {
        private readonly IResponseSynthesizer _synthesizer;
        private readonly IResponseFormatter _formatter;
        
        public async Task<FormattedResponse> ProcessResponseAsync(
            List<AgentResponse> agentResponses,
            string originalQuery,
            CancellationToken cancellationToken)
        {
            // Synthesize multi-agent responses
            var synthesized = await _synthesizer.SynthesizeAsync(
                agentResponses,
                cancellationToken);
            
            // Format for user
            var formatted = await _formatter.FormatAsync(
                synthesized,
                ResponseFormat.Explanatory,
                cancellationToken);
            
            return new FormattedResponse
            {
                Answer = formatted.Text,
                Confidence = synthesized.Confidence,
                Sources = agentResponses.Select(r => r.AgentId).ToList(),
                Metadata = formatted.Metadata
            };
        }
    }
}
```

---

## Communication Patterns

### Current Pattern: Synchronous HTTP with Retry

**Custom HTTP Client Implementation** (zero external dependencies):

```csharp
namespace Myriad.Core.Http
{
    /// <summary>
    /// Custom HTTP client with retry logic and circuit breaker
    /// </summary>
    public class ResilientHttpClient
    {
        private readonly HttpClient _httpClient;
        private readonly CircuitBreaker _circuitBreaker;
        private readonly int _maxRetries;
        private readonly TimeSpan _baseDelay;
        
        public ResilientHttpClient(
            HttpClient httpClient,
            CircuitBreaker circuitBreaker,
            int maxRetries = 3,
            TimeSpan? baseDelay = null)
        {
            _httpClient = httpClient;
            _circuitBreaker = circuitBreaker;
            _maxRetries = maxRetries;
            _baseDelay = baseDelay ?? TimeSpan.FromMilliseconds(300);
        }
        
        /// <summary>
        /// Send HTTP request with retry and circuit breaker
        /// </summary>
        public async Task<HttpResponseMessage> SendWithRetryAsync(
            HttpRequestMessage request,
            CancellationToken cancellationToken = default)
        {
            return await _circuitBreaker.ExecuteAsync(async () =>
            {
                HttpResponseMessage? lastResponse = null;
                Exception? lastException = null;
                
                for (int attempt = 0; attempt < _maxRetries; attempt++)
                {
                    try
                    {
                        var clonedRequest = await CloneRequestAsync(request, cancellationToken);
                        lastResponse = await _httpClient.SendAsync(clonedRequest, cancellationToken);
                        
                        // Check if successful
                        if (lastResponse.IsSuccessStatusCode)
                        {
                            return lastResponse;
                        }
                        
                        // Retry on 502, 503, 504
                        if (lastResponse.StatusCode == System.Net.HttpStatusCode.BadGateway ||
                            lastResponse.StatusCode == System.Net.HttpStatusCode.ServiceUnavailable ||
                            lastResponse.StatusCode == System.Net.HttpStatusCode.GatewayTimeout)
                        {
                            if (attempt < _maxRetries - 1)
                            {
                                // Exponential backoff
                                var delay = _baseDelay.Multiply(Math.Pow(2, attempt));
                                await Task.Delay(delay, cancellationToken);
                                continue;
                            }
                        }
                        
                        return lastResponse;
                    }
                    catch (HttpRequestException ex)
                    {
                        lastException = ex;
                        
                        if (attempt < _maxRetries - 1)
                        {
                            var delay = _baseDelay.Multiply(Math.Pow(2, attempt));
                            await Task.Delay(delay, cancellationToken);
                        }
                    }
                }
                
                // All retries failed
                if (lastResponse != null)
                {
                    return lastResponse;
                }
                
                throw lastException ?? new HttpRequestException("Request failed after all retries");
            });
        }
        
        private async Task<HttpRequestMessage> CloneRequestAsync(
            HttpRequestMessage request,
            CancellationToken cancellationToken)
        {
            var clone = new HttpRequestMessage(request.Method, request.RequestUri);
            
            // Clone headers
            foreach (var header in request.Headers)
            {
                clone.Headers.TryAddWithoutValidation(header.Key, header.Value);
            }
            
            // Clone content
            if (request.Content != null)
            {
                var contentBytes = await request.Content.ReadAsByteArrayAsync(cancellationToken);
                clone.Content = new ByteArrayContent(contentBytes);
                
                foreach (var header in request.Content.Headers)
                {
                    clone.Content.Headers.TryAddWithoutValidation(header.Key, header.Value);
                }
            }
            
            return clone;
        }
    }
}
```

**Circuit Breaker Implementation**:

```csharp
namespace Myriad.Core.Resilience
{
    /// <summary>
    /// Custom circuit breaker pattern implementation
    /// </summary>
    public class CircuitBreaker
    {
        private readonly int _failureThreshold;
        private readonly TimeSpan _timeout;
        private readonly ILogger _logger;
        
        private volatile CircuitState _state = CircuitState.Closed;
        private int _failureCount;
        private DateTime _lastFailureTime;
        private readonly object _lock = new();
        
        public CircuitBreaker(
            int failureThreshold = 5,
            TimeSpan? timeout = null,
            ILogger? logger = null)
        {
            _failureThreshold = failureThreshold;
            _timeout = timeout ?? TimeSpan.FromSeconds(60);
            _logger = logger ?? NullLogger.Instance;
        }
        
        public async Task<T> ExecuteAsync<T>(Func<Task<T>> operation)
        {
            // Check state
            if (_state == CircuitState.Open)
            {
                // Check if timeout has elapsed
                if (DateTime.UtcNow - _lastFailureTime > _timeout)
                {
                    _logger.LogInformation("Circuit breaker entering half-open state");
                    _state = CircuitState.HalfOpen;
                }
                else
                {
                    throw new CircuitBreakerOpenException(
                        "Circuit breaker is open - service unavailable");
                }
            }
            
            try
            {
                var result = await operation();
                
                // Success - reset if half-open
                if (_state == CircuitState.HalfOpen)
                {
                    _logger.LogInformation("Circuit breaker closing - service recovered");
                    Reset();
                }
                
                return result;
            }
            catch (Exception ex)
            {
                RecordFailure();
                throw;
            }
        }
        
        private void RecordFailure()
        {
            lock (_lock)
            {
                _failureCount++;
                _lastFailureTime = DateTime.UtcNow;
                
                if (_failureCount >= _failureThreshold)
                {
                    _logger.LogWarning(
                        "Circuit breaker opening - failure threshold reached ({Count})",
                        _failureCount);
                    
                    _state = CircuitState.Open;
                }
            }
        }
        
        private void Reset()
        {
            lock (_lock)
            {
                _failureCount = 0;
                _state = CircuitState.Closed;
            }
        }
    }
    
    public enum CircuitState
    {
        Closed,    // Normal operation
        Open,      // Failing - reject all requests
        HalfOpen   // Testing if service recovered
    }
    
    public class CircuitBreakerOpenException : Exception
    {
        public CircuitBreakerOpenException(string message) : base(message) { }
    }
}
```

### Target Pattern: Async Parallel Execution

```csharp
namespace Myriad.Services.Orchestrator.TaskExecution
{
    public class ParallelTaskExecutor : ITaskExecutor
    {
        private readonly IHttpClientFactory _httpClientFactory;
        private readonly ILogger<ParallelTaskExecutor> _logger;
        
        public async Task<List<AgentResponse>> ExecuteParallelAsync(
            IEnumerable<AgentInfo> agents,
            string query,
            string intent,
            CancellationToken cancellationToken)
        {
            // Create tasks for all agents
            var tasks = agents.Select(agent => 
                ExecuteAgentTaskAsync(agent, query, intent, cancellationToken));
            
            // Execute in parallel using Task.WhenAll
            var results = await Task.WhenAll(tasks);
            
            // Filter out failed results
            return results
                .Where(r => r.Status == "success")
                .ToList();
        }
        
        private async Task<AgentResponse> ExecuteAgentTaskAsync(
            AgentInfo agent,
            string query,
            string intent,
            CancellationToken cancellationToken)
        {
            try
            {
                var httpClient = _httpClientFactory.CreateClient(agent.AgentId);
                
                var request = new HttpRequestMessage(HttpMethod.Post, $"{agent.Endpoint}/process")
                {
                    Content = JsonContent.Create(new
                    {
                        query,
                        intent
                    })
                };
                
                using var timeout = new CancellationTokenSource(TimeSpan.FromSeconds(5));
                using var linked = CancellationTokenSource.CreateLinkedTokenSource(
                    cancellationToken, timeout.Token);
                
                var response = await httpClient.SendAsync(request, linked.Token);
                var content = await response.Content.ReadAsStringAsync(linked.Token);
                
                // Parse JSON (custom parser)
                var json = SimpleJsonParser.Parse(content);
                
                return new AgentResponse
                {
                    AgentId = agent.AgentId,
                    Status = "success",
                    Data = json,
                    ProcessingTimeMs = 0 // TODO: measure
                };
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Agent {AgentId} failed to process task", agent.AgentId);
                
                return new AgentResponse
                {
                    AgentId = agent.AgentId,
                    Status = "error",
                    Error = ex.Message
                };
            }
        }
    }
}
```

---

## Service Discovery

### Graph-Based Discovery

```csharp
namespace Myriad.Services.Orchestrator.AgentDiscovery
{
    public class GraphBasedDiscovery : IAgentDiscovery
    {
        private readonly IGraphDatabase _graphDb;
        private readonly EnhancedGraphIntelligence _intelligence;
        private readonly ILogger<GraphBasedDiscovery> _logger;
        
        public async Task<IEnumerable<AgentInfo>> DiscoverAgentsAsync(
            string concept,
            string intent,
            CancellationToken cancellationToken)
        {
            // Use enhanced graph intelligence for smart discovery
            var scoredAgents = await _intelligence.DiscoverAgentsAsync(
                concept,
                intent,
                context: null,
                cancellationToken);
            
            // Convert to AgentInfo
            return scoredAgents.Select(a => new AgentInfo
            {
                AgentId = a.AgentId,
                Endpoint = a.Endpoint,
                RelevanceScore = a.RelevanceScore,
                Confidence = a.Confidence
            });
        }
    }
}
```

---

## Production Infrastructure

### Docker Compose Configuration

```yaml
version: '3.8'

services:
  # Core Services
  orchestrator:
    build:
      context: ./src/Myriad.Services.Orchestrator
      dockerfile: Dockerfile
    ports:
      - "5000:80"
    environment:
      - ASPNETCORE_ENVIRONMENT=Production
      - GRAPHDB_URL=http://graphdb-manager:80
      - LIFECYCLE_MANAGER_URL=http://lifecycle-manager:80
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 1G
        reservations:
          memory: 512M
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:80/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    restart: unless-stopped
  
  graphdb-manager:
    build:
      context: ./src/Myriad.Services.GraphDatabase
      dockerfile: Dockerfile
    ports:
      - "5008:80"
    environment:
      - ASPNETCORE_ENVIRONMENT=Production
      - DATA_PATH=/data
    volumes:
      - graph-data:/data
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:80/health"]
      interval: 30s
    restart: unless-stopped
  
  input-processor:
    build:
      context: ./src/Myriad.Services.InputProcessor
      dockerfile: Dockerfile
    ports:
      - "5003:80"
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 256M
    restart: unless-stopped
  
  output-processor:
    build:
      context: ./src/Myriad.Services.OutputProcessor
      dockerfile: Dockerfile
    ports:
      - "5004:80"
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 256M
    restart: unless-stopped

volumes:
  graph-data:

networks:
  default:
    name: myriad_network
    driver: bridge
```

### Dockerfile Template

```dockerfile
# Myriad service Dockerfile template
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS base
WORKDIR /app
EXPOSE 80

FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src
COPY ["Myriad.Services.Orchestrator.csproj", "./"]
RUN dotnet restore
COPY . .
RUN dotnet build -c Release -o /app/build

FROM build AS publish
RUN dotnet publish -c Release -o /app/publish

FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "Myriad.Services.Orchestrator.dll"]
```

---

## API Contracts

### Standard Response Format

```csharp
namespace Myriad.Common.Models
{
    /// <summary>
    /// Standard response wrapper for all services
    /// </summary>
    public record StandardResponse<T>
    {
        public required string Status { get; init; } // "success", "error", "partial"
        public T? Data { get; init; }
        public ResponseMetadata? Metadata { get; init; }
        public List<ErrorInfo>? Errors { get; init; }
    }
    
    public record ResponseMetadata
    {
        public DateTime Timestamp { get; init; } = DateTime.UtcNow;
        public required string Service { get; init; }
        public string Version { get; init; } = "5.0";
        public long ProcessingTimeMs { get; init; }
    }
    
    public record ErrorInfo
    {
        public required string Code { get; init; }
        public required string Message { get; init; }
        public string? Details { get; init; }
    }
}
```

### Health Check Standard

```csharp
public record HealthCheckResponse
{
    public required string Status { get; init; } // "healthy", "degraded", "unhealthy"
    public required string Service { get; init; }
    public string Version { get; init; } = "5.0";
    public DateTime Timestamp { get; init; } = DateTime.UtcNow;
    public Dictionary<string, string>? Dependencies { get; init; }
}
```

---

## C# Implementation Patterns

### Minimal API Pattern

```csharp
var builder = WebApplication.CreateBuilder(args);

// Service registration
builder.Services.AddSingleton<IMyService, MyService>();

var app = builder.Build();

// Endpoints
app.MapGet("/endpoint", (IMyService service) => service.DoWork());

app.Run();
```

### Dependency Injection

```csharp
// Register in Program.cs
builder.Services.AddSingleton<IGraphDatabase, GraphDatabase>();
builder.Services.AddScoped<IOrchestratorService, OrchestratorService>();
builder.Services.AddTransient<ITaskExecutor, ParallelTaskExecutor>();

// Use in endpoints
app.MapPost("/process", async (
    ProcessRequest request,
    IOrchestratorService orchestrator) =>
{
    return await orchestrator.ProcessAsync(request);
});
```

### Background Services

```csharp
// Hebbian decay background service
public class HebbianDecayService : BackgroundService
{
    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        while (!stoppingToken.IsCancellationRequested)
        {
            await PerformDecayAsync(stoppingToken);
            await Task.Delay(TimeSpan.FromMinutes(15), stoppingToken);
        }
    }
}

// Register
builder.Services.AddHostedService<HebbianDecayService>();
```

---

**Document Version:** 1.0 C#  
**Last Updated:** 2025-01-09  
**Status:** Architecture Definition Phase

[← Overview](system-overview-csharp.md) | [↑ Back to Index](../INDEX.md) | [Neurogenesis →](neurogenesis-csharp.md)

using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Myriad.Services.Orchestrator;

var builder = WebApplication.CreateBuilder(args);

// 1. Register the Agent Registry as a Singleton (shared state)
builder.Services.AddSingleton<AgentRegistry>();

// 2. Register the Orchestrator Service
builder.Services.AddHttpClient<OrchestratorService>();

var app = builder.Build();

// --- Bootstrap Data (Simulating registration for MVP) ---
var registry = app.Services.GetRequiredService<AgentRegistry>();
// Register the Lightbulb Agent we created (assuming it runs locally on 5001)
registry.RegisterAgent("Lightbulb_AI", "http://localhost:5001");
// Register the Factory Agent (assuming it runs locally on 5002)
registry.RegisterAgent("Factory_AI", "http://localhost:5002");
// --------------------------------------------------------

app.MapGet("/health", () => new
{
    status = "healthy",
    service = "Orchestrator",
    timestamp = DateTime.UtcNow
});

// New Endpoint to trigger the ping manually
app.MapGet("/ping/{agentName}", async (string agentName, OrchestratorService orchestrator) =>
{
    var success = await orchestrator.PingAgentAsync(agentName);
    return success ? Results.Ok($"Successfully pinged {agentName}") : Results.Problem($"Failed to ping {agentName}");
});

app.Run();

namespace Myriad.Services.Orchestrator
{
    public partial class Program { }
}
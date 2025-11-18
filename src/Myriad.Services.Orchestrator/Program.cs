using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.Hosting;

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

// Minimal Health Check Endpoint
app.MapGet("/health", () => new
{
    status = "healthy",
    service = "Orchestrator",
    timestamp = DateTime.UtcNow
});

app.Run();

// Make Program class public for integration testing
public partial class Program { }
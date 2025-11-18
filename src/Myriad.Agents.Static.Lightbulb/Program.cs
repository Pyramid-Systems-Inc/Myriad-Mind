using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.Hosting;
using Microsoft.AspNetCore.Http;
using Myriad.Common; // Request/Response models
using System.Collections.Generic;
using System;

var builder = WebApplication.CreateBuilder(args);

// Hardcode port 5001 for this specific agent
builder.WebHost.UseUrls("http://localhost:5001");

var app = builder.Build();

// Define the Agent's Knowledge Base (Hardcoded for MVP)
var knowledgeBase = new Dictionary<string, object>
{
    { "definition", "An electric light with a wire filament heated to such a high temperature that it glows with visible light (incandescence)." },
    { "inventor", "Thomas Edison (commercial practical version)" },
    { "year", "1879" },
    { "impact", "Extended the workday into the night, revolutionizing factory productivity and social life." }
};

app.MapGet("/health", () => new
{
    status = "healthy",
    agent = "Lightbulb_AI",
    timestamp = DateTime.UtcNow
});

// The Core Intelligence Endpoint
app.MapPost("/process", (AgentRequest request) =>
{
    // In a full implementation, we would analyze request.Query
    // For this specialized MVP agent, we return our specific knowledge packet

    var response = new AgentResponse(
        SourceAgent: "Lightbulb_AI",
        Data: knowledgeBase
    );

    return Results.Ok(response);
});

app.Run();

namespace Myriad.Agents.Static.Lightbulb
{
    public partial class Program { }
}
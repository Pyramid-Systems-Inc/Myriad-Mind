using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.Hosting;
using Microsoft.AspNetCore.Http;
using Myriad.Common;
using System.Collections.Generic;
using System;

var builder = WebApplication.CreateBuilder(args);

// Hardcode port 5002
builder.WebHost.UseUrls("http://localhost:5002");

var app = builder.Build();

// Knowledge Base: Pre-electrical Factory Context
var knowledgeBase = new Dictionary<string, object>
{
    { "context", "Industrial factories prior to electrification." },
    { "limitation", "Production was limited by daylight hours." },
    { "hazard", "Gas lamps used for lighting were distinct fire hazards in dusty environments." },
    { "impact_of_light", "Reliable electric light allowed for safe 24-hour operation shifts." }
};

app.MapGet("/health", () => new 
{ 
    status = "healthy", 
    agent = "Factory_AI", 
    timestamp = DateTime.UtcNow 
});

app.MapPost("/process", (AgentRequest request) => 
{
    var response = new AgentResponse(
        SourceAgent: "Factory_AI",
        Data: knowledgeBase
    );

    return Results.Ok(response);
});

app.Run();

namespace Myriad.Agents.Static.Factory
{
    public partial class Program { }
}
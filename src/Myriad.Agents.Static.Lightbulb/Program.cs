using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.Hosting;

var builder = WebApplication.CreateBuilder(args);

// Hardcode port 5001 for this specific agent
builder.WebHost.UseUrls("http://localhost:5001");

var app = builder.Build();

app.MapGet("/health", () => new
{
    status = "healthy",
    agent = "Lightbulb_AI",
    timestamp = DateTime.UtcNow
});

app.Run();

// Class definitions must go at the bottom when using top-level statements
namespace Myriad.Agents.Static.Lightbulb
{
    public partial class Program { }
}
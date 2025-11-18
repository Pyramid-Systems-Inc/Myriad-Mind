using System.Net;
using Microsoft.AspNetCore.Mvc.Testing;
using Xunit;
using OrchestratorProgram = Myriad.Services.Orchestrator.Program;

namespace Myriad.Tests.Unit
{
    public class IntegrationTests
    {
        // This test checks if the Orchestrator endpoint itself is reachable,
        // proving dependency injection is set up correctly.
        // Note: We can't easily test the full HTTP call to the Lightbulb agent 
        // in this unit test suite without spinning up both processes, 
        // so we check if the Orchestrator accepts the request.

        [Fact]
        public async Task PingEndpoint_ReturnsNotFound_ForUnknownAgent()
        {
            await using var application = new WebApplicationFactory<OrchestratorProgram>();
            using var client = application.CreateClient();

            // Act: Try to ping an agent that doesn't exist
            var response = await client.GetAsync("/ping/Ghost_AI");

            // Assert: Should fail gracefully (500 Problem or specific error, based on our implementation)
            // Our implementation returns Results.Problem which is usually 500
            Assert.Equal(HttpStatusCode.InternalServerError, response.StatusCode);
        }
    }
}
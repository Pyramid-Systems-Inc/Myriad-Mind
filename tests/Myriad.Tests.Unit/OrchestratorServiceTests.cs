using System.Net;
using Microsoft.Extensions.Logging.Abstractions;
using Myriad.Services.Orchestrator;
using Myriad.Tests.Unit.Fakes;
using Xunit;

namespace Myriad.Tests.Unit
{
    public class OrchestratorServiceTests
    {
        [Fact]
        public async Task PingAgentAsync_ShouldCallCorrectUrl()
        {
            // Arrange
            var registry = new AgentRegistry();
            string agentName = "Test_AI";
            string agentUrl = "http://localhost:9999";
            registry.RegisterAgent(agentName, agentUrl);

            // Setup Fake HTTP Handler to capture the request
            var fakeHandler = new FakeHttpMessageHandler(new HttpResponseMessage(HttpStatusCode.OK));
            var httpClient = new HttpClient(fakeHandler);

            // Use NullLogger (built-in Microsoft extension)
            var logger = NullLogger<OrchestratorService>.Instance;

            var service = new OrchestratorService(registry, httpClient, logger);

            // Act
            var result = await service.PingAgentAsync(agentName);

            // Assert
            Assert.True(result); // Expect success
            Assert.NotNull(fakeHandler.LastRequest);
            Assert.Equal($"{agentUrl}/health", fakeHandler.LastRequest.RequestUri?.ToString());
        }
    }
}
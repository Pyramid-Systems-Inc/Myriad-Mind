using System.Net;
using Microsoft.Extensions.Logging.Abstractions;
using Myriad.Services.Orchestrator;
using Myriad.Tests.Unit.Fakes;
using Xunit;
using System.Net.Http.Json;
using Myriad.Common;

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
        [Fact]
        public async Task QueryAgentAsync_ShouldReturnAgentResponse()
        {
            // Arrange
            var registry = new AgentRegistry();
            string agentName = "Smart_AI";
            string agentUrl = "http://localhost:5005";
            registry.RegisterAgent(agentName, agentUrl);

            // Mock the Expected Response
            var expectedResponse = new AgentResponse("Smart_AI", new Dictionary<string, object> { { "fact", "tested" } });

            // Setup Fake Handler to return JSON
            var jsonContent = JsonContent.Create(expectedResponse);
            var fakeHandler = new FakeHttpMessageHandler(new HttpResponseMessage(HttpStatusCode.OK)
            {
                Content = jsonContent
            });
            var httpClient = new HttpClient(fakeHandler);
            var logger = NullLogger<OrchestratorService>.Instance;

            var service = new OrchestratorService(registry, httpClient, logger);
            var request = new AgentRequest("Test query", "test intent");

            // Act
            var result = await service.QueryAgentAsync(agentName, request);

            // Assert
            Assert.NotNull(result);
            Assert.Equal("Smart_AI", result.SourceAgent);
            Assert.Equal("tested", result.Data["fact"].ToString());

            // Verify request was a POST to /process
            Assert.NotNull(fakeHandler.LastRequest);
            Assert.Equal(HttpMethod.Post, fakeHandler.LastRequest.Method);
            Assert.Equal($"{agentUrl}/process", fakeHandler.LastRequest.RequestUri?.ToString());
        }
    }
}
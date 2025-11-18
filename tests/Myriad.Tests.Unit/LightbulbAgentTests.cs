using System.Net;
using System.Net.Http.Json;
using Microsoft.AspNetCore.Mvc.Testing;
using Myriad.Common; // Shared models
using Xunit;
using LightbulbProgram = Myriad.Agents.Static.Lightbulb.Program;

namespace Myriad.Tests.Unit
{
    public class LightbulbAgentTests
    {
        [Fact]
        public async Task GetHealth_ReturnsOkAndAgentName()
        {
            // (Existing test code...)
            await using var application = new WebApplicationFactory<LightbulbProgram>();
            using var client = application.CreateClient();
            var response = await client.GetAsync("/health");
            Assert.Equal(HttpStatusCode.OK, response.StatusCode);
            var content = await response.Content.ReadAsStringAsync();
            Assert.Contains("healthy", content);
            Assert.Contains("Lightbulb_AI", content);
        }

        [Fact]
        public async Task PostProcess_ReturnsKnowledgeData()
        {
            // Arrange
            await using var application = new WebApplicationFactory<LightbulbProgram>();
            using var client = application.CreateClient();

            var request = new AgentRequest("What is a lightbulb?", "define");

            // Act
            var response = await client.PostAsJsonAsync("/process", request);

            // Assert
            Assert.Equal(HttpStatusCode.OK, response.StatusCode);

            var result = await response.Content.ReadFromJsonAsync<AgentResponse>();
            Assert.NotNull(result);
            Assert.Equal("Lightbulb_AI", result.SourceAgent);
            Assert.True(result.Data.ContainsKey("definition"));
            Assert.Contains("electric light", result.Data["definition"].ToString());
        }
    }
}
using System.Net;
using System.Net.Http.Json;
using Microsoft.AspNetCore.Mvc.Testing;
using Myriad.Common;
using Xunit;
using FactoryProgram = Myriad.Agents.Static.Factory.Program;

namespace Myriad.Tests.Unit
{
    public class FactoryAgentTests
    {
        [Fact]
        public async Task PostProcess_ReturnsFactoryData()
        {
            await using var application = new WebApplicationFactory<FactoryProgram>();
            using var client = application.CreateClient();

            var request = new AgentRequest("Tell me about factories", "explain");

            var response = await client.PostAsJsonAsync("/process", request);

            Assert.Equal(HttpStatusCode.OK, response.StatusCode);

            var result = await response.Content.ReadFromJsonAsync<AgentResponse>();
            Assert.NotNull(result);
            Assert.Equal("Factory_AI", result.SourceAgent);
            Assert.True(result.Data.ContainsKey("context"));
            Assert.Contains("industrial", result.Data["context"].ToString().ToLower());
        }
    }
}
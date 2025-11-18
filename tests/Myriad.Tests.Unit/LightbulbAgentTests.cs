using System.Net;
using Microsoft.AspNetCore.Mvc.Testing;
using Xunit;
using LightbulbProgram = Myriad.Agents.Static.Lightbulb.Program;

namespace Myriad.Tests.Unit
{
    public class LightbulbAgentTests
    {
        [Fact]
        public async Task GetHealth_ReturnsOkAndAgentName()
        {
            // Arrange
            await using var application = new WebApplicationFactory<LightbulbProgram>();
            using var client = application.CreateClient();

            // Act
            var response = await client.GetAsync("/health");

            // Assert
            Assert.Equal(HttpStatusCode.OK, response.StatusCode);

            var content = await response.Content.ReadAsStringAsync();
            Assert.Contains("healthy", content);
            Assert.Contains("Lightbulb_AI", content);
        }
    }
}
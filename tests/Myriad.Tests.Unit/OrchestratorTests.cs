using System.Net;
using Microsoft.AspNetCore.Mvc.Testing;
using Myriad.Services.Orchestrator;
using Xunit;

namespace Myriad.Tests.Unit
{
    public class OrchestratorTests
    {
        [Fact]
        public async Task GetHealth_ReturnsOkAndHealthyStatus()
        {
            // Arrange
            // We use WebApplicationFactory to spin up the service in-memory for testing
            await using var application = new WebApplicationFactory<Program>();
            using var client = application.CreateClient();

            // Act
            var response = await client.GetAsync("/health");

            // Assert
            Assert.Equal(HttpStatusCode.OK, response.StatusCode);

            var content = await response.Content.ReadAsStringAsync();
            Assert.Contains("healthy", content);
            Assert.Contains("Orchestrator", content);
        }
    }
}
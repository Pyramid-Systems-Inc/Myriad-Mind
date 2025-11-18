using Myriad.Services.Orchestrator; // We will create this namespace
using Xunit;

namespace Myriad.Tests.Unit
{
    public class AgentRegistryTests
    {
        [Fact]
        public void RegisterAgent_ShouldStoreAgentUrl()
        {
            // Arrange
            var registry = new AgentRegistry();
            string agentName = "Lightbulb_AI";
            string agentUrl = "http://localhost:5001";

            // Act
            registry.RegisterAgent(agentName, agentUrl);
            var retrievedUrl = registry.GetAgentUrl(agentName);

            // Assert
            Assert.Equal(agentUrl, retrievedUrl);
        }

        [Fact]
        public void GetAgentUrl_ShouldReturnNull_IfAgentNotFound()
        {
            // Arrange
            var registry = new AgentRegistry();

            // Act
            var result = registry.GetAgentUrl("NonExistent_AI");

            // Assert
            Assert.Null(result);
        }
    }
}
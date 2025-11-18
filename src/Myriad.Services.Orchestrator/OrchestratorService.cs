using Microsoft.Extensions.Logging;
using Myriad.Common;
using System.Net.Http.Json;

namespace Myriad.Services.Orchestrator
{
    public class OrchestratorService
    {
        private readonly AgentRegistry _registry;
        private readonly HttpClient _httpClient;
        private readonly ILogger<OrchestratorService> _logger;

        public OrchestratorService(AgentRegistry registry, HttpClient httpClient, ILogger<OrchestratorService> logger)
        {
            _registry = registry;
            _httpClient = httpClient;
            _logger = logger;
        }

        public async Task<bool> PingAgentAsync(string agentName)
        {
            var url = _registry.GetAgentUrl(agentName);

            if (string.IsNullOrEmpty(url))
            {
                _logger.LogWarning("Agent {AgentName} not found in registry.", agentName);
                return false;
            }

            try
            {
                _logger.LogInformation("Pinging Agent {AgentName} at {Url}", agentName, url);

                // Call the /health endpoint of the agent
                var response = await _httpClient.GetAsync($"{url}/health");

                return response.IsSuccessStatusCode;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Failed to ping Agent {AgentName}", agentName);
                return false;
            }
        }

        public async Task<AgentResponse?> QueryAgentAsync(string agentName, AgentRequest request)
        {
            var url = _registry.GetAgentUrl(agentName);
            if (string.IsNullOrEmpty(url)) return null;

            try
            {
                var response = await _httpClient.PostAsJsonAsync($"{url}/process", request);

                if (response.IsSuccessStatusCode)
                {
                    return await response.Content.ReadFromJsonAsync<AgentResponse>();
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Failed to query Agent {AgentName}", agentName);
            }
            return null;
        }
    }
}
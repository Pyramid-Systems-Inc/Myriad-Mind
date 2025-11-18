using System.Collections.Concurrent;

namespace Myriad.Services.Orchestrator
{
    public class AgentRegistry
    {
        // Thread-safe dictionary to store agent URLs
        private readonly ConcurrentDictionary<string, string> _registry = new();

        public void RegisterAgent(string name, string url)
        {
            _registry[name] = url;
        }

        public string? GetAgentUrl(string name)
        {
            _registry.TryGetValue(name, out var url);
            return url;
        }

        public IEnumerable<string> GetAllAgentNames()
        {
            return _registry.Keys;
        }
    }
}
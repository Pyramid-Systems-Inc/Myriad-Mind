namespace Myriad.Common
{
    // The standard envelope for an agent's answer
    public record AgentResponse(
        string SourceAgent,
        Dictionary<string, object> Data
    );
}
namespace Myriad.Common
{
    // The standard envelope for asking an agent a question
    public record AgentRequest(
        string Query, 
        string Intent
    );
}
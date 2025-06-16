# Myriad Mind Data Communication Protocols

This document defines the standardized JSON protocols for communication between components in the Myriad Cognitive Architecture.

## Processor-to-Orchestrator Protocol (The "Task List")

**Purpose**: Sent from Input Processor to Orchestrator
**Format**:
```json
{
  "query_id": "xyz-123",
  "tasks": [
    { "task_id": 1, "intent": "define", "concept": "lightbulb", "args": {} },
    { "task_id": 2, "intent": "explain_limitation", "concept": "lightbulb", "args": {} }
  ]
}
```

**Fields**:
- `query_id`: Unique identifier for the query session
- `tasks`: Array of task objects to be distributed to agents
  - `task_id`: Sequential integer identifier for the task
  - `intent`: The action to be performed (e.g., "define", "explain_limitation")
  - `concept`: The subject matter (e.g., "lightbulb")
  - `args`: Additional parameters (currently empty object for MVP)

## Orchestrator-to-Agent Protocol (The "Agent Job")

**Purpose**: Sent from Orchestrator to an Agent
**Format**:
```json
{
  "task_id": 1,
  "intent": "define",
  "concept": "lightbulb",
  "args": { "detail_level": "high" }
}
```

**Fields**:
- `task_id`: The `task_id` from the original "Task List"
- `intent`: The specific action the agent should perform (e.g., "define", "explain_limitation")
- `concept`: The subject matter (e.g., "lightbulb")
- `args`: Additional parameters for the agent to perform the task (e.g., `{"detail_level": "high"}`)

## Agent-to-Orchestrator Protocol (The "Agent Result")

**Purpose**: Sent from Agent back to Orchestrator
**Format**:
```json
{
  "agent_name": "Lightbulb_Definition_AI",
  "status": "success",
  "data": "an electric device that produces light via an incandescent filament"
}
```

**Fields**:
- `agent_name`: The name of the responding agent
- `status`: Result status ("success" or "error")
- `data`: The agent's response data or error message

## Orchestrator-to-OutputProcessor Protocol (The "Collected Results")

**Purpose**: Sent from Orchestrator to Output Processor (Synthesizer)
**Format**:
```json
{
  "query_id": "xyz-123",
  "collected_results": {
    "1": { "agent_name": "Lightbulb_Definition_AI", "status": "success", "data": "an electric device..." },
    "2": { "agent_name": "Lightbulb_Function_AI", "status": "success", "data": "illuminates by converting..." }
  }
}
```

**Fields**:
- `query_id`: Unique identifier for the query session, same as in the "Task List"
- `collected_results`: An object where keys are `task_id` (as strings) and values are "Agent Result" objects.

## System Management Protocols

### Orchestrator-to-LifecycleManager Protocol (Agent Creation Request)

**Purpose**: Orchestrator requests `LifecycleManager` to create a new agent instance.
**Format**:
```json
{
  "concept_name": "new_concept",
  "agent_type": "FactBase"
}
```
**Fields**:
- `concept_name`: The primary concept the new agent will handle.
- `agent_type`: The type or template of agent to create (e.g., "FactBase", "Calculator").

### LifecycleManager-to-Orchestrator Protocol (Agent Creation Confirmation)

**Purpose**: `LifecycleManager` confirms agent creation and provides details.
**Format**:
```json
{
  "agent_name": "NewConcept_AI",
  "status": "success",
  "endpoint": "http://new_concept_ai:5001/query"
}
```
**Fields**:
- `agent_name`: The assigned name of the newly created agent.
- `status`: Result status ("success" or "error").
- `endpoint`: The network endpoint where the new agent can be reached.

### Orchestrator-to-AgentRegistry Protocol (Register Agent)

**Purpose**: Orchestrator requests `AgentRegistry` to register a new or updated agent's capabilities and endpoint.
**Format**:
```json
{
  "agent_name": "NewConcept_AI",
  "concept": "new_concept",
  "intent_map": {
    "define": "/query",
    "explain_details": "/explain"
  },
  "endpoint": "http://new_concept_ai:5001"
}
```
**Fields**:
- `agent_name`: The name of the agent to register.
- `concept`: The primary concept the agent handles.
- `intent_map`: An object mapping intents the agent can handle to specific paths on its endpoint.
- `endpoint`: The base network endpoint of the agent.

## Protocol Notes

- All communication uses JSON format
- HTTP POST is the standard transport method
- Agents perform their cognitive reasoning internally before returning results
- The orchestrator is intentionally "dumb" - it only routes tasks and collects results
- Each agent specializes in specific intents and concepts
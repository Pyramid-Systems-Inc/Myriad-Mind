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
{ "intent": "define" }
```
or
```json
{ "intent": "explain_limitation" }
```

**Fields**:
- `intent`: The specific action the agent should perform

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

## Protocol Notes

- All communication uses JSON format
- HTTP POST is the standard transport method
- Agents perform their cognitive reasoning internally before returning results
- The orchestrator is intentionally "dumb" - it only routes tasks and collects results
- Each agent specializes in specific intents and concepts
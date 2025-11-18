# Myriad Agent Communication Protocol

## Overview

All communication between the Orchestrator and Agents occurs via HTTP/JSON.

## Data Models

### AgentRequest

Sent by the Orchestrator to an Agent.

```json
{
  "query": "Why was the lightbulb important?",
  "intent": "explain"
}
```

### AgentResponse

Returned by an Agent to the Orchestrator.

```json
{
  "sourceAgent": "Lightbulb_AI",
  "data": {
    "fact_1": "The lightbulb extended working hours.",
    "invention_date": "1879"
  }
}
```

## Endpoints

### GET /health

Returns 200 OK if the agent is alive.

### POST /process

Accepts `AgentRequest`, returns `AgentResponse`.

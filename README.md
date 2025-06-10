# Myriad Mind - Aligned MVP 2.0

## Core Hypothesis
Intelligence can emerge from the orchestration of minimalist, specialized agents, where each agent contributes a piece of reasoned knowledge, rather than being a dumb data store.

## MVP Target Query
"Define a lightbulb and explain its limitation."

## Architecture Overview

This project implements the Myriad Cognitive Architecture with the following key principles:

- **Specialized Agents**: Each agent handles specific intents and performs cognitive reasoning internally
- **Dumb Orchestrator**: The orchestrator only routes tasks and collects results without reasoning
- **Clear Data Protocols**: Standardized JSON communication between all components
- **Microservice Architecture**: Each agent runs as an independent containerized service

## Project Structure

```
/project_myriad
|-- /agents
|   |-- /lightbulb_definition_ai     # Handles "define" intent
|   |-- /lightbulb_function_ai       # Handles "explain_limitation" intent
|-- /orchestration                   # Task routing and result collection
|-- /processing
|   |-- /input_processor            # Query parsing and task list generation
|   |-- /output_processor           # Result synthesis
|-- /tests                          # Unit tests
|-- docker-compose.yml              # Service orchestration
|-- PROTOCOLS.md                    # Data communication protocols
|-- README.md                       # This file
|-- requirements.txt                # Python dependencies
```

## Data Flow

1. **Input Processing**: Raw query → Task List (JSON)
2. **Orchestration**: Task List → Individual Agent Jobs
3. **Agent Processing**: Agent Jobs → Reasoned Results
4. **Output Processing**: Collected Results → Final Response

## Communication Protocols

All inter-component communication uses standardized JSON protocols defined in [`PROTOCOLS.md`](PROTOCOLS.md:1):

- **Processor-to-Orchestrator**: Task List format
- **Orchestrator-to-Agent**: Agent Job format  
- **Agent-to-Orchestrator**: Agent Result format

## Current Status: Phase 1 Complete

✅ Project initialization and directory structure
✅ Core data protocols defined
✅ Docker Compose configuration
✅ Clean foundation for cognitive agents

## Next Steps (Phase 2)

- Implement `lightbulb_definition_ai` Flask service
- Implement `lightbulb_function_ai` Flask service with cognitive reasoning
- Create Docker containers for each agent
- Network testing between services

## Development Setup

### Prerequisites
- Python 3.8+
- Docker & Docker Compose
- Git

### Installation
1. Clone the repository
2. Create virtual environment: `python -m venv venv`
3. Activate environment: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`

### Running the System
```bash
# Start all services
docker-compose up --build

# The agents will be available at:
# - lightbulb_definition_ai: http://localhost:5001
# - lightbulb_function_ai: http://localhost:5002
```

## Key Design Principles

1. **Cognitive Processing in Agents**: The "thinking" happens within specialized agents, not in central processors
2. **Minimal Orchestration**: The orchestrator is intentionally simple - just routing and collection
3. **Clear Separation of Concerns**: Each component has a single, well-defined responsibility
4. **Testable Architecture**: Every component can be unit tested independently
5. **Scalable Design**: New agents can be easily added to handle additional intents

## Testing

Run tests with:
```bash
pytest tests/
```

## Architecture Validation

The system logs will demonstrate:
- Task distribution from orchestrator to appropriate agents
- Cognitive reasoning happening within agents (not in processors)
- Proper data flow through all components
- Emergence of intelligence from agent orchestration
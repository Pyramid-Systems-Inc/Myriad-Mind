# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.2] - 2025-11-18

### Added

- **Core Protocol**: Created `Myriad.Common` library with `AgentRequest` and `AgentResponse` records.
- **Orchestrator**: Implemented `QueryAgentAsync` to perform HTTP POST requests to agents.
- **Agents**:
  - Implemented intelligence in `Lightbulb_AI` (hardcoded knowledge base).
  - Created `Factory_AI` microservice with pre-electrical industrial knowledge.
- **Testing**: Added unit tests for Protocol serialization and multi-agent integration.
- **Documentation**: Created `PROTOCOL.md` defining the JSON interface.

## [0.0.1] - 2025-11-18

### Added

- `Lightbulb_AI` microservice skeleton (Port 5001)
- `AgentRegistry` implementation with unit tests
- Orchestrator `/health` endpoint (verified via TDD)
- Initial solution structure (`Myriad.sln`)

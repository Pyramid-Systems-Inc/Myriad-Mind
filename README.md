# Myriad Cognitive Architecture - Phase 1

## Overview

The Myriad Cognitive Architecture is a distributed AI system where specialized microservice agents collaborate to answer queries. This implementation represents **Phase 1: Foundation & Core Component Setup** of the MVP development roadmap.

## Architecture

The system consists of:

- **Central Orchestrator**: Routes queries to appropriate agents and manages the AI registry
- **Specialized Agents**: Microservices that handle specific domains of knowledge
- **Agent Registry**: Maps keywords to agent addresses for query routing

## Phase 1 Components

### 1. Project Structure
```
Myriad-Mind/
├── orchestrator/
│   └── orchestrator.py          # Central orchestration logic
├── agents/
│   └── Lightbulb_AI/           # First specialized agent
│       ├── agent_app.py        # Flask application
│       ├── Dockerfile          # Container definition
│       ├── requirements.txt    # Python dependencies
│       ├── run.sh             # Linux/macOS run script
│       └── run.bat            # Windows run script
├── common/                     # Shared utilities (future use)
├── tests/                      # Test files (future use)
├── main.py                     # Main entry point
├── requirements.txt            # Root dependencies
└── README.md                   # This file
```

### 2. Central Orchestrator
- **File**: [`orchestrator/orchestrator.py`](orchestrator/orchestrator.py)
- **Features**:
  - AI_REGISTRY with hardcoded agent addresses
  - Core orchestration logic for keyword-based routing
  - Comprehensive logging of orchestrator state
  - Agent health checking capabilities

### 3. Lightbulb_AI Agent
- **Directory**: [`agents/Lightbulb_AI/`](agents/Lightbulb_AI/)
- **Features**:
  - Flask web service with `/query` endpoint
  - Dockerized for independent deployment
  - Currently returns hardcoded success message
  - Health check and info endpoints

## Prerequisites

- **Python 3.11+**
- **Docker** (for running agents)
- **Git** (for version control)

## Quick Start

### 1. Clone and Setup
```bash
git clone <repository-url>
cd Myriad-Mind

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Start the Lightbulb_AI Agent

**On Windows:**
```bash
cd agents/Lightbulb_AI
run.bat
```

**On Linux/macOS:**
```bash
cd agents/Lightbulb_AI
chmod +x run.sh
./run.sh
```

This will:
- Build the Docker image for Lightbulb_AI
- Start the container on port 5001
- Display available endpoints

### 3. Test the System

**Check agent status:**
```bash
python main.py --status
```

**Run a test query:**
```bash
python main.py --test
```

**Process a custom query:**
```bash
python main.py --query "Why was the lightbulb important for factories?"
```

## Usage Examples

### Basic Commands

```bash
# Check system status
python main.py --status

# Run test orchestration
python main.py --test

# Process a query
python main.py --query "lightbulb and factories"

# Enable verbose logging
python main.py --query "test query" --verbose

# Show help
python main.py --help
```

### Agent Endpoints

Once the Lightbulb_AI agent is running, you can access:

- **Health Check**: http://localhost:5001/health
- **Query Endpoint**: http://localhost:5001/query
- **Agent Info**: http://localhost:5001/info
- **Root Status**: http://localhost:5001/

### Example Query Flow

1. **Input**: `"Why was the lightbulb important for factories?"`
2. **Keyword Extraction**: `["lightbulb", "important", "factories"]`
3. **Agent Selection**: Routes to `Lightbulb_AI` based on "lightbulb" keyword
4. **Agent Query**: Sends request to `http://localhost:5001/query`
5. **Response**: Agent returns status information (Phase 1 implementation)

## Development

### Adding New Agents

To add a new agent (e.g., Factory_AI):

1. Create directory: `agents/Factory_AI/`
2. Copy and modify agent template from `agents/Lightbulb_AI/`
3. Update port number in Dockerfile and run scripts
4. Add agent to `AI_REGISTRY` in [`orchestrator.py`](orchestrator/orchestrator.py)

### Testing

```bash
# Test orchestrator directly
cd orchestrator
python orchestrator.py

# Test agent directly
cd agents/Lightbulb_AI
python agent_app.py
```

### Logs

- **Orchestrator logs**: `orchestrator.log`
- **Agent logs**: `docker logs lightbulb_ai`

## Phase 1 Success Criteria

✅ **Completed Features:**

1. **Project Structure**: Organized directories for orchestrator, agents, common, and tests
2. **Central Orchestrator**: 
   - AI_REGISTRY with hardcoded agent addresses
   - Core orchestration logic with keyword routing
   - Comprehensive logging system
3. **Lightbulb_AI Agent**:
   - Flask app with `/query` endpoint
   - Dockerized microservice
   - Returns hardcoded success message
   - Runs on port 5001
4. **Entry Point**: `main.py` with command-line interface
5. **Infrastructure**: Requirements, Docker setup, run scripts

## Next Steps (Future Phases)

- **Phase 2**: Implement actual agent intelligence and communication protocols
- **Phase 3**: Add input parsing and output synthesis
- **Phase 4+**: Advanced features, scaling, and new agent types

## Troubleshooting

### Common Issues

1. **Docker not found**: Ensure Docker is installed and running
2. **Port already in use**: Stop existing containers with `docker stop lightbulb_ai`
3. **Connection refused**: Verify agent container is running with `docker ps`
4. **Module not found**: Ensure virtual environment is activated and dependencies installed

### Debug Commands

```bash
# Check running containers
docker ps

# View agent logs
docker logs lightbulb_ai

# Check agent health
curl http://localhost:5001/health

# Stop agent
docker stop lightbulb_ai
```

## License

[License information to be added]

## Contributing

[Contribution guidelines to be added]
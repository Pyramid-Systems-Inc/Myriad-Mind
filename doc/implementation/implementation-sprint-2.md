# Implementation Plan - Sprint 2: Schema Enforcement & Monitoring

**Sprint 2 of 7** | [← Previous Sprint](implementation-sprint-1.md) | [Next Sprint →](implementation-sprint-3.md)

This document covers Sprint 2 of the Myriad-Mind implementation plan, focusing on graph schema enforcement, production monitoring, and health checks (Weeks 3-6).

[← Back to Implementation Overview](../INDEX.md#implementation) | [View All Sprints](../INDEX.md#implementation)

---

## SPRINT 1-2 Continuation: Critical Foundation (Weeks 3-6)

**Sprint Goal:** Complete production-ready infrastructure with schema enforcement, comprehensive monitoring, and health checks.

**Target Outcome:** Database integrity guaranteed through constraints, full observability via monitoring stack, and reliable health status across all services.

---

### Phase 1.3: Graph Schema Enforcement (Week 3)

#### Current Problem

From [`doc/GRAPH_SCHEMA.md`](../GRAPH_SCHEMA.md:1):

- Schema documented but constraints not enforced in database
- No uniqueness constraints on Agent.name, Concept.name
- No indexes for performance
- Can create duplicate/invalid data

#### Implementation Steps

**1.3.1 Create Schema Initialization Script (Day 1-2)**

Create new file: `scripts/init_schema.cypher`

```cypher
// Schema Initialization for Myriad Cognitive Architecture
// Version: 1.0.0
// Date: 2025-01-16

// ========================================
// CONSTRAINTS
// ========================================

// Agent constraints
CREATE CONSTRAINT agent_name_unique IF NOT EXISTS
FOR (a:Agent) REQUIRE a.name IS UNIQUE;

CREATE CONSTRAINT agent_name_exists IF NOT EXISTS
FOR (a:Agent) REQUIRE a.name IS NOT NULL;

CREATE CONSTRAINT agent_endpoint_exists IF NOT EXISTS
FOR (a:Agent) REQUIRE a.endpoint IS NOT NULL;

// Concept constraints
CREATE CONSTRAINT concept_name_unique IF NOT EXISTS
FOR (c:Concept) REQUIRE c.name IS UNIQUE;

CREATE CONSTRAINT concept_name_exists IF NOT EXISTS
FOR (c:Concept) REQUIRE c.name IS NOT NULL;

// Region constraints
CREATE CONSTRAINT region_name_unique IF NOT EXISTS
FOR (r:Region) REQUIRE r.name IS UNIQUE;

// ========================================
// INDEXES
// ========================================

// Agent indexes
CREATE INDEX agent_type_idx IF NOT EXISTS
FOR (a:Agent) ON (a.type);

CREATE INDEX agent_status_idx IF NOT EXISTS
FOR (a:Agent) ON (a.status);

CREATE INDEX agent_created_idx IF NOT EXISTS
FOR (a:Agent) ON (a.created_at);

// Concept indexes
CREATE INDEX concept_category_idx IF NOT EXISTS
FOR (c:Concept) ON (c.category);

CREATE INDEX concept_created_idx IF NOT EXISTS
FOR (c:Concept) ON (c.created_at);

// Full-text search indexes
CREATE FULLTEXT INDEX concept_search_idx IF NOT EXISTS
FOR (c:Concept) ON EACH [c.name, c.primary_definition];

// Relationship indexes (for Hebbian learning)
CREATE INDEX handles_concept_weight_idx IF NOT EXISTS
FOR ()-[r:HANDLES_CONCEPT]-() ON (r.weight);

CREATE INDEX handles_concept_success_idx IF NOT EXISTS
FOR ()-[r:HANDLES_CONCEPT]-() ON (r.success_rate);

CREATE INDEX handles_concept_last_used_idx IF NOT EXISTS
FOR ()-[r:HANDLES_CONCEPT]-() ON (r.last_used);

// ========================================
// SCHEMA VERSION TRACKING
// ========================================

MERGE (v:SchemaVersion {version: "1.0.0"})
SET v.created_at = timestamp(),
    v.description = "Initial schema with Hebbian learning and production constraints",
    v.last_updated = timestamp();
```

**1.3.2 Create Python Schema Initializer (Day 2-3)**

Create new file: `scripts/initialize_graph_schema.py`

```python
#!/usr/bin/env python3
"""
Initialize Neo4j graph schema with constraints and indexes.
Run this before first use or after schema updates.
"""

import os
import sys
from pathlib import Path
from neo4j import GraphDatabase

NEO4J_URI = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.environ.get("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.environ.get("NEO4J_PASSWORD", "password")

def read_cypher_file(filepath):
    """Read Cypher commands from file"""
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Split by semicolon and filter empty statements
    statements = [s.strip() for s in content.split(';') if s.strip() and not s.strip().startswith('//')]
    return statements

def initialize_schema(driver, cypher_file):
    """Execute schema initialization statements"""
    statements = read_cypher_file(cypher_file)
    
    with driver.session() as session:
        for i, statement in enumerate(statements, 1):
            try:
                print(f"[{i}/{len(statements)}] Executing: {statement[:60]}...")
                session.run(statement)
                print(f"  ✅ Success")
            except Exception as e:
                print(f"  ⚠️  Warning: {e}")
                # Continue on errors (constraints may already exist)
    
    print(f"\n✅ Schema initialization complete!")

def verify_schema(driver):
    """Verify schema was created successfully"""
    with driver.session() as session:
        # Check constraints
        result = session.run("SHOW CONSTRAINTS")
        constraints = [record for record in result]
        print(f"\n📊 Constraints created: {len(constraints)}")
        
        # Check indexes
        result = session.run("SHOW INDEXES")
        indexes = [record for record in result]
        print(f"📊 Indexes created: {len(indexes)}")
        
        # Check schema version
        result = session.run("MATCH (v:SchemaVersion) RETURN v.version as version, v.description as description")
        record = result.single()
        if record:
            print(f"📊 Schema version: {record['version']}")
            print(f"   {record['description']}")

if __name__ == "__main__":
    print("🔧 Initializing Neo4j Graph Schema for Myriad Cognitive Architecture\n")
    
    # Find schema file
    script_dir = Path(__file__).parent
    schema_file = script_dir / "init_schema.cypher"
    
    if not schema_file.exists():
        print(f"❌ Schema file not found: {schema_file}")
        sys.exit(1)
    
    # Connect to Neo4j
    try:
        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
        driver.verify_connectivity()
        print(f"✅ Connected to Neo4j at {NEO4J_URI}\n")
    except Exception as e:
        print(f"❌ Failed to connect to Neo4j: {e}")
        sys.exit(1)
    
    # Initialize schema
    try:
        initialize_schema(driver, schema_file)
        verify_schema(driver)
    finally:
        driver.close()
```

**1.3.3 Add Validation to GraphDB Manager (Day 3-4)**

File: [`src/myriad/services/graphdb_manager/validation.py`](../../src/myriad/services/graphdb_manager/validation.py:1)

Already exists! Verify it includes these validations:

- Agent: name, type, endpoint required
- Concept: name required, lowercase enforced
- Hebbian: weights in [0.0, 1.0], counts non-negative

If missing, add to validation.py:

```python
def validate_agent_properties(properties: dict) -> tuple[bool, str]:
    """Validate agent properties before creation"""
    required = ['name', 'type', 'endpoint']
    for field in required:
        if field not in properties or not properties[field]:
            return False, f"Missing required field: {field}"
    
    # Validate type
    if properties['type'] not in ['static', 'dynamic']:
        return False, "Agent type must be 'static' or 'dynamic'"
    
    # Validate endpoint URL
    endpoint = properties['endpoint']
    if not (endpoint.startswith('http://') or endpoint.startswith('https://')):
        return False, "Endpoint must be valid HTTP/HTTPS URL"
    
    # Validate status if provided
    if 'status' in properties:
        valid_statuses = ['active', 'inactive', 'unhealthy']
        if properties['status'] not in valid_statuses:
            return False, f"Status must be one of: {valid_statuses}"
    
    return True, "OK"
```

**1.3.4 Update Docker Startup Script (Day 4-5)**

Create new file: `scripts/startup.sh`

```bash
#!/bin/bash
# Startup script for Myriad services
# Initializes schema before starting services

echo "🚀 Starting Myriad Cognitive Architecture"

# Wait for Neo4j to be ready
echo "⏳ Waiting for Neo4j..."
until nc -z neo4j 7687; do
  sleep 1
done
echo "✅ Neo4j is ready"

# Initialize schema
echo "🔧 Initializing graph schema..."
python3 /app/scripts/initialize_graph_schema.py

# Start services
echo "✅ Schema initialized, starting services..."
```

Update [`docker-compose.yml`](../../docker-compose.yml:1) to run schema init:

```yaml
graphdb_manager_ai:
  # ... existing config ...
  volumes:
    - ./scripts:/app/scripts:ro
  entrypoint: ["/bin/bash", "-c"]
  command: ["python3 /app/scripts/initialize_graph_schema.py && python app.py"]
```

**Success Criteria:**

- ✅ Constraints prevent duplicate agent/concept names
- ✅ Indexes improve query performance (<100ms for agent discovery)
- ✅ Validation rejects invalid data
- ✅ Schema version tracked in graph

---

### Phase 1.4: Production Monitoring Stack (Week 4-5)

#### Current Problem

- No metrics collection or visualization
- Cannot diagnose production issues
- No alerting for failures
- Missing observability

#### Implementation Steps

**1.4.1 Add Prometheus (Day 1-2)**

Create `monitoring/prometheus.yml`:

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'orchestrator'
    static_configs:
      - targets: ['orchestrator:5010']
    metrics_path: '/metrics'
  
  - job_name: 'graphdb_manager'
    static_configs:
      - targets: ['graphdb_manager_ai:5008']
    metrics_path: '/metrics'
  
  - job_name: 'input_processor'
    static_configs:
      - targets: ['input_processor:5003']
    metrics_path: '/health'
  
  - job_name: 'output_processor'
    static_configs:
      - targets: ['output_processor:5004']
    metrics_path: '/health'
  
  - job_name: 'neo4j'
    static_configs:
      - targets: ['neo4j:2004']
  
  - job_name: 'redis'
    static_configs:
      - targets: ['redis:6379']
```

Add to [`docker-compose.yml`](../../docker-compose.yml:1):

```yaml
prometheus:
  image: prom/prometheus:latest
  container_name: prometheus
  ports:
    - "9090:9090"
  volumes:
    - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml:ro
    - prometheus_data:/prometheus
  networks:
    - myriad_network
  command:
    - '--config.file=/etc/prometheus/prometheus.yml'
    - '--storage.tsdb.path=/prometheus'
  restart: unless-stopped
```

**1.4.2 Add Grafana (Day 2-3)**

Create `monitoring/grafana/datasources/prometheus.yml`:

```yaml
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
    editable: true
```

Create `monitoring/grafana/dashboards/dashboard.yml`:

```yaml
apiVersion: 1

providers:
  - name: 'Myriad'
    orgId: 1
    folder: ''
    type: file
    disableDeletion: false
    updateIntervalSeconds: 10
    allowUiUpdates: true
    options:
      path: /etc/grafana/provisioning/dashboards
```

Add to [`docker-compose.yml`](../../docker-compose.yml:1):

```yaml
grafana:
  image: grafana/grafana:latest
  container_name: grafana
  ports:
    - "3000:3000"
  volumes:
    - ./monitoring/grafana/datasources:/etc/grafana/provisioning/datasources:ro
    - ./monitoring/grafana/dashboards:/etc/grafana/provisioning/dashboards:ro
    - grafana_data:/var/lib/grafana
  networks:
    - myriad_network
  environment:
    - GF_SECURITY_ADMIN_USER=admin
    - GF_SECURITY_ADMIN_PASSWORD=myriad
    - GF_USERS_ALLOW_SIGN_UP=false
  depends_on:
    - prometheus
  restart: unless-stopped

volumes:
  prometheus_data:
  grafana_data:
```

**1.4.3 Add Metrics to Services (Day 3-5)**

Add Prometheus client to each service. Example for orchestrator:

File: [`src/myriad/services/orchestrator/app.py`](../../src/myriad/services/orchestrator/app.py:1)

```python
from prometheus_client import Counter, Histogram, Gauge, generate_latest
import time

# Metrics
query_counter = Counter('myriad_queries_total', 'Total queries processed')
neurogenesis_counter = Counter('myriad_neurogenesis_total', 'Total neurogenesis events')
agent_discovery_time = Histogram('myriad_agent_discovery_seconds', 'Agent discovery time')
active_agents_gauge = Gauge('myriad_active_agents', 'Number of active agents')
hebbian_updates = Counter('myriad_hebbian_updates_total', 'Hebbian learning updates', ['outcome'])

@app.route('/metrics')
def metrics():
    """Prometheus metrics endpoint"""
    return generate_latest(), 200, {'Content-Type': 'text/plain; charset=utf-8'}

# In process function:
@app.route('/process', methods=['POST'])
def process():
    query_counter.inc()
    start_time = time.time()
    
    # ... processing logic ...
    
    agent_discovery_time.observe(time.time() - start_time)
    active_agents_gauge.set(len(enhanced_intelligence.agent_profiles))
```

**Success Criteria:**

- ✅ Prometheus collecting metrics from all services
- ✅ Grafana dashboards showing system health
- ✅ Real-time monitoring of agent count, response times, success rates

---

### Phase 1.5: Health Checks & Resource Limits (Week 6)

#### Implementation Steps

**1.5.1 Add Health Endpoints to All Services (Day 1-2)**

Standardize health check format across all services:

```python
@app.route('/health', methods=['GET'])
def health_check():
    """Standard health check endpoint"""
    health_status = {
        "status": "healthy",
        "service": "ServiceName",
        "version": "4.2.0",
        "timestamp": time.time()
    }
    
    # Check dependencies
    dependencies = {}
    
    # Check database connection (if applicable)
    try:
        # Test connection
        dependencies["database"] = "healthy"
    except:
        dependencies["database"] = "unhealthy"
        health_status["status"] = "degraded"
    
    health_status["dependencies"] = dependencies
    
    status_code = 200 if health_status["status"] == "healthy" else 503
    return jsonify(health_status), status_code
```

**1.5.2 Add Resource Limits to All Services (Day 2-3)**

Update [`docker-compose.yml`](../../docker-compose.yml:1) with resource limits:

```yaml
services:
  graphdb_manager_ai:
    # ... existing config ...
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          memory: 256M
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5008/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
  
  input_processor:
    # ... existing config ...
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 256M
        reservations:
          memory: 128M
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5003/health"]
      interval: 30s
      timeout: 10s
      retries: 3
  
  # Repeat for all services...
```

**Success Criteria:**

- ✅ All services have health endpoints
- ✅ All services have resource limits
- ✅ Docker Compose health checks passing
- ✅ Monitoring shows resource usage within limits

---

## Sprint 1-2 Summary

### Completed Deliverables

**Week 1-2: Foundation Infrastructure**

- ✅ Orchestrator extracted as independent microservice
- ✅ Resource limits on agent creation (max 20 concurrent)
- ✅ Lifecycle management with idle timeout and max age
- ✅ Agent usage tracking and queue management

**Week 3: Schema Enforcement**

- ✅ Neo4j constraints for data integrity
- ✅ Indexes for query performance
- ✅ Schema validation in GraphDB Manager
- ✅ Automated schema initialization

**Week 4-5: Monitoring Stack**

- ✅ Prometheus metrics collection
- ✅ Grafana dashboards and visualization
- ✅ Service-level metrics instrumentation
- ✅ Real-time observability

**Week 6: Health & Resources**

- ✅ Standardized health endpoints
- ✅ Docker resource limits on all services
- ✅ Health check automation
- ✅ Resource usage monitoring

### Key Achievements

1. **Production-Ready Infrastructure**: System can now operate safely in production with proper resource management
2. **Data Integrity**: Database constraints prevent invalid/duplicate data
3. **Observability**: Complete visibility into system health and performance
4. **Scalability**: Resource limits prevent exhaustion while supporting growth

### Next Steps

Sprint 3 will build on this foundation to implement async communication and performance optimizations, enabling 3-5x performance improvement through parallel task processing.

---

## Continue Reading

**Next:** [Sprint 3: Performance & Async Communication](implementation-sprint-3.md) - Async orchestrator, circuit breakers, and parallel processing

**Related Documentation:**

- [Project Index](../INDEX.md)
- [Architecture Overview](../architecture/)
- [Protocols](../protocols/)
- [Monitoring Guide](../MONITORING_GUIDE.md)

[← Previous Sprint](implementation-sprint-1.md) | [↑ Back to Index](../INDEX.md) | [Next Sprint →](implementation-sprint-3.md)

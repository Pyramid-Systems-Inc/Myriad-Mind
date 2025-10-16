# Neo4j Graph Schema - Myriad Cognitive Architecture

## Overview

The Myriad knowledge graph uses Neo4j to represent agents, concepts, and their relationships with Hebbian learning weights. This schema enables dynamic neurogenesis, agent specialization, and adaptive learning through connection strength adjustments.

## Node Types

### Agent Node

Represents both static and dynamic AI agents in the system.

**Label:** `Agent`

**Properties:**

- `name` (String, UNIQUE, REQUIRED) - Agent identifier (e.g., "lightbulb_definition", "dynamic_chemistry_agent")
- `type` (String, REQUIRED) - Agent type: "static" or "dynamic"
- `endpoint` (String, REQUIRED) - HTTP endpoint URL (e.g., "<http://lightbulb-definition:5001>")
- `port` (Integer) - Service port number
- `container_name` (String) - Docker container name (for dynamic agents)
- `template` (String) - Agent template used (for dynamic agents)
- `created_at` (Timestamp) - Agent creation timestamp
- `status` (String) - Agent status: "active", "inactive", "unhealthy"
- `description` (String, OPTIONAL) - Human-readable description

**Indexes:**

- Unique constraint on `name`
- Index on `type` for filtering
- Index on `status` for health monitoring
- Index on `created_at` for temporal queries

**Example:**

```cypher
CREATE (a:Agent {
  name: "lightbulb_definition",
  type: "static",
  endpoint: "http://lightbulb-definition:5001",
  port: 5001,
  status: "active",
  created_at: timestamp()
})
```

### Concept Node

Represents knowledge concepts that agents can handle.

**Label:** `Concept`

**Properties:**

- `name` (String, UNIQUE, REQUIRED) - Concept identifier (lowercase, e.g., "lightbulb", "photosynthesis")
- `primary_definition` (String) - Primary definition text
- `category` (String) - Concept category (e.g., "technology", "biology", "physics")
- `complexity` (Float, 0.0-1.0) - Complexity score
- `created_at` (Timestamp) - Concept creation timestamp
- `last_updated` (Timestamp) - Last modification timestamp

**Indexes:**

- Unique constraint on `name`
- Full-text index on `name` and `primary_definition` for search
- Index on `category` for filtering
- Index on `created_at` for temporal queries

**Example:**

```cypher
CREATE (c:Concept {
  name: "lightbulb",
  primary_definition: "An electric light with a filament or LED that emits light when heated",
  category: "technology",
  complexity: 0.3,
  created_at: timestamp()
})
```

### Region Node

Represents knowledge domains or specialized areas.

**Label:** `Region`

**Properties:**

- `name` (String, UNIQUE, REQUIRED) - Region identifier (e.g., "Physics", "Biology", "General")
- `description` (String) - Region description
- `created_at` (Timestamp) - Region creation timestamp

**Indexes:**

- Unique constraint on `name`

**Example:**

```cypher
CREATE (r:Region {
  name: "Physics",
  description: "Physical sciences and phenomena",
  created_at: timestamp()
})
```

## Relationship Types

### HANDLES_CONCEPT

Connects agents to concepts they can process, with Hebbian learning properties.

**Relationship:** `(Agent)-[HANDLES_CONCEPT]->(Concept)`

**Properties (Hebbian Learning):**

- `weight` (Float, 0.0-1.0, DEFAULT: 0.5) - Connection strength
- `usage_count` (Integer, DEFAULT: 0) - Total number of uses
- `success_count` (Integer, DEFAULT: 0) - Successful uses
- `failure_count` (Integer, DEFAULT: 0) - Failed uses
- `success_rate` (Float, 0.0-1.0) - Calculated: success_count / usage_count
- `decay_rate` (Float, DEFAULT: 0.01) - Learning decay rate
- `last_updated` (Timestamp) - Last Hebbian update timestamp
- `last_used` (Timestamp) - Last time relationship was used

**Hebbian Update Rules:**

- **Strengthening (Success):** `weight = min(1.0, weight + 0.05)`
- **Weakening (Failure):** `weight = max(0.0, weight - 0.02)`
- **Decay:** `weight = weight * (1.0 - decay_rate)` every 15 minutes

**Indexes:**

- Index on `weight` for priority queries
- Index on `success_rate` for performance analysis
- Index on `last_used` for temporal analysis

**Example:**

```cypher
CREATE (a:Agent {name: "lightbulb_definition"})-[r:HANDLES_CONCEPT {
  weight: 0.85,
  usage_count: 42,
  success_count: 40,
  failure_count: 2,
  success_rate: 0.952,
  decay_rate: 0.01,
  last_updated: timestamp(),
  last_used: timestamp()
}]->(c:Concept {name: "lightbulb"})
```

### BELONGS_TO

Connects agents or concepts to their knowledge regions.

**Relationships:**

- `(Agent)-[BELONGS_TO]->(Region)`
- `(Concept)-[BELONGS_TO]->(Region)`

**Properties:**

- `assigned_at` (Timestamp) - When relationship was created

**Example:**

```cypher
CREATE (a:Agent {name: "physics_specialist"})-[r:BELONGS_TO {
  assigned_at: timestamp()
}]->(region:Region {name: "Physics"})
```

## Graph Patterns

### Agent Discovery Pattern

Find agents that can handle a specific concept, ordered by Hebbian weight:

```cypher
MATCH (a:Agent)-[r:HANDLES_CONCEPT]->(c:Concept {name: $concept_name})
WHERE a.status = 'active'
RETURN a, r
ORDER BY r.weight DESC, r.success_rate DESC
LIMIT 5
```

### Neurogenesis Check Pattern

Check if a concept already has agents before creating new one:

```cypher
MATCH (c:Concept {name: $concept_name})<-[r:HANDLES_CONCEPT]-(a:Agent)
WHERE a.status = 'active' AND r.weight > 0.3
RETURN count(a) as agent_count
```

### Hebbian Weight Update Pattern

Strengthen or weaken connection based on task outcome:

```cypher
MATCH (a:Agent {name: $agent_name})-[r:HANDLES_CONCEPT]->(c:Concept {name: $concept_name})
SET r.usage_count = r.usage_count + 1,
    r.success_count = r.success_count + CASE $success WHEN true THEN 1 ELSE 0 END,
    r.failure_count = r.failure_count + CASE $success WHEN false THEN 1 ELSE 0 END,
    r.success_rate = toFloat(r.success_count) / toFloat(r.usage_count),
    r.weight = CASE 
      WHEN $success THEN CASE WHEN r.weight + 0.05 > 1.0 THEN 1.0 ELSE r.weight + 0.05 END
      ELSE CASE WHEN r.weight - 0.02 < 0.0 THEN 0.0 ELSE r.weight - 0.02 END
    END,
    r.last_updated = timestamp(),
    r.last_used = timestamp()
```

### Weight Decay Pattern

Apply periodic decay to all connections (run every 15 minutes):

```cypher
MATCH ()-[r:HANDLES_CONCEPT]->()
WHERE r.last_updated < timestamp() - 900000  // 15 minutes in milliseconds
SET r.weight = r.weight * (1.0 - r.decay_rate),
    r.last_updated = timestamp()
RETURN count(r) as decayed_relationships
```

### Agent Health Check Pattern

Find unhealthy or underperforming agents:

```cypher
MATCH (a:Agent)-[r:HANDLES_CONCEPT]->()
WHERE a.status = 'active'
WITH a, avg(r.success_rate) as avg_success, count(r) as concept_count
WHERE avg_success < 0.5 OR concept_count = 0
RETURN a.name, avg_success, concept_count
ORDER BY avg_success ASC
```

### Concept Coverage Pattern

Find concepts without sufficient agent coverage:

```cypher
MATCH (c:Concept)
OPTIONAL MATCH (c)<-[r:HANDLES_CONCEPT]-(a:Agent)
WHERE a.status = 'active' AND r.weight > 0.3
WITH c, count(a) as agent_count
WHERE agent_count < 2
RETURN c.name, agent_count, c.category
ORDER BY agent_count ASC, c.complexity DESC
```

## Data Integrity Rules

### Constraints

1. **Agent names must be unique** - Prevents duplicate agent registration
2. **Concept names must be unique** - Prevents duplicate concept definitions
3. **Region names must be unique** - Prevents duplicate knowledge domains
4. **Required fields must not be null** - Ensures data completeness

### Validation Rules

1. **Agent type** - Must be "static" or "dynamic"
2. **Agent status** - Must be "active", "inactive", or "unhealthy"
3. **Concept names** - Must be lowercase for consistency
4. **Hebbian weights** - Must be in range [0.0, 1.0]
5. **Success rates** - Must be in range [0.0, 1.0]
6. **Counts** - Must be non-negative integers
7. **Endpoints** - Must be valid HTTP/HTTPS URLs
8. **Ports** - Must be in range [1, 65535]

## Performance Considerations

### Indexed Queries

- Agent lookup by name: O(log n) - indexed
- Concept lookup by name: O(log n) - indexed
- Agent filtering by type/status: O(log n) - indexed
- Hebbian weight sorting: O(log n) - indexed

### Query Optimization

- Use `LIMIT` for large result sets
- Filter on indexed properties first
- Use `WITH` clause to reduce intermediate results
- Avoid cartesian products in multi-pattern queries

### Scaling Guidelines

- Expected node count: ~1,000 agents, ~10,000 concepts
- Expected relationship count: ~50,000 HANDLES_CONCEPT relationships
- Query response time target: < 100ms for agent discovery
- Batch operations for bulk updates (e.g., weight decay)

## Schema Version

**Current Version:** 1.0.0

**Change History:**

- **1.0.0** (2025-10-10): Initial schema with Hebbian learning, constraints, and indexes

## Schema Evolution

When updating the schema:

1. Document changes in this file
2. Create migration script in `scripts/migrations/`
3. Update schema version in `init_schema.cypher`
4. Test migration on development database
5. Update validation rules if needed

## References

- [Neo4j Constraints Documentation](https://neo4j.com/docs/cypher-manual/current/constraints/)
- [Neo4j Indexes Documentation](https://neo4j.com/docs/cypher-manual/current/indexes/)
- [Hebbian Learning](https://en.wikipedia.org/wiki/Hebbian_theory)
- [Myriad Architecture Documentation](ARCHITECTURE.md)

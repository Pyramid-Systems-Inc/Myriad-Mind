// Neo4j Schema Initialization for Myriad Cognitive Architecture
// Version: 1.0.0
// Run this script once to set up constraints and indexes
// Usage: Run via initialize_graph_schema.py or manually in Neo4j Browser

// ===== CONSTRAINTS =====

// Agent constraints
CREATE CONSTRAINT agent_name_unique IF NOT EXISTS
FOR (a:Agent) REQUIRE a.name IS UNIQUE;

CREATE CONSTRAINT agent_name_exists IF NOT EXISTS
FOR (a:Agent) REQUIRE a.name IS NOT NULL;

CREATE CONSTRAINT agent_type_exists IF NOT EXISTS
FOR (a:Agent) REQUIRE a.type IS NOT NULL;

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

// ===== INDEXES FOR PERFORMANCE =====

// Agent indexes
CREATE INDEX agent_type_idx IF NOT EXISTS
FOR (a:Agent) ON (a.type);

CREATE INDEX agent_status_idx IF NOT EXISTS
FOR (a:Agent) ON (a.status);

CREATE INDEX agent_created_at_idx IF NOT EXISTS
FOR (a:Agent) ON (a.created_at);

// Concept indexes
CREATE INDEX concept_category_idx IF NOT EXISTS
FOR (c:Concept) ON (c.category);

CREATE INDEX concept_created_at_idx IF NOT EXISTS
FOR (c:Concept) ON (c.created_at);

// Full-text search index for concepts
CREATE FULLTEXT INDEX concept_search_idx IF NOT EXISTS
FOR (c:Concept) ON EACH [c.name, c.primary_definition];

// ===== RELATIONSHIP INDEXES =====

// Index for Hebbian weight queries
CREATE INDEX handles_concept_weight_idx IF NOT EXISTS
FOR ()-[r:HANDLES_CONCEPT]-() ON (r.weight);

CREATE INDEX handles_concept_success_rate_idx IF NOT EXISTS
FOR ()-[r:HANDLES_CONCEPT]-() ON (r.success_rate);

CREATE INDEX handles_concept_last_used_idx IF NOT EXISTS
FOR ()-[r:HANDLES_CONCEPT]-() ON (r.last_used);

// ===== SCHEMA VERSION TRACKING =====

MERGE (v:SchemaVersion {version: "1.0.0"})
ON CREATE SET 
  v.created_at = timestamp(),
  v.description = "Initial schema with Hebbian learning, constraints, and indexes"
ON MATCH SET
  v.updated_at = timestamp();

// ===== CREATE DEFAULT REGIONS =====

MERGE (r1:Region {name: "General"})
ON CREATE SET r1.description = "General knowledge domain", r1.created_at = timestamp();

MERGE (r2:Region {name: "Science"})
ON CREATE SET r2.description = "Scientific concepts and theories", r2.created_at = timestamp();

MERGE (r3:Region {name: "Technology"})
ON CREATE SET r3.description = "Technology and engineering concepts", r3.created_at = timestamp();

MERGE (r4:Region {name: "Mathematics"})
ON CREATE SET r4.description = "Mathematical concepts and operations", r4.created_at = timestamp();

// ===== VERIFICATION QUERY =====

// Run this to verify schema setup
MATCH (v:SchemaVersion)
RETURN v.version as schema_version, v.created_at as created_at, v.description as description;
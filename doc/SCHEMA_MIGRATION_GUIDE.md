# Neo4j Schema Migration Guide

This guide explains how to migrate existing Myriad graph data to the new schema with constraints and indexes.

## Overview

The new schema (v1.0.0) introduces:
- **Constraints** - Ensure data uniqueness and integrity
- **Indexes** - Improve query performance
- **Validation** - Prevent invalid data from entering the graph
- **Standardization** - Consistent property naming and formats

## Migration Scenarios

### Scenario 1: Fresh Installation (Recommended)

For new installations, simply run the initialization script:

```bash
python scripts/initialize_graph_schema.py
```

This will:
1. Create all constraints
2. Create all indexes
3. Set up default regions
4. Track schema version

### Scenario 2: Existing Data Migration

If you have existing data in Neo4j, follow these steps:

#### Step 1: Backup Your Data

**CRITICAL:** Always backup before migration!

```bash
# Using provided backup script
bash scripts/backup_neo4j.sh

# Or manually via Neo4j Admin
neo4j-admin dump --database=neo4j --to=/path/to/backup.dump
```

#### Step 2: Analyze Existing Data

Check for potential constraint violations:

```cypher
// Check for duplicate agent names
MATCH (a:Agent)
WITH a.name as name, count(*) as cnt
WHERE cnt > 1
RETURN name, cnt
ORDER BY cnt DESC;

// Check for duplicate concept names
MATCH (c:Concept)
WITH c.name as name, count(*) as cnt
WHERE cnt > 1
RETURN name, cnt
ORDER BY cnt DESC;

// Check for concepts with non-lowercase names
MATCH (c:Concept)
WHERE c.name <> toLower(c.name)
RETURN c.name, toLower(c.name) as should_be;

// Check for missing required properties
MATCH (a:Agent)
WHERE a.name IS NULL OR a.type IS NULL OR a.endpoint IS NULL
RETURN a;
```

#### Step 3: Clean Existing Data

**Fix duplicate agents:**
```cypher
// Merge duplicate agents, keeping the first one
MATCH (a:Agent)
WITH a.name as name, collect(a) as agents
WHERE size(agents) > 1
WITH name, agents[0] as keep, agents[1..] as remove
UNWIND remove as r
MATCH (r)-[rel]-()
DELETE rel
DELETE r;
```

**Fix concept name casing:**
```cypher
// Convert all concept names to lowercase
MATCH (c:Concept)
WHERE c.name <> toLower(c.name)
SET c.name = toLower(c.name);
```

**Add missing required properties:**
```cypher
// Add default status to agents without it
MATCH (a:Agent)
WHERE a.status IS NULL
SET a.status = 'active';

// Add created_at timestamp to nodes without it
MATCH (n)
WHERE n:Agent OR n:Concept OR n:Region
AND n.created_at IS NULL
SET n.created_at = timestamp();
```

**Fix Hebbian relationships:**
```cypher
// Ensure all HANDLES_CONCEPT relationships have required properties
MATCH ()-[r:HANDLES_CONCEPT]->()
WHERE r.weight IS NULL OR r.usage_count IS NULL
SET r.weight = coalesce(r.weight, 0.5),
    r.usage_count = coalesce(r.usage_count, 0),
    r.success_count = coalesce(r.success_count, 0),
    r.failure_count = coalesce(r.failure_count, 0),
    r.success_rate = coalesce(r.success_rate, 0.5),
    r.decay_rate = coalesce(r.decay_rate, 0.01),
    r.last_updated = coalesce(r.last_updated, timestamp());
```

#### Step 4: Run Schema Initialization

After cleaning the data, run the initialization:

```bash
python scripts/initialize_graph_schema.py
```

**Note:** If constraints fail due to existing violations, return to Step 3 and fix the issues.

#### Step 5: Verify Migration

```cypher
// Verify schema version
MATCH (v:SchemaVersion)
RETURN v.version, v.created_at, v.description;

// Check constraints
SHOW CONSTRAINTS;

// Check indexes
SHOW INDEXES;

// Verify data integrity
MATCH (a:Agent)
WHERE a.name IS NULL OR a.type IS NULL OR a.endpoint IS NULL
RETURN count(a) as invalid_agents;

MATCH (c:Concept)
WHERE c.name IS NULL OR c.name <> toLower(c.name)
RETURN count(c) as invalid_concepts;
```

### Scenario 3: Development/Testing Reset

To completely reset the database and start fresh:

```cypher
// WARNING: This deletes ALL data!
MATCH (n) DETACH DELETE n;

// Drop all constraints
DROP CONSTRAINT agent_name_unique IF EXISTS;
DROP CONSTRAINT concept_name_unique IF EXISTS;
// ... drop other constraints

// Drop all indexes
DROP INDEX agent_type_idx IF EXISTS;
DROP INDEX concept_search_idx IF EXISTS;
// ... drop other indexes
```

Then run initialization:
```bash
python scripts/initialize_graph_schema.py
```

## Migration Checklist

Before migration:
- [ ] Backup database
- [ ] Test migration on development environment
- [ ] Review existing data for violations
- [ ] Plan downtime if needed

During migration:
- [ ] Stop services that write to Neo4j
- [ ] Clean data to meet constraints
- [ ] Run initialization script
- [ ] Verify constraints and indexes created

After migration:
- [ ] Verify data integrity
- [ ] Test key operations
- [ ] Restart services
- [ ] Monitor for errors

## Rollback Plan

If migration fails:

1. **Stop all services**
2. **Restore from backup:**
   ```bash
   neo4j-admin restore --from=/path/to/backup.dump --database=neo4j --force
   ```
3. **Restart Neo4j**
4. **Verify data**
5. **Restart services**

## Common Issues

### Issue: Constraint creation fails

**Error:** `Node(...) already exists with label...`

**Solution:** Duplicate nodes exist. Use queries from Step 3 to find and merge duplicates.

### Issue: Index creation fails

**Error:** `Unable to create index...`

**Solution:** Check if index already exists or conflicts with existing schema.

### Issue: Validation rejecting valid data

**Error:** `Validation failed: ...`

**Solution:** Check [`validation.py`](../src/myriad/services/graphdb_manager/validation.py) rules. Data may need format adjustment.

### Issue: Performance degradation after migration

**Solution:** Indexes may need time to populate. Check index status:
```cypher
SHOW INDEXES;
```

Wait for indexes to reach "ONLINE" state.

## Future Schema Changes

When updating the schema in the future:

1. **Document changes** in [`GRAPH_SCHEMA.md`](GRAPH_SCHEMA.md)
2. **Create migration script** in `scripts/migrations/v{version}.cypher`
3. **Update schema version** in `init_schema.cypher`
4. **Test on development** environment
5. **Update validation rules** if needed
6. **Document in this guide**

Example migration script structure:

```cypher
// scripts/migrations/v1.1.0.cypher
// Migration from v1.0.0 to v1.1.0

// Add new property
MATCH (a:Agent)
SET a.health_score = 1.0;

// Create new index
CREATE INDEX agent_health_score_idx IF NOT EXISTS
FOR (a:Agent) ON (a.health_score);

// Update schema version
MATCH (v:SchemaVersion)
SET v.version = "1.1.0",
    v.updated_at = timestamp(),
    v.description = "Added agent health scoring";
```

## Support

For issues or questions:
1. Check [`GRAPH_SCHEMA.md`](GRAPH_SCHEMA.md) for schema reference
2. Review [`validation.py`](../src/myriad/services/graphdb_manager/validation.py) for validation rules
3. Consult [Neo4j Documentation](https://neo4j.com/docs/)
4. Open an issue in the project repository

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-10-10 | Initial schema with constraints, indexes, and validation |
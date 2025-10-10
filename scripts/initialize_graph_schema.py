#!/usr/bin/env python3
"""
Neo4j Schema Initialization Script
Runs init_schema.cypher to set up constraints, indexes, and default data

Usage:
    python scripts/initialize_graph_schema.py

Environment Variables:
    NEO4J_URI - Neo4j connection URI (default: bolt://localhost:7687)
    NEO4J_USER - Neo4j username (default: neo4j)
    NEO4J_PASSWORD - Neo4j password (default: myriadneo4j)
"""

import os
import sys
from pathlib import Path
from typing import List, Tuple

try:
    from neo4j import GraphDatabase
except ImportError:
    print("❌ Error: neo4j package not installed")
    print("Install with: pip install neo4j")
    sys.exit(1)

# Configuration
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "myriadneo4j")

def read_cypher_file(filepath: Path) -> List[str]:
    """
    Read and parse Cypher file into statements
    
    Args:
        filepath: Path to .cypher file
        
    Returns:
        List of Cypher statements
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by semicolons, filter out comments and empty lines
    statements = []
    for stmt in content.split(';'):
        stmt = stmt.strip()
        # Skip empty statements and comment-only statements
        if stmt and not all(line.strip().startswith('//') or not line.strip() for line in stmt.split('\n')):
            statements.append(stmt)
    
    return statements

def execute_statement(session, statement: str, statement_num: int, total: int) -> Tuple[bool, str]:
    """
    Execute a single Cypher statement
    
    Args:
        session: Neo4j session
        statement: Cypher statement to execute
        statement_num: Current statement number
        total: Total number of statements
        
    Returns:
        (success, message)
    """
    try:
        result = session.run(statement)
        summary = result.consume()
        
        # Get statement type from summary
        counters = summary.counters
        changes = []
        if counters.nodes_created > 0:
            changes.append(f"{counters.nodes_created} nodes created")
        if counters.relationships_created > 0:
            changes.append(f"{counters.relationships_created} relationships created")
        if counters.properties_set > 0:
            changes.append(f"{counters.properties_set} properties set")
        if counters.constraints_added > 0:
            changes.append(f"{counters.constraints_added} constraints added")
        if counters.indexes_added > 0:
            changes.append(f"{counters.indexes_added} indexes added")
        
        change_msg = ", ".join(changes) if changes else "no changes"
        return True, f"✅ Statement {statement_num}/{total} executed successfully ({change_msg})"
    
    except Exception as e:
        error_msg = str(e)
        # Some constraint/index operations may warn if they already exist
        if "already exists" in error_msg.lower() or "equivalent" in error_msg.lower():
            return True, f"⚠️  Statement {statement_num}/{total} skipped (already exists)"
        return False, f"❌ Statement {statement_num}/{total} failed: {error_msg}"

def initialize_schema() -> bool:
    """
    Initialize Neo4j schema with constraints and indexes
    
    Returns:
        True if successful, False otherwise
    """
    print("=" * 70)
    print("🚀 Neo4j Schema Initialization - Myriad Cognitive Architecture")
    print("=" * 70)
    print(f"📍 Connecting to: {NEO4J_URI}")
    print(f"👤 User: {NEO4J_USER}")
    
    driver = None
    try:
        # Connect to Neo4j
        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
        driver.verify_connectivity()
        print("✅ Connected to Neo4j successfully\n")
        
        # Read schema file
        script_dir = Path(__file__).parent
        schema_file = script_dir / "init_schema.cypher"
        
        if not schema_file.exists():
            print(f"❌ Schema file not found: {schema_file}")
            return False
        
        print(f"📖 Reading schema file: {schema_file}")
        statements = read_cypher_file(schema_file)
        print(f"📝 Found {len(statements)} Cypher statements\n")
        
        if not statements:
            print("⚠️  No statements to execute")
            return False
        
        # Execute statements
        print("🔧 Executing schema statements...")
        print("-" * 70)
        
        success_count = 0
        warning_count = 0
        error_count = 0
        
        with driver.session() as session:
            for idx, statement in enumerate(statements, 1):
                success, message = execute_statement(session, statement, idx, len(statements))
                print(message)
                
                if success:
                    if "⚠️" in message:
                        warning_count += 1
                    else:
                        success_count += 1
                else:
                    error_count += 1
        
        print("-" * 70)
        print(f"\n📊 Execution Summary:")
        print(f"   ✅ Successful: {success_count}")
        print(f"   ⚠️  Warnings: {warning_count}")
        print(f"   ❌ Errors: {error_count}")
        
        # Verify schema version
        print("\n🔍 Verifying schema version...")
        with driver.session() as session:
            result = session.run("MATCH (v:SchemaVersion) RETURN v.version as version, v.description as description, v.created_at as created_at")
            record = result.single()
            
            if record:
                print("✅ Schema version verified:")
                print(f"   📌 Version: {record['version']}")
                print(f"   📝 Description: {record['description']}")
                print(f"   🕐 Created: {record['created_at']}")
            else:
                print("⚠️  Schema version tracking not found")
        
        # Show created constraints
        print("\n📋 Verifying constraints...")
        with driver.session() as session:
            result = session.run("SHOW CONSTRAINTS")
            constraints = list(result)
            print(f"✅ Found {len(constraints)} constraints")
            for constraint in constraints[:5]:  # Show first 5
                print(f"   • {constraint.get('name', 'unnamed')}")
            if len(constraints) > 5:
                print(f"   ... and {len(constraints) - 5} more")
        
        # Show created indexes
        print("\n📋 Verifying indexes...")
        with driver.session() as session:
            result = session.run("SHOW INDEXES")
            indexes = list(result)
            print(f"✅ Found {len(indexes)} indexes")
            for index in indexes[:5]:  # Show first 5
                print(f"   • {index.get('name', 'unnamed')}")
            if len(indexes) > 5:
                print(f"   ... and {len(indexes) - 5} more")
        
        if error_count > 0:
            print("\n⚠️  Schema initialized with some errors")
            return False
        else:
            print("\n" + "=" * 70)
            print("🎉 Schema initialized successfully!")
            print("=" * 70)
            return True
        
    except Exception as e:
        print(f"\n❌ Error initializing schema: {str(e)}")
        return False
    
    finally:
        if driver:
            driver.close()
            print("\n🔌 Disconnected from Neo4j")

def main():
    """Main entry point"""
    try:
        success = initialize_schema()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
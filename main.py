#!/usr/bin/env python3
"""
Myriad Mind - Main Application Entrypoint
Aligned MVP 2.0

This script orchestrates the complete flow:
1. Takes raw query string as argument
2. Calls InputProcessor to get Task List
3. Passes Task List to Orchestrator to get results
4. Passes results to OutputProcessor to get final sentence
5. Prints final sentence to console

Usage: python main.py "Define a lightbulb and explain its limitation."

Note: This is a Phase 4 implementation placeholder.
The actual components will be implemented in subsequent phases.
"""

import sys
import json
from typing import Dict, Any
from orchestration.orchestrator import process_tasks # Added for Phase 1.3

def main():
    """Main application entry point"""

    # Note: Query processing from sys.argv is temporarily bypassed for Phase 1.3 testing.
    # if len(sys.argv) != 2:
    #     print("Usage: python main.py \"<query>\"")
    #     print("Example: python main.py \"Define a lightbulb and explain its limitation.\"")
    #     sys.exit(1)
    # query = sys.argv[1]
    # print(f"Processing query: {query}")

    # Phase 4 Implementation (Placeholder):
    # 1. Call InputProcessor.process_query(query) -> Task List
    # 2. Call Orchestrator.execute_tasks(task_list) -> Results Dict
    # 3. Call OutputProcessor.synthesize_output(results) -> Final String
    # 4. Print final result

    # --- Temporary Test for Phase 1.3: Basic Agent Communication ---
    print("\n--- Running Phase 1.3 Orchestrator Test ---")
    sample_task_list = {
        "query_id": "test-query-001",
        "tasks": [
            {"task_id": 1, "intent": "define", "concept": "lightbulb", "args": {}},
            {"task_id": 2, "intent": "explain_limitation", "concept": "lightbulb", "args": {}}
        ]
    }
    print(f"Sample Task List for Orchestrator: {json.dumps(sample_task_list, indent=2)}")
    
    results = process_tasks(sample_task_list['tasks'])
    
    print("\n--- Orchestrator Results ---")
    print(json.dumps(results, indent=2))
    print("--- End of Phase 1.3 Orchestrator Test ---\n")
    
    # Original Phase 1 completion message (can be removed or kept as needed)
    # print("\n[Phase 1 Complete] Foundation ready for agent implementation.")
    # print("Next: Implement agents in Phase 2, then processors and orchestrator in Phase 3.")
    # print("Full integration will be completed in Phase 4.")

if __name__ == "__main__":
    main()
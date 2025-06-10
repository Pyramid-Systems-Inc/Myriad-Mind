"""
Main Entry Point for Myriad Cognitive Architecture
Phase 1 - Foundation & Core Component Setup
"""

import sys
import json
import argparse
import logging
from pathlib import Path

# Add orchestrator to path
sys.path.append(str(Path(__file__).parent / "orchestrator"))

from orchestrator import Orchestrator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def main():
    """Main function to run the Myriad Cognitive Architecture system."""
    parser = argparse.ArgumentParser(
        description="Myriad Cognitive Architecture - Phase 1 MVP",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --query "Why was the lightbulb important for factories?"
  python main.py --status
  python main.py --test
        """
    )
    
    parser.add_argument(
        '--query', '-q',
        type=str,
        help='Query to process through the system'
    )
    
    parser.add_argument(
        '--status', '-s',
        action='store_true',
        help='Check the status of all agents in the registry'
    )
    
    parser.add_argument(
        '--test', '-t',
        action='store_true',
        help='Run a test query to verify system functionality'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Initialize the orchestrator
    logger.info("Initializing Myriad Cognitive Architecture...")
    orchestrator = Orchestrator()
    
    try:
        if args.status:
            # Check agent status
            print("\n=== Agent Registry Status ===")
            status = orchestrator.get_registry_status()
            for agent_name, agent_status in status.items():
                print(f"{agent_name}: {agent_status}")
            print()
            
        elif args.test:
            # Run test query
            print("\n=== Running Test Query ===")
            test_keywords = ["lightbulb", "factories"]
            print(f"Test keywords: {test_keywords}")
            
            responses = orchestrator.orchestrate_query(test_keywords)
            
            print("\n=== Agent Responses ===")
            print(json.dumps(responses, indent=2))
            
        elif args.query:
            # Process user query
            print(f"\n=== Processing Query ===")
            print(f"Query: {args.query}")
            
            # Simple keyword extraction for Phase 1
            # In later phases, this will be handled by the Input Processor
            keywords = extract_keywords(args.query)
            print(f"Extracted keywords: {keywords}")
            
            responses = orchestrator.orchestrate_query(keywords)
            
            print("\n=== Agent Responses ===")
            print(json.dumps(responses, indent=2))
            
        else:
            # No specific action, show help and system info
            parser.print_help()
            print("\n=== System Information ===")
            print("Myriad Cognitive Architecture - Phase 1")
            print("Foundation & Core Component Setup")
            print(f"Registered agents: {list(orchestrator.AI_REGISTRY.keys())}")
            
    except KeyboardInterrupt:
        logger.info("System interrupted by user")
        print("\nSystem interrupted.")
        
    except Exception as e:
        logger.error(f"System error: {str(e)}")
        print(f"Error: {str(e)}")
        sys.exit(1)

def extract_keywords(query: str) -> list:
    """
    Simple keyword extraction for Phase 1.
    In later phases, this will be replaced by the Input Processor.
    
    Args:
        query: Raw user query string
        
    Returns:
        List of extracted keywords
    """
    # Simple implementation for Phase 1
    # Convert to lowercase and split into words
    words = query.lower().split()
    
    # Filter out common stop words and short words
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'was', 'were', 'is', 'are', 'be', 'been', 'have',
        'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should',
        'may', 'might', 'can', 'shall', 'must', 'ought', 'this', 'that',
        'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they',
        'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his', 'her', 'its',
        'our', 'their', 'what', 'when', 'where', 'why', 'how', 'who', 'which'
    }
    
    # Extract meaningful keywords
    keywords = []
    for word in words:
        # Remove punctuation
        clean_word = ''.join(c for c in word if c.isalnum())
        
        # Keep words that are longer than 2 characters and not stop words
        if len(clean_word) > 2 and clean_word not in stop_words:
            keywords.append(clean_word)
    
    return keywords

if __name__ == "__main__":
    main()
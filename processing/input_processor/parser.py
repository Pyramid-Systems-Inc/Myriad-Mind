"""
Advanced Parser for the Enhanced Input Processor
Implements Task 3.1.1: Advanced Parser with keyword/entity extraction using NLP libraries

This module provides sophisticated parsing capabilities to transform raw user queries
into structured data including concepts, relationships, and complexity analysis.
"""

import re
import uuid
from datetime import datetime
from typing import Dict, List, Any, Tuple, Optional
from dataclasses import dataclass, asdict

# For now, we'll implement a sophisticated rule-based parser
# In production, this would use spaCy or NLTK for full NLP capabilities
# import spacy
# import nltk

@dataclass
class ParsedQuery:
    """Structured representation of a parsed query"""
    primary_intent: str
    concepts: List[str]
    relationships: List[Dict[str, str]]
    complexity_score: float
    estimated_agents_needed: int

@dataclass
class QueryMetadata:
    """Metadata about the query session"""
    query_id: str
    original_query: str
    timestamp: str
    user_context: Dict[str, Any]

class AdvancedParser:
    """
    Advanced Parser implementing sophisticated query analysis
    
    This parser extracts:
    - Primary intent from the query
    - Key concepts and entities
    - Relationships between concepts
    - Complexity scoring
    - Agent estimation
    """
    
    def __init__(self):
        """Initialize the parser with knowledge bases and patterns"""
        # Intent patterns for recognition
        self.intent_patterns = {
            'define': [
                r'\b(?:what is|define|definition of|meaning of)\b',
                r'\b(?:explain what|tell me about)\b'
            ],
            'analyze_historical_context': [
                r'\b(?:historical|history|past|evolution|development)\b',
                r'\b(?:when did|how did.*develop|timeline)\b'
            ],
            'explain_impact': [
                r'\b(?:impact|effect|influence|consequence|result)\b',
                r'\b(?:why.*important|significance|role)\b'
            ],
            'compare': [
                r'\b(?:compare|comparison|versus|vs|difference|similar)\b',
                r'\b(?:better than|worse than|advantages|disadvantages)\b'
            ],
            'calculate': [
                r'\b(?:calculate|compute|math|number|quantity)\b',
                r'\b(?:how much|how many|total|sum)\b'
            ],
            'summarize': [
                r'\b(?:summarize|summary|overview|brief|outline)\b',
                r'\b(?:main points|key aspects|in short)\b'
            ]
        }
        
        # Concept extraction patterns
        self.concept_patterns = [
            r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b',  # Proper nouns
            r'\b(?:lightbulb|factory|factories|industrial|electricity|technology)\b',  # Domain-specific
            r'\b\w+(?:ing|tion|ness|ment|ity)\b'  # Abstract concepts
        ]
        
        # Relationship indicators
        self.relationship_patterns = {
            'causal': [r'\b(?:because|due to|caused by|resulted in|led to)\b'],
            'temporal': [r'\b(?:before|after|during|when|while)\b'],
            'comparative': [r'\b(?:than|versus|compared to|unlike)\b'],
            'functional': [r'\b(?:used for|purpose|function|role)\b']
        }
    
    def parse_query(self, query: str, user_context: Optional[Dict] = None) -> Tuple[QueryMetadata, ParsedQuery]:
        """
        Parse a raw query into structured components
        
        Args:
            query: Raw user query string
            user_context: Optional user context information
            
        Returns:
            Tuple of (QueryMetadata, ParsedQuery)
        """
        # Generate query metadata
        query_metadata = QueryMetadata(
            query_id=f"q_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{str(uuid.uuid4())[:8]}",
            original_query=query,
            timestamp=datetime.now().isoformat(),
            user_context=user_context or {
                "session_id": f"sess_{str(uuid.uuid4())[:8]}",
                "previous_queries": [],
                "preferred_detail_level": "standard"
            }
        )
        
        # Extract primary intent
        primary_intent = self._extract_primary_intent(query)
        
        # Extract concepts
        concepts = self._extract_concepts(query)
        
        # Extract relationships
        relationships = self._extract_relationships(query, concepts)
        
        # Calculate complexity score
        complexity_score = self._calculate_complexity_score(query, concepts, relationships)
        
        # Estimate agents needed
        estimated_agents_needed = self._estimate_agents_needed(concepts, relationships, complexity_score)
        
        parsed_query = ParsedQuery(
            primary_intent=primary_intent,
            concepts=concepts,
            relationships=relationships,
            complexity_score=complexity_score,
            estimated_agents_needed=estimated_agents_needed
        )
        
        return query_metadata, parsed_query
    
    def _extract_primary_intent(self, query: str) -> str:
        """Extract the primary intent from the query"""
        query_lower = query.lower()
        
        # Score each intent based on pattern matches
        intent_scores = {}
        for intent, patterns in self.intent_patterns.items():
            score = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, query_lower))
                score += matches
            intent_scores[intent] = score
        
        # Return the highest scoring intent, default to 'define'
        if intent_scores and max(intent_scores.values()) > 0:
            return max(intent_scores, key=intent_scores.get)
        return 'define'
    
    def _extract_concepts(self, query: str) -> List[str]:
        """Extract key concepts from the query"""
        concepts = set()
        
        # Extract using various patterns
        for pattern in self.concept_patterns:
            matches = re.findall(pattern, query, re.IGNORECASE)
            concepts.update([match.lower() for match in matches if len(match) > 2])
        
        # Filter out common words and return unique concepts
        stopwords = {'the', 'and', 'for', 'are', 'was', 'were', 'been', 'have', 'has', 'had', 'will', 'would', 'could', 'should'}
        filtered_concepts = [concept for concept in concepts if concept not in stopwords]
        
        return sorted(list(set(filtered_concepts)))[:10]  # Limit to top 10 concepts
    
    def _extract_relationships(self, query: str, concepts: List[str]) -> List[Dict[str, str]]:
        """Extract relationships between concepts"""
        relationships = []
        query_lower = query.lower()
        
        # Look for relationship patterns
        for rel_type, patterns in self.relationship_patterns.items():
            for pattern in patterns:
                if re.search(pattern, query_lower):
                    # For simplicity, create relationships between first two concepts
                    if len(concepts) >= 2:
                        relationships.append({
                            "type": rel_type,
                            "subject": concepts[0],
                            "object": concepts[1]
                        })
                        break
        
        return relationships
    
    def _calculate_complexity_score(self, query: str, concepts: List[str], relationships: List[Dict]) -> float:
        """Calculate complexity score based on query characteristics"""
        base_score = 0.1
        
        # Length factor
        length_factor = min(len(query.split()) / 20.0, 0.3)
        
        # Concept factor
        concept_factor = min(len(concepts) / 10.0, 0.3)
        
        # Relationship factor
        relationship_factor = min(len(relationships) / 5.0, 0.2)
        
        # Question complexity factor
        question_words = ['why', 'how', 'when', 'where', 'what', 'which', 'who']
        question_factor = sum(1 for word in question_words if word in query.lower()) * 0.1
        
        complexity_score = base_score + length_factor + concept_factor + relationship_factor + question_factor
        return min(complexity_score, 1.0)  # Cap at 1.0
    
    def _estimate_agents_needed(self, concepts: List[str], relationships: List[Dict], complexity_score: float) -> int:
        """Estimate number of agents needed to answer the query"""
        base_agents = 1
        
        # One agent per major concept
        concept_agents = len(concepts)
        
        # Additional agents for relationships
        relationship_agents = len(relationships)
        
        # Complexity multiplier
        complexity_multiplier = 1 + complexity_score
        
        estimated = int((base_agents + concept_agents + relationship_agents) * complexity_multiplier)
        return max(1, min(estimated, 10))  # Between 1 and 10 agents

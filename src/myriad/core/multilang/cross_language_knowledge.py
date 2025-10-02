"""
Cross-Language Knowledge Manager for Myriad Cognitive Architecture
=================================================================

This module provides cross-language knowledge sharing capabilities,
enabling concepts learned in one language to be accessible in all
supported languages.

Author: Myriad Cognitive Architecture Team
Version: 1.0 (Cross-Language Knowledge)
Date: 2025-10-02
"""

from typing import Dict, List, Optional, Set, Any
from dataclasses import dataclass, field
from datetime import datetime
import json

from .language_detector import Language
from .translation_service import get_translation_service, TranslationResult

@dataclass
class ConceptNode:
    """
    A concept node representing knowledge in multiple languages
    
    This is the core data structure for cross-language knowledge.
    Each concept has representations in multiple languages, all
    linked to the same underlying concept.
    """
    concept_id: str
    canonical_name: str  # Primary name (usually in English)
    language_variants: Dict[Language, str] = field(default_factory=dict)
    definitions: Dict[Language, str] = field(default_factory=dict)
    related_concepts: Set[str] = field(default_factory=set)
    properties: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    source_language: Language = Language.ENGLISH
    confidence: float = 1.0

@dataclass
class ConceptMapping:
    """Mapping between concepts across languages"""
    concept_id: str
    source_language: Language
    source_term: str
    target_language: Language
    target_term: str
    confidence: float
    mapping_method: str  # 'translation', 'manual', 'learned'
    created_at: datetime = field(default_factory=datetime.now)


class CrossLanguageKnowledgeManager:
    """
    Manages knowledge across multiple languages
    
    This manager:
    - Stores concepts with multi-language representations
    - Translates concepts across language boundaries
    - Ensures knowledge learned in one language benefits all languages
    - Maintains concept mappings and relationships
    """
    
    def __init__(self):
        """Initialize the cross-language knowledge manager"""
        self.translation_service = get_translation_service()
        
        # Concept storage: concept_id -> ConceptNode
        self.concepts: Dict[str, ConceptNode] = {}
        
        # Language index: (language, term) -> concept_id
        self.language_index: Dict[tuple, str] = {}
        
        # Concept mappings for tracking relationships
        self.mappings: List[ConceptMapping] = []
        
        # Statistics
        self.concepts_created = 0
        self.translations_added = 0
        self.cross_language_queries = 0
    
    def add_concept(self, concept_name: str, language: Language, 
                   definition: Optional[str] = None,
                   properties: Optional[Dict[str, Any]] = None) -> str:
        """
        Add a new concept to the knowledge base
        
        Args:
            concept_name: Name of the concept
            language: Language of the concept name
            definition: Optional definition of the concept
            properties: Optional properties/metadata
            
        Returns:
            concept_id: Unique identifier for the concept
        """
        # Check if concept already exists in this language
        index_key = (language, concept_name.lower())
        if index_key in self.language_index:
            return self.language_index[index_key]
        
        # Create new concept
        concept_id = f"concept_{len(self.concepts)}_{concept_name.lower().replace(' ', '_')}"
        
        concept_node = ConceptNode(
            concept_id=concept_id,
            canonical_name=concept_name,
            source_language=language,
            language_variants={language: concept_name},
            definitions={language: definition} if definition else {},
            properties=properties or {},
            confidence=1.0
        )
        
        # Store concept
        self.concepts[concept_id] = concept_node
        
        # Index it
        self.language_index[index_key] = concept_id
        
        self.concepts_created += 1
        
        # Automatically generate translations for common languages
        self._auto_translate_concept(concept_id, language, concept_name)
        
        return concept_id
    
    def _auto_translate_concept(self, concept_id: str, source_lang: Language, 
                                concept_name: str):
        """
        Automatically translate a concept to other supported languages
        
        Args:
            concept_id: The concept ID
            source_lang: Source language
            concept_name: Concept name to translate
        """
        # Target languages for auto-translation
        target_languages = [
            Language.ENGLISH, Language.SPANISH, Language.FRENCH, 
            Language.GERMAN, Language.CHINESE, Language.PORTUGUESE,
            Language.ITALIAN, Language.RUSSIAN
        ]
        
        concept_node = self.concepts[concept_id]
        
        for target_lang in target_languages:
            if target_lang == source_lang:
                continue
            
            # Try to translate
            translation_result = self.translation_service.translate(
                concept_name, source_lang, target_lang
            )
            
            if translation_result:
                # Add translation to concept
                concept_node.language_variants[target_lang] = translation_result.translated_text
                
                # Index the translation
                index_key = (target_lang, translation_result.translated_text.lower())
                self.language_index[index_key] = concept_id
                
                # Record the mapping
                mapping = ConceptMapping(
                    concept_id=concept_id,
                    source_language=source_lang,
                    source_term=concept_name,
                    target_language=target_lang,
                    target_term=translation_result.translated_text,
                    confidence=translation_result.confidence,
                    mapping_method=translation_result.method
                )
                self.mappings.append(mapping)
                
                self.translations_added += 1
    
    def get_concept(self, term: str, language: Language) -> Optional[ConceptNode]:
        """
        Get a concept by term and language
        
        Args:
            term: The term to look up
            language: The language of the term
            
        Returns:
            ConceptNode if found, None otherwise
        """
        index_key = (language, term.lower())
        concept_id = self.language_index.get(index_key)
        
        if concept_id:
            return self.concepts.get(concept_id)
        
        return None
    
    def get_concept_in_language(self, concept_id: str, 
                               target_language: Language) -> Optional[str]:
        """
        Get the representation of a concept in a specific language
        
        Args:
            concept_id: The concept ID
            target_language: Desired language
            
        Returns:
            Concept term in target language, or None if not available
        """
        concept_node = self.concepts.get(concept_id)
        if not concept_node:
            return None
        
        # Check if we have this language variant
        if target_language in concept_node.language_variants:
            return concept_node.language_variants[target_language]
        
        # Try to translate from source language
        source_term = concept_node.language_variants.get(concept_node.source_language)
        if source_term:
            translation_result = self.translation_service.translate(
                source_term, concept_node.source_language, target_language
            )
            
            if translation_result:
                # Cache this translation
                concept_node.language_variants[target_language] = translation_result.translated_text
                self.translations_added += 1
                return translation_result.translated_text
        
        return None
    
    def share_knowledge_across_languages(self, concept_id: str, 
                                        source_lang: Language,
                                        target_lang: Language) -> bool:
        """
        Share knowledge about a concept from source to target language
        
        Args:
            concept_id: The concept to share
            source_lang: Source language
            target_lang: Target language
            
        Returns:
            True if sharing was successful, False otherwise
        """
        concept_node = self.concepts.get(concept_id)
        if not concept_node:
            return False
        
        # Get source term
        source_term = concept_node.language_variants.get(source_lang)
        if not source_term:
            return False
        
        # Get or create target term
        target_term = self.get_concept_in_language(concept_id, target_lang)
        if not target_term:
            return False
        
        # Share definition if available
        if source_lang in concept_node.definitions:
            source_definition = concept_node.definitions[source_lang]
            
            # Translate definition
            translation_result = self.translation_service.translate(
                source_definition, source_lang, target_lang
            )
            
            if translation_result:
                concept_node.definitions[target_lang] = translation_result.translated_text
        
        # Update timestamp
        concept_node.updated_at = datetime.now()
        
        return True
    
    def ensure_multilingual_coverage(self, concept_id: str) -> Dict[Language, str]:
        """
        Ensure a concept has representations in all supported languages
        
        Args:
            concept_id: The concept ID
            
        Returns:
            Dictionary of language -> term for all available languages
        """
        concept_node = self.concepts.get(concept_id)
        if not concept_node:
            return {}
        
        # Languages to ensure coverage for
        target_languages = [
            Language.ENGLISH, Language.SPANISH, Language.FRENCH,
            Language.GERMAN, Language.CHINESE, Language.PORTUGUESE,
            Language.ITALIAN, Language.RUSSIAN
        ]
        
        results = {}
        
        for target_lang in target_languages:
            term = self.get_concept_in_language(concept_id, target_lang)
            if term:
                results[target_lang] = term
        
        return results
    
    def find_related_concepts(self, concept_id: str, 
                             language: Optional[Language] = None) -> List[str]:
        """
        Find concepts related to the given concept
        
        Args:
            concept_id: The concept ID
            language: Optional language for filtering
            
        Returns:
            List of related concept IDs
        """
        concept_node = self.concepts.get(concept_id)
        if not concept_node:
            return []
        
        return list(concept_node.related_concepts)
    
    def add_concept_relationship(self, concept_id_1: str, concept_id_2: str):
        """
        Add a relationship between two concepts
        
        Args:
            concept_id_1: First concept
            concept_id_2: Second concept
        """
        if concept_id_1 in self.concepts and concept_id_2 in self.concepts:
            self.concepts[concept_id_1].related_concepts.add(concept_id_2)
            self.concepts[concept_id_2].related_concepts.add(concept_id_1)
    
    def cross_language_search(self, query: str, query_language: Language,
                             search_languages: Optional[List[Language]] = None) -> List[ConceptNode]:
        """
        Search for concepts across multiple languages
        
        Args:
            query: Search query
            query_language: Language of the query
            search_languages: Languages to search in (None = all)
            
        Returns:
            List of matching ConceptNode objects
        """
        self.cross_language_queries += 1
        
        if search_languages is None:
            search_languages = [
                Language.ENGLISH, Language.SPANISH, Language.FRENCH,
                Language.GERMAN, Language.CHINESE, Language.PORTUGUESE,
                Language.ITALIAN, Language.RUSSIAN
            ]
        
        matches = []
        query_lower = query.lower()
        
        # First, try exact match in query language
        exact_match = self.get_concept(query, query_language)
        if exact_match:
            matches.append(exact_match)
        
        # Then search in other languages
        for language in search_languages:
            if language == query_language:
                continue
            
            # Translate query to this language
            translation_result = self.translation_service.translate(
                query, query_language, language
            )
            
            if translation_result:
                concept = self.get_concept(translation_result.translated_text, language)
                if concept and concept not in matches:
                    matches.append(concept)
        
        return matches
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about the knowledge base"""
        total_translations = sum(
            len(concept.language_variants) for concept in self.concepts.values()
        )
        
        return {
            'total_concepts': len(self.concepts),
            'concepts_created': self.concepts_created,
            'total_translations': total_translations,
            'translations_added': self.translations_added,
            'total_mappings': len(self.mappings),
            'cross_language_queries': self.cross_language_queries,
            'avg_translations_per_concept': total_translations / max(len(self.concepts), 1)
        }
    
    def export_knowledge_base(self) -> Dict[str, Any]:
        """Export the entire knowledge base for persistence"""
        return {
            'concepts': {
                cid: {
                    'concept_id': concept.concept_id,
                    'canonical_name': concept.canonical_name,
                    'language_variants': {
                        lang.value: term for lang, term in concept.language_variants.items()
                    },
                    'definitions': {
                        lang.value: defn for lang, defn in concept.definitions.items()
                    },
                    'related_concepts': list(concept.related_concepts),
                    'properties': concept.properties,
                    'source_language': concept.source_language.value,
                    'confidence': concept.confidence,
                    'created_at': concept.created_at.isoformat(),
                    'updated_at': concept.updated_at.isoformat()
                }
                for cid, concept in self.concepts.items()
            },
            'statistics': self.get_statistics()
        }
    
    def import_knowledge_base(self, data: Dict[str, Any]):
        """Import a knowledge base from exported data"""
        for concept_id, concept_data in data.get('concepts', {}).items():
            concept_node = ConceptNode(
                concept_id=concept_data['concept_id'],
                canonical_name=concept_data['canonical_name'],
                language_variants={
                    Language(lang): term 
                    for lang, term in concept_data['language_variants'].items()
                },
                definitions={
                    Language(lang): defn 
                    for lang, defn in concept_data['definitions'].items()
                },
                related_concepts=set(concept_data['related_concepts']),
                properties=concept_data['properties'],
                source_language=Language(concept_data['source_language']),
                confidence=concept_data['confidence'],
                created_at=datetime.fromisoformat(concept_data['created_at']),
                updated_at=datetime.fromisoformat(concept_data['updated_at'])
            )
            
            self.concepts[concept_id] = concept_node
            
            # Rebuild index
            for lang, term in concept_node.language_variants.items():
                index_key = (lang, term.lower())
                self.language_index[index_key] = concept_id


# Global knowledge manager instance
_global_knowledge_manager = None


def get_cross_language_knowledge_manager() -> CrossLanguageKnowledgeManager:
    """
    Get the global cross-language knowledge manager instance (singleton pattern)
    
    Returns:
        CrossLanguageKnowledgeManager: The global knowledge manager
    """
    global _global_knowledge_manager
    if _global_knowledge_manager is None:
        _global_knowledge_manager = CrossLanguageKnowledgeManager()
    return _global_knowledge_manager

"""
Multi-format Formatter for the Enhanced Output Processor
Implements Task 3.2.2: Multi-format Formatter with natural language generation

This module supports multiple output formats (explanatory_paragraph, structured_list, 
comparative_analysis), target length control (brief, standard, detailed), and 
evidence integration with source attribution and confidence indicators.
"""

import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

class OutputFormat(Enum):
    """Supported output formats"""
    EXPLANATORY_PARAGRAPH = "explanatory_paragraph"
    STRUCTURED_LIST = "structured_list"
    COMPARATIVE_ANALYSIS = "comparative_analysis"
    TECHNICAL_SUMMARY = "technical_summary"
    NARRATIVE = "narrative"

class TargetLength(Enum):
    """Target length options"""
    BRIEF = "brief"        # 1-2 sentences, ~50-100 words
    STANDARD = "standard"  # 1-2 paragraphs, ~100-200 words
    DETAILED = "detailed"  # 2-3 paragraphs, ~200-400 words

class EvidenceLevel(Enum):
    """Evidence integration levels"""
    MINIMAL = "minimal"    # No source attribution
    STANDARD = "standard"  # Basic source mentions
    DETAILED = "detailed"  # Full citations with confidence
    ACADEMIC = "academic"  # Formal citation style

@dataclass
class FormattingParameters:
    """Parameters controlling the formatting process"""
    output_format: OutputFormat
    target_length: TargetLength
    evidence_level: EvidenceLevel
    include_confidence: bool = True
    include_warnings: bool = True
    citation_style: str = "inline"
    language_style: str = "professional"

@dataclass
class FormattedResponse:
    """Final formatted response"""
    content: str
    format_type: str
    word_count: int
    confidence_indicator: Optional[str]
    citations: List[str]
    metadata: Dict[str, Any]

class MultiFormatFormatter:
    """
    Multi-format Formatter with natural language generation
    
    Features:
    - Multiple output formats (explanatory_paragraph, structured_list, comparative_analysis)
    - Target length control (brief, standard, detailed)
    - Evidence integration with source attribution and confidence indicators
    - Flexible citation styles and language adaptation
    - Natural language generation with coherent flow
    """
    
    def __init__(self):
        """Initialize the formatter with templates and configurations"""
        
        # Word count targets for different lengths
        self.length_targets = {
            TargetLength.BRIEF: (50, 100),
            TargetLength.STANDARD: (100, 200),
            TargetLength.DETAILED: (200, 400)
        }
        
        # Confidence level descriptions
        self.confidence_descriptions = {
            (0.9, 1.0): "with high confidence",
            (0.7, 0.9): "with moderate confidence",
            (0.5, 0.7): "with some uncertainty",
            (0.0, 0.5): "with low confidence"
        }
        
        # Transition phrases for natural flow
        self.transition_phrases = {
            'addition': ['Furthermore', 'Additionally', 'Moreover', 'In addition'],
            'contrast': ['However', 'Nevertheless', 'On the other hand', 'Conversely'],
            'causation': ['Therefore', 'Consequently', 'As a result', 'Thus'],
            'emphasis': ['Importantly', 'Notably', 'Significantly', 'Particularly'],
            'conclusion': ['In conclusion', 'Overall', 'To summarize', 'In summary']
        }
        
        # Format-specific templates
        self.format_templates = {
            OutputFormat.EXPLANATORY_PARAGRAPH: {
                'opening': "Based on the analysis, {main_point}",
                'supporting': "{transition} {evidence}",
                'closing': "{conclusion_phrase} {summary}"
            },
            OutputFormat.STRUCTURED_LIST: {
                'header': "Key findings:",
                'item_format': "• {point} ({confidence})",
                'footer': "Sources: {sources}"
            },
            OutputFormat.COMPARATIVE_ANALYSIS: {
                'similarities': "Common findings include:",
                'differences': "Key differences emerge in:",
                'conclusion': "Overall assessment:"
            }
        }
    
    def format_response(self, synthesized_content: str, 
                       evidence_sources: List[str],
                       confidence_score: float,
                       synthesis_metadata: Dict[str, Any],
                       formatting_parameters: FormattingParameters,
                       warnings: Optional[List[str]] = None) -> FormattedResponse:
        """
        Format synthesized content according to specified parameters
        
        Args:
            synthesized_content: Raw synthesized content from Synthesizer
            evidence_sources: List of source agent IDs
            confidence_score: Overall confidence in the synthesis
            synthesis_metadata: Metadata from synthesis process
            formatting_parameters: Formatting configuration
            warnings: Optional warnings to include
            
        Returns:
            FormattedResponse with properly formatted content
        """
        
        # Apply format-specific processing
        if formatting_parameters.output_format == OutputFormat.EXPLANATORY_PARAGRAPH:
            formatted_content = self._format_explanatory_paragraph(
                synthesized_content, formatting_parameters, synthesis_metadata
            )
        elif formatting_parameters.output_format == OutputFormat.STRUCTURED_LIST:
            formatted_content = self._format_structured_list(
                synthesized_content, formatting_parameters, synthesis_metadata
            )
        elif formatting_parameters.output_format == OutputFormat.COMPARATIVE_ANALYSIS:
            formatted_content = self._format_comparative_analysis(
                synthesized_content, formatting_parameters, synthesis_metadata
            )
        else:
            # Default to explanatory paragraph
            formatted_content = self._format_explanatory_paragraph(
                synthesized_content, formatting_parameters, synthesis_metadata
            )
        
        # Apply length control
        formatted_content = self._apply_length_control(
            formatted_content, formatting_parameters.target_length
        )
        
        # Add evidence and citations
        formatted_content, citations = self._add_evidence_attribution(
            formatted_content, evidence_sources, formatting_parameters.evidence_level
        )
        
        # Add confidence indicators
        confidence_indicator = None
        if formatting_parameters.include_confidence:
            confidence_indicator = self._generate_confidence_indicator(confidence_score)
            formatted_content = self._integrate_confidence_indicator(
                formatted_content, confidence_indicator
            )
        
        # Add warnings if requested
        if formatting_parameters.include_warnings and warnings:
            formatted_content = self._add_warnings(formatted_content, warnings)
        
        # Calculate final word count
        word_count = len(formatted_content.split())
        
        # Generate metadata
        metadata = self._generate_formatting_metadata(
            formatting_parameters, synthesis_metadata, word_count
        )
        
        return FormattedResponse(
            content=formatted_content,
            format_type=formatting_parameters.output_format.value,
            word_count=word_count,
            confidence_indicator=confidence_indicator,
            citations=citations,
            metadata=metadata
        )
    
    def _format_explanatory_paragraph(self, content: str, 
                                    parameters: FormattingParameters,
                                    metadata: Dict[str, Any]) -> str:
        """Format content as an explanatory paragraph"""
        
        # Split content into logical segments
        segments = self._segment_content(content)
        
        if not segments:
            return content
        
        # Build coherent paragraph
        formatted_parts = []
        
        # Opening with main point
        main_point = segments[0]
        formatted_parts.append(main_point)
        
        # Add supporting points with transitions
        for i, segment in enumerate(segments[1:], 1):
            if i == 1:
                transition = self._select_transition('addition')
            elif i == len(segments) - 1:
                transition = self._select_transition('conclusion')
            else:
                transition = self._select_transition('addition')
            
            formatted_parts.append(f"{transition}, {segment.lower()}")
        
        return " ".join(formatted_parts)
    
    def _format_structured_list(self, content: str, 
                              parameters: FormattingParameters,
                              metadata: Dict[str, Any]) -> str:
        """Format content as a structured list"""
        
        segments = self._segment_content(content)
        
        if not segments:
            return f"• {content}"
        
        # Create header
        header = "Key findings:"
        
        # Format each segment as a list item
        list_items = []
        for i, segment in enumerate(segments, 1):
            # Clean up segment for list format
            clean_segment = segment.strip().rstrip('.')
            list_items.append(f"{i}. {clean_segment}")
        
        return f"{header}\n" + "\n".join(list_items)
    
    def _format_comparative_analysis(self, content: str, 
                                   parameters: FormattingParameters,
                                   metadata: Dict[str, Any]) -> str:
        """Format content as a comparative analysis"""
        
        # Look for comparative indicators in metadata
        reinforcements = metadata.get('reinforcement_pairs', 0)
        contradictions = metadata.get('contradiction_pairs', 0)
        
        segments = self._segment_content(content)
        
        formatted_parts = []
        
        # Similarities section
        if reinforcements > 0:
            formatted_parts.append("Areas of agreement:")
            # Take first half of segments as agreements
            mid_point = len(segments) // 2
            for segment in segments[:mid_point]:
                formatted_parts.append(f"• {segment}")
        
        # Differences section
        if contradictions > 0:
            formatted_parts.append("\nAreas of divergence:")
            # Take second half as differences
            for segment in segments[mid_point:]:
                formatted_parts.append(f"• {segment}")
        
        # If no clear comparative structure, fall back to standard format
        if not formatted_parts:
            return self._format_explanatory_paragraph(content, parameters, metadata)
        
        return "\n".join(formatted_parts)
    
    def _segment_content(self, content: str) -> List[str]:
        """Segment content into logical parts"""
        # Split on sentence boundaries and common separators
        segments = re.split(r'[.!?]+\s+|;\s+|\.\s+(?=[A-Z])', content)
        
        # Clean and filter segments
        cleaned_segments = []
        for segment in segments:
            segment = segment.strip()
            if len(segment) > 10:  # Filter out very short segments
                cleaned_segments.append(segment)
        
        return cleaned_segments
    
    def _select_transition(self, transition_type: str) -> str:
        """Select an appropriate transition phrase"""
        phrases = self.transition_phrases.get(transition_type, [''])
        # Simple selection - could be made more sophisticated
        return phrases[0] if phrases else ''
    
    def _apply_length_control(self, content: str, target_length: TargetLength) -> str:
        """Apply length control to content"""
        current_word_count = len(content.split())
        min_words, max_words = self.length_targets[target_length]
        
        if current_word_count <= max_words:
            return content
        
        # Truncate if too long
        words = content.split()
        if target_length == TargetLength.BRIEF:
            # For brief, take first sentence or two
            sentences = re.split(r'[.!?]+', content)
            truncated = sentences[0]
            if len(truncated.split()) < min_words and len(sentences) > 1:
                truncated += ". " + sentences[1]
        else:
            # For standard/detailed, truncate at word boundary
            truncated = " ".join(words[:max_words])
            # Try to end at sentence boundary
            last_sentence_end = max(
                truncated.rfind('.'),
                truncated.rfind('!'),
                truncated.rfind('?')
            )
            if last_sentence_end > len(truncated) * 0.8:  # If close to end
                truncated = truncated[:last_sentence_end + 1]
        
        return truncated
    
    def _add_evidence_attribution(self, content: str, sources: List[str], 
                                evidence_level: EvidenceLevel) -> tuple[str, List[str]]:
        """Add evidence attribution based on level"""
        citations = []
        
        if evidence_level == EvidenceLevel.MINIMAL:
            return content, citations
        
        # Clean up source names for citation
        clean_sources = []
        for source in sources[:5]:  # Limit to 5 sources
            # Convert agent IDs to readable names
            clean_name = source.replace('_', ' ').replace('ai', '').replace('001', '').strip()
            clean_name = ' '.join(word.capitalize() for word in clean_name.split())
            clean_sources.append(clean_name)
            citations.append(clean_name)
        
        if evidence_level == EvidenceLevel.STANDARD:
            if clean_sources:
                attribution = f" (Sources: {', '.join(clean_sources)})"
                content += attribution
        
        elif evidence_level == EvidenceLevel.DETAILED:
            if clean_sources:
                attribution = f"\n\nSources consulted: {', '.join(clean_sources)}"
                content += attribution
        
        elif evidence_level == EvidenceLevel.ACADEMIC:
            # More formal citation style
            if clean_sources:
                numbered_citations = [f"[{i+1}] {source}" for i, source in enumerate(clean_sources)]
                content += f"\n\nReferences:\n" + "\n".join(numbered_citations)
        
        return content, citations
    
    def _generate_confidence_indicator(self, confidence_score: float) -> str:
        """Generate a confidence indicator description"""
        for (min_conf, max_conf), description in self.confidence_descriptions.items():
            if min_conf <= confidence_score < max_conf:
                return description
        return "with uncertain confidence"
    
    def _integrate_confidence_indicator(self, content: str, indicator: str) -> str:
        """Integrate confidence indicator into content"""
        # Add confidence indicator at the beginning
        if content.startswith("Based on"):
            # Insert after "Based on the analysis"
            insertion_point = content.find(",")
            if insertion_point > 0:
                return content[:insertion_point] + f" ({indicator})" + content[insertion_point:]
        
        # Default: add at the beginning
        return f"The analysis suggests {indicator} that {content.lower()}"
    
    def _add_warnings(self, content: str, warnings: List[str]) -> str:
        """Add warnings to the formatted content"""
        if not warnings:
            return content
        
        warning_text = "\n\nNote: " + "; ".join(warnings[:2])  # Limit to 2 warnings
        return content + warning_text
    
    def _generate_formatting_metadata(self, parameters: FormattingParameters,
                                    synthesis_metadata: Dict[str, Any],
                                    word_count: int) -> Dict[str, Any]:
        """Generate metadata about the formatting process"""
        return {
            'formatting_parameters': {
                'output_format': parameters.output_format.value,
                'target_length': parameters.target_length.value,
                'evidence_level': parameters.evidence_level.value
            },
            'output_metrics': {
                'final_word_count': word_count,
                'target_range': self.length_targets[parameters.target_length]
            },
            'synthesis_info': {
                'total_responses': synthesis_metadata.get('total_responses', 0),
                'avg_confidence': synthesis_metadata.get('avg_confidence', 0.0),
                'synthesis_strategy': synthesis_metadata.get('synthesis_strategy', 'unknown')
            }
        }

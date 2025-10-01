"""
Enhanced Agent Response Structure with Uncertainty Signaling
==========================================================

This module provides the enhanced agent response structure that incorporates
uncertainty signaling, allowing agents to communicate their confidence and
uncertainty about their responses.

Author: Myriad Cognitive Architecture Team
Version: 1.0 (Enhanced Agent Response)
Date: 2025-01-01
"""

from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, asdict
from enum import Enum
import json
import time

from .uncertainty_signals import UncertaintyAssessment, UncertaintyLevel, get_uncertainty_detector

class ResponseStatus(Enum):
    """Status of the agent response"""
    SUCCESS = "success"
    UNCERTAIN = "uncertain"
    CONFLICTING = "conflicting"
    PARTIAL = "partial"
    ERROR = "error"

@dataclass
class EnhancedAgentResponse:
    """
    Enhanced agent response structure with uncertainty signaling
    
    This structure allows agents to:
    - Provide their response data
    - Signal uncertainty and confidence
    - Indicate conflicting information
    - Suggest clarifications when needed
    """
    status: ResponseStatus
    data: Any
    confidence: float  # 0.0 to 1.0
    uncertainty_assessment: Optional[UncertaintyAssessment]
    metadata: Dict[str, Any]
    timestamp: float
    agent_name: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        result = asdict(self)
        
        # Convert uncertainty assessment to dict if present
        if self.uncertainty_assessment:
            result['uncertainty_assessment'] = asdict(self.uncertainty_assessment)
            # Convert enum values to strings
            result['uncertainty_assessment']['overall_uncertainty'] = self.uncertainty_assessment.overall_uncertainty.value
            
            # Convert uncertainty signals
            for signal in result['uncertainty_assessment']['uncertainty_signals']:
                signal['uncertainty_type'] = signal['uncertainty_type'].value
                signal['level'] = signal['level'].value
        
        # Convert status enum to string
        result['status'] = self.status.value
        
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EnhancedAgentResponse':
        """Create from dictionary"""
        # Convert status string back to enum
        if 'status' in data and isinstance(data['status'], str):
            data['status'] = ResponseStatus(data['status'])
        
        # Convert uncertainty assessment back to object
        if 'uncertainty_assessment' in data and data['uncertainty_assessment']:
            ua_data = data['uncertainty_assessment']
            
            # Convert overall uncertainty back to enum
            if 'overall_uncertainty' in ua_data and isinstance(ua_data['overall_uncertainty'], str):
                ua_data['overall_uncertainty'] = UncertaintyLevel(ua_data['overall_uncertainty'])
            
            # Convert uncertainty signals back to objects
            from .uncertainty_signals import UncertaintySignal, UncertaintyType
            converted_signals = []
            for signal_data in ua_data.get('uncertainty_signals', []):
                if 'uncertainty_type' in signal_data and isinstance(signal_data['uncertainty_type'], str):
                    signal_data['uncertainty_type'] = UncertaintyType(signal_data['uncertainty_type'])
                if 'level' in signal_data and isinstance(signal_data['level'], str):
                    signal_data['level'] = UncertaintyLevel(signal_data['level'])
                converted_signals.append(UncertaintySignal(**signal_data))
            
            ua_data['uncertainty_signals'] = converted_signals
            data['uncertainty_assessment'] = UncertaintyAssessment(**ua_data)
        
        return cls(**data)

class ResponseEnhancer:
    """
    Enhances standard agent responses with uncertainty signaling
    
    This class takes standard agent responses and enhances them with
    uncertainty assessment and appropriate status indicators.
    """
    
    def __init__(self):
        """Initialize the response enhancer"""
        self.uncertainty_detector = get_uncertainty_detector()
    
    def enhance_response(self, standard_response: Dict[str, Any], 
                        agent_name: str = "unknown") -> EnhancedAgentResponse:
        """
        Enhance a standard agent response with uncertainty signaling
        
        Args:
            standard_response: The standard response from an agent
            agent_name: Name of the agent providing the response
            
        Returns:
            EnhancedAgentResponse with uncertainty assessment
        """
        # Extract basic information
        status = self._extract_status(standard_response)
        data = self._extract_data(standard_response)
        confidence = self._extract_confidence(standard_response)
        metadata = self._extract_metadata(standard_response)
        
        # Assess uncertainty
        uncertainty_assessment = self.uncertainty_detector.assess_uncertainty(
            standard_response, agent_name
        )
        
        # Adjust status based on uncertainty
        if uncertainty_assessment.overall_uncertainty in [UncertaintyLevel.HIGH, UncertaintyLevel.VERY_HIGH]:
            if uncertainty_assessment.recommended_action in ["clarify", "research"]:
                status = ResponseStatus.UNCERTAIN
            elif uncertainty_assessment.recommended_action == "decline":
                status = ResponseStatus.ERROR
        
        # Adjust confidence based on uncertainty assessment
        if uncertainty_assessment.overall_uncertainty != UncertaintyLevel.VERY_LOW:
            # Reduce confidence based on uncertainty level
            uncertainty_factor = uncertainty_assessment.overall_uncertainty.value
            adjusted_confidence = confidence * (1.0 - uncertainty_factor * 0.5)
            confidence = max(0.1, adjusted_confidence)  # Ensure minimum confidence
        
        # Add uncertainty information to metadata
        metadata['uncertainty_detected'] = uncertainty_assessment.overall_uncertainty != UncertaintyLevel.VERY_LOW
        metadata['recommended_action'] = uncertainty_assessment.recommended_action
        metadata['uncertainty_signal_count'] = len(uncertainty_assessment.uncertainty_signals)
        
        return EnhancedAgentResponse(
            status=status,
            data=data,
            confidence=confidence,
            uncertainty_assessment=uncertainty_assessment,
            metadata=metadata,
            timestamp=time.time(),
            agent_name=agent_name
        )
    
    def _extract_status(self, response: Dict[str, Any]) -> ResponseStatus:
        """Extract status from standard response"""
        if 'status' in response:
            status_str = response['status'].lower()
            if status_str == 'success':
                return ResponseStatus.SUCCESS
            elif status_str in ['error', 'failed']:
                return ResponseStatus.ERROR
            elif status_str in ['partial', 'incomplete']:
                return ResponseStatus.PARTIAL
        
        # Default to success if no explicit status
        return ResponseStatus.SUCCESS
    
    def _extract_data(self, response: Dict[str, Any]) -> Any:
        """Extract data from standard response"""
        # Common data fields in agent responses
        for field in ['data', 'response', 'content', 'result', 'answer']:
            if field in response:
                return response[field]
        
        # If no specific data field, return the entire response
        return response
    
    def _extract_confidence(self, response: Dict[str, Any]) -> float:
        """Extract confidence from standard response"""
        if 'confidence' in response:
            return float(response['confidence'])
        
        # Try to infer confidence from other indicators
        if 'status' in response and response['status'].lower() == 'success':
            return 0.8  # Default confidence for successful responses
        else:
            return 0.5  # Neutral confidence
    
    def _extract_metadata(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Extract metadata from standard response"""
        metadata = {}
        
        # Common metadata fields
        for field in ['metadata', 'context', 'source', 'references']:
            if field in response:
                metadata[field] = response[field]
        
        # Add processing information
        metadata['enhanced'] = True
        metadata['enhancement_timestamp'] = time.time()
        
        return metadata


# Global response enhancer instance
response_enhancer = ResponseEnhancer()


def get_response_enhancer() -> ResponseEnhancer:
    """Get the global response enhancer instance"""
    return response_enhancer


def create_enhanced_response(standard_response: Dict[str, Any], 
                           agent_name: str = "unknown") -> EnhancedAgentResponse:
    """
    Convenience function to create an enhanced response from a standard response
    
    Args:
        standard_response: The standard response from an agent
        agent_name: Name of the agent providing the response
        
    Returns:
        EnhancedAgentResponse with uncertainty assessment
    """
    enhancer = get_response_enhancer()
    return enhancer.enhance_response(standard_response, agent_name)
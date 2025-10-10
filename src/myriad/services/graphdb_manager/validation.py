"""
Graph Schema Validation Module
Validates node and relationship properties before creation/update

This module ensures data integrity by validating properties against the
defined Neo4j graph schema before operations are executed.
"""

from typing import Dict, Tuple, Optional
from datetime import datetime
import re

class ValidationError(Exception):
    """Raised when validation fails"""
    pass

def validate_agent_properties(properties: Dict) -> Tuple[bool, Optional[str]]:
    """
    Validate agent node properties against schema requirements
    
    Args:
        properties: Dictionary of agent properties
        
    Returns:
        (is_valid, error_message) - True with None if valid, False with error message if invalid
    """
    required_fields = ['name', 'type', 'endpoint']
    
    # Check required fields
    for field in required_fields:
        if field not in properties or not properties[field]:
            return False, f"Missing required field: {field}"
    
    # Validate agent type
    valid_types = ['static', 'dynamic']
    if properties['type'] not in valid_types:
        return False, f"Invalid agent type: '{properties['type']}'. Must be one of {valid_types}"
    
    # Validate endpoint URL
    endpoint = properties['endpoint']
    if not (endpoint.startswith('http://') or endpoint.startswith('https://')):
        return False, f"Invalid endpoint URL: '{endpoint}'. Must start with http:// or https://"
    
    # Validate port if provided
    if 'port' in properties and properties['port'] is not None:
        try:
            port = int(properties['port'])
            if not (1 <= port <= 65535):
                return False, f"Invalid port number: {port}. Must be 1-65535"
        except (ValueError, TypeError):
            return False, f"Port must be an integer: {properties['port']}"
    
    # Validate status if provided
    if 'status' in properties and properties['status'] is not None:
        valid_statuses = ['active', 'inactive', 'unhealthy']
        if properties['status'] not in valid_statuses:
            return False, f"Invalid status: '{properties['status']}'. Must be one of {valid_statuses}"
    
    # Validate name format (no special characters except underscore and hyphen)
    name = properties['name']
    if not re.match(r'^[a-zA-Z0-9_-]+$', name):
        return False, f"Invalid agent name: '{name}'. Only alphanumeric, underscore, and hyphen allowed"
    
    return True, None

def validate_concept_properties(properties: Dict) -> Tuple[bool, Optional[str]]:
    """
    Validate concept node properties against schema requirements
    
    Args:
        properties: Dictionary of concept properties
        
    Returns:
        (is_valid, error_message)
    """
    # Check required fields
    if 'name' not in properties or not properties['name']:
        return False, "Missing required field: name"
    
    # Ensure name is lowercase
    name = properties['name']
    if name != name.lower():
        return False, f"Concept name must be lowercase: '{name}' should be '{name.lower()}'"
    
    # Validate name format (lowercase alphanumeric, underscore, hyphen)
    if not re.match(r'^[a-z0-9_-]+$', name):
        return False, f"Invalid concept name: '{name}'. Only lowercase alphanumeric, underscore, and hyphen allowed"
    
    # Validate complexity if provided
    if 'complexity' in properties and properties['complexity'] is not None:
        try:
            complexity = float(properties['complexity'])
            if not (0.0 <= complexity <= 1.0):
                return False, f"Complexity must be 0.0-1.0, got: {complexity}"
        except (ValueError, TypeError):
            return False, f"Complexity must be a number: {properties['complexity']}"
    
    # Validate category if provided
    if 'category' in properties and properties['category']:
        category = properties['category']
        if not re.match(r'^[a-zA-Z0-9_ -]+$', category):
            return False, f"Invalid category format: '{category}'"
    
    return True, None

def validate_region_properties(properties: Dict) -> Tuple[bool, Optional[str]]:
    """
    Validate region node properties
    
    Args:
        properties: Dictionary of region properties
        
    Returns:
        (is_valid, error_message)
    """
    # Check required fields
    if 'name' not in properties or not properties['name']:
        return False, "Missing required field: name"
    
    # Validate name format
    name = properties['name']
    if not re.match(r'^[a-zA-Z0-9_ -]+$', name):
        return False, f"Invalid region name: '{name}'"
    
    return True, None

def validate_hebbian_relationship(properties: Dict) -> Tuple[bool, Optional[str]]:
    """
    Validate HANDLES_CONCEPT relationship properties (Hebbian learning)
    
    Args:
        properties: Dictionary of relationship properties
        
    Returns:
        (is_valid, error_message)
    """
    # Validate weight
    if 'weight' in properties and properties['weight'] is not None:
        try:
            weight = float(properties['weight'])
            if not (0.0 <= weight <= 1.0):
                return False, f"Weight must be 0.0-1.0, got: {weight}"
        except (ValueError, TypeError):
            return False, f"Weight must be a number: {properties['weight']}"
    
    # Validate counts (must be non-negative integers)
    for count_field in ['usage_count', 'success_count', 'failure_count']:
        if count_field in properties and properties[count_field] is not None:
            try:
                count = int(properties[count_field])
                if count < 0:
                    return False, f"{count_field} cannot be negative: {count}"
            except (ValueError, TypeError):
                return False, f"{count_field} must be an integer: {properties[count_field]}"
    
    # Validate success_rate
    if 'success_rate' in properties and properties['success_rate'] is not None:
        try:
            success_rate = float(properties['success_rate'])
            if not (0.0 <= success_rate <= 1.0):
                return False, f"Success rate must be 0.0-1.0, got: {success_rate}"
        except (ValueError, TypeError):
            return False, f"Success rate must be a number: {properties['success_rate']}"
    
    # Validate decay_rate
    if 'decay_rate' in properties and properties['decay_rate'] is not None:
        try:
            decay_rate = float(properties['decay_rate'])
            if not (0.0 <= decay_rate <= 1.0):
                return False, f"Decay rate must be 0.0-1.0, got: {decay_rate}"
        except (ValueError, TypeError):
            return False, f"Decay rate must be a number: {properties['decay_rate']}"
    
    # Validate logical consistency
    if all(k in properties for k in ['usage_count', 'success_count', 'failure_count']):
        usage = int(properties['usage_count'])
        success = int(properties['success_count'])
        failure = int(properties['failure_count'])
        
        if success + failure != usage:
            return False, f"Inconsistent counts: success({success}) + failure({failure}) ≠ usage({usage})"
    
    return True, None

def sanitize_agent_properties(properties: Dict) -> Dict:
    """
    Sanitize and set defaults for agent properties
    
    Args:
        properties: Raw agent properties
        
    Returns:
        Sanitized properties with defaults applied
    """
    sanitized = properties.copy()
    
    # Set default status
    if 'status' not in sanitized or sanitized['status'] is None:
        sanitized['status'] = 'active'
    
    # Set created_at if not present
    if 'created_at' not in sanitized:
        sanitized['created_at'] = int(datetime.now().timestamp() * 1000)
    
    # Trim whitespace from string fields
    for field in ['name', 'type', 'endpoint', 'container_name', 'template', 'description']:
        if field in sanitized and isinstance(sanitized[field], str):
            sanitized[field] = sanitized[field].strip()
    
    return sanitized

def sanitize_concept_properties(properties: Dict) -> Dict:
    """
    Sanitize and set defaults for concept properties
    
    Args:
        properties: Raw concept properties
        
    Returns:
        Sanitized properties with defaults applied
    """
    sanitized = properties.copy()
    
    # Ensure lowercase name
    if 'name' in sanitized:
        sanitized['name'] = sanitized['name'].lower().strip()
    
    # Set created_at if not present
    if 'created_at' not in sanitized:
        sanitized['created_at'] = int(datetime.now().timestamp() * 1000)
    
    # Set last_updated to match created_at if not present
    if 'last_updated' not in sanitized:
        sanitized['last_updated'] = sanitized['created_at']
    
    # Set default complexity
    if 'complexity' not in sanitized or sanitized['complexity'] is None:
        sanitized['complexity'] = 0.5
    
    # Trim whitespace from string fields
    for field in ['name', 'primary_definition', 'category']:
        if field in sanitized and isinstance(sanitized[field], str):
            sanitized[field] = sanitized[field].strip()
    
    return sanitized

def sanitize_region_properties(properties: Dict) -> Dict:
    """
    Sanitize and set defaults for region properties
    
    Args:
        properties: Raw region properties
        
    Returns:
        Sanitized properties with defaults applied
    """
    sanitized = properties.copy()
    
    # Set created_at if not present
    if 'created_at' not in sanitized:
        sanitized['created_at'] = int(datetime.now().timestamp() * 1000)
    
    # Trim whitespace
    for field in ['name', 'description']:
        if field in sanitized and isinstance(sanitized[field], str):
            sanitized[field] = sanitized[field].strip()
    
    return sanitized

def sanitize_hebbian_relationship(properties: Dict) -> Dict:
    """
    Sanitize and set defaults for Hebbian learning relationship properties
    
    Args:
        properties: Raw relationship properties
        
    Returns:
        Sanitized properties with defaults applied
    """
    sanitized = properties.copy()
    
    # Set Hebbian defaults
    defaults = {
        'weight': 0.5,
        'usage_count': 0,
        'success_count': 0,
        'failure_count': 0,
        'success_rate': 0.5,
        'decay_rate': 0.01,
        'last_updated': int(datetime.now().timestamp() * 1000),
        'last_used': int(datetime.now().timestamp() * 1000)
    }
    
    for key, value in defaults.items():
        if key not in sanitized or sanitized[key] is None:
            sanitized[key] = value
    
    # Calculate success_rate if counts are present
    if 'usage_count' in sanitized and sanitized['usage_count'] > 0:
        success = sanitized.get('success_count', 0)
        usage = sanitized['usage_count']
        sanitized['success_rate'] = float(success) / float(usage)
    
    return sanitized

def validate_and_sanitize(label: str, properties: Dict) -> Tuple[bool, Optional[str], Dict]:
    """
    Convenience function to validate and sanitize in one call
    
    Args:
        label: Node label ('Agent', 'Concept', 'Region') or relationship type
        properties: Properties to validate and sanitize
        
    Returns:
        (is_valid, error_message, sanitized_properties)
    """
    if label == 'Agent':
        is_valid, error = validate_agent_properties(properties)
        if not is_valid:
            return False, error, properties
        return True, None, sanitize_agent_properties(properties)
    
    elif label == 'Concept':
        is_valid, error = validate_concept_properties(properties)
        if not is_valid:
            return False, error, properties
        return True, None, sanitize_concept_properties(properties)
    
    elif label == 'Region':
        is_valid, error = validate_region_properties(properties)
        if not is_valid:
            return False, error, properties
        return True, None, sanitize_region_properties(properties)
    
    elif label == 'HANDLES_CONCEPT':
        is_valid, error = validate_hebbian_relationship(properties)
        if not is_valid:
            return False, error, properties
        return True, None, sanitize_hebbian_relationship(properties)
    
    else:
        # Unknown label - pass through without validation
        return True, None, properties
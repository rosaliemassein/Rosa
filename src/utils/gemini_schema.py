"""
Utility to convert Pydantic models to Gemini-compatible schemas.
Removes unsupported fields like 'additionalProperties' and inlines $refs.
"""

from typing import Any, Dict
from pydantic import BaseModel


def resolve_refs(schema: Dict[str, Any], defs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Recursively resolve $ref references by inlining definitions.
    
    Args:
        schema: JSON schema dict or sub-schema
        defs: The $defs dictionary from the root schema
    
    Returns:
        Schema with all $refs resolved inline
    """
    if not isinstance(schema, dict):
        return schema
    
    # If this is a $ref, replace it with the actual definition
    if '$ref' in schema:
        ref_path = schema['$ref']
        # Extract the definition name (e.g., "#/$defs/Slide" -> "Slide")
        def_name = ref_path.split('/')[-1]
        if def_name in defs:
            # Recursively resolve the referenced definition
            return resolve_refs(defs[def_name].copy(), defs)
        return schema
    
    # Recursively process all nested schemas
    resolved = {}
    for key, value in schema.items():
        if isinstance(value, dict):
            resolved[key] = resolve_refs(value, defs)
        elif isinstance(value, list):
            resolved[key] = [
                resolve_refs(item, defs) if isinstance(item, dict) else item
                for item in value
            ]
        else:
            resolved[key] = value
    
    return resolved


def clean_schema_for_gemini(schema: Dict[str, Any]) -> Dict[str, Any]:
    """
    Recursively remove/transform fields that Gemini API doesn't support.
    
    Handles:
    - Removing unsupported fields (additionalProperties, title, default, etc.)
    - Converting anyOf patterns from Optional types to nullable types
    - Validating required fields match defined properties
    
    Args:
        schema: JSON schema dict (already with $refs resolved)
    
    Returns:
        Cleaned schema compatible with Gemini API
    """
    if not isinstance(schema, dict):
        return schema
    
    # Handle anyOf pattern from Pydantic Optional types:
    #   {"anyOf": [{"type": "string"}, {"type": "null"}]}  →  {"type": "string", "nullable": true}
    if 'anyOf' in schema:
        any_of = schema['anyOf']
        non_null = [s for s in any_of if not (isinstance(s, dict) and s.get('type') == 'null')]
        if non_null:
            result = clean_schema_for_gemini(non_null[0])
            result['nullable'] = True
            return result
    
    cleaned = {}
    
    for key, value in schema.items():
        # Skip fields that Gemini doesn't accept
        if key in ('additionalProperties', 'title', 'default', 'examples', '$defs'):
            continue
        
        # Recursively clean nested dicts
        if isinstance(value, dict):
            cleaned[key] = clean_schema_for_gemini(value)
        # Recursively clean lists
        elif isinstance(value, list):
            cleaned[key] = [
                clean_schema_for_gemini(item) if isinstance(item, dict) else item
                for item in value
            ]
        else:
            cleaned[key] = value
    
    # Safety: ensure required fields actually exist in properties
    if 'required' in cleaned and 'properties' in cleaned:
        cleaned['required'] = [
            r for r in cleaned['required']
            if r in cleaned['properties']
        ]
        # Remove empty required arrays
        if not cleaned['required']:
            del cleaned['required']
    
    return cleaned


def get_gemini_schema(model: type[BaseModel]) -> Dict[str, Any]:
    """
    Get a Gemini-compatible schema from a Pydantic model.
    
    This function:
    1. Gets the full JSON schema from Pydantic
    2. Resolves all $ref references by inlining definitions
    3. Removes unsupported fields like additionalProperties
    
    Args:
        model: Pydantic model class
    
    Returns:
        Clean schema dict ready for Gemini API
    """
    full_schema = model.model_json_schema()
    
    # Extract $defs if present
    defs = full_schema.pop('$defs', {})
    
    # Resolve all $ref references
    resolved_schema = resolve_refs(full_schema, defs)
    
    # Clean up unsupported fields
    return clean_schema_for_gemini(resolved_schema)

""" Module for generating structured form request payload """
import json

def create_request_payload(entries, include_comments: bool = True):
    """
    Generate a structured dictionary-like payload for form submission from given entries.
    
    Parameters:
        entries (list): List of form field entries.
        include_comments (bool): Whether to include comments explaining each field.
    
    Returns:
        str: Formatted string representation of the payload.
    """
    payload = "{\n"
    field_counter = 0

    for field in entries:
        # Add explanatory comments if enabled
        if include_comments:
            payload += f"    # Field: {field['container_name']}{(': ' + field['name']) if field.get('name') else ''}{' (required)' * field['required']}\n"
            if field.get('options'):
                payload += f"    #   Choices: {field['options']}\n"
            else:
                payload += f"    #   Input Type: {resolve_input_type(field['type'])}\n"
        
        # Generate the field identifier
        field_counter += 1
        field_value = json.dumps(field.get("default_value", ""), ensure_ascii=False)
        field_id = f'entry.{field["id"]}' if field.get("type") != "required" else field["id"]

        payload += f'    "{field_id}": {field_value}'
        payload += f"{(field_counter < len(entries)) * ','}\n"

    payload += "}"
    return payload

def resolve_input_type(field_type):
    """
    Get the expected input format or type for a specific field type.

    Parameters:
        field_type (int): Numeric identifier of the field type.

    Returns:
        str: Description of the expected input format or value type.
    """
    field_type_mapping = {
        0: "Short text",
        1: "Long text",
        2: "Single choice",
        3: "Dropdown menu",
        4: "Multiple selections",
        5: "Scale value",
        7: "Grid selection",
        9: "Date (YYYY-MM-DD)",
        10: "Time (HH:MM in 24-hour format)",
    }
    return field_type_mapping.get(field_type, "Free-text input")

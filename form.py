"""
Automated Extraction of Google Form Entries
Version 3:
    - Capable of handling a wide range of Google form field types.
    - Limited to single-page forms only.
    - Does not support file uploads due to authentication requirements.
Date: 2024-12-26
"""

import argparse
import json
import re
import requests
import generator

# Constants
DATA_IDENTIFIER = "FB_PUBLIC_LOAD_DATA_"
MULTI_PAGE_TYPE = 8
PLACEHOLDER_TEXT = "SAMPLE TEXT"

""" ------- Utility Functions ------- """

def convert_to_response_url(original_url: str):
    """
    Convert the standard Google Form URL to its response submission counterpart.
    """
    response_url = original_url.replace('/viewform', '/formResponse')
    if not response_url.endswith('/formResponse'):
        response_url = response_url.rstrip('/') + '/formResponse'
    return response_url

def extract_js_variable(variable_name: str, html_content: str):
    """
    Extract a variable value from JavaScript embedded in an HTML page.
    """
    regex = re.compile(rf'var\s{variable_name}\s=\s(.*?);')
    match = regex.search(html_content)
    if match:
        return json.loads(match.group(1))
    return None

def fetch_form_metadata(form_url: str):
    """
    Retrieve metadata from a Google Form by accessing its public data.
    """
    try:
        response = requests.get(form_url, timeout=10)
        response.raise_for_status()
        return extract_js_variable(DATA_IDENTIFIER, response.text)
    except requests.RequestException as e:
        print(f"Error: Unable to retrieve form data. Details: {e}")
        return None

""" ------- Main Logic ------- """

def analyze_form_structure(url: str, include_required_only=False):
    """
    Parse and structure the form fields from its metadata.
    """
    url = convert_to_response_url(url)
    metadata = fetch_form_metadata(url)

    if not metadata or not metadata[1] or not metadata[1][1]:
        print("Error: Form data could not be processed. Login might be required.")
        return None

    def process_entry(entry):
        """
        Extract key details for each form field entry.
        """
        field_name = entry[1]
        field_type = entry[3]
        field_data = []

        for subfield in entry[4]:
            details = {
                "id": subfield[0],
                "label": field_name,
                "type": field_type,
                "required": subfield[2] == 1,
                "options": [opt[0] or PLACEHOLDER_TEXT for opt in subfield[1]] if subfield[1] else None,
                "subfield_label": ' - '.join(subfield[3]) if len(subfield) > 3 and subfield[3] else None,
            }
            if include_required_only and not details['required']:
                continue
            field_data.append(details)
        return field_data

    entries = []
    page_count = 0
    for item in metadata[1][1]:
        if item[3] == MULTI_PAGE_TYPE:
            page_count += 1
            continue
        entries.extend(process_entry(item))

    # Add email collection if applicable
    if metadata[1][10][6] > 1:
        entries.append({
            "id": "emailAddress",
            "label": "Email Address",
            "type": "email",
            "required": True,
            "options": None,
        })

    # Add page history for multi-page forms
    if page_count > 0:
        entries.append({
            "id": "pageHistory",
            "label": "Page History",
            "type": "navigation",
            "required": False,
            "options": None,
            "default_value": ','.join(map(str, range(page_count + 1))),
        })

    return entries

def populate_form_fields(entries, data_generator):
    """
    Fill form fields using the specified data generation logic.
    """
    for entry in entries:
        # Skip if already populated
        if entry.get('default_value'):
            continue
        
        # Default to an empty list if options are not provided
        options = entry.get('options', [])
        if options is None:
            options = []

        # Remove placeholder text if present
        if PLACEHOLDER_TEXT in options:
            options.remove(PLACEHOLDER_TEXT)
        
        # Generate random value based on field type
        entry['default_value'] = data_generator(
            entry['type'], entry['id'], options,
            is_required=entry['required'], 
            entry_label=entry['label']  
        )
        
    return entries




def generate_request_payload(url, output="console", include_comments=True, data_generator=None):
    """
    Build the request payload for form submission.
    """
    # Analyze the form structure without filtering required-only fields
    fields = analyze_form_structure(url, include_required_only=False)  # Always include all fields
    if data_generator:
        fields = populate_form_fields(fields, data_generator)
    if not fields:
        return None
    payload = generator.create_request_payload(fields, include_comments)  # Pass only necessary args
    if output == "console":
        print(payload)
    elif output == "return":
        return payload
    else:
        with open(output, "w", encoding="utf-8") as file:
            file.write(payload)
            print(f"Output saved to {output}")
    return None




""" ------- Entry Point ------- """

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Google Form Automation Tool")
    parser.add_argument("url", help="URL of the Google Form")
    parser.add_argument("-o", "--output", default="console", help="Output destination (default: console)")
    parser.add_argument("-nc", "--no-comments", action="store_true", help="Exclude comments in output")
    args = parser.parse_args()

    # Removed the include_required_only argument here
    generate_request_payload(
        args.url,
        output=args.output,
        include_comments=not args.no_comments,  # Just pass the necessary arguments
    )

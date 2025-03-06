import os
import re
import json
from typing import List, Dict
from file_processing import process_file
from gpt_processing import extract_items_with_gpt
from gpt_processing import check_reimbursement

def process_invoices(file_path):
    filename = os.path.basename(file_path)  # Get only filename
    employee_id = extract_id_from_filename(filename)  #Extract ID from the filename

    if not employee_id:
        print(f"Skipping {filename} - Invalid format")
        return "Invalid format."  # Skip files with an incorrect format

    extracted_text = process_file(file_path)  # Extract text from file
    extracted_data = extract_items_with_gpt(extracted_text, employee_id)  # Extract structured data from GPT
    
    is_json_items = is_valid_json(extracted_data)  #Validate if the items were extracted
    
    if(is_json_items):
        reinbursed_items = check_reimbursement(extracted_data)
        return reinbursed_items
    else:
        return "No items extracted."
    

def extract_id_from_filename(filename):
    """Extract the ID from a filename formatted as ID_mmddyyyy.extension."""
    match = re.match(r"^([A-Za-z0-9]+)_\d{8}\.[a-z]+$", filename)
    if match:
        return match.group(1)  # The ID part
    return None  # Return None if the pattern doesn't match

def is_valid_json(json_string):
    """Check if a string is a valid JSON format."""
    try:
        json.loads(json_string)  # Try to parse JSON
        return True
    except json.JSONDecodeError:
        return False  # Invalid JSON format

import os
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict
from invoice_processor import process_invoices
from generate_results import generate_results

# Define input folder and output file
folder_path = r"C:\Users\LauraMartinez\OneDrive - Accelirate, Inc\Hackaton\TestFolder"
output_file = "results.xlsx"
exceptions_files = f"exceptions_{datetime.today().strftime('%m%d%Y')}.txt"

# Process invoices from the folder
def get_invoices(folder_path: str) -> List[Dict]:
    """
    Processes invoices from a given folder.
    - Lists all PDF and image files.
    - Extracts text for each file.
    - Calls GPT extraction to structure the data.
    - Returns structured results as a list of dictionaries.
    - Validates extracted items against company policy
    """
    valid_extensions = {".pdf", ".jpg", ".jpeg", ".png"}
    error_msgs = ["No items extracted", "Unsupported file format", "Invalid format"]
    results = []

    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        filename = os.path.basename(file_path)
        if os.path.isfile(file_path) and os.path.splitext(file)[1].lower() in valid_extensions:
            print(f"Processing {file}...")            
            results = process_invoices(file_path)  #Process file
            print(results)
            if all(msg not in results for msg in error_msgs):
                try:
                    json_results = json.loads(results)
                    generate_results(json_results, output_file) #Send data to output destination
                except Exception as e:
                    print(f"Error filling the report, file in process {filename}: {e}")
            elif not os.path.exists(exceptions_files):
                with open(exceptions_files, "w", encoding="utf-8") as file:
                    file.write(f"Invoices exception {datetime.today().strftime('%m%d%Y')}:\n")
            else:
                with open(exceptions_files, "a", encoding="utf-8") as file:
                    file.write(f"{filename}: {results}\n") 

    return results  # Return the processed results

# Run the function
invoice_data = get_invoices(folder_path)

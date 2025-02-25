import os
import pandas as pd
import requests
from typing import List, Dict

def ProcessInvoices(folder_path: str) -> List[Dict]:
    """
    Processes invoices from a given folder.
    - Lists all PDF and image files.
    - Calls ExtractData for each file.
    - Calls ValidateItems with the extracted data.
    - Returns validated results as a list of dictionaries.
    """
    valid_extensions = {".pdf", ".jpg", ".jpeg", ".png"}
    results = []
    
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        
        if os.path.isfile(file_path) and os.path.splitext(file)[1].lower() in valid_extensions:
            extracted_data = ExtractData(file_path)  # Call extraction function (Uncomment when implemented)
            validated_data = ValidateItems(extracted_data)  # Call validation function (Uncomment when implemented)
            
            """
            Sample of date to test filling out the files
            validated_data = [
                {"item": "Milk", "quantity": 2, "price": 3.50},
                {"item": "Bread", "quantity": 1, "price": 2.00},
                {"item": "Eggs", "quantity": 12, "price": 0.25}
            ]"""

            for item in validated_data:  # Flattening item-level data
                item["source_file"] = file  # Adding source file info
                results.append(item)
    
    return results

def GenerateResults(results: List[Dict], output_file: str, api_url: str = None):
    """
    Saves results to a CSV or Excel file based on the file extension.
    Optionally, sends data to an API if an API URL is provided.
    """
    df = pd.DataFrame(results)
    
    if output_file.endswith(".csv"):
        df.to_csv(output_file, index=False)
    elif output_file.endswith(".xlsx"):
        df.to_excel(output_file, index=False)
    else:
        raise ValueError("Unsupported file format. Use .csv or .xlsx")
    
    if api_url:
        for record in results:
            response = requests.post(api_url, json=record)
            if response.status_code != 200:
                print(f"Failed to send data to API: {response.status_code} - {response.text}")
            else:
                print("Successfully sent data to API.")

# Example Usage
folder_path = r"C:\Users\LauraMartinez\OneDrive - Accelirate, Inc\Hackaton\TestFolder"
output_file = "results.xlsx"
api_url = ""  # Optional API URL

results = ProcessInvoices(folder_path)
GenerateResults(results, output_file, api_url)

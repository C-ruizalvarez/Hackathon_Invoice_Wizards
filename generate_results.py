import pandas as pd
import os
import requests
from openpyxl import load_workbook
from typing import List, Dict

def generate_results(results: List[Dict], output_file: str, api_url: str = None):
    """
    Appends results to an existing CSV or Excel file.
    If the file does not exist, it is created.
    Optionally, sends data to an API if an API URL is provided.
    """
    df = pd.DataFrame(results)
    
    file_exists = os.path.exists(output_file)

    if not file_exists:
        # Create new file
            df.to_excel(output_file, index=False, engine="openpyxl")
            
    elif output_file.endswith(".csv"):
        df.to_csv(output_file, mode="a" if file_exists else "w", header=not file_exists, index=False)

    elif output_file.endswith(".xlsx"):
        with pd.ExcelWriter(output_file, mode="a", engine="openpyxl", if_sheet_exists="overlay") as writer:
                df.to_excel(writer, index=False, header=False, startrow=writer.sheets["Sheet1"].max_row)
                
    else:
        raise ValueError("Unsupported file format. Use .csv or .xlsx")

    #Send data to API if a URL is provided
    if api_url:
        for record in results:
            response = requests.post(api_url, json=record)
            if response.status_code != 200:
                print(f"Failed to send data to API: {response.status_code} - {response.text}")
            else:
                print("Successfully sent data to API.")

    print(f" Data appended to {output_file}")

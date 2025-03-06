import openai
import os
from openai import OpenAI

# Load OpenAI API Key
openai.api_key = 'sk-652f9acf82b249829e44ce8431f666ce'
client = OpenAI(api_key='sk-652f9acf82b249829e44ce8431f666ce', base_url="https://api.deepseek.com")

def load_prompt(file):
    """Load the GPT prompt from an external text file."""
    prompt_file = os.path.join(os.path.dirname(__file__), file)
    with open(prompt_file, "r", encoding="utf-8") as f:
        return f.read()

def extract_items_with_gpt(text,employee_id):
    """Send extracted text to GPT-4 to get structured data."""
    # Load the prompt details from the text file
    prompt_template = load_prompt("Items prompt.txt")
    
    # Insert the actual receipt text and employee id into the prompt
    prompt = prompt_template.replace("{employee_id}", employee_id)
    prompt = prompt.replace("{receipt_text}", text)

    # Send the prompt to GPT
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "system", "content": "You are an accounting assistant responsible for extracting data from receipts to obtain the list of purchased items, the cost per item, and the total receipt cost"},
                  {"role": "user", "content": prompt}],
        temperature=0
    )

    return response.choices[0].message.content

def check_reimbursement(items):
    """Function to check reimbursement using GPT API"""
    # Load the prompt from details the text file
    reinburs_policy = load_prompt("Reinbursment policy.txt")
    reinburs_template = load_prompt("Reinbursment prompt.txt")

    # Insert the actual receipt text and employee id into the prompt
    prompt = reinburs_template.replace("{items}", items)

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "system", "content": reinburs_policy},
        {"role": "user", "content": prompt}],
        temperature=0.2
    )

    return response.choices[0].message.content

import openai
import os

# Load OpenAI API Key securely from environment variables
openai_client = openai.Client(api_key=os.getenv("OPENAI_API_KEY"))

def load_prompt(file):
    """Load the GPT prompt from an external text file."""
    prompt_file = os.path.join(os.path.dirname(__file__), file)
    with open(prompt_file, "r", encoding="utf-8") as f:
        return f.read()

def extract_items_with_gpt(text, employee_id):
    """Send extracted text to GPT-4 to get structured data."""
    # Load the prompt details from the text file
    prompt_template = load_prompt("Items prompt.txt")
    
    # Insert the actual receipt text and employee ID into the prompt
    prompt = prompt_template.replace("{employee_id}", employee_id)
    prompt = prompt.replace("{receipt_text}", text)

    # Send the prompt to OpenAI GPT
    response = openai_client.chat.completions.create(
        model="gpt-4",  # Change to "gpt-3.5-turbo" if needed
        messages=[
            {"role": "system", "content": "You are an accounting assistant responsible for extracting data from receipts to obtain the list of purchased items, the cost per item, and the total receipt cost."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )
    
    return response.choices[0].message.content

def check_reimbursement(items):
    """Function to check reimbursement using GPT API"""
    # Load the prompt from details the text file
    reinburs_policy = load_prompt("Reinbursment policy.txt")
    reinburs_template = load_prompt("Reinbursment prompt.txt")

    # Insert the actual receipt text into the prompt
    prompt = reinburs_template.replace("{items}", items)

    response = openai_client.chat.completions.create(
        model="gpt-4",  # Change to "gpt-3.5-turbo" if needed
        messages=[
            {"role": "system", "content": reinburs_policy},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )
    
    return response.choices[0].message.content

text="""Camilo's Chicken wings

Calle 24a # SSB - 40
Medellin Colombia

SALE

03/06/2025 08:37 AM

BATCH #:0737A

APPR #:425BC

TRACE #: 9

CASH

1 Big Spicy wing

1 Aguila Beer

1 Chicharron Spicy
3 Margarita

SUBTOTAL: $63.29
TAX: $6.33
TOTAL: $69.62

TIP:

$20.14

$3.00
$30.15
$10.00

TOTAL:

APPROVED
THANK YOU
CUSTOMER COPY"""

print(extract_items_with_gpt(text,"123456"))


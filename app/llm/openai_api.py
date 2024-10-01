import openai, streamlit as st
client = openai.OpenAI()
model = "gpt-4o"


from config.coa import coa_list

def get_coa(description):
    user_content = f"""
        Task: Identify the Chart of Account (COA) that best matches the provided Vendor Name from the given list.
        
        Instructions:
        
        Always return a COA that most closely matches the Vendor Name, even if it's not an exact match.
        Provide only the COA description.
        Do not include any labels like "COA" or "Vendor" 
        Vendor Name: "{description}"
        
        COA List: {coa_list}        
    """

    # Make the API call using the variable
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a model trained to link COA in the coa_list to Vendor name."},
            {"role": "user", "content": user_content}
        ]
    )

    result = response.choices[0].message.content.strip().split("\n")

    coa = result[0].strip()
    if "COA:" in coa:
        coa = coa.replace("COA:", "").strip()

    return coa


def get_vendor(description):
    user_content = f"""
           You will be provided with a transaction description. Your task is to extract two pieces of information:
           The vendor name, which is the name of the company or service in the description.

           Focus on the part of the description that typically follows the date or a person's name, and is often a recognizable brand or service name.

           Return the vendor name, without any labels like "Vendor Name" in your response. 

           ### Examples
           Description: "12/19/22 YUNLIANGCHIU AMEXFINEHOTELSRES -$200.00"
           Response: "Amex Fine Hotels"

           Description: "THEHARFORDMUTUALINSURANCECOMPANY BELAIR MD 1234-INS"
           Response: "Harford Mutual Insurance Company"

           Description: "CIRCLE K #20850 MORRISVILLE NC 5678-GAS"
           Response: "Circle K"

           Description: "HARRIS TEETER CHAPEL HILL NC 9012-GRO"
           Response: "Harris Teeter"

           Now, extract the vendor name from the following description:
           Description: "{description}"
       """

    # Make the API call using the variable
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a model trained to extract vendor names from descriptions."},
            {"role": "user", "content": user_content}
        ]
    )

    vendor_name = response.choices[0].message.content.strip()
    # st.write(f"{vendor_name}")
    return vendor_name


def get_vendor_information(vendor_name):
    prompt = f"Provide basic business information for the vendor '{vendor_name}'."

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a model trained to provide business information."},
            {"role": "user", "content": prompt}
        ]
    )

    # Assuming the API returns a structured response; otherwise, parse as needed
    business_info = response.choices[0].message.content.strip()
    return business_info


def get_journal_entry_cc(transaction):
    prompt = f"""
    I have this transaction {transaction} from a credit card statement that I need to record as journal entries. 
    Each transaction includes the date, description, and amount. Please provide the journal entries in a structured format 
    using the double-entry accounting method.  

    Ensure to clearly state the accounts involved in the debit and credit entries without additional explanations.
"""
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system",
                 "content": "You are a model trained to book journal entries like a professional accountant."},
                {"role": "user", "content": prompt}
            ]
        )

        # Assuming the API returns a structured response; otherwise, parse as needed
        journal_entry = response.choices[0].message.content.strip()

        # Split the journal entry into separate lines if necessary
        journal_entries = journal_entry.splitlines()
        return journal_entries

    except Exception as e:
        # Handle exceptions, e.g., API errors
        print(f"Error fetching journal entry: {e}")
        return None


def get_journal_entry_cc2(transaction):
    prompt = f"""
                I have this transaction {transaction} from a credit card statement that I need to record as journal entries. 
                
                please put them in one line using following format:
                Date, Description, amount, Debit, Credit. Here is an example:
                
                Date: 09/10/23, Description: BESTBUY purchase, amount: 31.16, Debit: Office Supplies Expense $31.16, Credit: Credit Card Payable $31.16
                
                If the amount is negative, keep them as negative. 
                
                Ensure to clearly state the accounts involved in the debit and credit entries without additional explanations.
            """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system",
                 "content": "You are a model trained to book journal entries like a professional accountant."},
                {"role": "user", "content": prompt}
            ]
        )

        # Assuming the API returns a structured response; otherwise, parse as needed
        journal_entry = response.choices[0].message.content.strip()

        # Split the journal entry into separate lines if necessary
        journal_entries = journal_entry.splitlines()
        return journal_entries

    except Exception as e:
        # Handle exceptions, e.g., API errors
        print(f"Error fetching journal entry: {e}")
        return None


def get_journal_entry_bank(transaction):
    prompt = f"""
    I have this transaction {transaction} from a bank statement that I need to record as journal entries. 

    please put them in one line using following format:
    Date, Description, amount, Debit, Credit. Here is an example:

    Date: 09/10/23, Description: BESTBUY purchase, amount: 31.16, Debit: Office Supplies Expense $31.16, Credit: Credit Card Payable $31.16

    If the amount is negative, keep them as negative. 

    Ensure to clearly state the accounts involved in the debit and credit entries without additional explanations.
"""
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system",
                 "content": "You are a model trained to book journal entries like a professional accountant."},
                {"role": "user", "content": prompt}
            ]
        )

        # Assuming the API returns a structured response; otherwise, parse as needed
        journal_entry = response.choices[0].message.content.strip()

        # Split the journal entry into separate lines if necessary
        journal_entries = journal_entry.splitlines()
        return journal_entries

    except Exception as e:
        # Handle exceptions, e.g., API errors
        print(f"Error fetching journal entry: {e}")
        return None

import openai, streamlit as st
client = openai.OpenAI()

from config.coa import coa_list

def return_coa(description):
    user_content = f"""
        You will be provided with a Vendor name. Your task is to find a Chart of Account (COA) in the given list closely associated with the vendor name. 

        Return the COA without any labels like "COA" in your response.
        
        The Vendor Name given to you is:
        Vendor Name: "{description}"
        
        The Chart of Account (COA) list is: {coa_list}
        
    """

    # Make the API call using the variable
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system", "content": "You are a model trained to extract COA from Vendor name."},
            {"role": "user", "content": user_content}
        ]
    )

    result = response.choices[0].message.content.strip().split("\n")

    coa = result[0].strip()
    if "COA:" in coa:
        coa = coa.replace("COA:", "").strip()

    return coa


def return_vendor(description):
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
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system", "content": "You are a model trained to extract vendor names from descriptions."},
            {"role": "user", "content": user_content}
        ]
    )

    vendor_name = response.choices[0].message.content.strip()
    # st.write(f"{vendor_name}")
    return vendor_name

import openai, streamlit as st
client = openai.OpenAI()


def return_vendor_and_coa(description):
    user_content = f"""
        You will be provided with a transaction description. Your task is to extract two pieces of information:
        1. The vendor name, which is the name of the company or entity mentioned in the description.
        2. The Chart of Accounts (COA), which is typically a code or identifier related to the transaction.

        Return the vendor name and COA separately, without any labels like "Vendor Name" or "COA" in your response.

        ### Examples
        Description: "THEHARFORDMUTUALINSURANCECOMPANY BELAIR MD 1234-INS"
        Response: "Harford Mutual Insurance Company, 1234-INS"

        Description: "CIRCLE K #20850 MORRISVILLE NC 5678-GAS"
        Response: "Circle K, 5678-GAS"

        Description: "HARRIS TEETER CHAPEL HILL NC 9012-GRO"
        Response: "Harris Teeter, 9012-GRO"

        Now, extract the vendor name and COA from the following description:
        Description: "{description}"
    """

    # Make the API call using the variable
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system", "content": "You are a model trained to extract vendor names and COA from descriptions."},
            {"role": "user", "content": user_content}
        ]
    )

    result = response.choices[0].message.content.strip().split("\n")

    st.write(result)

    vendor_name = result[0].strip()
    coa = result[0].strip()
    if "COA:" in coa:
        coa = coa.replace("COA:", "").strip()
    if "Vendor Name:" in vendor_name:
        vendor_name = vendor_name.replace("Vendor Name:", "").strip()

    return vendor_name, coa


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

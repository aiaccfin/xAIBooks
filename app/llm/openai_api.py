import openai, streamlit as st
client = openai.OpenAI()

def return_vendor(description):
    user_content = f"""
        Given a description, please extract the vendor name. The vendor name is the entity or company name mentioned in the description. Do not show "vendor name" these 2 words in response.
    
        ### Example
        Description: "THEHARFORDMUTUALINSURANCECOMPANY BELAIR MD"
        Vendor Name: "Harford Mutual Insurance Company"
    
        Description: "CIRCLE K #20850 MORRISVILLE NC"
        Vendor Name: "Circle K"
    
        Description: "HARRIS TEETER CHAPEL HILL NC"
        Vendor Name: "Harris Teeter"
    
        Now, extract the vendor name from the following description:
        Description: "{description}"
    """

    # Make the API call using the variable
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system",  "content": "You are a model trained to extract vendor names from descriptions."},
            {"role": "user",    "content": user_content}
        ]
    )

    vendor_name = response.choices[0].message.content.strip()
    # st.write(f"{vendor_name}")
    return vendor_name

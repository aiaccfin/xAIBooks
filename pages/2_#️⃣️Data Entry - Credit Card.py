import streamlit as st, re, pandas as pd

from app.db.mongo_db import collection_vendor
from app.utils import streamlit_components
streamlit_components.streamlit_ui('🦣 Dashboard for Accountant')

from streamlit_extras.stateful_button import button
from app.llm.openai_api import return_vendor, return_coa, return_vendor_information

from app.data_entry import email_processing, pdf_processing
# -----------------------------------------------------------------------------------------------------------
tab1, tab2= st.tabs(["Extract from Statement", "Manual Entry"])

with tab2: st.info('🏗️ under construction...')

with tab1:
    if button("Load Credit Card Statement?", key='key1'):
        with st.spinner('Extracting Credit Card Statement...'):

            pdf_path = "./data/bs/USA/Sample-Credit Card Statement-US/Credit Card-AmEx 91009-Tea Hill-2023/2023-01-09.pdf"
            extracted_data = pdf_processing.extract_pdf_lines(pdf_path)
            st.write(extracted_data)
        st.success('Credit Card Statement Extracted!')
        if button("Process for Vendor and COA?", key='key2'):
            with st.spinner('AI analyzing vendor and COA...'):
                from app.db import mongo_db
                transactions = []
                for entry in extracted_data:
                    text = entry['text']
                    match = re.match(r'(\d{2}/\d{2}/\d{2}) (.+) (-?\$\d{1,3}(?:,\d{3})*\.\d{2})$', text)

                    if match:
                        date, description, amount = match.groups()
                        amount = amount.replace('$', '')
                        amount = float(amount.replace(',', ''))
                        vendor_name  =     return_vendor(description)
                        COA = return_coa(vendor_name)

                        if not collection_vendor.find_one(vendor_name):
                            business_info = return_vendor_information(vendor_name)
                            mongo_db.save_vendor_information(vendor_name, business_info)

                        transactions.append({
                            'clientID':'CC888',
                            'date': date,
                            'description': description,
                            'amount': amount,
                            'vendor_name': vendor_name,
                            'COA': COA
                        })

                df = pd.DataFrame(transactions)
                df['vendor_name'] = df['vendor_name'].str.replace(r'^\s*Vendor Name:\s*', '',regex=True)  # Remove "Vendor Name:" prefix
                df['vendor_name'] = df['vendor_name'].str.replace(r'\*\*', '',regex=True)  # Remove Markdown-style bold formatting
                df['vendor_name'] = df['vendor_name'].str.replace(r'\"', '', regex=True)  # Remove extra quotation marks
                df['COA'] = df['COA'].str.replace(r'\"', '', regex=True)  # Remove extra quotation marks

                df = df.drop(columns=['description'])
                st.dataframe(df)

                mongo_db.save_to_cc(transactions)

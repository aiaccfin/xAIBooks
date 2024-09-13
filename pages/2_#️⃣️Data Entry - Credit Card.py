import streamlit as st
from streamlit_extras.stateful_button import button

import os, re, glob, pandas

from app.db.db_handler import PGHandler
from app.utils import streamlit_components
from app.llm.openai_api import return_vendor, return_coa, return_vendor_information
from app.data_entry import email_processing, pdf_processing

streamlit_components.streamlit_ui('🦣 Dashboard for Accountant')
pg_handler = PGHandler()
# -----------------------------------------------------------------------------------------------------------
tab1, tab2 = st.tabs(["Extract from Statement", "Manual Entry"])

with tab2: st.info('🏗️ under construction...')

with tab1:
    if button("Load Credit Card Statement?", key='key1'):
        with st.spinner('Extracting Credit Card Statement...'):

            folder_path = "./data/xaibooks/cc"

            pdf_files = glob.glob(os.path.join(folder_path, "*.pdf"))
            pdf_files.sort(key=os.path.getmtime, reverse=True)

            if pdf_files:
                pdf_path = pdf_files[0]  # The latest file
            else:
                print("No PDF files found.")

            extracted_data = pdf_processing.extract_pdf_lines(pdf_path)
            st.write(extracted_data)
        st.success('Credit Card Statement Extracted!')
        if button("Process for Vendor and COA?", key='key2'):
            with st.spinner('AI analyzing vendor and COA...'):
                transactions = []
                for entry in extracted_data:
                    text = entry['text']
                    match = re.match(r'(\d{2}/\d{2}/\d{2})\*? (.+) (-?\$\d{1,3}(?:,\d{3})*\.\d{2})$', text)

                    if match:
                        date, description, amount = match.groups()
                        amount = amount.replace('$', '')
                        amount = float(amount.replace(',', ''))
                        vendor_name = return_vendor(description)
                        COA = return_coa(vendor_name)

                        pg_handler.save_vendor_if_not_exists(vendor_name)

                        transactions.append({
                            'clientID': 'CC888',
                            'date': date,
                            'description': description,
                            'amount': amount,
                            'vendor_name': vendor_name,
                            'COA': COA
                        })

                df = pandas.DataFrame(transactions)
                df['vendor_name'] = df['vendor_name'].str.replace(r'^\s*Vendor Name:\s*', '',
                                                                  regex=True)  # Remove "Vendor Name:" prefix
                df['vendor_name'] = df['vendor_name'].str.replace(r'\*\*', '',
                                                                  regex=True)  # Remove Markdown-style bold formatting
                df['vendor_name'] = df['vendor_name'].str.replace(r'\"', '', regex=True)  # Remove extra quotation marks
                df['COA'] = df['COA'].str.replace(r'\"', '', regex=True)  # Remove extra quotation marks

                df = df.drop(columns=['description'])
                st.dataframe(df)

                pg_handler.save_cc_postgres(transactions)

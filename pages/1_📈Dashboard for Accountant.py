import streamlit as st, re, pandas as pd
from streamlit_extras.stateful_button import button
from app.utils import streamlit_components
from app.llm.openai_api import return_vendor, return_coa

streamlit_components.streamlit_ui('🦣 Dashboard for Accountant')

from app.data_entry import email_processing, pdf_processing
from app.db import mongo_db
# -----------------------------------------------------------------------------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Data Entry: CC", "Data Entry: Bank Statement", "Data Entry: Email", "Data Entry: Manual", "DB Structure"])

with tab3:
    if button("Extract from Email", key="button3"):    email_processing.email_extraction()

with tab1:
    if button("CC ?", key="button1"):
        pdf_path = "./data/bs/USA/Sample-Credit Card Statement-US/Credit Card-AmEx 91009-Tea Hill-2023/2023-01-09.pdf"
        extracted_data = pdf_processing.extract_pdf_lines(pdf_path)
        st.write(extracted_data)

        if button("Vendor ?", key="button12"):
            transactions = []
            for entry in extracted_data:
                text = entry['text']
                match = re.match(r'(\d{2}/\d{2}/\d{2}) (.+) (-?\$\d{1,3}(?:,\d{3})*\.\d{2})$', text)

                if match:
                    date, description, amount = match.groups()
                    amount = amount.replace('$', '')
                    amount = float(amount.replace(',', ''))
                    vendor_name  =     return_vendor(description)

                    transactions.append({
                        'clientID':'CC888',
                        'date': date,
                        'description': description,
                        'amount': amount,
                        'vendor_name': vendor_name
                    })

            df = pd.DataFrame(transactions)
            df['vendor_name'] = df['vendor_name'].str.replace(r'^\s*Vendor Name:\s*', '',regex=True)  # Remove "Vendor Name:" prefix
            df['vendor_name'] = df['vendor_name'].str.replace(r'\*\*', '',regex=True)  # Remove Markdown-style bold formatting
            df['vendor_name'] = df['vendor_name'].str.replace(r'\"', '', regex=True)  # Remove extra quotation marks

            df = df.drop(columns=['description'])
            st.dataframe(df)

            mongo_db.save_to_cc(transactions)

            if button("COA ?", key="button13"):
                for transaction in transactions:
                    vendor_name = transaction.get('vendor_name')
                    coa  =     return_coa(vendor_name)
                    transaction['coa'] = coa

                df = pd.DataFrame(transactions)
                df = df.drop(columns=['description', '_id'])
                st.dataframe(df)

                mongo_db.save_to_cc(transactions)

import streamlit as st, re
from streamlit_extras.stateful_button import button
from app.utils import streamlit_components

streamlit_components.streamlit_ui('🦣 Dashboard for Accountant')

from app.data_entry import email_processing, pdf_processing
from app.db import mongo_db
# -----------------------------------------------------------------------------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Data Entry: Bank Statement", "Data Entry: Receipt", "Data Entry: Email", "Data Entry: Manual", "DB Structure"])

with tab3:
    if button("Extract from Email", key="button3"):    email_processing.email_extraction()

with tab1:
    if button("extract PDF?", key="button1"):
        # Example usage
        pdf_path = "./data/bs/USA/Sample-Bank Statement-US/Bank Statement-BOA Checking (4760)-Tea Hill-20230101-20231231/eStmt_2023-02-28.pdf"  # Path to your PDF file
        extracted_data = pdf_processing.extract_pdf_lines(pdf_path)
        # print(extracted_data)  # Print extracted data to see the format
        st.write(extracted_data)  # Print extracted data to see the format

        if button("Regex?", key="button12"):
            transactions = []
            for entry in extracted_data:
                text = entry['text']
                # Regex to match transaction lines (e.g., date and amount at the end)
                # match = re.match(r'(\d{2}/\d{2}/\d{2}) (.+) (\d+,\d+\.\d{2})$', text)
                match = re.match(r'(\d{2}/\d{2}/\d{2}) (.+) (-?\d+,\d+\.\d{2})$', text)

                if match:
                    date, description, amount = match.groups()
                    amount = float(amount.replace(',', ''))
                    transactions.append({
                        'clientID':'C101',
                        'date': date,
                        'description': description,
                        'amount': amount
                    })

            mongo_db.save_to_mongodb(transactions)

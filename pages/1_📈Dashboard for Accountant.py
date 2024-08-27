import streamlit as st, re
from streamlit_extras.stateful_button import button
from app.utils import streamlit_components

streamlit_components.streamlit_ui('🦣 Dashboard for Accountant')

from app.data_entry import email_processing, pdf_processing
from app.db import mongo_db
# -----------------------------------------------------------------------------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Data Entry: CC", "Data Entry: Bank Statement", "Data Entry: Email", "Data Entry: Manual", "DB Structure"])

with tab3:
    if button("Extract from Email", key="button3"):    email_processing.email_extraction()

with tab1:
    if button("CC?", key="button1"):
        pdf_path = "./data/bs/USA/Sample-Credit Card Statement-US/Credit Card-AmEx 91009-Tea Hill-2023/2023-01-09.pdf"
        extracted_data = pdf_processing.extract_pdf_lines(pdf_path)
        st.write(extracted_data)

        if button("Regex?", key="button12"):
            transactions = []
            for entry in extracted_data:
                text = entry['text']
                # Regex to match transaction lines (e.g., date and amount at the end)
                # match = re.match(r'(\d{2}/\d{2}/\d{2}) (.+) (\d+,\d+\.\d{2})$', text)
                # match = re.match(r'(\d{2}/\d{2}/\d{2}) (.+) (-?\$\d+,\d+\.\d{2})$', text)
                match = re.match(r'(\d{2}/\d{2}/\d{2}) (.+) (-?\$\d{1,3}(?:,\d{3})*\.\d{2})$', text)

                if match:
                    date, description, amount = match.groups()
                    amount = amount.replace('$', '')
                    amount = float(amount.replace(',', ''))
                    transactions.append({
                        'clientID':'CC888',
                        'date': date,
                        'description': description,
                        'amount': amount
                    })

            st.write(transactions)
            mongo_db.save_to_cc(transactions)

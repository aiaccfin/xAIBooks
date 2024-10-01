import streamlit as st
from app.utils import streamlit_components
streamlit_components.streamlit_ui('🦣 Dashboard')
# -----------------------------------------------------------------------------------------------------------
tab1, tab2 = st.tabs(["Extract from Statement", "Manual Entry"])


def get_journal_entry_cc(text):
    # Example logic to extract date, description, amount, vendor_name, and COA
    # Replace this with your actual extraction logic
    parts = text.split()
    date = parts[0]
    description = parts[1]
    amount = float(parts[-1])

    if "CREDITADJUSTMENT" in description:
        amount = -amount  # Treat credit adjustment as a negative amount

    vendor_name = description  # Just using description as vendor for now
    COA = "Expense Account" if "ADY" not in description else "Liability Account"  # Simplified COA logic

    return {
        'date': date,
        'description': description,
        'amount': amount,
        'vendor_name': vendor_name,
        'COA': COA
    }


with tab1:

    # st.image('./images/invoices.jpeg')
    import pandas as pd
    import streamlit as st


    # Example extracted_data
    extracted_data = [
        {"text": "09/17/23 WALMARTPLUSMONTHLY -13.92"},
        {"text": "09/29/23 DISNEYPLUSADY -11.82"},
        {"text": "10/09/23 CREDITADJUSTMENT 46.85"}
    ]

    with st.spinner('AI booking...'):
        transactions = []

        for entry in extracted_data:
            text = entry['text']
            journal_entry = get_journal_entry_cc(text)

            # Collecting the journal entry data
            if "CREDITADJUSTMENT" in journal_entry['description']:
                # Adjust for credit adjustment
                transactions.append({
                    'clientID': 'CC888',
                    'date': journal_entry['date'],
                    'description': journal_entry['description'],
                    'debit': 0,
                    'credit': abs(journal_entry['amount']),  # Credit for the adjustment
                    'vendor_name': journal_entry['vendor_name'],
                    'COA': "Credit Card Payable"
                })
            else:
                # Normal expenses
                transactions.append({
                    'clientID': 'CC888',
                    'date': journal_entry['date'],
                    'description': journal_entry['description'],
                    'debit': abs(journal_entry['amount']),  # Debit for the expense
                    'credit': 0,
                    'vendor_name': journal_entry['vendor_name'],
                    'COA': journal_entry['COA']
                })

                # Credit the liability account for the credit card
                transactions.append({
                    'clientID': 'CC888',
                    'date': journal_entry['date'],
                    'description': journal_entry['description'],
                    'debit': 0,
                    'credit': abs(journal_entry['amount']),  # Credit for the credit card payable
                    'vendor_name': 'Credit Card Payable',
                    'COA': "Credit Card Payable"
                })

        # Creating a DataFrame from the transactions list
        df = pd.DataFrame(transactions)

        # Display the DataFrame in Streamlit
        st.dataframe(df)

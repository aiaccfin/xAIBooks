import streamlit as st, re, pandas as pd

from apps.utils import streamlit_components
streamlit_components.streamlit_ui('🦣 Workflow Diagram')
from streamlit_extras.stateful_button import button
# -----------------------------------------------------------------------------------------------------------
st.image('./images/workflow.png')
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Trial Balance", "General Ledger", "Vendor List", "Raw Transactions","ChatBot"])
# from apps.db import mongo_db
from apps.db.db_postgres import PGHandler
pg_handler = PGHandler()

with tab1:

    df = pg_handler.get_journals()

    # Group by account and sum debits and credits
    trial_balance = df.groupby('account').agg(
        total_debit=('debit', 'sum'),
        total_credit=('credit', 'sum')
    ).reset_index()

    # Calculate the difference (debit - credit)
    trial_balance['difference'] = trial_balance['total_debit'] - trial_balance['total_credit']

    # Display Trial Balance in Streamlit
    st.title("Trial Balance")

    # Display the trial balance table
    st.dataframe(trial_balance)

    # Check if the trial balance is balanced
    total_debits = trial_balance['total_debit'].sum()
    total_credits = trial_balance['total_credit'].sum()

    st.code(f'total debits: {total_debits}')
    st.code(f'total credits: {total_credits}')

    if total_debits - total_credits <0.001:
        st.success("The Trial Balance is **balanced**.")
    else:
        st.error(f"The Trial Balance is **not balanced**. Debits: {total_debits}, Credits: {total_credits}")

    st.info('drill down will be implemented by front end')

with tab2:
    if button("General Ledger", key="button12"):
        df = pg_handler.get_journals()
        grouped_df = df.groupby('account')

        # Streamlit display
        st.title("General Ledger with Details")

        # Loop through each account and display the account along with the transactions
        for account, transactions in grouped_df:
            # Display account header
            st.subheader(f"Account: {account}")

            # Show the details (transactions) under this account
            st.dataframe(transactions[['date', 'description', 'debit', 'credit']])

            # Optionally, you can add a summary for debits and credits per account
            total_debit = transactions['debit'].sum()
            total_credit = transactions['credit'].sum()
            st.write(f"**Total Debit**: {total_debit:.2f}")
            st.write(f"**Total Credit**: {total_credit:.2f}")
            st.write("---")


with tab3:
    if button("Show Vendor Information ?", key="button13"):
        vendors = pg_handler.get_vendors()
        for vendor in vendors:
            vendor_name, business_info = vendor
            st.write(f"**Vendor Name**: {vendor_name}")
            st.write(f"**Business Information**: {business_info}")
            st.divider()

        # vendors = mongo_db.collection_vendor.find()
        # for vendor in vendors:
        #     st.write(f"**Vendor Name**: {vendor['name']}")
        #     st.write(f"**Business Information**: {vendor['information']}")
        #     st.divider()

with tab4:
    if button("Show Raw Credit Card Transactions ?", key="button14"):
        data = pg_handler.get_raw_cc()

        columns = [desc[0] for desc in pg_handler.cursor.description]
        df = pd.DataFrame(data, columns=columns)
        # df.drop(columns=['_id', 'description'], inplace = True)
        st.dataframe(df)

with tab5:
    import streamlit as st
    import pandas as pd

    # Sample journal data
    data = [
        {"clientid": "CC888", "date": "2023-10-09", "description": "CREDITADJUSTMENT", "account": "Credit Card Payable",
         "debit": 46.85, "credit": 0.00},
        {"clientid": "CC888", "date": "2023-10-09", "description": "CREDITADJUSTMENT", "account": "Bad Debts Expense",
         "debit": 0.00, "credit": 46.85},
        {"clientid": "CC888", "date": "2023-09-10", "description": "BESTBUY 00160229500001602 DURHAM NC",
         "account": "Office Equipment", "debit": 31.16, "credit": 0.00},
        {"clientid": "CC888", "date": "2023-09-10", "description": "BESTBUY 00160229500001602 DURHAM NC",
         "account": "Credit Card Payable", "debit": 0.00, "credit": 31.16},
        {"clientid": "CC888", "date": "2023-09-11", "description": "THEHOMEDEPOT DURHAM NC",
         "account": "Repairs and Maintenance Expense", "debit": 25.22, "credit": 0.00},
        {"clientid": "CC888", "date": "2023-09-11", "description": "THEHOMEDEPOT DURHAM NC",
         "account": "Credit Card Payable", "debit": 0.00, "credit": 25.22},
        {"clientid": "CC888", "date": "2023-09-12", "description": "UBEREATS help.uber.com CA",
         "account": "Travel and Entertainment Expense", "debit": 34.42, "credit": 0.00},
        {"clientid": "CC888", "date": "2023-09-12", "description": "UBEREATS help.uber.com CA",
         "account": "Credit Card Payable", "debit": 0.00, "credit": 34.42},
        {"clientid": "CC888", "date": "2023-09-12", "description": "WEGMANSCHAPELHILL#140000000140 CHAPELHILL NC",
         "account": "Inventory", "debit": 180.35, "credit": 0.00},
        {"clientid": "CC888", "date": "2023-09-12", "description": "WEGMANSCHAPELHILL#140000000140 CHAPELHILL NC",
         "account": "Credit Card Payable", "debit": 0.00, "credit": 180.35},
        # Add the rest of the data here...
    ]

    # Convert the list of dictionaries to a pandas DataFrame
    df = pd.DataFrame(data)

    # Optionally, set the 'date' column as a datetime type for better formatting
    df['date'] = pd.to_datetime(df['date'])

    # Group by account and sum debits and credits
    trial_balance = df.groupby('account').agg(
        total_debit=('debit', 'sum'),
        total_credit=('credit', 'sum')
    ).reset_index()

    # Calculate the difference (debit - credit)
    trial_balance['difference'] = trial_balance['total_debit'] - trial_balance['total_credit']

    # Display Trial Balance in Streamlit
    st.title("Trial Balance")

    # Display the trial balance table
    st.dataframe(trial_balance)

    # Check if the trial balance is balanced
    total_debits = trial_balance['total_debit'].sum()
    total_credits = trial_balance['total_credit'].sum()

    if total_debits - total_credits < 0.01:
        st.success("The Trial Balance is **balanced**.")
    else:
        st.error(f"The Trial Balance is **not balanced**. Debits: {total_debits}, Credits: {total_credits}")
